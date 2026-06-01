# sebs.github.io

Personal hub for Sebastian Schürmann — the authoritative node for identity,
projects, writing, and talks. **Own the hub, rent the reach:** blog posts stay
on [dev.to](https://dev.to/sebs); this site links out to them and self-hosts
projects + talks.

## Architecture

- **Static site, built with Jekyll, deployed via GitHub Actions.**
  A full Actions build (not the native Pages build) is used so the dev.to
  writing feed can be fetched at deploy time and the OG image rasterized.
- **The legacy archive is preserved verbatim.** The old Hexo-generated posts
  (`/2014/…` … `/2019/…`, plus `/archives/`, `/tags/`, `/page/`) have no YAML
  front matter, so Jekyll copies them through untouched — every existing
  permalink still resolves. Don't add front matter to those files.

## One-time setup (required to publish)

In the repository: **Settings → Pages → Build and deployment → Source →
"GitHub Actions."** The `.github/workflows/deploy.yml` workflow then builds and
deploys on every push to `master`/`main`, on a daily schedule (to refresh the
dev.to feed), and on manual dispatch.

> Sponsor CTAs are intentionally hidden until GitHub Sponsors is enabled — see
> `_data/profiles.yml`.

## Editing content (no templates to touch)

All content lives in `_data/`:

| File                  | Drives                                                    |
| --------------------- | -------------------------------------------------------- |
| `_data/profiles.yml`  | Hero/footer links, JSON-LD `sameAs`, sponsor flag        |
| `_data/projects.yml`  | Project cards                                             |
| `_data/talks.yml`     | `/talks` page + homepage teaser (`featured` + `history`)  |
| `_data/writing.yml`   | Seed/fallback for Writing (overwritten by the dev.to feed at deploy) |

Talk slides go in `assets/talks/` (PDF) or as a SpeakerDeck embed URL — see the
comments in `_data/talks.yml`.

## Local development

```sh
bundle install
bundle exec jekyll serve   # http://localhost:4000
```

`scripts/fetch_devto.py` populates the live writing feed (run automatically in
CI; safe to run locally if you have network access).

## TODOs left in the data files

Search for `TODO` in `_data/*.yml`: confirm the LinkedIn slug, npm download
figure, the `claude-ecosystems-skills` license, and replace the placeholder
talks with real titles/venues/slides.
