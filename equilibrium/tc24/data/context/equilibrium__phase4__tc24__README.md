# Phase 4b: the collaborator TC24 reference

**The reference is Xingting's `ngfile_p1_run_eq_modx03_20260527`.** The
[provenance table](EQUILIBRIUM_PROVENANCE.md) owns the mail, file, deck and
historical-run evidence. It is the equilibrium selected by maintained GPEC
inputs and identified by the exact MD5 in Logan's results. JINTRAC,
`gfile_chease` and Leonardo's CHEASE file are explicit variants.

The five-code convergence/cost study and measured export package are
implemented and executed. **Accuracy qualification remains open.** The
reference's popularity is evidence of identity, not numerical accuracy.
No candidate here is admitted for production perturbation calculations.

## Exact supplied-input replay

The August Edoardo EXPEQ and MARS namelist are copied without physics edits
for MARS CHEASE. Public CHEASE receives the same plasma boundary and profiles
in its supported EXPEQ format; unsupported `NQMIN`, `QWIDTH0`, `ROTE`, `NTOR`
entries are omitted, and unused downstream `MSMAX=40` is reduced to 20.
These translations are explicit in [reference_study.py](reference_study.py).

The supplied selector is **NSTTP=2 (Istar), NCSCAL=4 (no current rescaling)**.
CURRT corresponds to 15.563913 MA but is not an enforced current constraint.
The supplied log reports 15.5614975 MA; the re-run MARS log reports
15.5614977 MA. Agreement with the printed log does not imply round-off
agreement with the separately delivered gfile.

| Replay, NS=NT=80 | Process wall / s | Output Ip / MA | Bpol L2 difference from received modx03 |
|---|---:|---:|---:|
| MARS CHEASE, supplied deck | 16.43 | 15.5614977 | 8.421e-3 |
| Public CHEASE, translated deck | 26.20 | 15.5438362 | 9.235e-3 |

[replay.csv](reference/replay.csv) retains roots, signed axis flux and psi/Bpol
comparisons on the common interior sample. No native Btor result is claimed
for the MARS replay: that NOUT reader requires a separately delivered F profile.
Public/MARS replay differences and the source-file discrepancy remain measured,
not explained away as round-off or used to fit an input.

## Common interior problem

[reference_case.json](reference/reference_case.json) and its two CSVs own
the numerical input. The domain is the 128-mode, vertically asymmetric curve
extracted at source s_pol=0.995 from 4096 rays. It excludes the separatrix.
All fields below are SI, COCOS 3: BR=-psi_Z/R, BZ=psi_R/R, Bphi=F/R.
The source CHEASE COCOS-2→3 map gives negative F, current and axis psi, and
negative q. JINTRAC uses the explicitly adopted 7→3 map and has the opposite
physical field polarity; no sign is fitted across variants.

| Reference input | Value |
|---|---:|
| Source axis psi in the new edge-zero gauge / Wb rad⁻¹ | -11.82338145675 |
| Enclosed current from the independent Ampere contour / A | -15481528.84405 |
| F at the new edge / T m | -32.85217412825 |
| Pressure at the new edge / Pa | 10534.8939315 |

The forward law uses s=1-psi/psi_axis, with the solved axis flux. Derivative
shapes P(s), G(s) come from differentiating the stored pressure and F²/2
primitives and resampling their derivatives on 513 normalized-flux knots.
The inconsistent JINTRAC derivative columns never enter a solve. A common
positive amplitude multiplies both shapes and fixes total current. This is
a **derivative-shape/current** contract, not fixed dimensional p(s) primitives:
scaling psi by a scales derivatives by a and pressure/F² differences by a².
F_edge is fixed; MARS's final pressure additive constant follows its native
PRNORM operation and does not enter the GS force equation.

Both CHEASE variants use NSTTP=1/NCSCAL=2 for this derived problem. KIN6D P3
uses main [5dfb9df](https://github.com/itpplasma/kin6d/commit/5dfb9df), on the
curved cubic-profile implementation 2d8142a. It integrates the signed source
current before Dirichlet elimination and applies the same homogeneous scale.
Analytic current and field-scaling oracles pass; CPU and Debug each pass 81/81.
This new capability does not alter the supplied Istar replay. The retained
binary was built before the commit, so its embedded stamp names 2d8142a with
a dirty tree; the tested source was subsequently committed as 5dfb9df.
Pre-execution binary hashes remain authoritative for the executed states.

VMEC++ and DESC receive boundary, p(s_tor), iota(s_tor) and full Phi from the
finest public CHEASE state (NS32 for variants). This is a finite-reference
inverse transfer: q and Phi are prescribed, current is a measured output.
It becomes equivalent to the forward state only to the accuracy of the
reference and transfer. The small prescribed-q error is not an independent
q prediction. DESC's useful runs use retained VMEC geometry as an initial
guess, followed by a native DESC solve; the default-initialization failures
are also retained. Seed production cost is additional to DESC's tabulated wall.

## Convergence and cost

[Runs](reference/runs.csv), [common comparisons](reference/comparison.csv),
[adjacent differences](reference/convergence.csv) and the
[execution inventory](reference/execution.csv) contain all retained outcomes.
One thread per solve, fixed CPU affinity, hard 300-second limit; elapsed
process wall includes setup. These are single observations on a shared host,
not a timing uncertainty study; KIN6D n32 overlapped the initial test workload.

The comparator is public CHEASE NS128/NT256, **not an exact solution**.
Bpol/psi use R-weighted L2 over 1200 fixed area-uniform interior points
(0.001<s_pol<0.98). Maxima use the same samples, not continuous-domain bounds.
q is compared on 80 points, 0.05≤s_tor≤0.98. Axis, volume, flux and current
errors are separate columns. Failed coordinate inversions invalidate the
whole field comparison; no failed points are omitted from a reported norm.
NOUT psi/BR/BZ receive CHEASE's explicitly logged final SCALE before combining
with delivered F; this is the executed PRNORM map, not a fitted normalization.

This table retains the original study's binary pins and timings; the later
KIN6D controls below do not relabel those measurements.

| Code / finest completed state | Wall / s | Bpol L2 difference | psi L2 difference | q max difference |
|---|---:|---:|---:|---:|
| Public CHEASE, 128×256 | 190.94 | comparator | comparator | comparator |
| MARS CHEASE, 128×256 | 78.84 | 3.052e-5 | 3.437e-7 | 1.215e-6 |
| KIN6D P3, n96, 8479 free DOF | 230.49 | 1.368e-3 | 2.867e-5 | 3.765e-3 |
| VMEC++, ns129/mpol33 | 72.50 | 1.961e-3 | 1.422e-4 | 5.200e-4 |
| DESC, L20/M10, VMEC seed | 143.69 | 3.334e-2 | 1.313e-2 | 6.715e-9 (prescribed) |

CHEASE ladders are NS=16/32/64/128, NT=2NS. KIN6D uses n=16/24/32/48/64/96.
VMEC++ ns257/mpol49 and DESC L24/M12 hit the time limit. DESC's lower default
seeds hit iteration caps and had nonfinite readback points; the VMEC seed
improves stopping but does not qualify its fields. Finest VMEC++ current is
0.301% below the prescribed-forward target in magnitude; DESC is 8.56% below.
The retained spectral decks also truncate the pinned 128-mode boundary.
[Geometric distances](reference/spectral_boundary_resolution.csv), measured
between both curves on 131072-point closed polylines, give maximum nearest-curve
distances of 161.50/120.93 mm at DESC M=10/12 and 19.05 mm at VMEC++ max m=32
(mpol=33). These are geometric distances; tangential parameter differences do
not determine them. Thus the field comparisons include substantial boundary
error. A native L24/M12 restart from retained DESC L20/M10 also hits the 300 s
cap before saving a state; it supplies no refined accuracy point. DESC's target
qualification remains open, and no native solver defect is established.

The [fixed-angular VMEC controls](reference/vmecpp_controls.csv) retain the
same NS128 reference p/iota/Phi transfer, tcon0=0 and ftol=1e-12, while fixing
mpol=33 and refining NS=33/65/129. [Successive differences](reference/vmecpp_self_convergence.csv)
give Bpol radial order 1.30 and psi order 1.74, consistent with the predicted
at-least-first-order radial convergence. Absolute Bpol differences remain
2.71e-3/2.06e-3/1.96e-3. The [boundary truncation](reference/vmecpp_boundary_truncation.csv)
is substantial: mpol=17/25/33/49 miss the pinned 128-mode curve by
76.5/36.5/19.2/6.00 mm maximum (11.67/5.15/2.62/0.834 mm RMS). These
are different physical domains, so the absolute difference and current gap
cannot establish a native solver defect. At fixed NS65, mpol49 fails native
stopping after 157.45 s: fsql=1.31e-10 exceeds ftol=1e-12 despite small R/Z
residuals. Its failed input and log are retained. No angular target or wrong-limit
claim follows. New controls use CPU5, one thread; their single-run times do not
replace the earlier cost ladder or establish a matched hardware ranking.

For resolved smooth fields, the predicted cubic FE rates are psi O(h⁴),
Bpol O(h³). Adjacent CHEASE differences give apparent Bpol rates 2.81 then
1.87; KIN6D's original generalized three-grid rate is 2.07 (psi 3.53).
The retained n128/192/256 ladder instead gives 1.09 for Bpol and 1.19 for psi
on its last three grids. Its n192→256 Bpol difference is 3.514e-4.
These do not yet establish the required asymptotic regime. The finite-reference
and mixed radial/angular VMEC ladder also preclude a target-level extrapolation.
Do not use cross-code agreement as a replacement for these missing error bounds.
KIN6D's recovered-flux estimates fall from 1.97 to 0.678 Wb m⁻¹ᐟ²; status 4
identifies a frozen-source estimate, not a proved nonlinear stability bound.

[Quadrature controls](reference/kin6d_controls.csv) use KIN6D `af84393`,
the same modx03 inputs and nonlinear tolerance 1e-9. At n96, changing only
the source quadrature tolerance from 1e-7 to 1e-5 reduces process wall time
from 33.13 to 13.93 seconds (native solve 31.86 to 12.46 seconds). On the
same 1200 field points and 80 q points, the changes are psi L2 1.692e-7,
Bpol L2 1.455e-6, Bpol max 2.169e-5 and q max 6.535e-7. This is a measured
tolerance sensitivity, separate from spatial error. Both unchanged-main
n320 tolerances hit the 300-second cap. These single-core timings overlap
other lanes and remain exploratory; they establish no fastest-code claim.

The isolated rank-one Newton-response candidate `1996a4e` completes the same
n320, 1e-5-quadrature input in 197.05 seconds, versus unchanged main's
300-second cap: an observed bounded speed ratio greater than 1.52 under
these conditions. Its residual is 1.381e-10. The final safeguarded implementation
is on KIN6D main at `f6a33c9`, with CPU and Debug each passing 106/106 tests.
The estimator takes 35.95 seconds and its recovery reaches
the 6000-iteration cap, so its frozen-source estimate is not minimized.
The n256→n320 Bpol difference is 2.412e-4, psi 1.398e-6 and q 3.670e-5.
That comparison changes quadrature tolerance as well as mesh resolution;
it does not establish a clean spatial convergence rate.

The [held-quadrature refinement](reference/kin6d_refinement.csv) uses the same
physics and quadrature 1e-5 at n256/320/384. The n320 source remains the retained
rank candidate; n256 and n384 use promoted main `f6a33c9`. At n256, the change
from its original 1e-7 quadrature gives only Bpol L2 1.418e-7 and psi L2 2.807e-8.
The new ladder gives generalized Bpol order 3.66 (predicted 3), and psi 3.57
(predicted 4, with finest psi already below target). Median cell flux spans in
the outer pedestal are 0.02236/0.01840/0.01534; its source variation scale is
about 0.017. The original low rates were preasymptotic numerical resolution.
98.94% of the last squared Bpol difference lies at s_pol>0.9.

Against finite public CHEASE NS320/NT640, KIN6D n384 gives psi L2 3.744e-7,
Bpol L2 6.031e-5 and Bpol max 4.700e-4: Bpol remains about six times its L2
target. The full-B L2/max values 1.040e-5/1.021e-4 do not replace the component
gates. Axis relative error is 3.002e-5, about thirty times target; public
NS256→320 axis uncertainty is only 1.098e-9. Volume/Phi differences are
5.302e-9/3.652e-8. The public Bpol difference 5.336e-5 remains finite-reference
uncertainty, separate from KIN6D self-convergence. Native q qualification uses
the consumer's separately pinned refined profile readback.

The [matched fine-q readback](reference/kin6d_q_convergence.csv) holds the
saved q5 n256/320/384 PDE states and uses 2049 radial/320 angular points for
all three. Against the same public NS320 state, max q gaps on held s_tor
labels 0.05–0.98 are 2.352e-4/1.148e-4/5.866e-5; at the original physical
points they are 2.439e-4/1.106e-4/6.573e-5. The separate public NS256→320
changes are 1.129e-5 on held labels and 1.152e-5 at physical points. These
finite-reference differences are not exact-error bounds; q is not yet
qualified at 1e-5. Adjacent held-label changes, with fixed NS320 normalization,
fall from 1.204e-4 to 5.610e-5. No Richardson q order is inferred: the signed
difference profiles have a 73% residual after fitting a common leading mode,
and only 45% of sampled labels have the same difference sign. The independent
n256 q5/q7 fine-readback sensitivity is only 7.104e-8. Readback-only costs are
9.40/12.60/14.65 s; they exclude the original PDE producers. Saved fields are
unchanged, and original coarse-readback timings and conclusions retain their
original scope.

The completed n384 process takes 448.66 s, including 396.88 s for mesh,
assembly/solve/current normalization together and 47.70 s for the estimator;
contour and area readback take 0.50/2.36 s. Five Newton iterations converged,
but linear-iteration and phase counters were not recorded, so no finer timing
breakdown is asserted. These concurrent-lane times remain exploratory. The
recovery again stops at 6000 iterations with status 4: its frozen-source
estimate is not minimized and does not establish nonlinear reliability.

[Finite-reference controls](reference/reference_uncertainty.csv) compare
the retained public CHEASE NS128/NT256 and NS256/NT512 states on the same
original samples, with norms normalized by NS256. Their differences are
psi L2 7.624e-6, Bpol L2 6.218e-4 and q max 9.914e-5. KIN6D n256 versus
that NS256 state gives psi L2 1.653e-6, Bpol L2 2.578e-4 and q max 2.912e-3.
Both execute NSTTP=1/NFUNRHO=0, bypassing mapped-profile feedback into the
PDE. Their NCHI change from 1000 to 600 affects the angular export mesh,
not the native field solve or q contour integrals. It does not confound the
native Bpol difference. The delivered q difference still includes changes
in NT quadrature and NPSI/NISO profile sampling, so it supplies no separate rate.
Thus the older NS128 comparison contains appreciable reference uncertainty;
the newer comparison still does not qualify KIN6D at the targets.
The candidate n320 state versus NS256 gives psi L2 7.853e-7, Bpol L2
1.112e-4 and q max 2.934e-3 using the original readback configuration.

The larger [public NS320 reference](reference/reference_uncertainty_n320.csv)
completes in 1133.66 s, with 37.50 GiB peak resident memory. NS256→320 differences
on the same 1200 points are psi L2 4.944e-7, Bpol L2/max 5.336e-5/2.383e-4
and q max 1.129e-5. The largest Bpol difference lies in the interior at
s_pol=0.295. Unequal-grid apparent rates are 3.13 for psi and 2.62 for Bpol,
but successive difference vectors are poorly aligned; these estimates do not
establish a Richardson error bound. Bpol and q reference uncertainty still
exceed their targets.

Saved-state readback controls hold the n256 mesh, field and profile law fixed.
The original 129-radial/160-angular readback is reproduced byte for byte;
257/320 and 2049/320 reduce the q gap against public NS256 at held s_tor
from 2.912e-3 to 7.115e-4 and 2.288e-4. At the same physical sample points,
the final gap is 2.364e-4. Native q at common psi agrees within 1.04e-14 and
edge toroidal flux is unchanged: coarse radial-label interpolation explains
most of the original q gap. The final readback takes 9.30 seconds, without a
PDE solve. Differences imply apparent orders 3.79 for cumulative flux labels
and 2.90 for q interpolation across unequal refinements; these do not establish
an asymptotic rate. The remaining producer/reference gap exceeds the 1e-5 target
and remains unqualified. Executed settings and raw roots are in
[the control table](reference/kin6d_controls.csv); original producer costs and
finite-reference comparisons remain unchanged.

## Received variants

Each variant has public/MARS NS32, VMEC++ ns33/mpol17, DESC L12/M6 with VMEC
seed, and KIN6D P3 n16 (Leonardo n24 after a coarse axis rejection).
Native outputs, stopping failures and consumer chains are retained. DESC's
coarse gfile/Leonardo solves stop successfully but their incomplete physical
readbacks remain invalid; JINTRAC DESC hits its iteration cap.

[variants.csv](reference/variants.csv) compares original files on their common
interior support. Relative Bpol-magnitude differences from modx03 are 0.222%
(gfile_chease), 3.00% (JINTRAC), and 2.10% (Leonardo). Signed differences are
also retained: JINTRAC is about 200% because its declared physical polarity
is reversed. The derived normalized-current variants are distinct equilibria,
not attempts to force the same field. Leonardo retains R0=6.0 and F_edge=31.80.

## Exports, artifacts and reproduction

[EXPORTS.md](EXPORTS.md) owns the measured candidate G-EQDSK/Boozer package,
consumer failures and unused paths. [artifacts.json](reference/artifacts.json)
links generated PNG/PDF figures; [export_package.json](reference/export_package.json)
links the portable candidate archive. Plots/PDFs are not committed.

Use a fresh tag for every execution. Solver environments and binary pins are
resolved by `equilibrium.phase1.compare.environment`; raw manifests retain
commands, source revisions and pre-execution input/binary hashes.

```sh
python -m equilibrium.phase4.tc24.reference_study --prepare
python -m equilibrium.phase4.tc24.reference_study --replay mars --tag <unique-tag>
python -m equilibrium.phase4.tc24.reference_study --code public --ns 32 --tag <unique-tag>
python -m equilibrium.phase4.tc24.reference_study --code kin6d --n 48 --binary <gs_phase1-at-5dfb9df> --tag <unique-tag>
python -m equilibrium.phase4.tc24.reference_study --code vmecpp --level 2 --reference <public-run> --tag <unique-tag>
python -m equilibrium.phase4.tc24.reference_study --code desc --level 2 --reference <public-run> --seed <vmec-run/wout.nc> --tag <unique-tag>
<code-python> -m equilibrium.phase4.tc24.reference_analysis --run <run> --reference <public-run>
python -m equilibrium.phase4.tc24.reference_exports --producer <run> --tag <unique-tag>
python -m equilibrium.phase4.tc24.reference_report --output <disk-directory> --upload --package
```

`--name jintrac`, `gfile_chease` or `leonardo` selects a variant.
The report assembles retained runs; it does not launch hidden solves. Actual
vector reader launches use `reference_exports.consumer`, with producer,
export, kind (`gpec`/`neo2`), unique tag and CPU arguments. Fine grid preparation
can select the fixed libneo source through `--eqdsk-reader`; see EXPORTS.

## Historical JINTRAC setup

The concurrent [KIN6D performance study](kin6d_performance/README.md) improves
costs and extends convergence for the historical absolute-psi JINTRAC control.
Its timings, status-5 estimator and n384 results are retained there; they do
not describe the normalized-current modx03 states tabulated above.

The old top-level `case.json`, absolute-psi profile/boundary CSVs, scripts,
figures, package index and unsent collaborator-note draft remain historical.
They defined a different nonlinear problem with a low-current branch and
53.4% Bpol source difference. That was our setup error for benchmark replay;
it does not identify the collaborators' equilibrium or qualify a solver.
JINTRAC also has an independent source-file defect: both supplied derivative
integrals have the opposite sign and a 1.3007% amplitude mismatch to their
own primitives. [ERRATA](../../ERRATA.md) separates these two findings.
No mail was sent or drafted during the re-pin. Historical artifacts are not
the current E5 contract; the `reference/` inputs and provenance above are.

Chris&AI
