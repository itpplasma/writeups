#!/usr/bin/env bash
# Render radiation_collision.tex to OUTPUT_DIR (default: a temporary directory).
# Figures are regenerated with make_figures.py (numpy, scipy, matplotlib).
set -euo pipefail
writeup_root=$(cd "$(dirname "$0")" && pwd)
writeup_output=${1:-$(mktemp -d)}
mkdir -p "$writeup_output"
python3 "$writeup_root/make_figures.py" "$writeup_output" > "$writeup_output/figures.log"
python3 "$writeup_root/make_tables.py" "$writeup_root/numeric_results.json" "$writeup_output"
for writeup_pass in 1 2 3; do
  TEXINPUTS="$writeup_output:" pdflatex -interaction=batchmode -halt-on-error \
    -output-directory "$writeup_output" "$writeup_root/radiation_collision.tex" \
    > "$writeup_output/render-$writeup_pass.log"
done
printf '%s\n' "$writeup_output/radiation_collision.pdf"
