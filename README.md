# sebs.github.io

Personal hub for Sebastian Schürmann — the authoritative node for identity,
projects, writing, and talks. **Own the hub, rent the reach:** blog posts stay
on [dev.to](https://dev.to/sebs); this site links out to them and self-hosts
projects + talks.

## Architecture

- **Static site, built with Jekyll, deployed via GitHub Actions.**
  A full Actions build (not the native Pages build) is used so the dev.to
  writing feed and npm download stats can be fetched at deploy time, the OG
  image rasterized, and the `jekyll-archives` plugin run.
- **The `/packages/` page is data-driven from a PURL config.** List package
  URLs in `_data/packages.yml`; `scripts/fetch_npm_stats.py` resolves the npm
  download counts and release metadata at build time into `_data/npm_stats.yml`
  (committed as a seed, refreshed on every deploy).
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
| `_data/npm_stats.yml` | Seed/fallback for `/packages/` (overwritten by the npm registry at deploy) |

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
bundle exec jekyll serve   # http://localhost:4000
```

`scripts/fetch_devto.py` populates the live writing feed and
`scripts/fetch_npm_stats.py` the npm download stats (both run automatically in
CI; safe to run locally if you have network access).

## TODOs left in the data files

Search for `TODO` in `_data/*.yml`: confirm the LinkedIn slug, npm download
figure, and the `claude-ecosystems-skills` license. (Most talks are missing a
venue — fill in `venue:` in `_data/talks.yml` if you track those down.)
