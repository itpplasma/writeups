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
KIN6D's axis remains an open candidate under [EQ-D15](../../ERRATA.md#eq-d15).
VMEC++ sampled Bpol-max orders are 0.56/0.71 (A3/Cerfon). Its near-axis
maxima and DESC shaped boundary truncation retain the
method/representation classifications in [EQ-D20](../../ERRATA.md#eq-d20).

The shaped DESC ladder reaches L=M=16 at 280.10 s, with Bpol L2
6.597e-04. The next attempted L=M=18 exceeded the 300-second native
worker cap. Its failure log and inputs remain registered and archived; no
metric row or convergence claim was invented for it. These are budget-limited
results for the documented boundary representation, not a spectral accuracy floor.

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
