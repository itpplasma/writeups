# KIN6D prescribed-q results

KIN6D `ccabcc5` ports the reviewed inverse branch and adds curved P2/P3
prescribed-q equilibria to `gs_phase1`. The native contract is constant physical
pprime, signed q(s_pol), signed total Phi and the supplied boundary. The solver
recovers a cubic FFprime law and signed F_edge. The nominal case F_edge is not
a constraint. The adapter retains the solved law for native field readback.
The subsequent integration pins FortNum `bfea03a`, which accepts convergence
on Brent's final permitted update; it repairs a retained Debug inverse check.
The archived convergence runs above precede that status-only dependency fix.

Twelve one-thread CPU runs use the unchanged Phase 3 cases and physical query
points. Every solve completed within 300 s; the slowest producer took 102.84 s.
[kin6d_comparison.csv](kin6d_comparison.csv),
[kin6d_self_convergence.csv](kin6d_self_convergence.csv) and
[kin6d_finest.csv](kin6d_finest.csv) retain resolution, cost, fields, q, axis,
volume, flux, curl current and integrated source current. Raw artifacts and
pre-execution hashes are in the run registry under tag
`kin6d-inverse-20261009-ccabcc5`. No timing repeats or leadership claim are made.

## Convergence

Solovev uses 24/48/96/192 boundary nodes and E1/E2 use 25/37/55/81. All meshes
are curved P3 with maximum area `(2*pi*a/n)^2/2`, `2*n+1` radial points and one
cubic FFprime interval. These budgets are refined together. Norms use the
same 600 R-weighted interior samples as the other-code study; they are not
whole-plasma bounds. The circular reference is the finest inverse state;
its zero errors in the CSV do not establish exactness.

| Case / resolution | psi rel. L2 | Bpol rel. L2 | F rel. L2 | q rel. max | Producer s |
|---|---:|---:|---:|---:|---:|
| E1 n37 vs n81 | 1.53e-7 | 3.09e-6 | 2.45e-7 | 3.16e-6 | 6.04 |
| E2 n55 vs n81 | 5.03e-8 | 1.77e-6 | 4.15e-8 | 1.82e-6 | 33.56 |
| Solovev n48 vs exact | 2.67e-7 | 8.30e-6 | 2.47e-7 | 2.94e-6 | 2.42 |
| Solovev n192 vs exact | 1.02e-9 | 7.82e-8 | 9.68e-10 | 3.16e-8 | 102.84 |

Those E1/E2/n48 Solovev rows also meet the sampled field maxima, axis, volume
and Phi targets. Signed Phi relative errors are below 3.8e-12 throughout.
Solovev's final refinement gives orders 3.94 in psi, 3.32 in Bpol and 4.00
in F. The independent cell-quadrature CTest also checks recovered FFprime
against exact zero and requires order >=3.5; it passes. Constant-q CTests
have last-triplet psi/BR/BZ/Btor orders 4.19/4.59/4.11/3.85 (E1) and
4.45/3.41/3.74/3.85 (E2). The CSV's log2 reduction is a reduction factor,
not an h-order for the non-doubling circular ladder.

Integrated source currents at the finest grids are -1.101493992 MA (E1),
-1.111790442 MA (E2) and -12.785832262 MA (Solovev). Solovev's relative
current error is 7.36e-10. These integrals use the actual curved P3 mesh and
executed law, with an 8/10-point quadrature comparison; the sampled jphi
column separately uses the common finite-difference curl. The latter has
lower regularity across FE faces and is not the recovered FFprime law.

Finest public CHEASE and KIN6D Bpol differences are 7.66e-8 (E1) and
4.95e-7 (E2); the corresponding F differences are 1.08e-8 and 7.70e-9.
Public CHEASE and DESC therefore agree with the inverse KIN6D reference
within the field targets. Existing bounded VMEC++/DESC target gaps on the
other cases are unchanged by this port.

## Export and scope

[kin6d_exports.csv](kin6d_exports.csv) reports native, rectangular EQDSK and
actual libneo field readback at levels 1 and 3, using 129/257-square exports.
Finest libneo Bpol errors are 4.88e-8 (E1 versus native n81), 2.73e-7 (E2
versus native n81), and 5.33e-8 (Solovev versus exact). The field readers
preserve the executed F profile. Behavioral producer tests reverse q and Phi,
recover the reversed toroidal field, reload the native law, and round-trip
signed EQDSK q, Phi and fields. The nominal-F header defect is fixed with a
failing-before/passing-after regression; see EQ-KINV-1 in ERRATA.

The supported branch has an isolated interior minimum of psi and constant
nonpositive pprime. The inverse-input/curved contour sensitivity product is
unavailable; retained affine-P2 derivative oracles remain supported. The
nonlinear majorant has status 4 (frozen-source diagnostic), not an error bound
for the complete inverse problem. Its inverse stability/effectivity cell is
still open. No certificate, complete Phase 3 qualification, or downstream
GPEC/NEO-2 KIN6D inverse qualification is claimed here.

## Reproduction

From the controller checkout after applying the patch, with a built KIN6D
`gs_phase1`, use a unique new tag:

```sh
export TMPDIR=/home/ert/code/worktrees/_lanes/kin6d-inverse/tmp
export KIN6D_BINARY=/home/ert/code/worktrees/kin6d-inverse/build/gs_phase1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
mkdir -p "$TMPDIR"
python -m equilibrium.phase3.compare --tag NEW_UNIQUE_TAG --codes kin6d --cpu 12 --kin6d-binary "$KIN6D_BINARY" --lane /home/ert/code/worktrees/_lanes/kin6d-inverse
python -m equilibrium.phase3.exports --codes kin6d --levels 1 3 --cpu 13 --result-file kin6d_exports.csv
python -m equilibrium.phase3.analyze
uv run python ops/run_registry.py
```

For source-current integration on a retained run, call
`python -m equilibrium.phase3.worker /RAW_RUN/request.json --current-only`.
`analyze` adopts the finest inverse KIN6D reference for circular cases. The
KIN6D-only CSVs here use that same analysis restricted to the twelve KIN6D
JSON rows and the original point files; historical other-code CSVs are left
for the controller's combined regeneration.

Chris&AI
