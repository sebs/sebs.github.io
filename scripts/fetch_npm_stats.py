#!/usr/bin/env python3
"""Fetch npm download statistics for the packages listed in _data/packages.yml.

Input : _data/packages.yml — a `purls:` list of Package URLs (pkg:npm/...).
Output: _data/npm_stats.yml — JSON (a valid subset of YAML), so Jekyll parses it
        as a data file. This is a build-time artifact: it is regenerated on every
        deploy and is NOT committed to the repo (it is gitignored).

Unlike scripts/fetch_devto.py (which keeps a committed seed), there is no seed
here — the daily figures would drift and mislead. On a total failure we write
nothing and the /packages/ page falls back to its empty state; a single package
that errors is recorded with an `error` field rather than aborting the run. Only
the stdlib is used (no PyYAML / requests), so it runs anywhere Python 3 does.

Data sources (no auth required):
  - https://api.npmjs.org/downloads/range/last-year/<pkg>  daily series — the
        day/week/month/year totals are all summed from this one response, so we
        make a single download request per package (see `_get_json` on why).
  - https://registry.npmjs.org/<pkg>                        registry metadata

The registry document is far richer than the download counts, and every extra
field below comes out of the *same* response — no additional requests. The
/packages/ page is a catalogue of command-line tools, not a download
leaderboard, so we keep what makes each package recognisable (its `bin`
command, its keywords, real example invocations lifted from its README) and
the full publish history behind `time`, which the release heatmap is drawn
from. The per-package sparklines and the movers board come from the daily
download series already fetched for the totals.
"""
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import date, timedelta

CONFIG = "_data/packages.yml"
OUT = "_data/npm_stats.yml"
UA = {"User-Agent": "sebs.github.io build (npm stats)"}
TIMEOUT = 30
RETRIES = 4   # api.npmjs.org answers bursts of requests with HTTP 429

# Aggregate-chart geometry (inline SVG viewBox is "0 0 100 40" in the template).
CHART_W, CHART_H, CHART_WEEKS = 100, 40, 52

# Per-package sparkline geometry (viewBox "0 0 100 24"), drawn in the table.
SPARK_W, SPARK_H, SPARK_WEEKS = 100, 24, 26

# A package needs this many downloads in the *preceding* 30 days before we are
# willing to call a change in its numbers a trend. Below it, a handful of CI
# runs swings the percentage into the hundreds and the movers board becomes
# noise.
MOVER_FLOOR = 40

# A change smaller than this (in percent) is not a move, however steady.
MOVER_MIN_PCT = 10

# Cap on example commands kept per package (see `readme_examples`), and the
# longest one we keep: the hero terminal shows one command at a time, and a
# longer line wraps awkwardly on a phone.
MAX_EXAMPLES = 4
MAX_EXAMPLE_LEN = 80

# Fenced-code languages treated as shell. An unlabelled fence counts too.
SHELL_LANGS = {"", "bash", "sh", "shell", "console", "zsh", "shell-session"}

# Keywords (almost) every package carries. They describe the family, not the
# package, so they are left out of each package's keyword list.
FAMILY_KEYWORDS = {"cli", "api-client", "germany"}
MAX_KEYWORDS = 6

# A package's domain, derived from its keywords: the first entry whose set
# intersects them wins, so order matters. `opendata` is a near catch-all, so
# the statistics bucket goes last, and entgeltatlas (tagged both
# `arbeitsagentur` and `statistik`) lands with work. Anything matching nothing
# falls into FALLBACK_DOMAIN.
DOMAINS = [
    ("Parliament & transparency", {"bundestag", "bundesrat", "parlament", "parliament",
                                   "election", "wahl", "lobbying", "transparency",
                                   "informationsfreiheit", "foi"}),
    ("Environment & weather", {"environment", "weather", "wetter", "hydrology",
                               "water-level", "marine", "radiation", "air-quality",
                               "umweltbundesamt"}),
    ("Energy & mobility", {"energy", "energie", "electricity", "strom",
                           "bundesnetzagentur", "ev-charging", "traffic", "verkehr"}),
    ("Work & education", {"arbeitsagentur", "jobs", "salary", "apprenticeship",
                          "ausbildung"}),
    ("Public administration", {"verwaltung", "fim", "fitko", "xzufi"}),
    ("Warnings & news", {"civil-protection", "travel-warning", "news"}),
    ("Culture & heritage", {"cultural-heritage", "glam", "museums"}),
    ("Statistics & open data", {"statistik", "destatis", "official-statistics",
                                "regionalstatistik", "budget", "finance",
                                "opendata", "open-data"}),
]
FALLBACK_DOMAIN = "Developer tools"

# Release-heatmap intensity: a cell with at least HEAT_STEPS[i] releases is
# level i+1. Fixed, roughly logarithmic steps rather than a linear scale — a
# single release is the common case and has to stay visible next to the days
# the whole CLI family was published at once.
HEAT_STEPS = (1, 2, 4, 10)
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def _get_json(url):
    """GET + parse JSON, retrying on 429/5xx with backoff (honours Retry-After).

    api.npmjs.org rate-limits bursty traffic with HTTP 429. With one download
    request per package this is rarely hit, but a retry keeps a transient 429
    from zeroing out a package's numbers for the whole build.
    """
    for attempt in range(RETRIES):
        req = urllib.request.Request(url, headers=UA)
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == RETRIES - 1:
                raise
            retry_after = (exc.headers.get("Retry-After") or "").strip()
            delay = int(retry_after) if retry_after.isdigit() else 2 ** attempt
            time.sleep(min(delay, 30))
    raise RuntimeError(f"exhausted retries for {url}")   # unreachable


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


def _tail_sum(daily, days):
    """Sum the most recent `days` of a {date: count} series; None if unavailable.

    Replaces the per-period api.npmjs.org `point` calls: the last-year daily
    series (already fetched for the chart) contains every period, so one request
    per package covers day/week/month/year and keeps us under the rate cap.
    """
    if not daily:
        return None
    ordered = sorted(daily)                       # oldest -> newest
    return sum(daily[d] for d in ordered[-days:])


def daily_series(pkg):
    """Last year of downloads as a {date: count} dict (empty on failure).

    Uses an *explicit* `<start>:<end>` range rather than the `last-year`
    relative window on purpose: npm's relative-period endpoints
    (last-week/last-year) lag several days behind the explicit range. A package
    published in the last few days therefore reports an all-zero series under
    `last-year` even though its downloads are already visible via an explicit
    range (and on npmjs.com), zeroing out every dl_* figure for that package.
    """
    end = date.today()
    start = end - timedelta(days=365)
    try:
        data = _get_json(f"https://api.npmjs.org/downloads/range/{start}:{end}/{_api_name(pkg)}")
        days = data.get("downloads") or []
    except Exception:  # noqa: BLE001
        return {}
    return {d["day"]: int(d.get("downloads") or 0) for d in days if d.get("day")}


def _trim_incomplete_tail(dates, daily):
    """Drop trailing days npm hasn't finished aggregating yet.

    npm's download counts for the most recent day or two are partial — the data
    lags — so the final days sit far below normal volume (today is usually 0).
    Left in, they drag the last weekly bucket toward zero and the chart looks
    like it falls off a cliff. Compare each trailing day to the typical recent
    daily volume and drop it while it looks partial, so the series ends on the
    last day that has complete data.
    """
    if len(dates) < 30:
        return dates
    window = sorted(daily[d] for d in dates[-30:-3])   # exclude the maybe-partial tail
    baseline = window[len(window) // 2]                # median daily volume
    cutoff = baseline * 0.4
    end = len(dates)
    while end and daily[dates[end - 1]] < cutoff:
        end -= 1
    return dates[:end]


def weekly_totals(daily, days):
    """7-day totals over the sorted `days`, as (week_start_dates, totals),
    oldest -> newest. Days missing from `daily` count as zero.

    Buckets are anchored at the *newest* day so the final one is always a
    complete week; the short remainder falls at the old end and is dropped.
    (Bucketing from the oldest day instead leaves a 1-6 day final bucket that
    dips to near-zero.)
    """
    starts, totals = [], []
    for stop in range(len(days), 6, -7):
        starts.append(days[stop - 7])
        totals.append(sum(daily.get(d, 0) for d in days[stop - 7:stop]))
    return starts[::-1], totals[::-1]


def aggregate_chart(daily_by_date, days):
    """Bucket a {date: total} series into ~52 weekly totals and pre-render the
    SVG geometry for one combined area chart. Returns a dict the template drops
    straight into an inline <svg viewBox="0 0 100 40">; `values` and `starts`
    feed the chart's hover readout."""
    if len(days) < 14:
        return None
    starts, weeks = weekly_totals(daily_by_date, days)
    starts, weeks = starts[-CHART_WEEKS:], weeks[-CHART_WEEKS:]
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
        "start": starts[0],                            # first day of the first plotted week
        "end": days[-1],
        "values": weeks,
        "starts": starts,
    }


def sparkline(daily, days):
    """The last SPARK_WEEKS weekly totals as a polyline for an inline
    <svg viewBox="0 0 100 24">, plus the end point (drawn as a dot) and the
    figures the row's aria-label reads out. None without two weeks of data."""
    _, weeks = weekly_totals(daily, days)
    weeks = weeks[-SPARK_WEEKS:]
    if len(weeks) < 2:
        return None
    peak = max(weeks)
    n = len(weeks)
    pad = 2                                   # keeps the stroke and dot inside the box
    span = SPARK_H - 2 * pad
    pts = []
    for i, w in enumerate(weeks):
        x = round(i / (n - 1) * SPARK_W, 2)
        y = round(SPARK_H - pad - (w / peak * span if peak else 0), 2)
        pts.append((x, y))
    return {
        "points": " ".join(f"{x},{y}" for x, y in pts),
        "end_x": pts[-1][0],
        "end_y": pts[-1][1],
        "peak": peak,
        "last": weeks[-1],
        "weeks": n,
    }


def trend(daily, days):
    """The last 30 complete days against the 30 before them.

    None when there is not enough history, or when the earlier window sits
    below MOVER_FLOOR (see there for why)."""
    if len(days) < 60:
        return None
    now = sum(daily.get(d, 0) for d in days[-30:])
    before = sum(daily.get(d, 0) for d in days[-60:-30])
    if before < MOVER_FLOOR:
        return None
    return {"pct": round((now - before) / before * 100), "now": now, "before": before}


def movers(packages, n=3):
    """The biggest risers and fallers by `trend`, at most `n` each way."""
    rated = [p for p in packages if p.get("trend") and abs(p["trend"]["pct"]) >= MOVER_MIN_PCT]
    up = sorted((p for p in rated if p["trend"]["pct"] > 0), key=lambda p: -p["trend"]["pct"])
    down = sorted((p for p in rated if p["trend"]["pct"] < 0), key=lambda p: p["trend"]["pct"])

    def slim(p):
        return {"name": p["name"], "command": p.get("command") or "", **p["trend"]}

    if not up and not down:
        return None
    return {"up": [slim(p) for p in up[:n]], "down": [slim(p) for p in down[:n]]}


def short_name(pkg):
    """`@scope/name` -> `name`; the scope is the same for most of the family."""
    return pkg.rsplit("/", 1)[-1]


def release_heatmap(packages, today):
    """Year-by-week grid of every release, GitHub-contribution style.

    One row per calendar year from the first release to this one — including
    years without a release, whose empty rows are part of the story — and 53
    week columns (day-of-year // 7, so the last holds a day or two). Each cell
    carries its count `n`, intensity level `l` (see HEAT_STEPS) and, when it
    has releases, its week-start date `d` and a label `p` naming them; `f`
    marks weeks still in the future.
    """
    events = sorted(
        (day, p.get("command") or short_name(p["name"]), ver)
        for p in packages
        for day, ver in p.get("_releases") or []
    )
    if not events:
        return None

    cells_by_key = {}
    for day, who, ver in events:
        d = date.fromisoformat(day)
        key = (d.year, (d.timetuple().tm_yday - 1) // 7)
        cells_by_key.setdefault(key, []).append(f"{who} {ver}")

    # Through this year, or the last release if one is somehow dated ahead of
    # it — an empty `years` would leave the section claiming releases it does
    # not draw.
    last_year = max(today.year, int(events[-1][0][:4]))
    years = []
    for year in range(int(events[0][0][:4]), last_year + 1):
        cells = []
        for week in range(53):
            start = date(year, 1, 1) + timedelta(days=7 * week)
            hits = cells_by_key.get((year, week), [])
            n = len(hits)
            cell = {"n": n, "l": sum(n >= step for step in HEAT_STEPS)}
            if n:
                cell["d"] = start.isoformat()
                cell["p"] = ", ".join(hits[:6]) + (f" and {n - 6} more" if n > 6 else "")
            if start > today:
                cell["f"] = 1
            cells.append(cell)
        years.append({"year": year, "count": sum(c["n"] for c in cells), "cells": cells})

    per_day = Counter(day for day, _, _ in events)
    return {
        "total": len(events),
        "first": events[0][0],
        "years": years,
        "quiet": [y["year"] for y in years if not y["count"]],
        "busiest": [{"date": d, "n": n} for d, n in per_day.most_common(3)],
        # Month labels for the column axis, placed at the week holding the 1st.
        # One label row is shared by every year, so it is approximate by
        # construction: a leap year runs a column late from March on.
        "months": [{"label": label, "col": (date(2001, m, 1).timetuple().tm_yday - 1) // 7}
                   for m, label in enumerate(MONTHS, start=1)],
    }


def safe_url(value):
    """An `http(s)://` URL, or "" — anything else is dropped.

    `homepage` and `repository.url` are free-form strings written by whoever
    published the package. They end up in `href`s, so a `javascript:` (or
    `data:`) URL would run on click; only the two schemes a link needs survive.
    """
    url = (value or "").strip()
    return url if re.match(r"https?://[^\s\"'<>]+$", url) else ""


def iso_day(value):
    """The `YYYY-MM-DD` head of a registry timestamp, or "" if it is not one.

    Registry `time` values are server-generated, so a malformed one is only
    theoretical — but parsing it later, outside the per-package `try`, would
    take down the whole run and leave the page with no data at all.
    """
    if not isinstance(value, str):
        return ""
    try:
        return date.fromisoformat(value[:10]).isoformat()
    except ValueError:
        return ""


def bin_names(pkg, bin_field):
    """Command names a package installs. npm allows `bin` to be a bare path,
    which installs one command named after the unscoped package."""
    if isinstance(bin_field, str):
        return [short_name(pkg)]
    if isinstance(bin_field, dict):
        return [name for name in bin_field if isinstance(name, str) and name]
    return []


def domain_of(keywords):
    """First DOMAINS entry sharing a keyword with the package (see there)."""
    tags = {k.lower() for k in keywords}
    for name, domain_tags in DOMAINS:
        if tags & domain_tags:
            return name
    return FALLBACK_DOMAIN


def _fenced_blocks(markdown):
    """Yield (language, lines) for each fenced code block in a markdown string.

    A closing fence must use the opening fence's character, be at least as
    long and carry no info string — so a ``` inside a ```` block is content.
    """
    fence, lang, buf = None, "", []
    for line in markdown.splitlines():
        m = re.match(r"\s{0,3}(`{3,}|~{3,})\s*([\w+-]*)", line)
        if fence is None:
            if m:
                fence, lang, buf = m.group(1), m.group(2).lower(), []
        elif m and m.group(1).startswith(fence) and not m.group(2):
            yield lang, buf
            fence = None
        else:
            buf.append(line)


def _strip_comment(line):
    r"""Drop a trailing shell `# comment` — one that follows whitespace and sits
    outside quotes, so `jq '.[] | "#\(.id)"'` survives intact."""
    single = double = False
    for i, ch in enumerate(line):
        if ch == "'" and not double:
            single = not single
        elif ch == '"' and not single:
            double = not double
        elif ch == "#" and not single and not double and i and line[i - 1].isspace():
            return line[:i]
    return line


def readme_examples(readme, pkg, bins):
    """Up to MAX_EXAMPLES commands from the README's shell blocks that run this
    package — the hero terminal types them out verbatim.

    A line qualifies when its first word is one of the package's `bin` names,
    or it is `npx <package or command> ...`; a leading `$ ` prompt is
    tolerated. That skips install lines, set-up (`cd`, `export`) and anything
    outside a shell block. Also skipped: bare `--help`/`--version` calls (every
    CLI has them, so they say nothing about this one), continued lines,
    `<placeholder>` arguments (copying them runs nothing), and lines over
    MAX_EXAMPLE_LEN once a trailing `# comment` is stripped. Invocations with
    arguments are preferred over bare ones.
    """
    if not bins:
        return []
    runners = set(bins) | {pkg}
    with_args, bare, seen = [], [], set()
    for lang, lines in _fenced_blocks(readme):
        if lang not in SHELL_LANGS:
            continue
        for line in lines:
            cmd = _strip_comment(re.sub(r"^\s*\$\s+", "", line)).strip()
            words = cmd.split()
            if not words or cmd in seen:
                continue
            if words[0] == "npx":
                rest = [w for w in words[1:] if not w.startswith("-")]
                if not rest or rest[0] not in runners:
                    continue
                args = words[words.index(rest[0]) + 1:]
            elif words[0] in runners:
                args = words[1:]
            else:
                continue
            help_only = args and set(args) <= {"--help", "-h", "help", "--version", "-v", "-V"}
            if (help_only or cmd.endswith("\\") or len(cmd) > MAX_EXAMPLE_LEN
                    or re.search(r"<[A-Za-z][\w-]*>", cmd)):
                continue
            seen.add(cmd)
            (with_args if args else bare).append(cmd)
    return (with_args + bare)[:MAX_EXAMPLES]


def metadata(pkg):
    """Everything the page shows that comes from the registry document.

    `_releases` — every (date, version) publish event — feeds the release
    heatmap and is dropped before the file is written.
    """
    out = {
        "description": "", "version": "", "license": "",
        "first_publish": "", "last_publish": "", "versions": 0,
        "repo_url": "", "homepage": "",
        "bin": [], "keywords": [], "examples": [], "domain": FALLBACK_DOMAIN,
        "size_kb": None, "node": "", "deps": 0,
        "_releases": [],
    }
    try:
        doc = _get_json(f"https://registry.npmjs.org/{_api_name(pkg)}")
    except Exception:  # noqa: BLE001
        return out

    latest = (doc.get("dist-tags") or {}).get("latest", "")
    manifest = (doc.get("versions") or {}).get(latest) or {}
    out["version"] = latest
    out["description"] = (doc.get("description") or "").strip()
    out["versions"] = len(doc.get("versions") or {})
    out["homepage"] = safe_url(doc.get("homepage"))

    out["bin"] = bin_names(pkg, manifest.get("bin"))
    keywords = [k.strip() for k in manifest.get("keywords") or doc.get("keywords") or []
                if isinstance(k, str) and k.strip()]
    out["domain"] = domain_of(keywords)
    skip = FAMILY_KEYWORDS | {b.lower() for b in out["bin"]}
    out["keywords"] = [k for k in keywords if k.lower() not in skip][:MAX_KEYWORDS]
    readme = doc.get("readme") or manifest.get("readme") or ""
    out["examples"] = readme_examples(readme, pkg, out["bin"])

    size = (manifest.get("dist") or {}).get("unpackedSize")
    if isinstance(size, (int, float)) and size > 0:
        out["size_kb"] = round(size / 1024)
    engines = manifest.get("engines")
    if isinstance(engines, dict) and isinstance(engines.get("node"), str):
        out["node"] = engines["node"].strip()
    deps = manifest.get("dependencies")
    out["deps"] = len(deps) if isinstance(deps, dict) else 0

    repo = doc.get("repository")
    if isinstance(repo, dict):
        url = (repo.get("url") or "").strip()
        out["repo_url"] = safe_url(
            re.sub(r"^git\+|\.git$", "", url).replace("git://", "https://")
        )

    lic = doc.get("license")
    if isinstance(lic, dict):
        lic = lic.get("type", "")
    out["license"] = lic or ""

    times = doc.get("time") or {}
    out["first_publish"] = iso_day(times.get("created"))
    out["last_publish"] = iso_day(times.get(latest) or times.get("modified"))
    out["_releases"] = sorted(
        (day, ver) for ver, day in (
            (ver, iso_day(ts)) for ver, ts in times.items()
            if ver not in ("created", "modified") and isinstance(ts, str)
        ) if day
    )
    return out


def collect(pkg):
    meta = metadata(pkg)
    daily = daily_series(pkg)
    rec = {
        "name": pkg,
        "npm_url": f"https://www.npmjs.com/package/{pkg}",
        "dl_day": _tail_sum(daily, 1),
        "dl_week": _tail_sum(daily, 7),
        "dl_month": _tail_sum(daily, 30),
        "dl_year": sum(daily.values()) if daily else None,
        "error": None,
        # `_daily` is consumed to build the aggregate chart, sparklines and
        # trends, then dropped before the file is written (it would bloat the
        # output file otherwise).
        "_daily": daily,
        **meta,
    }
    rec["command"] = rec["bin"][0] if rec["bin"] else ""
    if rec["dl_month"] is None and not rec["version"]:
        rec["error"] = "not found on npm"
    return rec


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def main():
    purls = read_purls(CONFIG)
    npm_pkgs = [p for p in (parse_npm_purl(x) for x in purls) if p]
    if not npm_pkgs:
        print(f"no npm purls in {CONFIG}, writing nothing", file=sys.stderr)
        return 0

    packages, ok = [], 0
    for pkg in npm_pkgs:
        print(f"fetching {pkg} ...", file=sys.stderr)
        try:
            rec = collect(pkg)
        except Exception as exc:  # noqa: BLE001
            print(f"  failed: {exc}", file=sys.stderr)
            rec = {"name": pkg, "npm_url": f"https://www.npmjs.com/package/{pkg}",
                   "error": str(exc), "domain": FALLBACK_DOMAIN, "bin": [], "command": ""}
        if not rec.get("error"):
            ok += 1
        packages.append(rec)

    if ok == 0:
        print("every package fetch failed, writing nothing "
              "(the /packages/ page will show its empty state)", file=sys.stderr)
        return 0

    def s(key):
        return sum(p.get(key) or 0 for p in packages)

    # One calendar for every series: the union of all packages' days, with the
    # partial tail npm has not finished aggregating cut off once — so the
    # combined chart, the sparklines and the movers all end on the same
    # complete day. (Trimming each package on its own would eat the genuine
    # zero days of a quiet package.)
    agg = {}
    for p in packages:
        for day, count in (p.get("_daily") or {}).items():
            agg[day] = agg.get(day, 0) + count
    days = _trim_incomplete_tail(sorted(agg), agg)
    chart = aggregate_chart(agg, days)
    for p in packages:
        daily = p.get("_daily") or {}
        p["spark"] = sparkline(daily, days) if daily else None
        p["trend"] = trend(daily, days)

    # Domain groups, busiest first. The table's default view is grouped, so
    # the package list is ordered group by group, then by 30-day downloads.
    groups = {}
    for p in packages:
        g = groups.setdefault(p["domain"], {"name": p["domain"], "id": _slug(p["domain"]),
                                            "count": 0, "dl_month": 0})
        g["count"] += 1
        g["dl_month"] += p.get("dl_month") or 0
        p["domain_id"] = g["id"]
    domains = sorted(groups.values(), key=lambda g: (-g["dl_month"], g["name"]))
    rank = {g["name"]: i for i, g in enumerate(domains)}
    packages.sort(key=lambda p: (rank[p["domain"]], -(p.get("dl_month") or 0), p["name"]))

    first_years = [int(p["first_publish"][:4]) for p in packages if p.get("first_publish")]
    totals = {
        "packages": len([p for p in packages if not p.get("error")]),
        "clis": len([p for p in packages if p.get("bin") and not p.get("error")]),
        "dl_day": s("dl_day"),
        "dl_week": s("dl_week"),
        "dl_month": s("dl_month"),
        "dl_year": s("dl_year"),
        "releases": s("versions"),
        "since": min(first_years) if first_years else None,
        # Both are page copy ("Last 26 weeks", "at least 40 downloads"), so the
        # template reads them from here rather than repeating the constants.
        "spark_weeks": SPARK_WEEKS,
        "mover_floor": MOVER_FLOOR,
        # Downloads per day over the last 30 complete days — the hero's
        # "since you opened this page" counter ticks at this rate.
        "rate": round(sum(agg[d] for d in days[-30:]) / 30, 2) if len(days) >= 30 else None,
    }
    heatmap = release_heatmap(packages, date.today())
    board = movers(packages)

    for p in packages:
        p.pop("_daily", None)      # keep the output file small
        p.pop("_releases", None)

    payload = {
        "generated": date.today().isoformat(),
        "totals": totals,
        "chart": chart,
        "movers": board,
        "heatmap": heatmap,
        "domains": domains,
        "packages": packages,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    print(f"wrote {len(packages)} packages ({ok} ok) to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
