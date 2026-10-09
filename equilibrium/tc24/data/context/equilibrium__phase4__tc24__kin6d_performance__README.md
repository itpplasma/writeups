# TC24 performance, convergence and practical error estimate

This study uses the historical absolute-psi JINTRAC control. The current
[collaborator modx03 reference and normalized-current study](../README.md)
is a different physical contract; these costs/errors do not transfer to it.

KIN6D commit **b98297d**, branch `lane/kin6d-tc24perf`, based on/rebased onto
`origin/main` 2d8142a. No delegation. This fills the Phase 4 TC24 cost/convergence
and Phase 1 nonlinear-estimator items. No new physical model, profile refit or
flux-axis rescaling was made.

## Cost defect and repair

Baseline n=48 took 72.835 s in this lane (73.199 s total). Perf attributed
17.6% to repeated basis jets, 16.4% to source evaluation and 10.7% to cut
callbacks, plus other repeated quadrature work. Dense C1 tables unnecessarily
paid for individual knot cuts. Cached positive rules now precede retained
cut integration; interior closed cuts keep their topology-aware path.
Newton uses a separate approximate Jacobian budget, reuses that Jacobian near
convergence, and checks the load at the requested source tolerance.
Default equation tangent/adjoint assembly retains its requested accuracy.

After assembly improved, nested stiffness solves in GMRES dominated. A
symmetric absolute-flux Jacobian now tries diagonal-preconditioned CG with an
explicit residual check and retains the general fallback. At n=128 this
reduced an intermediate 31.60 s solve to 8.2--10.1 s. No generic library code
was duplicated or changed.

CPU 0, one thread, AMD Ryzen 9 5950X, GNU Fortran 16.2.1, CMake cpu/Release:

| Boundary n | Free DOF | Prior solve s | New solve s | Estimator s | Full run s | Newton |
|---:|---:|---:|---:|---:|---:|---:|
| 48 | 2107 | 88.374 | 8.821 | 0.203 | 9.128 | 5 |
| 96 | 8389 | 149.920 | 8.149 | 2.276 | 10.680 | 5 |
| 128 | 15100 | 291.892 | 10.141 | 3.886 | 14.336 | 5 |
| 192 | 33724 | — | 21.374 | 17.341 | 39.477 | 6 |
| 256 | 60349 | — | 44.007 | 48.560 | 93.842 | 5 |
| 384 | 136792 | — | 222.224 | 93.008 | unavailable | 6 |

`timings.csv` retains exact values, roots and revision identities. n=128 is a
clean b98297d run; the preceding profiled run took 8.214 s solve / 12.440 s
total. Their meshes, source laws and profile outputs are byte-identical.
The clean run's peak RSS was 34,088 KiB (33.3 MiB). Timing variation and
other-core CTest activity are not hidden; this is not a hardware leadership
claim. The original and optimized n=48 fields differ by only 3.38e-7 in psi
L2 and 1.87e-7 in Bpol L2, far below their mesh errors.

The second n=384 primal completed below the 300 s solve limit. Its profiler
wrapper timed out at 300 s while the child finished the estimator and wrote
the full native summary. This is registered as an aborted wrapper with usable
native output, not a successful timed run. The first n=384 attempt had no
usable checkpoint. The runner now terminates the entire process group on
timeout, and the app writes its converged primal mesh before the estimator.

## Convergence diagnosis

C2 cubic p/G primitives give C1 piecewise-quadratic sources. Such sources have
bounded weak second derivatives, so, under smooth-domain elliptic and adjoint
regularity, they permit H4 solutions and P3 energy/L2 orders 3/4. C2 primitive
knots do not inherently impose order 2. The 513-knot manufactured behavioral
test uses an independent closed sum for its forcing and gives psi orders
4.108/4.077 and Bpol orders 3.356/3.286.

The pinned TC24 law has knot spacing 0.02330 Wb/rad and sharp source curvature
near psi=0.7. About 94% of the n=192-to-384 squared energy difference lies at
psi=0.3--1.0, only 17.5% of the area; 49.6% lies at psi=0.6--0.8. The 128-mode
Fourier boundary also needs refinement: P3 position RMS errors for n=48/96/
192/384 are 5.56e-4/3.07e-5/2.93e-6/1.74e-7 m. The evidence supports
preasymptotic source/geometry resolution, not a regularity-imposed order-2 cap.

Common physical-domain comparison uses 384 Gauss radial points and 4096
shifted angles (1,572,864 points); 99.9549% of the polar domain is common to
all four represented domains. The norms are unnormalized meridional L2.
Energy is sqrt(integral R*|delta Bpol|^2 dR dZ). No fit or flux normalization
is applied. Doubling comparison quadrature from 192x2048 changes the finest
pair's psi norm by 0.058% and Bpol norm by 1.45%; reported rates are about
1.94/3.62 for psi and 1.20/2.49 for Bpol.

| Fine n | psi pair L2 | Bpol pair L2 | psi order | Bpol order | Energy Richardson | Estimate | Ratio |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 48 | — | — | — | — | — | 3.10959 | — |
| 96 | 2.10850e-3 | 9.16465e-3 | — | — | 3.45083e-3 | 1.58072 | 458 |
| 192 | 5.48708e-4 | 3.98229e-3 | 1.942 | 1.202 | 1.56778e-3 | 0.570986 | 364 |
| 384 | 4.44962e-5 | 7.08907e-4 | 3.624 | 2.490 | 2.76516e-4 | 0.201315 | 728 |

Richardson divides consecutive energy differences by 2^3-1. It is a formal
comparison using the expected asymptotic order, not a bound, especially in
this preasymptotic sequence. `convergence-fine.csv` retains the full table.
Full third-order TC24 Bpol convergence remains an **open defect candidate**;
the present data must not be relabeled as a demonstrated asymptotic limit.
Larger solves were not attempted after n=384 approached the local time limit.

At n=96, tightening source quadrature from 1e-7 to 1e-9 changes psi L2 by
5.41e-7 and Bpol L2 by 1.98e-7 (about 0.1% / 0.005% of the next mesh
difference). Newton weak residuals are 4e-13--4e-12. Those tolerances do not
explain the observed reduced rates. The law remains absolute psi, with the
forward axis tending to 5.309643; historical label 11.869883 is not imposed.

## Practical nonlinear estimate

The opt-in absolute-flux path forms the positive part of the source-derivative
mass, numerically estimates its largest A-relative eigenvalue, and returns
`M0/alpha_hat` with **status 5** when alpha_hat is positive. TC24 gives
alpha_hat about 0.285. The eigenpair residual is included in that numerical
estimate; it does not prove a spectral or continuous coercivity bound. The
recovered M0 already contains the Newton residual. Nonlinear remainder,
existence, geometry, integration and input/model uncertainty are not bounded.
Status 4 remains for unavailable/unstable comparisons and normalized-axis
laws without a supplied conditional bound. Assumptions are documented in
KIN6D docs/grad-shafranov.md.

Behavioral checks cover a monotone exact-error limit (effectivity 1.18), a
positive-source manufactured problem with nonzero algebraic residual
(alpha_hat 0.435, effectivity 2.54--2.71), rejection of an unstable comparison,
and normalized-axis unavailability. The TC24 estimate is conservative by
hundreds relative to formal Richardson. Recovery hits its 6000-iteration cap
at n=256/384 and reports that fact separately. Sharpening/recovery speed is
not claimed solved here.

## Export/readback and tests

The existing producer and repository EQDSK reader were rechecked on the
optimized n=128 field, at the same 2560 interior points used previously:
257/513 grids give psi RMS 7.556e-6/2.916e-6 Wb/rad and Bpol RMS
1.653e-4/1.543e-4 T. These agree with the earlier producer study. This checks
the repository parser plus SciPy reconstruction; no new GPEC/NEO-2/Boozer
consumer qualification or exterior vacuum claim is made.

The quadrature-work oracle fails before (P3 41,808 / P2 147,456 source calls)
and passes after (208 each), while independently checking load and Jacobian
integrals. Baseline instrumentation added only a counter and unused
compatibility arguments. C0/C1 interior islands and three-crossing oracles
pass. Focused CPU/Debug checks and initial full CPU/Debug suites pass 83/83.
After commit/rebase/rebuild, full CPU passes **83/83 in 214.92 s** and full
Debug passes **83/83 in 756.10 s**. Recipe scripts pass Ruff. No introduced
build warnings were found. The
documented Fo drivers are absent; native CMake/CTest authority is used and no
Fo evidence is claimed.

## Reproduction

The archived roots in the CSVs retain binary/input hashes, the exact KIN6D
source diff, configurations and native outputs. Large arrays and EQDSKs stay
under those raw roots. The following scripts are experiment recipes, not a
mandatory Python scientific layer in KIN6D. Source laws remain native Fortran.

From this directory, with a disk scratch directory and one thread:

```sh
python run_tc24.py repeat 128 --repo /home/ert/code/kin6d --scratch DISK_LANE
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python compare_tc24.py \
  ROOT_N48 ROOT_N96 ROOT_N192 ROOT_N384 \
  --radial 384 --angular 4096 --output DISK_LANE/convergence-fine.csv
OPENBLAS_NUM_THREADS=1 python analyze_tc24.py --source ROOT_N48/source.dat \
  --coarse ROOT_N192/post/common_fields_384_4096.npz \
  --fine ROOT_N384/post/common_fields_384_4096.npz --output DISK_LANE
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python export_tc24.py ROOT_N128 \
  --output DISK_LANE/export_accuracy.json
```

`run_tc24.py` accepts `--quad`, `--perf`, `--inputs` and `--binary`; its default
inputs are the pinned archived source/boundary. It registers new solver runs
in a scratch registry copy and renders Markdown with `ops/run_registry.py`.
Merge those entries into the controller registry. Both successful and failed
runs must be retained. Its 300 s process-group cap can leave only a converged
primal checkpoint on the largest mesh; `compare_tc24.py` supports that case.
Readback and quadrature diagnostics are postprocessing of registered runs.
