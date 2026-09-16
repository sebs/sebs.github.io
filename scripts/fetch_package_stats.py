#!/usr/bin/env python3
"""Fetch download statistics for the packages listed in _data/packages.yml.

Input : _data/packages.yml — a `purls:` list of Package URLs (pkg:npm/... or
        pkg:pypi/...).
Output: _data/package_stats.yml — JSON (a valid subset of YAML), so Jekyll
        parses it as a data file. This is a build-time artifact: it is
        regenerated on every deploy and is NOT committed to the repo (it is
        gitignored).

There is no committed seed — the daily figures would drift and mislead. On a total failure we write
nothing and the /packages/ page falls back to its empty state; a single package
that errors is recorded with an `error` field rather than aborting the run. Only
the stdlib is used (no PyYAML / requests), so it runs anywhere Python 3 does.

Two registries, one record shape. Everything downstream — the combined chart,
the sparklines, the movers board, the release heatmap, the catalogue table —
reads the same fields regardless of where a package came from, so `collect`
normalises both registries into one dict and nothing after it branches on
`registry` except for display.

Data sources (no auth required):
  npm
  - https://api.npmjs.org/downloads/range/<start>:<end>/<pkg>  daily series —
        the day/week/month/year totals are all summed from this one response,
        so we make a single download request per package (see `_get_json`).
  - https://registry.npmjs.org/<pkg>                           metadata
  PyPI
  - https://pypistats.org/api/packages/<pkg>/overall           daily series.
        PyPI itself publishes no download counts; pypistats.org is the public
        front end for the BigQuery dataset that carries them. Mirror traffic is
        excluded — it is bandersnatch cloning the index, not installs, and it
        outnumbers the real figure several times over.
  - https://pypi.org/pypi/<pkg>/json                           metadata
  - the latest wheel's `entry_points.txt`                      console scripts

The metadata document is far richer than the download counts, and nearly every
extra field below comes out of that *same* response. The /packages/ page is a
catalogue of command-line tools, not a download leaderboard, so we keep what
makes each package recognisable (the command it installs, its keywords, real
example invocations lifted from its README) and the full publish history the
release heatmap is drawn from.

The one request neither registry document covers is the PyPI console-script
name: npm puts `bin` in the registry JSON, but PyPI exposes entry points
nowhere in its API — they live inside the wheel. Hence `wheel_console_scripts`,
which reads that one member out of the archive. A hand-maintained name in the
config would go stale silently, which is worse than one extra request.
"""
import configparser
import io
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections import Counter
from datetime import date, timedelta

CONFIG = "_data/packages.yml"
OUT = "_data/package_stats.yml"
UA = {"User-Agent": "sebs.github.io build (package stats)"}
TIMEOUT = 30
RETRIES = 4   # api.npmjs.org answers bursts of requests with HTTP 429

# Registries we know how to resolve. `label` is what the page prints; `runtime`
# labels the interpreter constraint each ecosystem records (npm `engines.node`,
# PyPI `requires_python`).
REGISTRIES = {
    "npm": {"label": "npm", "runtime": "Node"},
    "pypi": {"label": "PyPI", "runtime": "Python"},
}

# Ceiling on the wheel we download for its entry points. A pure-Python CLI wheel
# is tens of kilobytes; anything past this is shipping compiled artefacts and is
# not worth pulling into a page build for one filename.
MAX_WHEEL_BYTES = 8 * 1024 * 1024

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
# longest one we keep: a longer line wraps awkwardly on a phone.
MAX_EXAMPLES = 4
MAX_EXAMPLE_LEN = 80

# Fenced-code languages treated as shell. An unlabelled fence counts too.
SHELL_LANGS = {"", "bash", "sh", "shell", "console", "zsh", "shell-session"}

# Commands that run a package without installing it, per registry — a README
# line starting with one of these is an example of *this* package when the
# package (or one of its commands) is the next word along. `pipx run foo` and
# `uv run foo` put a subcommand in between; `_runner_target` skips it.
RUNNERS = {"npm": {"npx"}, "pypi": {"uvx", "pipx", "uv"}}
RUNNER_SUBCOMMANDS = {"run", "tool"}

# Keywords (almost) every package carries. They describe the family, not the
# package, so they are left out of each package's keyword list.
FAMILY_KEYWORDS = {"cli", "api-client", "germany"}
MAX_KEYWORDS = 6

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


def _get_bytes(url, cap):
    """GET raw bytes, refusing a body over `cap`. None on any failure.

    Reads one byte past the cap so an oversized body is recognised without
    pulling the whole thing into memory.
    """
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read(cap + 1)
    except Exception:  # noqa: BLE001
        return None
    return None if len(body) > cap else body


def parse_purl(purl):
    """`pkg:<type>/[@scope/]name[@version][?quals][#subpath]` -> (type, name).

    Returns None for anything that is not a PURL of a registry in REGISTRIES.
    PyPI names are normalised per PEP 503 (lowercase, runs of `-_.` collapsed to
    a single `-`), which is the form both pypi.org and pypistats.org index under.
    """
    purl = purl.strip()
    if not purl.startswith("pkg:"):
        return None
    rest = purl[len("pkg:"):]
    kind, _, rest = rest.partition("/")
    kind = kind.lower()
    if kind not in REGISTRIES or not rest:
        return None
    rest = rest.split("?", 1)[0].split("#", 1)[0]   # drop qualifiers / subpath
    rest = urllib.parse.unquote(rest)               # %40 -> @, %2f -> /
    if kind == "npm":
        if rest.startswith("@"):                    # scoped: keep the first @
            at = rest.find("@", 1)
            if at != -1:
                rest = rest[:at]
        else:
            rest = rest.split("@", 1)[0]            # drop @version
    else:
        rest = rest.split("@", 1)[0]
        rest = re.sub(r"[-_.]+", "-", rest).lower()
    return (kind, rest) if rest else None


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
    """Sum the last `days` *calendar* days of a {date: count} series, ending on
    its newest day. None if the series is empty.

    Replaces the per-period api.npmjs.org `point` calls: the last-year daily
    series (already fetched for the chart) contains every period, so one request
    per package covers day/week/month/year and keeps us under the rate cap.

    Counting calendar days rather than the last `days` entries matters because
    pypistats omits days with no downloads entirely. Slicing the key list would
    silently reach back weeks for a quiet package and report it as a week's
    worth. npm returns explicit zeros, so for npm the two agree.
    """
    if not daily:
        return None
    end = max(daily)
    start = (date.fromisoformat(end) - timedelta(days=days - 1)).isoformat()
    return sum(c for d, c in daily.items() if start <= d <= end)


def npm_daily_series(pkg):
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


def pypi_daily_series(pkg):
    """Last year of downloads as a {date: count} dict (empty on failure).

    `overall` returns the package's whole history in one response, so it is
    clipped to the same 365-day window npm is fetched over — otherwise a
    long-lived package would out-scale the chart against its own past rather
    than against the other packages. Days with no downloads are absent from the
    response rather than zero; every consumer here reads the series through
    `.get(day, 0)` against a shared calendar, so the gaps read as zeroes.
    """
    try:
        data = _get_json(f"https://pypistats.org/api/packages/{pkg}/overall?mirrors=false")
        rows = data.get("data") or []
    except Exception:  # noqa: BLE001
        return {}
    cutoff = (date.today() - timedelta(days=365)).isoformat()
    return {r["date"]: int(r.get("downloads") or 0)
            for r in rows if r.get("date") and r["date"] >= cutoff}


def _trim_incomplete_tail(dates, daily):
    """Drop trailing days the registries haven't finished aggregating yet.

    Both registries' counts for the most recent day or two are partial — the
    data lags — so the final days sit far below normal volume (today is usually
    0). Left in, they drag the last weekly bucket toward zero and the chart
    looks like it falls off a cliff. Compare each trailing day to the typical
    recent daily volume and drop it while it looks partial, so the series ends
    on the last day that has complete data.
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
    """Year-by-month grid of every release.

    One row per calendar year from the first release to this one — including
    years without a release, whose empty rows are part of the story — and 12
    month columns. Each cell carries its count `n`, intensity level `l` (see
    HEAT_STEPS) and, when it has releases, its month-start date `d` and a label
    `p` naming them; `f` marks months still in the future.
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
        cells_by_key.setdefault((d.year, d.month), []).append(f"{who} {ver}")

    # Through this year, or the last release if one is somehow dated ahead of
    # it — an empty `years` would leave the section claiming releases it does
    # not draw.
    last_year = max(today.year, int(events[-1][0][:4]))
    years = []
    for year in range(int(events[0][0][:4]), last_year + 1):
        cells = []
        for month in range(1, 13):
            start = date(year, month, 1)
            hits = cells_by_key.get((year, month), [])
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
        # Column axis labels, one per month column.
        "months": list(MONTHS),
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


def _runner_target(words, names):
    """For a line led by a no-install runner (`npx`, `uvx`, `pipx run`, …),
    the arguments after the package it runs — or None if it runs something else.

    Flags and the runner's own subcommand (`pipx run`, `uv tool`) are stepped
    over to find the package name.
    """
    for i, word in enumerate(words[1:], 1):
        if word.startswith("-") or word in RUNNER_SUBCOMMANDS:
            continue
        return words[i + 1:] if word in names else None
    return None


def readme_examples(readme, pkg, bins, registry):
    """Up to MAX_EXAMPLES commands from the README's shell blocks that run this
    package — the catalogue's expanded rows show them verbatim.

    A line qualifies when its first word is one of the package's command names,
    or it runs the package through that registry's no-install runner (`npx …`,
    `uvx …`, `pipx run …`); a leading `$ ` prompt is tolerated. That skips
    install lines, set-up (`cd`, `export`) and anything outside a shell block.
    Also skipped: bare `--help`/`--version` calls (every CLI has them, so they
    say nothing about this one), continued lines, `<placeholder>` arguments
    (copying them runs nothing), and lines over MAX_EXAMPLE_LEN once a trailing
    `# comment` is stripped. Invocations with arguments are preferred over bare
    ones.
    """
    if not bins:
        return []
    names = set(bins) | {pkg}
    runners = RUNNERS.get(registry, set())
    with_args, bare, seen = [], [], set()
    for lang, lines in _fenced_blocks(readme):
        if lang not in SHELL_LANGS:
            continue
        for line in lines:
            cmd = _strip_comment(re.sub(r"^\s*\$\s+", "", line)).strip()
            words = cmd.split()
            if not words or cmd in seen:
                continue
            if words[0] in runners:
                args = _runner_target(words, names)
                if args is None:
                    continue
            elif words[0] in names:
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


def _blank_metadata():
    """The metadata fields every record carries, whatever its registry.

    `runtime` holds the interpreter constraint the ecosystem records (npm's
    `engines.node`, PyPI's `requires_python`); REGISTRIES says what to call it.
    `_releases` — every (date, version) publish event — feeds the release
    heatmap and is dropped before the file is written.
    """
    return {
        "description": "", "version": "", "license": "",
        "first_publish": "", "last_publish": "", "versions": 0,
        "repo_url": "", "homepage": "",
        "bin": [], "keywords": [], "examples": [],
        "size_kb": None, "runtime": "", "deps": 0,
        "_releases": [],
    }


def npm_metadata(pkg):
    """Everything the page shows that comes from the npm registry document."""
    out = _blank_metadata()
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
    skip = FAMILY_KEYWORDS | {b.lower() for b in out["bin"]}
    out["keywords"] = [k for k in keywords if k.lower() not in skip][:MAX_KEYWORDS]
    readme = doc.get("readme") or manifest.get("readme") or ""
    out["examples"] = readme_examples(readme, pkg, out["bin"], "npm")

    size = (manifest.get("dist") or {}).get("unpackedSize")
    if isinstance(size, (int, float)) and size > 0:
        out["size_kb"] = round(size / 1024)
    engines = manifest.get("engines")
    if isinstance(engines, dict) and isinstance(engines.get("node"), str):
        out["runtime"] = engines["node"].strip()
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


def wheel_console_scripts(files):
    """Command names the latest wheel installs, read from its `entry_points.txt`.

    PyPI's API is silent on entry points — they exist only inside the built
    distribution — so this is the one place we fetch a package file. Failures
    (no wheel, oversized, unreadable archive, no entry points) all mean "no
    commands", which is also the honest answer for a library.
    """
    wheel = next((f for f in files if f.get("packagetype") == "bdist_wheel"), None)
    url = safe_url((wheel or {}).get("url"))
    if not url:
        return []
    body = _get_bytes(url, MAX_WHEEL_BYTES)
    if not body:
        return []
    try:
        with zipfile.ZipFile(io.BytesIO(body)) as zf:
            member = next((n for n in zf.namelist()
                           if n.endswith(".dist-info/entry_points.txt")), None)
            if not member:
                return []
            text = zf.read(member).decode("utf-8", "replace")
        parser = configparser.ConfigParser()
        parser.optionxform = str            # command names are case-sensitive
        parser.read_string(text)
    except Exception:  # noqa: BLE001
        return []
    return list(parser["console_scripts"]) if parser.has_section("console_scripts") else []


def _pypi_license(info):
    """A short licence name: the SPDX expression, else a `License ::` classifier.

    The legacy `license` field is free text and often holds the entire licence,
    so it is only trusted when it is short enough to be a name.
    """
    expr = (info.get("license_expression") or "").strip()
    if expr:
        return expr
    for classifier in info.get("classifiers") or []:
        if isinstance(classifier, str) and classifier.startswith("License :: "):
            name = classifier.rsplit(" :: ", 1)[-1].strip()
            if name and name != "OSI Approved":
                return re.sub(r"\s+License$", "", name)
    legacy = (info.get("license") or "").strip()
    return legacy if 0 < len(legacy) <= 40 and "\n" not in legacy else ""


def _pypi_runtime_deps(requires_dist):
    """Count install-time dependencies, skipping the ones behind an extra.

    `requires_dist` entries carry PEP 508 markers; `extra == "dev"` pins a
    dependency to an optional group nobody installing the tool receives, so
    counting them would overstate what the package actually pulls in.
    """
    total = 0
    for spec in requires_dist or []:
        if not isinstance(spec, str):
            continue
        marker = spec.partition(";")[2]
        if "extra" not in marker:
            total += 1
    return total


def pypi_metadata(pkg):
    """Everything the page shows that comes from the PyPI JSON document."""
    out = _blank_metadata()
    try:
        doc = _get_json(f"https://pypi.org/pypi/{pkg}/json")
    except Exception:  # noqa: BLE001
        return out
    info = doc.get("info") or {}

    out["version"] = (info.get("version") or "").strip()
    out["description"] = (info.get("summary") or "").strip()
    out["license"] = _pypi_license(info)
    out["runtime"] = (info.get("requires_python") or "").strip()
    out["deps"] = _pypi_runtime_deps(info.get("requires_dist"))

    urls = doc.get("urls") or []
    out["bin"] = wheel_console_scripts(urls)
    # `keywords` is one free-text field, comma-separated by convention but
    # sometimes spaces.
    raw = (info.get("keywords") or "").strip()
    parts = raw.split(",") if "," in raw else raw.split()
    keywords = [k.strip() for k in parts if k.strip()]
    skip = FAMILY_KEYWORDS | {b.lower() for b in out["bin"]}
    out["keywords"] = [k for k in keywords if k.lower() not in skip][:MAX_KEYWORDS]
    out["examples"] = readme_examples(info.get("description") or "", pkg, out["bin"], "pypi")

    # The wheel is what almost everyone installs; fall back to the sdist so a
    # wheel-less package still reports a size.
    dist = (next((f for f in urls if f.get("packagetype") == "bdist_wheel"), None)
            or next((f for f in urls if f.get("packagetype") == "sdist"), None) or {})
    size = dist.get("size")
    if isinstance(size, (int, float)) and size > 0:
        out["size_kb"] = round(size / 1024)

    project_urls = info.get("project_urls") or {}
    by_key = {k.strip().lower(): v for k, v in project_urls.items() if isinstance(k, str)}
    for key in ("repository", "source", "source code", "code"):
        out["repo_url"] = safe_url(by_key.get(key))
        if out["repo_url"]:
            break
    out["homepage"] = safe_url(by_key.get("homepage") or info.get("home_page"))

    # Every version's first file upload is that version's release date. A
    # version with no files left (all yanked or deleted) never shipped, so it is
    # neither counted nor plotted.
    releases = []
    for version, files in (doc.get("releases") or {}).items():
        days = sorted(d for d in (iso_day(f.get("upload_time_iso_8601") or f.get("upload_time"))
                                  for f in files or []) if d)
        if days:
            releases.append((days[0], version))
    out["_releases"] = sorted(releases)
    out["versions"] = len(releases)
    if releases:
        out["first_publish"] = releases[0][0]
        out["last_publish"] = next(
            (day for day, version in releases if version == out["version"]), releases[-1][0])
    return out


FETCHERS = {
    "npm": (npm_metadata, npm_daily_series,
            lambda pkg: f"https://www.npmjs.com/package/{pkg}"),
    "pypi": (pypi_metadata, pypi_daily_series,
             lambda pkg: f"https://pypi.org/project/{pkg}/"),
}


def package_url(registry, pkg):
    return FETCHERS[registry][2](pkg)


def install_command(registry, pkg, bins):
    """The line to paste to get this package.

    A package that installs commands is a tool, and wants the tool installer of
    its ecosystem — one that puts the command on `PATH` in its own environment
    (`npm i -g`, `pipx install`). A package without commands is a library and
    gets the plain installer, which is what you would add to a project.
    """
    if registry == "pypi":
        return f"pipx install {pkg}" if bins else f"pip install {pkg}"
    return f"npm i -g {pkg}" if bins else f"npm i {pkg}"


def collect(registry, pkg):
    fetch_metadata, fetch_daily, _ = FETCHERS[registry]
    meta = fetch_metadata(pkg)
    daily = fetch_daily(pkg)
    rec = {
        "name": pkg,
        "registry": registry,
        "registry_label": REGISTRIES[registry]["label"],
        "runtime_label": REGISTRIES[registry]["runtime"],
        "url": package_url(registry, pkg),
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
    rec["install"] = install_command(registry, pkg, rec["bin"])
    if rec["dl_month"] is None and not rec["version"]:
        rec["error"] = f"not found on {REGISTRIES[registry]['label']}"
    return rec


def main():
    purls = read_purls(CONFIG)
    targets = [t for t in (parse_purl(x) for x in purls) if t]
    if not targets:
        print(f"no supported purls in {CONFIG}, writing nothing", file=sys.stderr)
        return 0

    packages, ok = [], 0
    for registry, pkg in targets:
        print(f"fetching {registry}:{pkg} ...", file=sys.stderr)
        try:
            rec = collect(registry, pkg)
        except Exception as exc:  # noqa: BLE001
            print(f"  failed: {exc}", file=sys.stderr)
            rec = {"name": pkg, "registry": registry,
                   "registry_label": REGISTRIES[registry]["label"],
                   "runtime_label": REGISTRIES[registry]["runtime"],
                   "url": package_url(registry, pkg),
                   "error": str(exc), "bin": [], "command": "",
                   "install": install_command(registry, pkg, [])}
        if not rec.get("error"):
            ok += 1
        packages.append(rec)

    if ok == 0:
        print("every package fetch failed, writing nothing "
              "(the /packages/ page will show its empty state)", file=sys.stderr)
        return 0

    def s(key):
        return sum(p.get(key) or 0 for p in packages)

    # One calendar for every series, across both registries: the union of all
    # packages' days, with the partial tail cut off once — so the combined
    # chart, the sparklines and the movers all end on the same complete day.
    # (Trimming each package on its own would eat the genuine zero days of a
    # quiet package.) It also fills in the days pypistats omits: a PyPI package
    # is read through this calendar, so its gaps become the zeroes they are.
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

    # One flat catalogue, busiest first — the same 12-month figure the table
    # shows, so its resting order matches the column it is sorted under.
    packages.sort(key=lambda p: (-(p.get("dl_year") or 0), p["name"]))

    first_years = [int(p["first_publish"][:4]) for p in packages if p.get("first_publish")]
    live = [p for p in packages if not p.get("error")]
    per_registry = Counter(p["registry"] for p in live)
    totals = {
        "packages": len(live),
        "clis": len([p for p in live if p.get("bin")]),
        # Ordered as REGISTRIES declares them, so the page's "n on npm, m on
        # PyPI" line does not reshuffle when a package is added.
        "registries": [{"registry": r, "label": REGISTRIES[r]["label"], "packages": per_registry[r]}
                       for r in REGISTRIES if per_registry[r]],
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
        "packages": packages,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    print(f"wrote {len(packages)} packages ({ok} ok) to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
