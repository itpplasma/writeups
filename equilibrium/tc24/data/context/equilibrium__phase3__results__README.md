# Phase 3: prescribed-q equilibria

Public CHEASE, VMEC++ and DESC converge on the same three inverse contracts.
MARS CHEASE does not produce an accepted inverse equilibrium. The KIN6D lane
now supplies [curved P3 inverse results](kin6d.md) on these same contracts.
These results fill PLAN Phase 3's recovered F, current, fields and q versus
resolution and producer time cells; they do not close Phase 3 qualification.

## Contracts and executed modes

[cases.json](../cases.json) and [cases.py](../cases.py) define the inputs under
the signed [case contract](../../CASE_CONTRACT.md). Canonical COCOS 3 uses
psi_edge=0, negative psi_axis, positive q and Phi. The map is
`dPhi=2*pi*q*dpsi`; its signed integral and inverse interpolation are tested.
F, FFprime and total current are outputs. No reference error sets a scale.

| Case | Boundary | p_prime [Pa/(Wb/rad)] | q | Phi_edge [Wb] |
|---|---|---:|---|---:|
| E1_constant_q_A10 | Circle R0=6.2 m, a=0.62 m | 0 | +1.5 | 6.400429545011558 |
| E2_constant_q_A10 | Same circle | -146292.26472199883 | +1.5 | 6.400429545011558 |
| Solovev_inverse_A3 | Phase 1 polynomial analytic LCFS | -146292.26472199883 | analytic q(psi) | 92.49423744163455 |

Both circular cases have psi_axis=-0.6791066666666667 Wb/rad; E2 has
p_axis=99348.05225447423 Pa. Solovev has psi_axis=-7.545629629629919 Wb/rad,
p_axis=1103867.2472719778 Pa, exact F=32.86 T m and FFprime=0. Its regular
axis formula is `q=q_axis*R0^3*mean(R^-3)`, with
`R^2=R0^2+2*R0*a*sqrt(s_pol)*cos(theta)` and q_axis=1.5.
There are 1025 radial profile knots and 2048 boundary/angular samples.

Public CHEASE executes NSTTP=5/NCSCAL=1; MARS executes NSTTP=4/NCSCAL=4.
Public QSPEC normalizes axis q; MARS reads q from EXPEQ and NCSCAL=4
does not apply QSPEC normalization. The adapter preserves q when changing
the native field normalization. A scalar root in F_edge enforces the declared
Phi while holding the input physical p_prime fixed; all native trials are retained
and included in cost. The final mapped NCSCAL=1 correction scales the delivered
p_prime as well as psi/Bpol. At NS=NT128, final SCALE is 1.00000056 (E1),
1.00000267 (E2) and 0.999997522 (Solovev); the latter two delivered pressure
derivatives depart from the fixed contract by these factors. This is the
executed q-axis/edge-F normalization, not an unrecorded reader gain. VMEC++ uses ncurr=0, prescribed iota=+1/q on its negative-signgs
branch. DESC uses iota=-1/q under its recorded angle map. Their pressure and
iota tables use s_tor obtained by integrating q, not by identifying psi with Phi.

Executed pins and recoverable CHEASE source/binary archives are in
[source_pins.json](source_pins.json). Public CHEASE includes held fixes #13/#15;
the MARS integration includes #39/#41/#42/#43 and the retained forward repairs.
VMEC++ is 0.8.1 (`a4150a4e`); DESC is the pinned 0.17.3 fork (`2888389d`).
The original other-code study below is preserved; KIN6D execution and readback
are reported separately in [kin6d.md](kin6d.md).

## Native convergence and cost

[comparison.csv](comparison.csv) contains all 38 accepted final samples;
[finest.csv](finest.csv) selects the finest accepted resolution per solver/case.
CHEASE uses NS=NT=16,32,64,128, RELAX=0.3 and a 257-square EQDSK export.
VMEC++ uses ns=33,65,129,257 at mpol=24; E2 additionally completes ns=513.
DESC uses L=M=4,6,8,10; Solovev additionally completes L=M=12.
Every native solve is local, one thread and capped at 300 s. Producer times
include native preparation/export and all CHEASE flux-root trials, but exclude
the subsequent comparison/consumer measurements. DOF is each representation's
reported scalar coefficient count, not a common matrix dimension.

Norms are R-weighted estimates from 600 fixed area-uniform physical points:
Solovev s_pol<=0.98, circular cases geometric radius squared <=0.90 a^2.
The latter restriction leaves a common shell for curl evaluation. Thus these
are sampled interior norms, not whole-plasma/LCFS maximum guarantees. q is
checked at 40 fixed s_tor values from 0.05 to 0.98. j_phi is the physical curl
of the sampled field; FFprime is inferred from that current and the prescribed
p_prime. Total current independently uses signed LCFS Ampere circulation.
No profile, phase, sign, gain or geometry is fitted to reduce comparison error.

EQ-D103: current CSV metrics use final-stage native fields. The shared NOUT
reader applies the logged final SCALE to all Hermite jets and axis psi before
combining them with delivered F. These corrected independent readbacks replace
the previous metrics; frozen raw NOUT, EQDSK, consumer files and sample NPZs
remain unchanged. All 12 scaled native axes agree with final EQDSK axes within
printed precision. Consumer and export metrics were recomputed offline at the
unchanged physical queries, without solver or consumer reruns.

| Case / solver | Finest | Bpol rel. L2 | F rel. L2 | j_phi rel. L2 | q rel. max | Producer s |
|---|---|---:|---:|---:|---:|---:|
| E1 / public CHEASE | NS128 | reference | reference | reference | 5.59e-07 | 176.7 |
| E1 / VMEC++ | ns257 | 1.91e-06 | 2.80e-09 | 7.96e-06 | 0.00e+00 | 16.8 |
| E1 / DESC | L10 | 5.61e-07 | 1.37e-09 | 6.20e-07 | 0.00e+00 | 58.3 |
| E2 / public CHEASE | NS128 | reference | reference | reference | 2.68e-06 | 277.5 |
| E2 / VMEC++ | ns513 | 5.35e-06 | 4.83e-09 | 1.93e-05 | 0.00e+00 | 164.9 |
| E2 / DESC | L10 | 2.67e-06 | 3.49e-09 | 2.92e-06 | 0.00e+00 | 66.1 |
| Solovev / public CHEASE | NS128 | 2.61e-06 | 2.42e-09 | 8.89e-05 | 2.48e-06 | 221.9 |
| Solovev / VMEC++ | ns257 | 8.40e-05 | 1.89e-06 | 8.79e-04 | 5.70e-07 | 26.8 |
| Solovev / DESC | L12 | 1.48e-05 | 2.95e-07 | 1.10e-04 | 3.01e-13 | 78.8 |

### Selected sampled target-passing states

The table selects the least-cost retained sampled passing state after final-stage
readback correction. E1/E2 use the KIN6D n81 inverse reference; Solovev uses
the exact state. Targets are psi L2 1e-6, Bpol/Btor L2 1e-5 and max 1e-4,
q max 1e-5, and axis, volume and signed Phi relative error 1e-6.
No retained public E2 or Solovev state meets the psi target; their finest errors
are 2.66e-6 against common KIN6D and 2.47e-6 against exact Solovev. The former
public selections are superseded, not retained as passing observations.

| Case / retained row | DOF | psi L2 | Bpol L2 / max | Btor L2 / max | q max | Axis / volume rel. | Phi rel. | Producer s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| [E1 / public CHEASE NS=NT=64](E1_constant_q_A10_chease_public_2.json) | 16640 | 4.57e-07 | 4.73e-07 / 5.53e-07 | 1.09e-08 / 1.17e-08 | 4.68e-07 | 1.00e-08 / 1.02e-08 | 9.75e-11 | 67.991 |
| [E1 / KIN6D](E1_constant_q_A10_kin6d_1.json) | 1489 | 1.53e-07 | 3.09e-06 / 3.14e-05 | 2.45e-07 / 2.44e-07 | 3.16e-06 | 1.30e-07 / 2.45e-07 | 3.69e-12 | 6.038 |
| [E2 / KIN6D](E2_constant_q_A10_kin6d_2.json) | 3262 | 5.03e-08 | 1.77e-06 / 6.46e-06 | 4.15e-08 / 4.11e-08 | 1.82e-06 | 8.55e-07 / 4.14e-08 | 4.44e-16 | 33.556 |
| [Solovev / KIN6D](Solovev_inverse_A3_kin6d_1.json) | 2854 | 2.67e-07 | 8.30e-06 / 4.32e-05 | 2.47e-07 / 2.42e-07 | 2.94e-06 | 1.68e-08 / 1.04e-07 | 1.78e-15 | 2.423 |

[passing_states_common_reference.csv](passing_states_common_reference.csv) owns
these numeric cells. For public CHEASE, samples_path/hash identify raw NOUT
from which the corrected independent readback is evaluated; frozen sample NPZs
predate final-stage correction. KIN6D entries retain their native sample identity.
The linked JSONs own resolution, time and raw roots. The maintained analyzer
re-evaluates CHEASE raw NOUT at retained NPZ queries and recomputes its native
LCFS current without altering historical NPZ/current files. It does not scale
cached fields, so new final-stage outputs are not scaled twice. Export comparison
uses this same readback for native candidates and finite references while keeping
actual delivered-reader fields fixed. Boozer/consumer references and mapped-cell
effectivity use the shared native reader directly.

Reproduce the common-reference table with both circular KIN6D level-3 inputs:

```sh
mkdir -p /DISK/phase3-common
cp equilibrium/phase3/results/*_kin6d_?.json equilibrium/phase3/results/*_chease_public_?.json equilibrium/phase3/results/*_points.npz /DISK/phase3-common/
python -m equilibrium.phase3.analyze --output /DISK/phase3-common
```

Select the passing `(case, code, level)` keys from the resulting corrected
comparison CSV. The original other-code comparison uses only the 38 retained
public/VMEC++/DESC JSON keys, so E1/E2 retain their public finite reference.

Times retain KIN6D `ccabcc5` (binary SHA256 `a32c4ee0…`) and public CHEASE
`b179fc6` (`3f5a914a…`); full pins stay in the linked raw manifests. Both ran on
`mailuefterl`, CPU12/thread1, in different execution windows. Concurrent host
load was not recorded or controlled, and these timings have no repeats.
The common producer timer sums `worker.run` calls: one KIN6D call versus
two/three/two public flux-root trials for E1/E2/Solovev. Its broad scope aligns:
input/mesh preparation, solve, native export and native profile/state readback
are included; KIN6D's estimator is included and CHEASE has no matching stage.
Export products differ (KIN6D mesh/profile files versus CHEASE NOUT/EQDSK).
Oracle field sampling and subsequent consumer conversions are excluded.
Original timing pins, cost curves and 300-s-per-native-solve caps are retained.
Thus these are retained producer measurements, not matched pure-solver
benchmarks or a fastest-code claim. Uncontrolled contention, finite circular
reference uncertainty and the excluded edge shell prevent a reproducible speed
ranking or an absolute whole-domain accuracy claim.

Solovev errors use the exact answer. The original E1/E2 tables use public NS128 native
NOUT references; the KIN6D supplement compares against them. Reference zeros in
the CSV are not accuracy measurements. The corrected public last-triplet
Bpol differences do not establish an
asymptotic reference-error bound: final q-axis normalization contributes a
resolution-dependent field gain. VMEC++ field differences decrease approximately
as h^1.5 (at least its expected first-order radial rate), and DESC has geometric
degree convergence. [self_convergence.csv](self_convergence.csv) reports
successive differences and last-triplet estimates; DESC's `richardson` column
is a geometric-tail estimate for degree increments, not an algebraic h-order.
These estimates are not rigorous bounds or a replacement for the pending
KIN6D a posteriori estimator.

[KIN6D effectivity measurements](kin6d_effectivity.csv), reproduced with
`python -m equilibrium.phase3.kin6d_effectivity`, compare the whole-domain
majorant with componentwise field errors on the existing interior point sets.
The ratios are 1.33–1.44 against exact inverse Solovev, 1.42–4.21 for E1/E2,
and 16–60 for the two TC24 ladders. The sampled E1/E2 script uses the KIN6D
level-3 reference and is unaffected by the public NOUT correction. The excluded edge shell means these ratios
are upper estimates of whole-domain effectivity; they cannot establish that
the estimator never underestimates the full error. Finite-reference Richardson
corrections assume
aligned errors and an asymptotic order; they are estimates, not bounds.
The CSV reports Monte Carlo standard errors for the sampled norms, excluding
reference and domain-truncation uncertainty. TC24 ladders use different point
sets and are compared separately.

[Full-domain inverse Solovev measurements](kin6d_effectivity_native_solovev.csv)
integrate the field energy error over every mapped P3 cell of the retained
native mesh. At 658, 2,854, 11,575 and 46,558 free DOF, majorant/error is 1.178,
1.165, 1.166 and 1.161, with field-energy error decreasing approximately as h³.
Raising quadrature order from 8 to 12 changes the error norm by at most 1.6e-11
relative; the reader reproduces all retained field samples exactly. The status-4
majorant remains a frozen-source diagnostic, not a nonlinear error bound.
[Full-domain circular measurements](kin6d_effectivity_native_circular.csv) now
use the corrected public NS128 native field at identical mapped-cell quadrature
nodes. Maintained native readback gives majorant/error 1.1044/1.1058/1.0218
for E1 and 1.1179/1.0786/0.7857 for E2 across levels 0/1/2. Thus the fine E2
ratio is below one. The finite reference has unbounded reference uncertainty,
so this is neither proof of estimator failure nor continuous reliability.
These remain frozen-source diagnostics. Raising quadrature 8 to 12 changes the norm by at most
5.91e-6; independent P3 gradients agree with native fields within 5.82e-12,
and all retained samples are reproduced. Reader f6a33c9/build66037bab is recorded
separately from solve identity. The original raw runs remain unchanged; logged
SCALE is part of the reference input identity. Reproduce with a verified absolute `FO_DRIVER` and optional
`FO_DRIVER_SHA256`, `KIN6D_ROOT` and `FO_CMAKE_BUILD_DIR`, then run
`python -m equilibrium.phase3.mesh_quadrature`; circular cases additionally use
`--case E1_constant_q_A10 --reference equilibrium/phase3/results/E1_constant_q_A10_chease_public_3.json --out E1-effectivity.csv`
(and the corresponding E2 paths and output filename). Native readback uses
`fo exec --no-build`, without changing or rerunning the stored solves.

Exact signed Solovev current is -12.785832252 MA. Corrected public NS128
relative current error is 2.48e-06; recovered FFprime RMS is
5.73e-04 T. The CSVs retain current, curl, force, axis and
volume measurements; final mapped normalization is included in field/current
errors and is not removed to match exact truth.

VMEC++ Solovev still misses psi, Bpol and axis targets; ns513 hits the 300 s cap.
VMEC++ E2 reaches the field target at NS513 but its axis error is 2.02e-6
against the retained public-CHEASE reference, or 2.184e-6 against the common
KIN6D inverse level 3 reference. A single unchanged-physics native continuation
NS513→897 at M24 and ftol=1e-18 is retained in
[vmecpp_target_controls.csv](vmecpp_target_controls.csv). It costs 236.61 s on
CPU1/thread1, separately from the retained 164.91 s seed-production cost,
and exhausts its configured 16000-iteration native budget: fsqr=3.538e-17.
The saved state passes every
physical field/flux/volume gate against both references, but its axis error is
9.750e-7 against public CHEASE and 1.140e-6 against common KIN6D. Their native
axis offset is 1.645e-7 relative, so the public comparison does not close the
common-reference gate. Observed radial axis reduction against public CHEASE
has order 1.30, consistent with the prior ladder; the warm state remains
unqualified at the common target and native stopping. E2 has a numerical
resolution/cost classification with finite-reference sensitivity; no native
defect is established. q/Phi are input-transfer checks. The existing samples and common references are reused without a solve.

| Inverse case | Retained VMEC++ result | Remaining target/budget |
|---|---|---|
| E1 constant-q | NS257, 16.79 s; common-KIN axis 7.136e-7 | Sampled targets and native stopping pass. |
| E2 constant-q | NS897, additional 236.61 s; common-KIN axis 1.140e-6 | Axis and strict native stopping remain open; observed per-iteration cost would make a 40000-iteration NS897 budget about 590 s, without guaranteeing convergence. |
| Exact Solovev | NS257, 26.83 s; axis 1.472e-4, Bpol L2 8.404e-5 | Expected-rate radial convergence; NS513 already timed out at 300 s. Extrapolating the latest axis rate needs order 17000 radial surfaces, not an affordable target control. |

The axis/resolution and iteration-budget projections are estimates, not executed
fine-grid results or matched costs. All native inputs, saved states and capped
attempts remain retained; historical curves and timing pins are unchanged.
The original DESC Solovev L12 curve misses psi, Bpol and axis targets. The
retained L14/400 state already meets all sampled exact targets but exhausts its
`gtol=1e-12` budget. A same-input warm restart with `gtol=1e-9` stops after two
iterations: psi L2=2.91e-7, Bpol L2/max=2.08e-6/5.16e-6, Btor L2=3.72e-8,
axis=5.84e-9 and volume=3.11e-14. Prescribed q/Phi transfer errors are
3.11e-13/0. [Native stopping controls](desc_target_controls.csv) retain both
states and settings. The additional 34.03 s on CPU6 is a warm restart cost;
the original CPU14 timing and historical capped flags remain unchanged.
This closes DESC's sampled target and stopping gap without a solver fix.

The plotted KIN6D P3 forward point is an existing Phase 1 n=48 result with
2854 DOF, Bpol error 7.83e-6 and mean producer time 0.272 s across three timing
repeats. It used Phase 1's 4000 points and forward FFprime; it is explicitly
context, not an inverse timing/rate claim. E1/E2 forward references prescribe
different q and cannot serve as constant-q truth.

## Export and actual-consumer readback

All twelve accepted public grids were read as native Hermite NOUT, EQDSK by
the repository, and EQDSK through actual libneo (the direct NEO-RT field path).
[exports.csv](exports.csv) uses the same 600 physical points. At NS32/128,
[boozer.csv](boozer.csv) checks the libneo Fourier conversion plus actual
scalar NEO-RT/NEO-2 readback; [consumers.csv](consumers.csv) adds actual
GPEC/DCON and full NEO-2 vector/current/Jacobian/flux-label readback.
Consumer norms use their own R-weighted physical query grids and are not
identical quadratures to the producer norms above.

| Finest public input / reader | E1 Bpol L2 | E2 Bpol L2 | Solovev Bpol L2 |
|---|---:|---:|---:|
| EQDSK / actual libneo | 8.91e-09 | 9.94e-09 | 2.55e-06 |
| GPEC/DCON | 8.00e-07 | 1.54e-06 | 2.86e-06 |
| Full NEO-2 | 6.22e-08 | 6.91e-08 | 2.49e-06 |

On the frozen Solovev NS128 export, m24 Boozer truncation leaves a worst-surface
Bpol L2 error of 5.48e-5 and s_tor error 2.46e-5. Refining only Fourier m to48
reduces them to 2.56e-6 and 5.17e-7; |B| is 5.31e-8 and q is 2.53e-6.
[boozer_m48.csv](boozer_m48.csv) retains that control. This is a converging
numerical truncation effect, not a new solver defect. Full NEO-2 uses m48 for
the finest Solovev row; other rows use m24. Finest GPEC/NEO-2 Jacobian errors
are <=2.35e-7. For constant-q reader rows, q error measures transfer relative
to native NS128; imposed-q error remains in comparison.csv.

The NOUT prescribed-q layout defect is repaired with an exact-field regression
([EQ-P3X-1](../../ERRATA.md#eq-p3x-1-prescribed-q-nout-record-layout)). NEO-2 uses
the retained multi-surface reader repair #193. MARS supplies no valid native
state to export. VMEC++/DESC downstream conversion has no executed perturbation consumer here;
the [Phase 1 path disposition](../../phase1/results_export/README.md#consumer-inventory-and-bounded-gaps)
applies to the same native wout/HDF5 states. These exclusions do not qualify an
unused converter. KIN6D inverse NEO-2 and native-contour Hamada checks are in
[the KIN6D supplement](kin6d.md).

## MARS disposition and reproducibility

MARS has no accepted prescribed-q equilibrium. Historical failures retain their
executed patch sets; [EQ-D88](../../ERRATA.md#eq-d88) distinguishes omitted known
fixes from the residual failure in the fully corrected source. The NS64 warm
Solovev comparator includes qualified fork PR30/31/37/39/41/42/45 and excludes PR43,
the zero-moment regression, the public-algorithm port and superseded axis extrapolation.
Its owning native gates pass, but both NINSCA=100 and NINSCA=1 fail the coupled solve.

The independently checked first constrained GS linear solve has relative residual
1.054e-12. Exact-source replay locates most of the first departure in near-axis
prescribed-q/coarea differentiation. Compatible retained forward fields reduce
the inferred source error strongly with physical mesh refinement, but its irregular
rate remains unqualified; [EQ-D88](../../ERRATA.md#eq-d88) owns the controls and
limits. Failed states supply failure evidence, not convergence or cost-to-target data.

Fork PR39/41/42 and public PR15 have scoped source-parent regressions. PR43 is
closed with its branch, complete reproducers and isolated axis/under-axis controls
retained; its continuous TMF/source representations remain inconsistent. Issue44
retains the unresolved inverse failure. Current heads, prerequisites and dispositions
are owned by [UPSTREAM_PRS](../../../review/UPSTREAM_PRS.md).
MARS Pair A/B and full inverse qualification are not claimed.

The [run registry](../../../results/run_registry.json) owns job IDs, commits,
pre-execution hashes, manifests, admissions and raw locations. Each selected
JSON here lists its native root and every normalization trial. Raw requests,
decks, logs, outputs and consumer manifests stay under
`/home/ert/data/iter_tc24/phase1/<code>/runs/<tag>`. No running jobs remain.
Focused behavioral regressions: 29 passed, 1 skipped (libneo unavailable in
the pytest venv; the actual libneo reader executions succeeded separately).

From the repository root, with a disk scratch directory and a unique new tag:

```sh
export TMPDIR=/home/ert/code/worktrees/_lanes/phase3x/tmp
mkdir -p "$TMPDIR"
python -m equilibrium.phase3.compare --tag NEW_UNIQUE_TAG --codes chease_public chease_mars vmecpp desc --public-source PUBLIC_CHECKOUT --mars-source MARS_CHECKOUT
python -m equilibrium.phase3.exports
python -m equilibrium.phase3.boozer
python -m equilibrium.phase3.boozer --mpol 48 --cases Solovev_inverse_A3 --levels 3
python -m equilibrium.phase3.consumers
python -m equilibrium.phase3.analyze
python -m equilibrium.phase3.plot --figures DISK_FIGURE_DIRECTORY
uv run python ops/run_registry.py
```

Use the pinned native Make configurations/build logs in source_pins.json;
force MARS rebuilds with `make -B`. compare.py owns the documented separate
solver Python environments and the finer levels; native paths can be restored
from the source archives. Analysis/plot commands reuse retained data without
solver execution. PNG/PDF URLs and SHA256s are in [artifacts.json](artifacts.json).

| Case | Convergence and cost | Consumer readback |
|---|---|---|
| E1 constant-q | [PNG](https://box.sloppy.at/dfb91.png), [PDF](https://box.sloppy.at/4e4bc.pdf) | [PNG](https://box.sloppy.at/bc0b6.png), [PDF](https://box.sloppy.at/5647f.pdf) |
| E2 constant-q | [PNG](https://box.sloppy.at/ed25f.png), [PDF](https://box.sloppy.at/9c2fa.pdf) | [PNG](https://box.sloppy.at/9ee41.png), [PDF](https://box.sloppy.at/ad9e1.pdf) |
| Analytic Solovev q | [PNG](https://box.sloppy.at/6059e.png), [PDF](https://box.sloppy.at/d7126.pdf) | [PNG](https://box.sloppy.at/8cf95.png), [PDF](https://box.sloppy.at/4faa9.pdf) |

KIN6D's native producer, signed export/readback checks, resolution ladder and
run command are in [kin6d.md](kin6d.md). `kin6d_slot` remains available for
importing separately registered runs. Re-running `equilibrium.phase3.analyze`
with the delivered KIN6D JSON rows adopts its finest inverse result as the
circular-case reference; the historical other-code CSVs above remain unchanged
in this patch.

Chris&AI
