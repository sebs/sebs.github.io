# sebs.github.io

Personal hub for Sebastian Schürmann — the authoritative node for identity,
projects, writing, and talks. The blog is self-hosted at `/blog/`; the articles
that used to live on dev.to were migrated here.

## Architecture

- **The UI is the IBM Carbon Design System.** Not a copy of it — the real
  `@carbon/styles` Sass sources are compiled from `node_modules` at build time.
  Jekyll 4.4 ships `jekyll-sass-converter` 3.x (dart-sass via `sass-embedded`),
  which supports Sass modules, so `assets/css/main.scss` can `@use` Carbon
  directly and no JS bundler is involved. See **Working on the UI** below.
- **Static site, built with Jekyll, deployed via GitHub Actions.**
  A full Actions build (not the native Pages build) is used so the package
  download stats can be fetched at deploy time, the OG image rasterized, and the
  `jekyll-archives`, `jekyll-feed` and `jekyll-redirect-from` plugins run.
- **The `/packages/` page is data-driven from a PURL config.** List package
  URLs in `_data/packages.yml` — `pkg:npm/…` or `pkg:pypi/…` — and
  `scripts/fetch_package_stats.py` resolves the download counts and release
  metadata at build time into `_data/package_stats.yml` (a build-time artifact,
  regenerated on every deploy — not committed, so the live figures never go
  stale in git). Adding a package is one line in that file; nothing downstream
  branches on which registry it came from except for display. It is a catalogue
  of command-line tools rather than a download table: the same registry
  responses per package also yield the command each one installs, its keywords
  (which sort it into a domain group), real example invocations lifted from its
  README, and the publish history behind the release heatmap.
  `assets/js/packages.js` adds the behaviour on top — table sorting and
  filtering, copy buttons, and the chart readouts — and the page degrades to its
  static render without it.

  The two registries are not symmetrical. npm publishes downloads itself; PyPI
  publishes none, so the figures come from pypistats.org (the public front end
  for the BigQuery dataset) with mirror traffic excluded — counted in, mirrors
  outnumber real installs several times over. npm puts `bin` in the registry
  document; PyPI exposes entry points nowhere in its API, so the console-script
  name is read out of the latest wheel's `entry_points.txt`.
- **The blog is markdown in `_posts/`.** The old Hexo posts were converted to
  clean markdown (see `scripts/extract_posts.py` for how), the dev.to
  articles were exported with `scripts/export_devto.py`, images and all, and
  the 2012–2015 posts from dissident-trainings.de were imported with
  `scripts/import_dissident_trainings.py`. Imported posts carry
  `original_source`/`original_url` (rendered as an "Originally published on"
  note) and a `canonical_url` pointing at the original while it is online. Each
  post pins its URL via `permalink:` in front matter
  (e.g. `/2019/01/04/Monorepos-with-Lerna/`), so every existing link still
  resolves. The `post` layout renders them; `blog/index.html` is the `/blog/`
  index (the old `/archives/` index redirects there); `jekyll-archives`
  regenerates the `/tags/:name/` and `/archives/:year/[:month/]` listing pages;
  `jekyll-feed` publishes `/feed.xml`.

## One-time setup (required to publish)

In the repository: **Settings → Pages → Build and deployment → Source →
"GitHub Actions."** The `.github/workflows/deploy.yml` workflow then builds and
deploys on every push to `master`/`main`, on a daily schedule (to refresh the
package download stats), and on manual dispatch.

> Sponsor CTAs are intentionally hidden until GitHub Sponsors is enabled — see
> `_data/profiles.yml`.

## Editing content (no templates to touch)

Most content lives in `_data/`:

| File                  | Drives                                                    |
| --------------------- | -------------------------------------------------------- |
| `_data/profiles.yml`  | Hero/footer links, JSON-LD `sameAs`, sponsor flag        |
| `_data/projects.yml`  | Project cards                                             |
| `_data/talks.yml`     | `/talks` page + homepage teaser (`featured` + `history`)  |
| `_data/packages.yml`  | npm/PyPI PURLs for the `/packages/` stats page            |
| `_data/topics.yml`    | The blog's topics: name, meta description and intro of each `/tags/<topic>/` page |
| `_data/tag_redirects.yml` | Retired free-form tags → the topic their `/tags/<tag>/` URL now redirects to |

Talk slides go in `assets/talks/` (PDF) or as a SpeakerDeck embed URL — see the
comments in `_data/talks.yml`.

Long-form posts are markdown in `_posts/`, named `YYYY-MM-DD-slug.md`. Front
matter sets `title`, `date`, a `permalink` (the file's slug doesn't affect the
URL — the permalink does), and for search and social previews:

- `description` — 120–155 characters, a real summary (it is the search
  snippet), never a cut-off first sentence;
- `tags` — 1–3 topic slugs from `_data/topics.yml`, most relevant first. Topics
  drive the topic pages, the "Related posts" block and `article:tag`;
- `image` — optional social card, 1200×630. Put a cover in
  `assets/posts/<slug>/`, point `image:` at it and run
  `python3 scripts/optimize_images.py`: it cuts `og.jpg`, converts post images
  to WebP at ≤ 1600px and rewrites the references.

The `post` layout, `nav: writing` highlight, and `og_type: article` are applied
automatically via `defaults` in `_config.yml`. Posts appear on `/blog/`, in the
homepage Writing section and in `/feed.xml` without further wiring.

### SEO plumbing

- `_includes/head.html` emits `BlogPosting` and `BreadcrumbList` JSON-LD plus
  `article:*` meta for posts, composes titles and descriptions for topic and
  date pages, and marks thin pages `noindex, follow` (topics with fewer than
  three posts, all month archives).
- `sitemap.xml` is hand-written and lists only indexable pages; it also leaves
  out posts whose `canonical_url` points at another site.
- `_plugins/` holds three small build-time plugins: `related_posts.rb` (shared
  topics → `page.related`), `tag_redirects.rb` (redirect pages from
  `_data/tag_redirects.yml`) and `image_attributes.rb` (width, height and lazy
  loading on post images, read from the files).

## Local development

```sh
bundle install
npm ci                     # vendors @carbon/styles into node_modules/
bundle exec jekyll serve   # http://localhost:4000
```

`npm ci` is required — without `node_modules/` the stylesheet cannot compile
and the build fails. `.npmrc` sets `ignore-scripts=true`: Carbon and IBM Plex
are pure asset packages, and the only lifecycle scripts in the tree are IBM
telemetry postinstalls.

`scripts/fetch_package_stats.py` populates the npm and PyPI download stats (runs
automatically in CI; safe to run locally if you have network access).

## Working on the UI

| Path                      | Holds                                                        |
| ------------------------- | ------------------------------------------------------------ |
| `assets/css/main.scss`    | The entry point: Carbon config, themes, and the list of Carbon components the site pulls in |
| `_sass/site/*.scss`       | The thin site layer — only the compositions Carbon has no component for |
| `_includes/icon.html`     | ~24 icons vendored from `@carbon/icons` as raw 32×32 path data |
| `_includes/data-table.html` | Reusable Carbon Data Table driven from a `_data/*.yml` list  |
| `_includes/post-list.html`  | Reusable Carbon Structured List of posts                     |
| `assets/js/*.js`            | Progressive enhancement only — `theme.js` (mode toggle), `shell.js` (mobile nav), `packages.js` (the `/packages/` catalogue) |

Rules of thumb:

- **Adding a Carbon component** is one more `@use` line in
  `assets/css/main.scss` — only the components the site renders are compiled in,
  which is why the bundle is ~35 KB gzipped rather than all of Carbon.
- **Do not write raw colours, font sizes, or spacing values.** Use Carbon's
  tokens: `theme.$text-secondary`, `type.type-style("body-01")`,
  `spacing.$spacing-05`. Both colour modes then follow for free — and stay
  inside the set below rather than reaching for a new step.
- **Themes** are Carbon's Gray 100 (dark, the default) and White (light),
  swapped by the `data-theme` attribute on `<html>` — see `_sass/site/_themes.scss`.
- **Adding an icon:** copy the `<path>` out of
  `https://cdn.jsdelivr.net/npm/@carbon/icons@11/svg/32/<name>.svg` into
  `_includes/icon.html`. (`@carbon/icons` is not a dependency — it is 126 MB
  for ~30 icons — so there is no local copy to read it from.)

### The set this site sticks to

Carbon ships a large scale. The site uses a deliberately small slice of it, so
building a page means picking from these tables instead of inventing a step.

**Type — six roles, and nothing below 14px.**

| Role | Carbon style | Size | Used for |
| --- | --- | --- | --- |
| Display | `fluid-display-01` | fluid | the hero name — once per site |
| Page title | `productive-heading-06` | 42px | `h1` on a sub-page, post titles |
| Section title | `productive-heading-04` | 28px | `h2`, the figures in stat tiles |
| Subhead | `productive-heading-03` | 20px | `h3`, tile and card titles |
| Body | `body-02` | 16px | prose and section leads |
| Detail | `body-01` | 14px | everything else — meta, labels, table cells, captions |

Monospace is the Detail step plus `@include type.font-family("mono")`, not a
seventh size. Labels that need weight (the eyebrow, the footer wordmark) are
Detail at `font-weight: 600`. **14px is the floor:** Carbon's Tag and Breadcrumb
render at 12px on their own and are lifted back to Detail in `_base.scss` —
small text was the single biggest legibility problem this site had.

**Colour — two text greys, one accent.**

| Token | Job |
| --- | --- |
| `$text-primary` | headings, and anything that must read first |
| `$text-secondary` | every other piece of text — meta, labels, captions |
| `$link-primary` (+ `-hover`, `$link-visited`) | links, and the accent every chart draws in |
| `$background`, `$layer-01`, `$layer-accent-01`, `$layer-hover-01` | surfaces |
| `$border-subtle-01`, `$border-strong-01` | hairlines and rules |
| `$background-inverse`, `$text-inverse` | tooltips |
| `$focus`, `$highlight`, `$text-error` | system states |

There is no third grey — `$text-helper` and the `$icon-*` pair were folded into
`$text-secondary`, and `$interactive` into `$link-primary`, so links and data
share one blue.

**Spacing — six steps** from Carbon's scale: `03` (0.5rem), `05` (1rem),
`06` (1.5rem), `07` (2rem), `09` (3rem), `10` (4rem). Inline gaps use 03 and 05,
blocks use 06 and 07, sections use 09 and 10.

## TODOs left in the data files

Search for `TODO` in `_data/*.yml`: confirm the LinkedIn slug, npm download
figure, and the `claude-ecosystems-skills` license. (Most talks are missing a
venue — fill in `venue:` in `_data/talks.yml` if you track those down.)
