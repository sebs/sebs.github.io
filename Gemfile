source "https://rubygems.org"

# Built and deployed via GitHub Actions (not the native Pages build) so the
# dev.to writing feed can be fetched at build time. Versions are pinned for
# reproducible deploys.
gem "jekyll", "~> 4.3"
gem "jekyll-sitemap", "~> 1.4"
# Regenerates the writing tag/date archives from the markdown posts (replaces
# the old static Hexo listing pages). Plugin build, so the Actions deploy uses
# it — the native Pages build would not.
gem "jekyll-archives", "~> 2.3"

# Keep modern Ruby happy (stdlib gems unbundled in Ruby 3.4+).
gem "csv"
gem "base64"
gem "bigdecimal"
gem "logger"
