# Phase 1: common five-code comparison

[A3](solovev_lcfs_A3.csv) and [Cerfon](solovev_cerfon_iter.csv) were produced by
`equilibrium.phase1.driver`; each code has at least four resolutions on each
case. No preliminary rows were copied. All runs used
CPU 10 of the same Ryzen 9 5950X workstation, one numerical thread, and a
300-second native-worker limit. The workstation was shared, so single-run
wall times include ambient load; timing variability was not estimated.

The gate applies all PLAN thresholds to the common samples: 4000 fixed
physical points, volume weights R, s_pol<=0.98, and 40 q samples over
0.05<=s_tor<=0.98. It excludes the outer 2% poloidal-flux shell and is not a
whole-plasma bound. Native convergence is required; force RMS is reported in
the CSVs and is not a gate. Native iteration counts are in CSV metadata;
the public CHEASE build does not print them.

| Case | Code | Setting | wall s | psi L2 | Bpol L2 | Gate | psi/Bpol rate |
|---|---|---|---:|---:|---:|---|---|
| A3 | KIN6D P2 | 384 | 3.807 | 8.368e-08 | 1.573e-05 | best | p=3.03/2.02 |
| A3 | CHEASE public | 64 | 5.984 | 1.810e-07 | 6.624e-06 | pass | p=4.95/3.68 |
| A3 | CHEASE MARS | 64 | 2.926 | 1.838e-07 | 6.954e-06 | pass | p=4.50/3.25 |
| A3 | VMEC++ | 257, m=24 | 24.214 | 1.927e-05 | 1.259e-04 | best | p=1.72/1.15 |
| A3 | DESC | 14 | 200.396 | 2.388e-07 | 1.741e-06 | pass | alpha=1.13/1.01 |
| Cerfon | KIN6D P2 | 192 | 0.829 | 5.514e-07 | 5.838e-05 | best | p=3.20/2.16 |
| Cerfon | CHEASE public | 128 | 19.955 | 2.567e-08 | 1.707e-06 | pass | p=4.39/3.42 |
| Cerfon | CHEASE MARS | 128 | 12.440 | 2.928e-08 | 2.246e-06 | pass | p=4.29/3.22 |
| Cerfon | VMEC++ | 257, m=32 | 53.448 | 2.856e-05 | 3.196e-04 | best | p=1.35/0.97 |
| Cerfon | DESC | 16 | 280.097 | 7.772e-05 | 6.597e-04 | best | alpha=0.88/0.68 |

The selected row minimizes recorded wall time among passing rows. If none
passes, it minimizes the largest error/target ratio among finite native-converged
rows. Settings mean boundary nodes for curved KIN6D P2; NS=NT for CHEASE;
ns with the stated mpol for VMEC++; and L=M for DESC. All exact case boundary
samples are retained; CHEASE uses 257x257 G-EQDSK export, RELAX=0, dense
boundary input and folded band ordering. VMEC++ uses ntheta=4*mpol and the
previous lane's tolerances; DESC uses the documented graded continuation.
The complete executed settings and native metadata are in the CSVs. DOF
means free FE unknowns for KIN6D, assembled 4*(NS+1)*NT for CHEASE,
represented ns*(3*mpol-2) coefficients for VMEC++ (including constrained
coefficients), and free optimizer variables for DESC.

Rates fit the three finest finite native-converged points. Algebraic p means
error proportional to h^p: h=DOF^-1/2 for KIN6D, 1/NS for CHEASE, 1/(ns-1)
for VMEC++. DESC alpha means error proportional to exp(-alpha*M). The
plot legends instead give slopes against DOF or time; these are different
exponents. For public CHEASE A3 the NS32 warning excludes that row from
fits and figures; the retained CSV records its finite errors and failed
native convergence flag.

Predictions recorded before the runs were KIN6D psi/Bpol orders 3/2,
CHEASE 4/3, VMEC++ radial Bpol order 1, and exponential DESC convergence.
KIN6D and both CHEASE variants meet the field predictions; VMEC++ Bpol
matches the first-order radial prediction.
CHEASE's finer below-target differences do not justify further diagnosis.
KIN6D's historical axis errors are repaired by the local quartic recovery
recorded under [EQ-D15](../../ERRATA.md#eq-d15).
The original VMEC++ sampled Bpol-max orders are 0.56/0.71 (A3/Cerfon).
The [fixed physical point continuation](vmecpp_nearaxis_controls.csv) retains
NS257/513/1025 and the same 4000-point clouds and exact references. A3
NS513→1025 gives maximum order 0.925 and Bpol L2 order 1.100; the original
NS257 maximizer, held at the same physical point, gives order 1.331 as its
native radial coordinate moves from cell 1.98 to 3.99. This supports expected
first-order numerical convergence, despite maximum 4.027e-4 remaining above
target. Cerfon's maximum remains unclassified under [EQ-D12](../../ERRATA.md#eq-d12);
radial staggering alone does not establish a half-order prediction.
DESC shaped-boundary truncation is classified in [EQ-D20](../../ERRATA.md#eq-d20).

Cerfon retained-input checks exclude a pressure/iota or flux-sign mismatch:
at NS257 the executed half-grid pressure and iota errors against the exact
physical laws are 1.24e-9 and 6.13e-10 relative (pressure is in Pa). Full-grid
`presf`/`iotaf` reconstruct adjacent half-grid values with endpoint extrapolation;
their errors decrease at order 2, rather than measuring the input spline error.
The native axis agrees between `rmnc` and `raxis_cc`; its signed error crosses
-0.244 to +0.222 mm on NS129→257, with axis self-difference order 1.61. Thus the
small last absolute-error reduction does not demonstrate a wrong-limit plateau;
the fixed-angular contribution remains unclassified, without a demonstrated defect.
Retained `solovev_cerfon_iter_ns*_mp32_tight` attempts hold NS, mpol=32,
ntheta=128 and physical inputs fixed while changing ftol from 1e-14 to 1e-18.
At NS257 the Bpol maximum changes by 2.07e-8 and axis relative error by
1.53e-9, far below the respective 2.36e-3 and 3.41e-5 gaps. Only NS33
passes the tighter native stop; NS65/129/257 exhaust the 40000-iteration
budget with fsql=2.06e-17/2.90e-16/2.15e-16 and remain diagnostic states.
Thus stopping is not the dominant observed error; these attempts do not
qualify a tight-tolerance production ladder. Native JSON and metrics are
retained beside each registered raw run under `phase1/vmecpp/runs/`.
The [fixed-NS257 angular control](vmecpp_cerfon_angular_control.csv) increases
mpol32→48 and ntheta128→192 while preserving profiles and every boundary
coefficient (added boundary modes are zero). It converges at ftol=1e-14 in
101.49 native seconds: Bpol L2 changes 3.19638e-4→3.19524e-4 and maximum
2.35775e-3→2.35791e-3 at the same near-axis sample (s_pol=0.0084962).
The signed axis error changes by only 8.60 nm. Solution angular resolution
and stopping therefore do not explain the dominant retained gap. Fixed
boundary truncation is not tested by this control. Bulk radial convergence
remains expected first order. The new Cerfon NS513→1025 continuation gives
Bpol L2 order 1.004 and order 1.183 at the original NS257 maximizer
(cells 3.30→6.63). The NS513/1025 maximizer is the same fixed physical point,
index 2759, 0.18439 m from the exact axis. Its relative error decreases
1.646e-3→1.005e-3→6.786e-4 on NS513/1025/1537, giving orders 0.712 then
0.968 as it moves from cells 1.92→3.84→5.77. At the original NS257
maximizer, NS1025→1537 gives order 1.690 (cells 6.63→9.96); bulk Bpol L2
gives order 1.072. Both resolved fixed physical probes therefore support
expected first-order radial convergence. The retained-cloud maximum changes
to a closer physical point, index 1755, at NS1537: radius 0.11770 m,
cell 2.66, relative error 7.655e-4. Its maximum-envelope order is 0.671;
that new point's own error gives order 0.625 from cells 1.78→2.66. The slower
envelope continues to sample the first few radial cells and is not evidence
for a universal half-order law, an attained maximum target, or a native defect.
The original persistent-probe rate is explained as preasymptotic radial
behavior; the current maximum envelope is explicitly retained as a limitation.

Both serialized NS513 restart and uninterrupted NS257→513→1025 attempts
with DELT=0.9 fail with repeated bad Jacobians at NS1025. The same saved
NS513 state with DELT=0.1 converges at the original ftol=1e-14 in 981.87
native seconds (984.05 process seconds), 32745 iterations, fsqr=9.979e-15,
fsqz=5.688e-15 and fsql=6.918e-16. Thus the failed refinement is an iteration
configuration limitation, rather than loss of serialized restart state or
an inherently invalid refined geometry. Failed states remain in the CSV and
raw roots but are excluded from rates. A3's successful additional NS513/1025
solves cost 35.54/121.98 native seconds. These warm costs preserve the original
cold cost curves and do not support a matched speed ranking. Cerfon's additional
NS1025→1537 solve converges at the same tolerance in 923.80 native seconds,
20208 iterations, fsqr=9.980e-15, fsqz=3.668e-15 and fsql=6.598e-16.
These controls use CPU5/thread1 under ambient workstation load. The retained
scratch `nearaxis_curve.py` reproduces the CSV using `WoutField`, `Exact`
and the existing points; input/binary hashes and native histories are beside
each registered raw root.
The scratch `compare_cerfon_angular.py` uses the existing `measure`, `Exact`
and fixed-point reader; `comparison.json` beside the new raw run retains
all quantities and native settings. This control is not a matched cost curve.

The original shaped DESC ladder reaches L=M=16 at 280.10 s, with Bpol L2
6.597e-4; the cold M18 attempt exceeded its 300 s cap. Same-profile/Phi
native warm controls refine the exact sampled boundary to M24/M32 and reduce
Bpol L2 to 2.675e-5/1.311e-6, a factor of about 20 per eight added modes.
The final M32 state meets every sampled PLAN quantity: psi L2 8.99e-8,
Bpol max 5.31e-6, Btor L2 7.83e-9, axis 7.22e-9 and volume 8.95e-13.
q and Phi check prescribed input transfer. The strict warm controls cap at
200/150 iterations. With case-specific gtol=1e-9, the same M32 state stops
natively after one iteration; every physical norm was checked again afterward.
This closes the shaped DESC sampled accuracy/stopping cell through spectral
refinement, without a producer or solver defect. The tolerance does not change
producer defaults. [Target controls](desc_target_controls.csv) retain the full
measurement rows. Warm solve costs are 83.28 s (M24), 185.87 s (M32) and
37.60 s (calibrated stop), including load/JAX and excluding readback on CPU6,
one thread. These supplement the original CPU10 cost curve; they are not a
matched cold time-to-target measurement. Original failed runs remain archived.

The [current cold DESC replays](desc_cold_cost.csv) now qualify both exact
cases on CPU7/one thread with unchanged physical decks and no retained seed
or persistent JIT cache. Each row is one observation, not a matched five-code
speed comparison. Producer cost includes the separately measured existing
input preparation, cold native imports/JIT/all continuation/solve/save, and
native H5 load; common physical-oracle evaluation and sample serialization
are excluded. Every PLAN physical norm and the actual final stopping receipt
is retained in the CSV and registered raw roots. q/Phi remain input-transfer
checks. The historical curves and warm-control costs are unchanged.

| Case | L=M | Preparation / s | Cold native process / s | H5 load / s | Producer / s | Native stop | All physical targets |
|---|---:|---:|---:|---:|---:|---|---|
| A3 | 14 | 0.0747 | 229.6282 | 0.5323 | 230.2352 | gtol1e-12;225 final+306 seed iterations | pass |
| Cerfon | 32 | 23.9916 | 455.7538 | 0.5189 | 480.2642 | gtol1e-9;12 final+648 seed iterations | pass |

A3 uses the retained native 4/6/8/10/12 continuation and maxiter 400.
Cerfon uses 4/6/8/10/12/14/16/24, maxiter 200, strict1e-12 coarse stopping
and case-specific final gtol1e-9. Its M16/M24 intermediate stages hit their
200-iteration caps; the subsequent M32 state satisfies native stopping and
all targets. No intermediate capped seed is admitted as an equilibrium.
Peak native RSS is 4.349/4.233GiB. Background load is recorded at both ends;
other processes were not controlled. Physical-oracle evaluations take
113.94/769.01 s separately; their immutable existing math was not changed.


CHEASE fields here are G-EQDSK readback; KIN6D uses native FE readback,
VMEC++ native wout coefficients and DESC native HDF5. q and Phi for the
spectral producers are prescribed constraints, not independent accuracy
predictions. The separate end-to-end export lane owns the additional export
paths. No full equilibrium-slice closure or NTV accuracy claim follows.

Timing is the existing producer wall_s: KIN6D mesh, assembly and solve;
CHEASE input preparation, process and native export; VMEC++ input mapping,
process and native export; DESC input mapping, cold JAX compilation and all
continuation stages. KIN6D contour readback and every producer's common
metric evaluation are excluded. Driver elapsed time is retained in manifests.

## Remaining VMEC++ accuracy targets

The remaining VMEC++ target gaps have the following scheduling estimates.
They hold angular settings and physics fixed and extrapolate retained rates;
the projected fine-grid solutions and timings have not been measured.
The cold-cost estimates assume quadratic radial cost and do not qualify a
native restart route. Shared load and different CPU assignments preclude a
speed ranking. No listed projected large grid was launched.

| Phase/case | Retained NS / process s | Controlling gap | Rate used | Estimated target NS / cold s |
|---|---:|---|---:|---:|
| 1 A3 | 1025 / 122.83 additional | Bpol maximum 4.027e-4 | 0.925 | Expected-rate numerical closure; no target-forcing run |
| 1 Cerfon | 1537 / 925.48 additional | Bpol maximum 7.655e-4; persistent probe 6.786e-4 | 0.671 envelope / 0.968 fixed probe | Expected-rate fixed-probe closure; no maximum target extrapolation |
| 2 E1/A3.1 | 513 / 20.37 | axis 6.261e-6 | 1.260 | ~2200 / ~375 |
| 2 E2/A10 | 769 / 264.54 + 1.09 | all sampled gates pass after strict restart | measured | 769 / 265.63 |
| 2 E2/A3.1 | 513 / 18.38 | axis 2.652e-5 | 1.278 | ~6700 / ~3100 |
| 4a E4/E1 | 257 / 8.65 | axis 3.672e-5 | 1.201 | ~5100 / ~3500 |
| 4a E4/E2 | 257 / 10.52 | axis 8.969e-5 | 1.191 | ~11200 / ~20000 |

Bulk Bpol rates meet VMEC++'s at-least-first-order radial prediction. A3 is
an expected-rate numerical limitation. Cerfon's persistent physical probe at
cell 5.77 gives order 0.968; the new maximizing point remains at cell 2.66.
Fixed-probe convergence and the slower maximum envelope are kept distinct.
Cerfon's signed axis crossing supports self-convergence,
but does not justify an absolute axis-error extrapolation. E2/A10's strict saved-state continuation is measured in
[Phase 2 controls](../../phase2/results/vmecpp_target_controls.csv); original
Phase 1/2/4a curves and source pins remain unchanged.

## Reproduction

Run from the repository root with the previous lanes' environments present:

```sh
TMPDIR=/home/ert/code/worktrees/_lanes/final-compare/tmp \
  /home/ert/code/worktrees/_lanes/vmecpp/.venv/bin/python \
  -m equilibrium.phase1.compare --tag final_compare_repeat_01 \
  --codes chease_public chease_mars kin6d vmecpp desc \
  --kin6d-binary /home/ert/code/worktrees/_lanes/final-compare/bin/gs_phase1_p2 \
  --output-dir /home/ert/code/worktrees/_lanes/final-compare/repeat_01
```

Use a new tag and output directory for each repeat. KIN6D alone, using the
current binary after the separate KIN6D lane is integrated:

```sh
TMPDIR=/home/ert/code/worktrees/_lanes/final-compare/tmp /home/ert/code/worktrees/_lanes/vmecpp/.venv/bin/python -m equilibrium.phase1.compare --codes kin6d --tag final_compare_kin6d_rerun_01 --kin6d-binary /home/ert/code/kin6d/build/gs_phase1 --output-dir /home/ert/code/worktrees/_lanes/final-compare/kin6d-rerun
```

The present producer explicitly uses P2. Selecting P3 requires the separate
lane's producer integration; changing only a label would not select P3.

```sh
for case in solovev_lcfs_A3 solovev_cerfon_iter; do
  TMPDIR=/home/ert/code/worktrees/_lanes/final-compare/tmp \
    /home/ert/code/worktrees/_lanes/vmecpp/.venv/bin/python \
    -m equilibrium.phase1.plot equilibrium/phase1/results/$case.csv \
    --output-dir /home/ert/code/worktrees/_lanes/final-compare/plots
done
```

[ARTIFACTS](../../ARTIFACTS.md) owns the uploaded PNG/PDF URLs. Generated
plots are not committed. Raw runs and failed attempts are under
`/home/ert/data/iter_tc24/phase1/<code>/runs/final_compare_20261009*` and
registered in `results/run_registry.json`. Each archive retains its request,
pre-execution hashes, code/binary pin, command, PID, native output, driver log,
manifest and result. CSV workdirs resolve that storage symlink to
`/mnt/storage/data2/iter_tc24/phase1/...`.

Source pins: KIN6D cc89c37 (clean P2 executable copied before launch), public
CHEASE b942066, MARS CHEASE 104053d, VMEC++ a4150a4 (0.8.1), DESC 2888389
(backported 0.17.3 imported from the previous lane's desc0173 worktree).
The completed-run lookup was repaired for storage symlinks in 71441c379;
this changed registry bookkeeping only. The retained CSV metrics were unchanged.

Validation: common driver/metrics and CHEASE/VMEC++ adapters 20 passed;
native CHEASE integration 2 passed; KIN6D native producer 2 passed;
DESC sign/exterior readback 1 passed. The runner's symlink oracle fails on
the original lookup and passes with the fix. Ruff and registry validation pass.

Chris&AI
