#!/usr/bin/env python3
"""Fetch npm download statistics for the packages listed in _data/packages.yml.

Input : _data/packages.yml — a `purls:` list of Package URLs (pkg:npm/...).
Output: _data/npm_stats.yml — JSON (a valid subset of YAML), so Jekyll parses it
        the same as the committed seed.

Like scripts/fetch_devto.py, this never fails the build: on a total failure we
leave the existing committed seed in place, and a single package that errors is
recorded with an `error` field rather than aborting the run. Only the stdlib is
used (no PyYAML / requests), so it runs anywhere Python 3 does.

Data sources (no auth required):
  - https://api.npmjs.org/downloads/point/<period>/<pkg>   point totals
  - https://api.npmjs.org/downloads/range/last-year/<pkg>  daily series (sparkline)
  - https://registry.npmjs.org/<pkg>                        registry metadata
"""
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import date

CONFIG = "_data/packages.yml"
OUT = "_data/npm_stats.yml"
UA = {"User-Agent": "sebs.github.io build (npm stats)"}
TIMEOUT = 30

# Aggregate-chart geometry (inline SVG viewBox is "0 0 100 40" in the template).
CHART_W, CHART_H, CHART_WEEKS = 100, 40, 52


def _get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.load(resp)


def parse_npm_purl(purl):
    """`pkg:npm/[@scope/]name[@version][?quals][#subpath]` -> package name.

    Returns None for anything that is not an npm PURL.
    """
    purl = purl.strip()
    prefix = "pkg:npm/"
    if not purl.startswith(prefix):
        return None
    rest = purl[len(prefix):]
    rest = rest.split("?", 1)[0].split("#", 1)[0]   # drop qualifiers / subpath
    rest = urllib.parse.unquote(rest)               # %40 -> @, %2f -> /
    if rest.startswith("@"):                        # scoped: keep the first @
        at = rest.find("@", 1)
        if at != -1:
            rest = rest[:at]
    else:
        rest = rest.split("@", 1)[0]                # drop @version
    return rest or None


def read_purls(path):
    """Pull purls from the config's YAML list items, without a PyYAML dependency.

    Matches `  - pkg:...` lines only, so the `pkg:...` examples in the file's
    `#` comments are ignored. Surrounding quotes are stripped.
    """
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.readlines()
    except OSError as exc:
        print(f"cannot read {path}: {exc}", file=sys.stderr)
        return []
    purls = []
    for line in lines:
        m = re.match(r"\s*-\s*['\"]?(pkg:[^\s'\"]+)", line)
        if m:
            purls.append(m.group(1))
    return purls


def _api_name(pkg):
    """Path segment for the npm APIs (scope slash must be percent-encoded)."""
    return pkg.replace("/", "%2f") if pkg.startswith("@") else pkg


def downloads_point(pkg, period):
    try:
        data = _get_json(f"https://api.npmjs.org/downloads/point/{period}/{_api_name(pkg)}")
        return int(data.get("downloads") or 0)
    except Exception:  # noqa: BLE001
        return None


def daily_series(pkg):
    """Last year of downloads as a {date: count} dict (empty on failure)."""
    try:
        data = _get_json(f"https://api.npmjs.org/downloads/range/last-year/{_api_name(pkg)}")
        days = data.get("downloads") or []
    except Exception:  # noqa: BLE001
        return {}
    return {d["day"]: int(d.get("downloads") or 0) for d in days if d.get("day")}


def aggregate_chart(daily_by_date):
    """Bucket a {date: total} series into ~52 weekly totals and pre-render the
    SVG geometry for one combined area chart. Returns a dict the template drops
    straight into an inline <svg viewBox="0 0 100 40">."""
    dates = sorted(daily_by_date)
    if len(dates) < 14:
        return None

    # Oldest -> newest weekly buckets (sum 7 consecutive days).
    weeks = []
    for i in range(0, len(dates), 7):
        weeks.append(sum(daily_by_date[d] for d in dates[i:i + 7]))
    weeks = weeks[-CHART_WEEKS:]
    if len(weeks) < 2:
        return None

    peak = max(weeks) or 1
    n = len(weeks)
    pts = []
    for i, w in enumerate(weeks):
        x = round(i / (n - 1) * CHART_W, 2)
        y = round(CHART_H - (w / peak) * CHART_H, 2)
        pts.append(f"{x},{y}")
    line = " ".join(pts)
    area = f"0,{CHART_H} {line} {CHART_W},{CHART_H}"   # closed polygon for the fill
    return {
        "line_points": line,
        "area_points": area,
        "peak_week": peak,
        "weeks": n,
        "start": dates[0],
        "end": dates[-1],
    }


def metadata(pkg):
    """description, version, license, publish dates, release count."""
    out = {
        "description": "", "version": "", "license": "",
        "first_publish": "", "last_publish": "", "versions": 0,
        "repo_url": "", "homepage": "",
    }
    try:
        doc = _get_json(f"https://registry.npmjs.org/{_api_name(pkg)}")
    except Exception:  # noqa: BLE001
        return out

    latest = (doc.get("dist-tags") or {}).get("latest", "")
    out["version"] = latest
    out["description"] = (doc.get("description") or "").strip()
    out["versions"] = len(doc.get("versions") or {})
    out["homepage"] = (doc.get("homepage") or "").strip()

    repo = doc.get("repository")
    if isinstance(repo, dict):
        url = (repo.get("url") or "").strip()
        out["repo_url"] = re.sub(r"^git\+|\.git$", "", url).replace("git://", "https://")

    lic = doc.get("license")
    if isinstance(lic, dict):
        lic = lic.get("type", "")
    out["license"] = lic or ""

    times = doc.get("time") or {}
    out["first_publish"] = (times.get("created") or "")[:10]
    out["last_publish"] = (times.get(latest) or times.get("modified") or "")[:10]
    return out


def collect(pkg):
    meta = metadata(pkg)
    daily = daily_series(pkg)
    dl_month = downloads_point(pkg, "last-month")
    rec = {
        "name": pkg,
        "npm_url": f"https://www.npmjs.com/package/{pkg}",
        "dl_day": downloads_point(pkg, "last-day"),
        "dl_week": downloads_point(pkg, "last-week"),
        "dl_month": dl_month,
        "dl_year": sum(daily.values()) if daily else None,
        "error": None,
        # `_daily` is consumed to build the aggregate chart, then dropped before
        # the file is written (it would bloat the committed seed otherwise).
        "_daily": daily,
        **meta,
    }
    if rec["dl_month"] is None and not rec["version"]:
        rec["error"] = "not found on npm"
    return rec


def main():
    purls = read_purls(CONFIG)
    npm_pkgs = [p for p in (parse_npm_purl(x) for x in purls) if p]
    if not npm_pkgs:
        print(f"no npm purls in {CONFIG}, keeping committed seed", file=sys.stderr)
        return 0

    packages, ok = [], 0
    for pkg in npm_pkgs:
        print(f"fetching {pkg} ...", file=sys.stderr)
        try:
            rec = collect(pkg)
        except Exception as exc:  # noqa: BLE001
            print(f"  failed: {exc}", file=sys.stderr)
            rec = {"name": pkg, "npm_url": f"https://www.npmjs.com/package/{pkg}",
                   "error": str(exc)}
        if not rec.get("error"):
            ok += 1
        packages.append(rec)

    if ok == 0:
        print("every package fetch failed, keeping committed seed", file=sys.stderr)
        return 0

    def s(key):
        return sum(p.get(key) or 0 for p in packages)

    totals = {
        "packages": len([p for p in packages if not p.get("error")]),
        "dl_day": s("dl_day"),
        "dl_week": s("dl_week"),
        "dl_month": s("dl_month"),
        "dl_year": s("dl_year"),
        "releases": s("versions"),
    }

    # One combined chart: sum every package's daily series by date, then bucket.
    agg = {}
    for p in packages:
        for day, count in (p.get("_daily") or {}).items():
            agg[day] = agg.get(day, 0) + count
    chart = aggregate_chart(agg)

    packages.sort(key=lambda p: p.get("dl_month") or 0, reverse=True)
    for p in packages:
        p.pop("_daily", None)   # keep the committed seed small

    payload = {
        "generated": date.today().isoformat(),
        "totals": totals,
        "chart": chart,
        "packages": packages,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    print(f"wrote {len(packages)} packages ({ok} ok) to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
