# sebs.github.io

Personal hub for Sebastian Schürmann — the authoritative node for identity,
projects, writing, and talks. **Own the hub, rent the reach:** blog posts stay
on [dev.to](https://dev.to/sebs); this site links out to them and self-hosts
projects + talks.

## Architecture

- **The UI is the IBM Carbon Design System.** Not a copy of it — the real
  `@carbon/styles` Sass sources are compiled from `node_modules` at build time.
  Jekyll 4.4 ships `jekyll-sass-converter` 3.x (dart-sass via `sass-embedded`),
  which supports Sass modules, so `assets/css/main.scss` can `@use` Carbon
  directly and no JS bundler is involved. See **Working on the UI** below.
- **Static site, built with Jekyll, deployed via GitHub Actions.**
  A full Actions build (not the native Pages build) is used so the dev.to
  writing feed and npm download stats can be fetched at deploy time, the OG
  image rasterized, and the `jekyll-archives` plugin run.
- **The `/packages/` page is data-driven from a PURL config.** List package
  URLs in `_data/packages.yml`; `scripts/fetch_npm_stats.py` resolves the npm
  download counts and release metadata at build time into `_data/npm_stats.yml`
  (a build-time artifact, regenerated on every deploy — not committed, so the
  live figures never go stale in git).
- **The legacy posts are markdown in `_posts/`.** The old Hexo posts were
  converted to clean markdown (see `scripts/extract_posts.py` for how). Each
  post pins its **original URL** via `permalink:` in front matter
  (e.g. `/2019/01/04/Monorepos-with-Lerna/`), so every existing link still
  resolves. The `post` layout renders them; `jekyll-archives` regenerates the
  `/tags/:name/` and `/archives/:year/[:month/]` listing pages, and
  `archives.html` is the top-level `/archives/` index.

## One-time setup (required to publish)

In the repository: **Settings → Pages → Build and deployment → Source →
"GitHub Actions."** The `.github/workflows/deploy.yml` workflow then builds and
deploys on every push to `master`/`main`, on a daily schedule (to refresh the
dev.to feed), and on manual dispatch.

> Sponsor CTAs are intentionally hidden until GitHub Sponsors is enabled — see
> `_data/profiles.yml`.

## Editing content (no templates to touch)

Most content lives in `_data/`:

| File                  | Drives                                                    |
| --------------------- | -------------------------------------------------------- |
| `_data/profiles.yml`  | Hero/footer links, JSON-LD `sameAs`, sponsor flag        |
| `_data/projects.yml`  | Project cards                                             |
| `_data/talks.yml`     | `/talks` page + homepage teaser (`featured` + `history`)  |
| `_data/writing.yml`   | Seed/fallback for Writing (overwritten by the dev.to feed at deploy) |
| `_data/packages.yml`  | PURLs for the `/packages/` npm-stats page                 |

Talk slides go in `assets/talks/` (PDF) or as a SpeakerDeck embed URL — see the
comments in `_data/talks.yml`.

Long-form posts are markdown in `_posts/`, named `YYYY-MM-DD-slug.md`. Front
matter sets `title`, `date`, `tags`, an optional `description`, and a
`permalink` (the file's slug doesn't affect the URL — the permalink does). The
`post` layout, `nav: writing` highlight, and `og_type: article` are applied
automatically via `defaults` in `_config.yml`.

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

`scripts/fetch_devto.py` populates the live writing feed and
`scripts/fetch_npm_stats.py` the npm download stats (both run automatically in
CI; safe to run locally if you have network access).

## Working on the UI

| Path                      | Holds                                                        |
| ------------------------- | ------------------------------------------------------------ |
| `assets/css/main.scss`    | The entry point: Carbon config, themes, and the list of Carbon components the site pulls in |
| `_sass/site/*.scss`       | The thin site layer — only the compositions Carbon has no component for |
| `_includes/icon.html`     | ~24 icons vendored from `@carbon/icons` as raw 32×32 path data |
| `_includes/data-table.html` | Reusable Carbon Data Table driven from a `_data/*.yml` list  |
| `_includes/post-list.html`  | Reusable Carbon Structured List of posts                     |

Rules of thumb:

- **Adding a Carbon component** is one more `@use` line in
  `assets/css/main.scss` — only the components the site renders are compiled in,
  which is why the bundle is ~35 KB gzipped rather than all of Carbon.
- **Do not write raw colours, font sizes, or spacing values.** Use Carbon's
  tokens: `theme.$text-secondary`, `type.type-style("body-01")`,
  `spacing.$spacing-05`. Both colour modes then follow for free.
- **Themes** are Carbon's Gray 100 (dark, the default) and White (light),
  swapped by the `data-theme` attribute on `<html>` — see `_sass/site/_themes.scss`.
- **Adding an icon:** copy the `<path>` out of
  `node_modules/@carbon/icons/svg/32/<name>.svg` into `_includes/icon.html`.
  (`@carbon/icons` is not a dependency — it is 126 MB for ~24 icons.)

## TODOs left in the data files

Search for `TODO` in `_data/*.yml`: confirm the LinkedIn slug, npm download
figure, and the `claude-ecosystems-skills` license. (Most talks are missing a
venue — fill in `venue:` in `_data/talks.yml` if you track those down.)
