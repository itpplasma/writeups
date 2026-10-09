#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
: "${TMPDIR:?Set TMPDIR to a disk directory before building}"
case "$TMPDIR" in /tmp|/tmp/*) echo 'TMPDIR must be on disk, outside /tmp' >&2; exit 2;; esac
mkdir -p "$TMPDIR" build
python figures.py
python tables.py
python ledger.py
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build report.tex
