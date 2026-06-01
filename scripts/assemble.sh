#!/usr/bin/env bash
# Copy the legacy Hexo archive into the built site verbatim. Run AFTER
# `jekyll build`. These directories are excluded from Jekyll (see _config.yml)
# so their permalinks ship exactly as-is — including paths with non-ASCII
# characters that Jekyll would otherwise mangle or fail on.
set -euo pipefail

DEST="${1:-_site}"
LEGACY=(2014 2016 2017 2018 2019 archives page tags css)

mkdir -p "$DEST"
for d in "${LEGACY[@]}"; do
  if [ -e "$d" ]; then
    cp -R "$d" "$DEST/"
    echo "assembled: $d -> $DEST/"
  fi
done
