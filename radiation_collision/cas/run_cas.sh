#!/usr/bin/env bash
# Run every fortsym derivation script and require each binding r### to be 0.
# FORTSYM_WL_RUN overrides the runner (default: fortsym_wl_run on PATH).
set -euo pipefail
cas_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
runner="${FORTSYM_WL_RUN:-fortsym_wl_run}"
out_dir="${1:-$(mktemp -d)}"
mkdir -p "$out_dir"
scripts=(resonance_variance harmonic_sums angular_integrals tensor_coordinates
         kernel convergence thresholds closure drag)
total=0
status=0
for name in "${scripts[@]}"; do
  src="$cas_dir/$name.wl"
  if [ "$name" = angular_integrals ]; then
    cat "$cas_dir/angular_antiderivatives.wl" "$src" > "$out_dir/$name.full.wl"
    src="$out_dir/$name.full.wl"
  fi
  "$runner" "$src" > "$out_dir/$name.out" 2>&1 || true
  if summary=$(awk -v name="$name" '
      /^UNSUPPORTED/ { bad = 1; print "  " $0 }
      $1 == "R" && $2 ~ /^r[0-9][0-9][0-9]$/ {
        n++; if ($3 != "0") { bad = 1; print "  nonzero " $2 } }
      END { printf "%-20s %3d checks\n", name, n; exit bad }' "$out_dir/$name.out"); then
    echo "PASS $summary"
  else
    echo "FAIL $summary"
    status=1
  fi
  total=$((total + $(grep -c -E '^R	r[0-9]{3}	' "$out_dir/$name.out" || true)))
done
echo "fortsym exact checks: $total bindings, outputs in $out_dir"
exit $status
