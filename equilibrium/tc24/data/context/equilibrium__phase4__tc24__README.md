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

For resolved smooth fields, the predicted cubic FE rates are psi O(h⁴),
Bpol O(h³). Adjacent CHEASE differences give apparent Bpol rates 2.81 then
1.87; KIN6D's latest generalized three-grid rate is 2.07 (psi 3.53).
These do not yet establish the required asymptotic regime. The finite-reference
and mixed radial/angular VMEC ladder also preclude a target-level extrapolation.
Do not use cross-code agreement as a replacement for these missing error bounds.
KIN6D's recovered-flux estimates fall from 1.97 to 0.678 Wb m⁻¹ᐟ²; status 4
identifies a frozen-source estimate, not a proved nonlinear stability bound.

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
