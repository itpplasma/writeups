#!/usr/bin/env bash
# Checked algebra only; native solver/mesh validity requires independent probes.
set -euo pipefail
cas_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
runner="${FORTSYM_WL_RUN:-/home/ert/code/fortsym/build/bin/fortsym_wl_run}"
output="${1:-/tmp/desc-force-native.out}"
"${runner}" "${cas_dir}/desc_force_correspondence.wl" >"${output}"
awk '
  $1 == "R" && $2 ~ /^r[0-9][0-9][0-9]$/ {
    seen[$2]++; if ($3 != "0") bad=1
  }
  END {
    for (i=1; i<=10; i++) if (seen[sprintf("r%03d",i)] != 1) bad=1
    if (bad) exit 1
    print "PASS exact native FortSym DESC correspondence: 10/10"
  }
' "${output}"
