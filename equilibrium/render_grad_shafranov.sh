#!/usr/bin/env bash
set -euo pipefail
writeup_root=$(cd "$(dirname "$0")" && pwd)
writeup_output=${1:-/tmp/writeups-gs-20261007}
mkdir -p "$writeup_output"
for writeup_pass in 1 2; do
 pdflatex -interaction=batchmode -halt-on-error -output-directory "$writeup_output" "$writeup_root/grad_shafranov.tex" > "$writeup_output/render-$writeup_pass.log"
done
printf '%s\n' "$writeup_output/grad_shafranov.pdf"
