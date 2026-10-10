# Equilibrium discrepancies and errata

## Defect ledger

Scope: PLAN Phase 0 DC-2 and the Phase 1–5 accuracy studies. Each row identifies
an existing defect record or explicitly unexplained candidate; an unexplained
value is not a confirmed solver bug. Status describes publication/integration,
not physical qualification. PR open includes drafts; MARS downstream Pair A/B
and human review remain separate gates.

Statuses were reconciled on 2026-10-09 with owning main histories, MR !20
and live PR state. KIN6D main `f1d1791` includes inverse `60bef4c`, performance
`313cde5` and FortNum `901aae0`. New iter_tc24 repairs are **PR open in
[MR !20](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/merge_requests/20)**
until Chris merges them. Historical own-code fixes already on main retain that
status. A closed superseded PR is linked to its active replacement.

Related IDs can share one short current entry. Their full historical text,
withdrawn-code handoffs, tool repairs, superseded diagnostics and below-target
reconstruction studies are in [ERRATA_ARCHIVE](ERRATA_ARCHIVE.md), verbatim.
Earlier uses of “defect” for a nonzero numerical residual do not establish a
code defect under the [PLAN criterion](../PLAN.md#defect-closure-cross-cutting).

| Code | Entry ID | Defect or candidate | Status | PR / commit |
|---|---|---|---|---|
| iter_tc24 / CHEASE reader | [EQ-P3X-1](#eq-p3x-1-prescribed-q-nout-record-layout) | Public prescribed-q NOUT rejected by the forward-only record offsets | PR open | [MR20 / 7fb43ca9d](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/merge_requests/20); quadratic-field regression |
| iter_tc24 / Phase 3 analysis | [EQ-P3X-2](#eq-p3x-2-provenance-metadata-in-result-collection) | Source-provenance index treated as a solver result, aborting reproducible analysis | PR open | [MR20 / e230623ee](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/merge_requests/20); exact-field metadata regression |
| iter_tc24 / DESC producer | [EQ-CYL-1](#eq-cyl-1-desc-continuation-and-omitted-zero-modes) | Continuation rejects a valid symmetric deck with omitted zero Fourier families | fixed on main | `test_desc_continuation_accepts_omitted_zero_fourier_families` |
| libneo | [EQ-EXPORT-1](#eq-export-1-libneo-efit-python-wrapper-kind-map) | EFIT Python wrapper passes float arguments to double Fortran routines | PR open | [libneo #422](https://github.com/itpplasma/libneo/pull/422), `1b867ec` |
| libneo | [EQ-EXPORT-4](#eq-export-4-boozer-geometry-serialization) | Eight-digit geometry coefficients corrupt radial derivative readback | PR open | [fork PR5](https://github.com/krystophny/libneo/pull/5), `08ace36`; independent circular metric regression |
| NEO-2 | [EQ-EXPORT-3](#eq-export-3-neo-2-multiple-surface-initialization) | Full magnetic reader aborts on the second surface | PR open | [PR193](https://github.com/itpplasma/NEO-2/pull/193), `a0b7039` |
| KIN6D | [EQ-P4A-1](#eq-p4a-1) | Valid P3 functional estimate discarded at recovery iteration cap | fixed on main | [99fa2c8](https://github.com/itpplasma/kin6d/commit/99fa2c8) |
| FortNum | [EQ-OH-1](#eq-oh-1) | Brent root finder rejected interpolation steps and fell back to bisection | fixed on main | [fortnum 5f166bc](https://github.com/lazy-fortran/fortnum/commit/5f166bc); kin6d `82d4d1f` pins it |
| KIN6D | [EQ-D76](#eq-d76) | Invalid mu0 accepted | fixed on main | [c8cbbe8](https://github.com/itpplasma/kin6d/commit/c8cbbe8) |
| KIN6D | [EQ-D78](#eq-d78) | P2 connectivity interpreted as P1 | fixed on main | [f073eba](https://github.com/itpplasma/kin6d/commit/f073eba) |
| KIN6D | [EQ-D83](#eq-d83) | Gauge-dependent field/current derivatives | fixed on main | [PR1](https://github.com/itpplasma/kin6d/pull/1) |
| KIN6D | [EQ-D94](#eq-d94) | Valid face endpoint falsely rejected by JVP | fixed on main | [PR3](https://github.com/itpplasma/kin6d/pull/3) |
| KIN6D | [EQ-D99](#eq-d99) | Profile cuts aliased by polynomial source quadrature | fixed on main | [PR4](https://github.com/itpplasma/kin6d/pull/4); inverse integrated as `60bef4c` |
| KIN6D | [EQ-D110](#eq-d110) | Directional load error/gauge omitted | fixed on main | [60bef4c](https://github.com/itpplasma/kin6d/commit/60bef4c) ports the reviewed inverse repair |
| KIN6D | [EQ-D116](#eq-d116) | Outside reference point accepted | fixed on main | [a262675](https://github.com/itpplasma/kin6d/commit/a262675); PR6 closed after integration |
| KIN6D | [EQ-D15](#eq-d15) | Curved P2 magnetic-axis recovery has irregular refinement | fixed on main | [451fa5b](https://github.com/itpplasma/kin6d/commit/451fa5b); local quartic recovery and refinement tests |
| FortFEM | [EQ-D70](#eq-d70) | P2 Hessians omit product terms | fixed on main | [25975b3](https://github.com/lazy-fortran/fortfem/commit/25975b3) |
| FortFEM | [EQ-D75](#eq-d75) | Piola derivative invalid-map success status | fixed on main | [aa05f2c](https://github.com/lazy-fortran/fortfem/commit/aa05f2c) |
| FortFEM | [EQ-D90](#eq-d70) | Large-origin P2 geometry cancellation | fixed on main | [9d0994b](https://github.com/lazy-fortran/fortfem/commit/9d0994b) |
| FortFEM | [EQ-D93](#eq-d75) | Invalid NURBS geometry accepted | fixed on main | [054822d](https://github.com/lazy-fortran/fortfem/commit/054822d) |
| Public CHEASE | [EQ-D14](#eq-d14) | Vertical box mixes SI/normalized units | PR open | [SPC !93](https://gitlab.epfl.ch/spc/chease/-/merge_requests/93) |
| Public CHEASE | [EQ-D23](#eq-d23) | Thin-flux smoothing has too few knots; failed spline status overwritten | PR open | [SPC !95](https://gitlab.epfl.ch/spc/chease/-/merge_requests/95) (cutoff), [SPC !96](https://gitlab.epfl.ch/spc/chease/-/merge_requests/96) (status); PR2 superseded |
| Public CHEASE | [EQ-D30](#eq-d30) | Band counts and addresses overflow int32 | PR open | [PR3](https://github.com/itpplasma/chease/pull/3) |
| Public CHEASE | [EQ-D46](#eq-d46) | Fourth smoothed-jet slot duplicated | PR open | [SPC !94](https://gitlab.epfl.ch/spc/chease/-/merge_requests/94) |
| Public CHEASE | [EQ-D59](#eq-d59) | Singleton/zero-pivot factorization errors | PR open | [PR18](https://github.com/itpplasma/chease/pull/18), split from performance PR5 |
| Public CHEASE | [EQ-D72](#eq-d72) | Effective quadrature count/capacity mismatch | PR open | [PR10](https://github.com/itpplasma/chease/pull/10) |
| Public CHEASE | [EQ-D72](#eq-d72) | Radial endpoint uses singular axis operator | PR open | [PR10](https://github.com/itpplasma/chease/pull/10) |
| Public CHEASE | [EQ-D85](#eq-d72) | Unmatched boundary angle uses unset index | PR open | [PR10](https://github.com/itpplasma/chease/pull/10) |
| Public CHEASE | [EQ-D84](#eq-d84) | Zero-tension q interpolation ignores failure | PR open | [PR13](https://github.com/itpplasma/chease/pull/13) |
| Public CHEASE | [EQ-D85](#eq-d72) | Unsupported Gaussian order uses unset weights | PR open | [PR10](https://github.com/itpplasma/chease/pull/10) |
| Public CHEASE | [EQ-D88](#eq-d88) | Axis normalization predates smoothing | PR open | [PR15](https://github.com/itpplasma/chease/pull/15) |
| Public CHEASE | [EQ-D08](#eq-d08), [EQ-D31](#eq-d31) | Unexplained export/force accuracy; candidate only | open candidate | No numerical-code PR established |
| MARS CHEASE | [EQ-D39](#eq-d39) | Cubic profile primitive factor/sign wrong | PR open | [PR6](https://github.com/gafusion/MARS-Q/pull/6); fork PR30 closed |
| MARS CHEASE | [EQ-D46](#eq-d46) | Fourth smoothed-jet slot duplicated | PR open | [PR7](https://github.com/gafusion/MARS-Q/pull/7); fork PR31 closed |
| MARS CHEASE | [EQ-D59](#eq-d59) | Factorization edge errors/unset success status | PR open | [PR45](https://github.com/krystophny/MARS-Q/pull/45), split from performance PR32 |
| MARS CHEASE | [EQ-D63](#eq-d63) | Axis F uses TMF as interpolation coordinate | PR open | [PR35](https://github.com/krystophny/MARS-Q/pull/35) |
| MARS CHEASE | [EQ-D72](#eq-d72) | Quadrature count/capacity mismatch | PR open | [PR37](https://github.com/krystophny/MARS-Q/pull/37) |
| MARS CHEASE | [EQ-D72](#eq-d72) | Radial endpoint uses singular axis operator | PR open | [PR37](https://github.com/krystophny/MARS-Q/pull/37) |
| MARS CHEASE | [EQ-D84](#eq-d84) | Prescribed-q source-current sign wrong | PR open | [PR39](https://github.com/krystophny/MARS-Q/pull/39) |
| MARS CHEASE | [EQ-D87](#eq-d87) | Undefined/incorrect inner coarea | PR open | [PR42](https://github.com/krystophny/MARS-Q/pull/42); PR40 closed |
| MARS CHEASE | [EQ-D88](#eq-d88) | Axis normalization predates smoothing | PR open | [PR41](https://github.com/krystophny/MARS-Q/pull/41) |
| MARS CHEASE | [EQ-D88](#eq-d88) | Singular F² source/current primitive | open candidate; unqualified PR closed | [PR43](https://github.com/krystophny/MARS-Q/pull/43) branch and isolated regressions retained; [issue44](https://github.com/krystophny/MARS-Q/issues/44) |
| MARS CHEASE | [EQ-D88](#eq-d88) | Remaining inverse failure is unexplained | open candidate | [issue44](https://github.com/krystophny/MARS-Q/issues/44) |
| VMEC++ | [EQ-D12](#eq-d12) | Unexplained boundary/force convergence; candidate only | open candidate | No native solver repair established |
| VMEC++ / readers | [EQ-D22](#eq-d22), [EQ-D29](#eq-d22) | Incorrect odd-mode/axis reconstruction | fixed on main | [Retained reader revisions](data/vmecpp_axis_readback_20261007/manifest.json) |
| DESC / readers | [EQ-D19](#eq-d19) | External profile converts a JAX tracer with NumPy | fixed on main | iter_tc24 `8a2830829` |
| DESC | [EQ-D33](#eq-d19) | Incorrect signed basis labels/units (metadata only) | PR open | [PR2348](https://github.com/PlasmaControl/DESC/pull/2348); fork PR4/5 closed |
| DESC | [DESC-D01](#eq-d19) | Unconverged coordinate inversion returned as computed; docstring promises NaN | fixed on main (reader) | Residual check in `desc_physical_points.py`; upstream PR2347 closed (maintainers keep the behavior) |
| DESC | [EQ-D20](#eq-d20) | Shaped Cerfon boundary truncation | limitation: targets reached at M32 | [Native refinement/stopping controls](phase1/results/desc_target_controls.csv) |
| DESC | [EQ-D20](#eq-d20) | Unexplained unconverged TC24 accuracy | open candidate | No native solver defect established |
| INTERPOS / readers | [EQ-D23](#eq-d23) | Spline failure overwritten by later success | PR open | [MR1](https://gitlab.tugraz.at/plasma/libs/interpos/-/merge_requests/1) |
| INTERPOS / readers | [EQ-D03](#eq-d03) | Valid omitted-E exponent rejected | fixed on main | iter_tc24 `06a0c32ca` |
| INTERPOS / readers | [EQ-D54](#eq-d03) | Incomplete producer-aware COCOS conversion | fixed on main | iter_tc24 `3837efd2f` |
| INTERPOS / readers | [EQ-D57](#eq-d03) | VMEC chart fixture/flux map wrong | open candidate | Repair checked; publication revision unrecorded |
| INTERPOS / readers | [EQ-D24](#eq-d24) | Mixed P1/smooth inverse-profile construction | fixed on main | iter_tc24 `d393327fa`; unsafe ingress blocked |
| INTERPOS / readers | [EQ-D38](#eq-d24) | Nonfinite/incomplete radial maps accepted | fixed on main | iter_tc24 `5e9204e34` |
| INTERPOS / readers | [EQ-D78](#eq-d78) | Mesh version/connectivity ignored | fixed on main | iter_tc24 `d393327fa` |
| INTERPOS / readers | [EQ-D35](#eq-d35) | Inner sample reported as domain-wide force | fixed on main | [Corrected outer readback](data/tc24_shared_force_20261007/README.md) |
| INTERPOS / readers | [EQ-D60](#eq-d35) | Indexwise grids/dimensional tolerance mixed | fixed on main | iter_tc24 `81ab49ff5` |
| INTERPOS / readers | [EQ-D69](#eq-d35) | Vertex-only boundary maximum mislabeled | open candidate | Historical field unchanged; whole-edge correction retained |
| INTERPOS / readers | [EQ-D102](#eq-d88) | Generated standalone/forward EXPEQ headers invalid | corrected reproducer retained | closed [PR43](https://github.com/krystophny/MARS-Q/pull/43) branch preserves generated-input fix; separate local forward fix retained |
| INTERPOS / readers | [EQ-D103](#eq-d103) | Pre/post-normalization fields combined | PR open (TC24 path); other producers open | [MR20 / e76ae302e](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/merge_requests/20); logged-stage polynomial regression |
| INTERPOS / readers | [EQ-D105](#eq-d35) | Nonfinite cylinder references accepted | fixed on main | [Versioned v2 harness](data/periodic_cylinder_native_kim_20261008_v2/README.md) |
| INTERPOS / readers | [EQ-D107](#eq-d35) | Sample RMS mislabeled as volume RMS | fixed on main | iter_tc24 `ef464e4ca` |
| INTERPOS / readers | [EQ-D109](#eq-d109) | Pressure oracle mixed reference interpolations | fixed on main | iter_tc24 `ece8d6bf4` |
| External evaluator | [EQ-D89](#eq-d89) | Physical force norm omits metric cross term | PR open | [PR1](https://github.com/dpanici/VMECerror/pull/1) |
| FortSym | [EQ-D111](#eq-d111) | Generated real64 alias shadows legal arguments | fixed on main | [f749e65](https://github.com/lazy-fortran/fortsym/commit/f749e65) |
| KIN6D | [EQ-KINV-1](#eq-kinv-1-exported-central-field-used-the-nominal-input-f) | Nominal F used in the producer EQDSK header | PR open | [MR20 / afbd61e90](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/merge_requests/20); manufactured profile regression |
| FortNum | [EQ-KINV-2](#eq-kinv-2-brent-rejected-convergence-on-its-last-permitted-update) | Convergence rejected on the last allowed Brent update | fixed on main | [901aae0](https://github.com/lazy-fortran/fortnum/commit/901aae0); KIN6D `fde93a9` pin |
| KIN6D | [EQ-CYL-2](#eq-cyl-2-kin6d-coarse-p3-readback-failures) | Coarse Lundquist P3 axis/readback rejection | fixed on main | KIN6D `bb2ec06` / `0e56e29`; both retained inputs replay successfully |
| iter_tc24 | [EQ-TC24-1](#eq-tc24-1-signed-boozer-comparison-readback) | Unsigned Boozer comparison drops poloidal polarity | PR open | [MR20 / 0e9f8d1b5](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/merge_requests/20); analytic polarity regressions |
| libneo | [EQ-TC24-2](#eq-tc24-2-boozer-converter-signed-prescribed-boundary) | Prescribed Boozer boundary assumes increasing psi | PR open | [PR3](https://github.com/krystophny/libneo/pull/3) |
| iter_tc24 | [EQ-TC24-3](#eq-tc24-3-wrong-absolute-psi-tc24-setup) | Absolute-psi setup selects a different TC24 problem | PR open | [MR20 / e76ae302e](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/merge_requests/20); explicit normalized-current contract |
| iter_tc24 | [EQ-TC24-5](#eq-tc24-5-native-contour-checker-loses-exterior-initial-guesses) | Exterior first guess rejects a valid native contour | PR open | [MR20 / e76ae302e](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/merge_requests/20); signed circular q/flux oracles |
| iter_tc24 | [EQ-TC24-6](#eq-tc24-6-gpec-comparison-drops-the-toroidal-flux-sign) | GPEC comparison drops signed toroidal flux | PR open | [MR20 / e76ae302e](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/merge_requests/20); four polarity oracles |
| GPEC | [EQ-TC24-7](#eq-tc24-7-gpec-field-line-failure-diagnostic) | Field-line failure formatter overflows its buffer | PR open | [PR1](https://github.com/krystophny/GPEC/pull/1); underlying step-limit failure remains open |
| libneo | [EQ-TC24-8](#eq-tc24-8-libneo-python-eqdsk-four-digit-dimensions) | Four-digit EQDSK dimensions fail whitespace parsing | PR open | [PR4](https://github.com/krystophny/libneo/pull/4) |
| libneo | [EQ-EXPORT-2](#eq-export-2-boozer-flux-boundary-and-header-precision) | Regular boundary scan and low-precision header limit exported flux | PR open | [PR423](https://github.com/itpplasma/libneo/pull/423); personal-fork PR2 closed |
| KIN6D / TC24 | [EQ-TC24-3](#eq-tc24-3-wrong-absolute-psi-tc24-setup) | modx03 Bpol rates and nonlinear estimator stability unqualified | open candidate | [Convergence](phase4/tc24/reference/convergence.csv); status-4 estimate is diagnostic |

## Live entries

<a id="eq-d03"></a>

## EQ-D03: GEQDSK parsing and convention maps

Class: defect; affected: shared GEQDSK reader and sign-convention fixtures. The reader rejected valid
omitted-E Fortran exponents, and current-sign inference could apply the wrong CHEASE COCOS map. Explicit
conversion now transforms the complete flux/field/current/derivative tuple; parser and all-16-COCOS physical
oracles pass. Fix: iter_tc24 `06a0c32ca` / `3837efd2f`, [reader](../NEO-RT/standardize_tc24_eqdsk.py); status:
fixed on main. Related EQ-D54/EQ-D57 details are archived; the corrected VMEC chart fixture preserves physical
fields, but its published repair revision is not identified in the retained record. Current data must declare
their source convention.

<a id="eq-d04"></a>

## EQ-D04: TC24 input consistency and polarity

Class: confirmed **source-file inconsistency** in the original JINTRAC export. The integrals of its
stored pprime and FFprime are −1.013007 times the changes in p and F²/2: wrong sign and 1.3007% amplitude,
invariant under a coherent COCOS map. Preserve the received bytes. No original exporter code or mail
instruction establishes a repair; no producer PR is inferred. This source is now a variant, not the TC24
reference. The collaborators' modified CHEASE reference and its usage are established in the
[provenance table](phase4/tc24/EQUILIBRIUM_PROVENANCE.md). Our separate absolute-psi setup mistake is
EQ-TC24-3; derivative reconstruction alone never made that problem a faithful source replay.

<a id="eq-d08"></a>

## EQ-D08: CHEASE export interpolation

Class: unexplained; affected: public CHEASE GEQDSK reconstruction. The retained E0 default export gives
reconstructed q error 1.67e-5 at normalized poloidal flux 0.95, versus 1.35e-8 with NEQDXTPO=4; native q is
already much more accurate. Exterior treatment and nonlocal smoothing both affect interior values, so a solver
defect is not established. Fix/PR: none; retain the explicit export selector and test its refinement in Phase
1. Status: open export-accuracy attribution; [original controls](../review/EQUILIBRIUM_CHEASE.md).

<a id="eq-d09"></a>

## EQ-D09: MARS CHEASE final-grid relaxation

Class: discretization (iteration error); affected: MARS CHEASE E0. Finest-grid under-relaxation retained
coarse derivative error despite passing the update stopping test. At NS128, delivered edge q changes from
1.558576423 to 1.558556473 with RELAX=0, matching the independent exact-edge integral. Fix: the E0 input
factory requests RELAX=0; status: controlled for this linear exact case, with nonlinear stopping qualification
separate. No general solver repair is claimed; [same-input
control](data/chease_mars_folded_order_20261008_gs_stage_ns128_smooth1_relax0_v3/delivered_q_and_source.json)
feeds Phase 1.

<a id="eq-d12"></a>

## EQ-D12: VMEC++ force and boundary convergence

Class: unexplained; affected: VMEC++ and its physical-field readback. The coarse TC24 boundary differs by 4.83
cm; finer boundary runs fail. On fixed physical points, tcon1/ns65 → tcon0/ns65 → tcon0/ns129 changes
force/gradp from 1.170 to 0.116 to 0.063, but the ns257 state fails native stopping. These controls identify
sensitivity, not an expected-rate convergence result or a confirmed solver defect. Fix/PR: none; status: open
in Phase 4, including the EQ-D11/EQ-D36 controls. Preserve distinct native covariant/contravariant routes;
[data](data/tc24_force_multi_code_20261007/README.md).

<a id="eq-d13"></a>

- **Phase 1 classification:** the [common comparison](phase1/results/README.md) gives Bpol L2 orders
  1.15 (E0 A3) and 0.97 (Cerfon) over the finest three radial grids, consistent with first-order bulk
  convergence. Maximum errors peak in the first two radial cells; their slower rates (A3 0.56, Cerfon 0.71)
  have the axis finite-difference method classification in EQ-D20. The historical TC24 residual remains an
  open Phase 4 candidate; this Phase 1 result does not resolve it.

## EQ-D13: CHEASE source-law interpolation

Class: input mismatch; affected: both CHEASE TC24 profile adapters. An axis-flux fixed point below 3e-8 still
leaves approximately 0.85–1.15% pressure-derivative and 0.55–0.92% FFprime differences at NS64: native cubic
interpolation differs from the requested piecewise-linear law. Fix/PR: no universal correction; the
[Phase 4b normalized derivative-shape law](phase4/tc24/README.md) supersedes that historical setup;
source interpolation remains part of input transfer, not proof of identical delivered fields. Status: open Phase 4
input-equivalence gate; [profile models](PROFILE_MODELS.md) and
[controls](../research_notes/Remaining%20equilibrium%20discrepancy%20causes/contracts.md).

<a id="eq-d14"></a>

## EQ-D14: Public CHEASE vertical export box

Class: defect; affected: public CHEASE psibox. Mixing the SI axis height with normalized extrema enlarges the
TC24 export box from about 7.35 m to 13.91 m; MARS does not share this error. Fix: use normalized RZMAG before
SI conversion, [SPC !93](https://gitlab.epfl.ch/spc/chease/-/merge_requests/93), `24647f3`. Status: PR open; shifted
exact-case controls fail before and pass after, with the native equilibrium unchanged. This fixes coordinates,
not field convergence.

<a id="eq-d15"></a>

## EQ-D15: KIN6D finite-element representation

Class: discretization; affected: KIN6D P1 fields and polygon boundaries. Fourfold smaller triangle area
reduces the E1/A10 native Bpol difference from 2.790% to 1.346%; exact quadratic interpolation also reproduces
the roughly 1.7% raw boundary-current deficit. Cell-plus-edge current and the conserved variational reaction
are distinct (EQ-D37/EQ-D56). Fix/PR: no implementation defect established; status: explained
finite-representation contribution; the Phase 1 curved-P2 refinement is summarized below.
[Independent current diagnosis](../research_notes/Equilibrium%20discrepancies%20and%20repairs/eqd56.md); avoid
treating vertex-only boundary errors as whole-edge accuracy (EQ-D69).

Phase 1 curved P2 at `cc89c37`: the [common comparison](phase1/results/README.md) finds
the predicted psi/Bpol rates on both exact cases and q below target at the finest settings.
Those historical axis errors are repaired on main `451fa5b`: local quartic
recovery restores refinement on both exact cases. The current P2/P3 CSVs
retain the passing geometry/field results; coarse cylinder axis rejection is
a separate candidate (EQ-CYL-2).

<a id="eq-d19"></a>

## EQ-D19: DESC profile and diagnostic interfaces

Class: defect; affected: project DESC profile adapter and diagnostic metadata.
JAX-compatible profile knots fixed the tracer conversion on main `8a2830829`.
Signed helical labels and units (metadata only; numerical formulas unchanged) are in
open [upstream PR2348](https://github.com/PlasmaControl/DESC/pull/2348); fork PR2/4/5 are
closed. The accepted-step callback PR1 is a closed feature, retained only in historical
execution pins. DESC-D01: `map_coordinates` returns unconverged (e.g. exterior)
inversions as computed although its docstring promises NaN; DESC maintainers keep
that behavior for optimization, so [PR2347](https://github.com/PlasmaControl/DESC/pull/2347)
is closed. Our reader now accepts a point only if the `full_output` root-finding residual
is at most 1e-9 (exterior control: residual 1.6, interior 7e-15). These repairs do not
close TC24 convergence.

<a id="eq-d20"></a>

## EQ-D20: DESC TC24 convergence

Class: unresolved accuracy; affected: DESC TC24 controls. The current modx03
decks truncate the pinned boundary substantially, and the L24/M12 warm restart
hits its time cap without a saved refined state. The [TC24 study](phase4/tc24/README.md)
owns geometric distances and executed stopping. This establishes a boundary
mismatch, but does not assign every field deviation to it or establish a native
solver defect. Earlier contract observations remain in the archived data.

<a id="eq-d22"></a>

Phase 1 shaped case: boundary representation is a numerical limitation.
DESC uses the same poloidal basis for the fixed boundary and solution.
Refining its exact-boundary representation to M24/M32 reduces Bpol L2 to
2.68e-5/1.31e-6. At M32 every sampled target and native stopping pass with
case-specific gtol=1e-9; no solver patch is needed. The
[exact-case study](phase1/results/README.md) owns the norms and warm-start
costs, which do not replace the original cold timing curve.

## EQ-D22: VMEC parity and axis readback

Class: defect; affected: project VMEC++/wout evaluators. Cubic interpolation in s of odd Fourier modes invents
axis derivatives; parity-aware interpolation reduces the exact circular Jacobian error from 2.59e-4 to
1.55e-13. Native hidden m=1 axis coefficients also require explicit endpoint recovery (EQ-D29);
source-faithful readback matches native half-grid fields within 8e-14. Fix: retained project evaluators on
main, [axis readback](data/vmecpp_axis_readback_20261007/manifest.json), [independent
controls](../review/EQUILIBRIUM_VMEC_PP_SIMPLE_CONTROL.md). Status: reader repairs verified; the TC24 force
discrepancy remains open and is not assigned to a native VMEC++ defect. The analytical and regularized readers now preserve canonical
psi under chart reversal: a physical chart-reversal regression failed with reversed psi and passes
after `35583217c`; retained negative-signgs values are unchanged. The Phase 1 producer and the legacy
physical-point APIs now share one parity-aware reader with native m1 axis restoration; exact circular
axis/near-axis round trips fail with the previous physical-point reader and pass after consolidation.

<a id="eq-d23"></a>

## EQ-D23: CHEASE thin-flux current and spline failure

Class: defect; affected: public CHEASE and INTERPOS. An absolute smoothing cutoff leaves too few knots in
A20/A40; INTERPOS then overwrites failed factorization status, producing underflowed current headers. [CHEASE
PR2](https://github.com/itpplasma/chease/pull/2) uses a relative cutoff/minimum knots, and [INTERPOS
MR1](https://gitlab.tugraz.at/plasma/libs/interpos/-/merge_requests/1) preserves failure. Status: PR open for
both; parent/fixed controls recover about -274005/-68469 A with unchanged flux/profile/q arrays. EQ-D49 is the
same defect. MR2 is a fixture-path repair, not another numerical defect;
[evidence](data/gs_case_chain_audit_20261007/README.md).

<a id="eq-d24"></a>

Split: [SPC !95](https://gitlab.epfl.ch/spc/chease/-/merge_requests/95) uses a flux-relative cutoff with at
least four knots; [SPC !96](https://gitlab.epfl.ch/spc/chease/-/merge_requests/96) preserves failed interpolation status
through export. Each has a native test that fails on the parent and passes after; PR2 is superseded.
Phase 1 note: public axis-q extrapolation error falls from 8e-6 to 6e-7 (E0, NS16 to 64) and q on
0.05<=s_tor<=0.98 passes; no axis extrapolation repair is justified at the current target.

## EQ-D24: Mixed finite-element inverse-profile mapping

Class: defect; affected: project P1-to-VMEC profile mapper. Combining P1 contour geometry with smooth
reconstructed gradients gives up to 7.03% q error on an exact quadratic oracle. Production input construction
now rejects that mixed representation; diagnostic replay cannot emit solver input. Finite spans and complete
axis/edge coverage are checked separately (EQ-D38, main `5e9204e34`). Fix: ingress guards on main `d393327fa`;
status: unsafe path blocked, a convergent replacement remains open for Phase 3.
[Mapper](adapters/vmecpp_from_mesh.py); no fitted q or post-hoc smoothing is admitted.

<a id="eq-d25"></a>

## EQ-D25: TC24 separatrix domain

Class: model-domain limit; affected: nested-flux solvers and TC24 comparisons. The original field has an
X-point, while stored CHEASE boundaries sit about 9 cm away and the coarse Fourier boundary about 13.5 cm
away. Exact separatrix coordinates are singular for the nested-surface formulations. The
[Phase 4b boundary definition](phase4/tc24/README.md) pins one asymmetric smooth curve near source
psi_N=0.995 and measures its source-contour reconstruction/projection differences. Status: common
geometry defined; its representation in each solver and resulting equilibrium accuracy remain unqualified.
No solver PR follows from this model-domain limit; [historical audit](../review/TC24_XPOINT_AUDIT.md).

<a id="eq-d30"></a>

## EQ-D30: CHEASE band-address overflow

Class: defect; affected: public CHEASE counts and linear-factor addresses. NS128/NT1024 needs 2,170,601,472
entries, beyond signed int32; overflow skips initialization and corrupts offsets. [CHEASE
PR3](https://github.com/itpplasma/chease/pull/3) uses 64-bit counts/addresses with independent count, zeroing
and known-solution controls. Status: PR open; exact E0 interior parity passes, but a complete large-address
equilibrium has not been demonstrated. No long run is authorized by this record; [retained
pair](data/chease_band64_e0_pair_20261007/prelaunch.json).

<a id="eq-d31"></a>

## EQ-D31: CHEASE native and exported force

Class: unexplained; affected: both CHEASE variants' TC24 field reconstructions. Raw and smoothed-export
derivatives have different errors; angular refinement reduces the public raw GS/source residual from about
25.1% to 11.2% but has not established the expected convergence rate. Exact-E0 interpolation controls explain
much of that separate case's finite-bicubic error. Fix/PR: none established for the remaining TC24
discrepancy; status: open Phase 4 convergence finding. A nonzero weak residual is not itself a confirmed
implementation defect. [Native/export controls](data/chease_native_hermite_audit_20261007/README.md);
historical local-bound analyses are archived.

<a id="eq-d35"></a>

## EQ-D35: Comparison domains and diagnostic measures

Class: defect; affected: project comparison readers. Inner TC24 samples missed over 97% of one state's squared
force; corrected outer queries expose the discrepancy. Related corrections use common physical export points
instead of array indices (EQ-D60, main `81ab49ff5`), distinguish sampled RMS from volume RMS (EQ-D107,
`ef464e4ca`), and reject nonfinite cylinder references (EQ-D105). Status: these repairs are retained; the
historical KIN boundary producer still reports vertices only (EQ-D69), so whole-edge measurement must replace
that field. [Outer-domain data](data/tc24_shared_force_20261007/README.md); [cylinder
correction](data/periodic_cylinder_native_kim_20261008_v2/README.md).

<a id="eq-d39"></a>

## EQ-D39: MARS CHEASE cubic profile primitive

Class: defect; affected: MARS CHEASE ISOFUN. The cubic integral uses the wrong curvature factor and upward
sign. [MARS PR6](https://github.com/gafusion/MARS-Q/pull/6) repairs both directions (fork PR30 closed); native polynomial
controls change from 8/12 to 12/12. One E5 deck changes F and q by 2.7e-5 relative while psi/current remain
unchanged. Status: PR open; controlled-law equilibrium effects and downstream Pair A/B remain pending. [Native
evidence](data/chease_lane_closure_20261007/README.md).

<a id="eq-d46"></a>

## EQ-D46: CHEASE smoothing permutation

Class: defect; affected: both CHEASE SMOOTH routines. The fourth write repeats the third slot, corrupting
cached angular/mixed derivatives. [SPC !94](https://gitlab.epfl.ch/spc/chease/-/merge_requests/94), `b4ed34f`, and
[MARS PR7](https://github.com/gafusion/MARS-Q/pull/7) (fork PR31 closed), historical `e14c6d1`, pass parent-failing four-jet controls.
Status: PR open; inspected physical paths read another array, so this confirmed typo does not explain the
retained force or edge-q discrepancies. MARS Pair A/B remains pending.

<a id="eq-d59"></a>

## EQ-D59: CHEASE factorization edge cases

Class: defect; affected: both CHEASE band-factor routines. Singleton input reads outside storage, a zero pivot
can evade rejection, and MARS leaves successful status uninitialized. [CHEASE
PR5](https://github.com/itpplasma/chease/pull/5) and [MARS PR32](https://github.com/krystophny/MARS-Q/pull/32)
include the repairs alongside contiguous updates; independent dense residual and empty/singleton/singular
controls pass. Status: PR open; no retained equilibrium error is attributed to these edge cases. DC-8 must
assess the mixed correctness/performance PR scope.

<a id="eq-d63"></a>

## EQ-D63: MARS CHEASE axis-field coordinate

Class: defect; affected: MARS CHEASE MAPPIN. Axis-F interpolation supplies TMF(4) where its fourth coordinate
must be CSM(4); constant-F tests hide the error. [MARS PR35](https://github.com/krystophny/MARS-Q/pull/35),
`0e129cf`, changes native-call controls from 2/8 to 8/8 and repairs the ordinary source-integral check without
changing psi/q/nonaxis profiles. Status: PR open; downstream Pair A/B pending. [Actual-call and ordinary
evidence](data/chease_mars_axis_f_oracle_20261008/receipt.json).

<a id="eq-d70"></a>

## EQ-D70: FortFEM polynomial kernels and geometry

Class: defect; affected: FortFEM triangular P2 kernels. Missing product terms made two edge-basis second
derivatives zero instead of -8; independent quadratic reproduction fails 15/18 on the parent. Fix: generated
kernels on main
[25975b3](https://github.com/lazy-fortran/fortfem/commit/25975b30d7740f27b1b918cfd3ce16e6d9980469). Related
large-origin cancellation in legacy P2 geometry (EQ-D90) is fixed on main
[9d0994b](https://github.com/lazy-fortran/fortfem/commit/9d0994b2fb959fb8088327fb8edb5615ec728f68), with
translated-affine controls improving from 18/144 to 144/144. Status: fixed on main; the latter API was not the
executed KIN6D inverse geometry, so it does not explain that discrepancy.

<a id="eq-d72"></a>

## EQ-D72: CHEASE quadrature and boundary validation

Class: defect; affected: both CHEASE variants. Selector expansion leaves stale counts or overwrites storage;
radial endpoint quadrature evaluates a singular axis operator. [CHEASE
PR10](https://github.com/itpplasma/chease/pull/10)/[PR11](https://github.com/itpplasma/chease/pull/11) and
[MARS PR37](https://github.com/krystophny/MARS-Q/pull/37)/[PR38](https://github.com/krystophny/MARS-Q/pull/38)
repair counts/capacity and reject the radial endpoint. Separate public undefined boundary brackets and
unsupported Gaussian orders (EQ-D85) are repaired in
[PR12](https://github.com/itpplasma/chease/pull/12)/[PR14](https://github.com/itpplasma/chease/pull/14).
Status: PR open; native parent-failing moment, sentinel and invalid-input controls pass after, with default
outputs preserved.

<a id="eq-d75"></a>

## EQ-D75: FortFEM invalid-geometry status

Class: defect; affected: FortFEM tetrahedral Piola derivatives and NURBS geometry APIs. Successful
intermediate validation overwrote failure status, allowing collapsed/reversed maps or invalid
weights/denominators to return success. Fixes: main
[aa05f2c](https://github.com/lazy-fortran/fortfem/commit/aa05f2c) and
[054822d](https://github.com/lazy-fortran/fortfem/commit/054822dc93c55b6d40fde4ba0c158abdd0611139) (EQ-D93).
Independent valid/invalid-domain, derivative and cleared-output controls fail before and pass after. Status:
fixed on main; neither API was used by the retained Grad–Shafranov consumer, so no equilibrium error is
attributed to them.

<a id="eq-d76"></a>

## EQ-D76: KIN6D permeability validation

Class: defect; affected: KIN6D solve_gs_profiles. The API accepted zero/negative mu0 and let NaN reach the
nonlinear solve. Main [c8cbbe8](https://github.com/itpplasma/kin6d/commit/c8cbbe8) enforces the
finite-positive precondition before state mutation. Independent valid/zero/negative/NaN calls change from 1/4
to 4/4 passing, with fifteen native GS tests passing. Status: fixed on main; this is input validation, not a
change to the physical model.

<a id="eq-d78"></a>

## EQ-D78: Finite-element mesh representation ingress

Class: defect; affected: KIN6D reference reader and project P1 field/profile readers. Ignoring the mesh
version or extra connectivity silently interprets a six-node P2 element as P1. KIN6D main `f073eba` handles
its supported P2 input explicitly; project main `d393327fa` rejects unsupported versions and forged P1 rows.
Independent curved-quadratic and extra-connectivity controls fail on the parent and pass after. Status: fixed
on main for the stated readers; a generic P2 producer still needs its Phase 1 field/q convergence checks.
[Behavioral regressions](adapters/test_kin_mesh_representation.py).

<a id="eq-d83"></a>

## EQ-D83: KIN6D flux-gauge derivatives

Class: defect; affected: KIN6D scalar-jet composition. Contractions of large absolute nodal flux introduce
spurious field/current for a constant gauge and can reject a stationary axis. Subtracting one local flux value
before primal and directional derivative contractions restores the gauge identity. [KIN6D
PR1](https://github.com/itpplasma/kin6d/pull/1) is merged; independent polynomial/gauge/current/axis checks
change from 313 failures to zero. Status: fixed on main; this does not remove information already lost when
input fluxes were rounded.

<a id="eq-d84"></a>

## EQ-D84: CHEASE prescribed-q source contracts

Class: defect; affected: both CHEASE variants. Public zero-tension NSTTP5 requests an unsupported INTERPOS
boundary combination and ignores failure; [CHEASE PR13](https://github.com/itpplasma/chease/pull/13) uses the
native interpolation branch. Its full native ISOFUN regression fails eight zero-tension
polynomial/mapping cases on the source parent and passes after repair; nonzero-tension
and legacy-selector controls, Make, shared CTest and the retained NS16 inverse smoke pass.
The scoped PR uses the existing shared test target and removes the standalone test packet.
MARS NSTTP4 gives its source-current coefficient the wrong sign; [MARS
PR39](https://github.com/krystophny/MARS-Q/pull/39) restores the native GS chain rule. Status: PR open, with
parent-failing interpolation and signed circle/ellipse controls passing after. Public mixed-stage metrics are
superseded by EQ-D103; MARS full prescribed-q convergence remains unresolved under EQ-D88.

<a id="eq-d87"></a>

## EQ-D87: MARS prescribed-q inner coarea

Class: defect; affected: MARS CHEASE PROFILE. NSTTP4 consumes undefined axis values when tracing begins at
IP>1, and the legacy CID2 axis formula uses the wrong reciprocal meaning. [MARS
PR40](https://github.com/krystophny/MARS-Q/pull/40) repairs initialization; its q4 continuation is superseded
by actual axis-centered inner-contour integration in [PR42](https://github.com/krystophny/MARS-Q/pull/42). The
latter passes 56 native controls and reduces held-field inner error from 62.7% below 3.4e-13. Status: PR open;
the full pilot still fails later, so neither PR is a complete inverse-equilibrium repair.

<a id="eq-d102-mars-standalone-reproducer-generates-invalid-native-expeq-headers"></a>
<a id="eq-d88"></a>

## EQ-D88: CHEASE axis normalization and MARS inverse failure

Class: defect for stale axis normalization; unexplained for the remaining MARS
prescribed-q iteration failure. [Public CHEASE PR15](https://github.com/itpplasma/chease/pull/15)
and [MARS PR41](https://github.com/krystophny/MARS-Q/pull/41) move SMOOTH before
MAGAXE so the field and its axis normalization agree. Both have source-parent
failures, passing repaired polynomial controls and native Make/smoke checks.
Current heads and prerequisites are owned by [UPSTREAM_PRS](../review/UPSTREAM_PRS.md).

The fully corrected warm NS64/NISO100 Solovev comparator contains qualified
fork PR30/31/37/39/41/42/45, checked against actual source changes and eight owning native
test groups. It fails after 39.98 s with mapping residual 1.000035 and positive
psi. Changing only NINSCA=100 to 1 also fails after 2.32 s: the first field update
matches, immediate coarea refresh gives residual 0.999979, and the second field
becomes positive. Prolonged iteration with frozen coareas is therefore not the
sole cause. Neither run supplies an admitted equilibrium.

Independent multiplication of the retained first constrained GS matrix by the
unrelaxed solution gives relative residual 1.054e-12 and normwise backward error
3.324e-16; center expansion, numbering and boundary constraints agree. The seed
has residual 0.005122 against that same load. Independent load assembly agrees
with the retained native load to 2.13e-7 relative. Using exact Solovev pprime=-4/3
and FFprime=0 on the same operator reduces the seed residual to 4.42e-6, locating
most of the first departure in prescribed-q source reconstruction. The largest
FFprime error, 12.51, occurs at Gauss radius 0.000937 below the first coarea knot
0.00505. CURENT differentiates separate rho splines and divides by rho.

With exact analytic coarea data and the same 1025-point q input, native endpoint
differentiation errors fall 2.419e-3 → 2.490e-4 → 2.291e-5 on 100/199/397 knots,
at orders 3.28/3.44. That smooth-data numerical error is too small to explain the
retained state. Compatible exact-source forward NS32/64/128 fields instead give
inferred FFprime errors 37.14 → 11.18 → 0.236 at fixed probes; changing angular
quadrature 256→512 affects them by at most 1.62e-5. Physical mesh refinement
therefore strongly reduces the field/coarea differentiation error, but irregular
orders 1.73/5.57 do not qualify an asymptotic rate. No further defect or repair is
established. The failed coupled inverse iteration remains open in
[issue44](https://github.com/krystophny/MARS-Q/issues/44). Offline inputs, source
hashes and oracle results are retained in
`/mnt/storage/codex-equilibrium-20261010/mars_inverse/scratch/runs/solovev-qualified-firstlinear64/`.

Earlier controls retain their actual patch sets. The fork PR30/31/39/41 plus superseded
axis-extrapolation control omitted PR42. The separate PR39/41/42 control omitted
PR30/31; its negative-F-squared abort is explained by the existing PR30 cubic-primitive
defect. It does not establish a new defect in the fully patched source. With that fix,
the frozen continuous q/coarea resplining discrepancy decreases at third order;
that numerical investigation is closed. Native coarea also agrees with independent
physical-contour integration on the sampled post-update field.

[MARS PR43](https://github.com/krystophny/MARS-Q/pull/43) is closed, with its branch
and isolated axis/under-axis regressions retained. Its direct finite-source API
does not make continuous TMF interpolation consistent with the differentiated
F-squared representation, and it has no qualified full inverse solve. Its header
corrections affect generated test inputs (EQ-D102), not the production parser.
The separate local forward-header fix remains retained. The earlier `450d4d8`
zero-moment regression and unqualified public-algorithm port are also excluded:
the native mode-4 identity is `CID2=1/CIDQ`; BASIS4 does not accumulate the
Bp-squared moment used by the rejected regression.

Leonardo's February 10, 2025 package explicitly distinguishes public and MARS
namelists. Its executed DEMO EXPEQ decks/logs use `NSTTP=2, NCSCAL=4,
NSMOOTH=1`; the EQDSK import runs internally as NSTTP=1. Controller replay of
the supplied EXPEQ profiles with NS/NT changed from 80 to 32 completes on
both untouched MARS and the minimal corrected source in 11.53/10.84 s.
Printed Ip=18.0295556 MA and psi_axis=-21.1905375 Wb/rad agree; q_axis changes
from 1.07349502 to 1.07349744 (2.25 ppm). This checks the working forward path,
not the inverse-q contract. Supplier input SHA-256 is
`cd05519ac95734b8b4b389410a642974a767b3c9c7e87bff34d3f6585cbf893e`;
the original deck is `plasma/data:DEMO/MARS/DEMO_2019_EQUIL_Boozer/CHEASE/DATABASE/EXPEQ.OUT_Istarnew_CS/run_0/INPUTS/chease_namelist`.
All controller inputs, source/binary hashes and outcomes are in the run registry
under `mars-regression-20261010-*`; raw files share its single registered root.

The retained public-algorithm pilot `w2dqmom` reaches residual 7.22e-12 but
q=1.997–2.718 instead of 1.5, so it remains rejected. Its integrated toroidal
flux is 6.41823 Wb versus public 6.43094 Wb; `2*pi*psi_axis` is a poloidal
flux offset. No further source fix is qualified. Full inverse states remain unqualified;
empty final outputs are failed equilibria.

<a id="eq-d89"></a>

## EQ-D89: External force-norm cross term

Class: defect; affected: the external VMECerror evaluator, not DESC's native force calculation. Omitting the
metric cross term gives an incorrect physical-force norm on nonorthogonal charts. [Upstream VMECerror
PR1](https://github.com/dpanici/VMECerror/pull/1) restores it; independent sheared/signed Cartesian-curl
controls change from 12 failures to 16 passes. Status: PR open in the recorded index; historical paper ranking
impact is unknown because the executed historical fields/checkout are unidentified. Native DESC already
computes the complete norm; [derivation and
reproducer](../research_notes/Retained%20equilibrium%20discrepancy%20closure/nested_desc_paper_audit.md).

<a id="eq-d94"></a>

## EQ-D94: KIN6D cell-arc derivative endpoints

Class: defect; affected: KIN6D cell-arc JVP. Re-solving a known face root with a stricter fallback tolerance
falsely rejects a valid contour. [KIN6D PR3](https://github.com/itpplasma/kin6d/pull/3) evaluates the stored
intersection directly; the amplitude identity changes from status 7 to success with 4.44e-16 error.
Independent refined-mesh and native regression controls pass without changing q/root tolerances. Status: fixed
on main; coupled inverse physical accuracy remains separate.

<a id="eq-d99"></a>

## EQ-D99: KIN6D profile-cut integration

Class: defect; affected: KIN6D source loads and derivatives. Polynomial quadrature aliases piecewise profile
laws composed with P2 flux, giving a 10.60% error on an exact load oracle. Generic cut integration is
published in [FortFEM
5af7291](https://github.com/lazy-fortran/fortfem/commit/5af7291d1dae8abf991ff228450700668f64853a), and forward
[KIN6D PR4](https://github.com/itpplasma/kin6d/pull/4) is merged with primal/JVP/VJP regressions. Status:
forward and inverse fixes on main; `60bef4c` ports the reviewed `3a73515` repair. The historical branch-only q/current differences are superseded by
the [curved-P3 inverse study](phase3/results/kin6d.md), which measures the
recovered law, signed source current and field convergence.

The legacy piecewise-linear load still rejects mapped geometry and P3. The separate cubic-profile
path is implemented on main `2d8142a`; normalized current scaling follows in `5dfb9df`, with analytic
current/field scaling oracles and 81/81 CPU plus 81/81 Debug tests. The [TC24 P3 study](phase4/tc24/README.md)
now executes this path. Numerical convergence and estimator qualification remain separate.

<a id="eq-d103"></a>

## EQ-D103: Public CHEASE output-stage normalization

Class: defect; affected: project public-CHEASE observer. Combining pre-PREMAP NOUT fields with
post-TSHIFT/PRNORM EQDSK F changes the represented state. Applying the logged SCALE=1.00000202 gives
final-stage q deviation 2.071835e-6 and sampled strong-force RMS 0.926410 N/m³; the approximately 2.02e-6
normalization shift exceeds the PLAN flux target. Fix: [logged-stage readback
correction](../research_notes/Retained%20equilibrium%20discrepancy%20closure/chease_cqa10_public_postmap_budget_v1.json),
without fitting. Status: historical metrics corrected; Phase 1/3 producers must read one consistent final
stage. The re-pinned TC24 reader applies the explicitly logged final SCALE to NOUT psi/BR/BZ while
retaining final EQDSK F. A polynomial readback test fails before and passes after this map; no ratio
of measured fields or axis values is fitted. No solver defect is inferred.

<a id="eq-d109-vmec-solovev-pressure-diagnostic-mixes-reference-interpolations"></a>
<a id="eq-d109"></a>

## EQ-D109: VMEC++ pressure comparison oracle

Class: defect; affected: project analytic_oracle. Comparing physical-point pressure with a separately linearly
interpolated reference mixed labels and interpolation error. The repaired metric uses exact p(R,Z) at the
field-query points; exact-pressure and injected-error tests fail before and pass after. Status: fixed on main
`ece8d6bf4`; [regression](adapters/test_vmecpp_analytic_oracle.py). Held ns129 pressure RMS changes from the
historical mixed 2.791758702e-7 to 1.666730161e-5; flux/B metrics and the native equilibrium are unchanged.

<a id="eq-d110-kin6d-source-jvp-omits-its-global-quadrature-budget"></a>
<a id="eq-d110"></a>

## EQ-D110: KIN6D directional quadrature and gauge

Class: defect; affected: KIN6D profile_load_products JVP. Only primal estimates entered the global quadrature
check, so an unresolved directional load could report success; tangent composition also failed to shift flux
and knots consistently. Reviewed [3a73515](https://github.com/itpplasma/kin6d/commit/3a73515) checks
directional estimates and differentiates the gauge-shifted inputs, passing 45/45 CPU and Debug tests. Status:
fixed on main `60bef4c`, ported from the reviewed branch. Curved P2/P3
inverse convergence is now measured in Phase 3. Curved inverse sensitivity
and nonlinear-estimator stability remain outside that qualification.

<a id="eq-d111"></a>

## EQ-D111: FortSym generated kind-name collision

Class: defect; affected: FortSym Fortran generator used by KIN6D. Emitting dp=>real64 collides with a legal
argument named dp and prevents compilation. Main
[f749e65](https://github.com/lazy-fortran/fortsym/commit/f749e65a4c00f014d88d0a4786a0689662b6a28f) selects a
case-insensitively unique kind alias for declarations and literals. Generated collision kernels compile and
reproduce independent values; the unchanged KIN6D generator passes its native controls. Status: fixed on main;
no physical parameter rename or hand-edited generated kernel is needed.

## EQ-TC24-1: Signed Boozer comparison readback

Class: defect; affected: iter_tc24's independent Boozer comparison, exposed by
the positive-axis TC24 case. The contour q oracle used unsigned poloidal
circulation, and vector reconstruction always followed increasing canonical
theta. They now retain the sign of dpsi/ds: q uses the signed circulation and
B uses sign(Phi_edge/q) times the unit tangent. Analytic circular oracles cover
both poloidal and toroidal polarities: three new polarity cases fail before
the fix and all six pass after it; 31 focused tests pass. Status: fixed on
the completion branch, [MR !20](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/merge_requests/20) open. No solver or libneo change.

## EQ-TC24-2: Boozer converter signed prescribed boundary

Class: defect; affected: libneo's prescribed finite-flux Boozer boundary.
The bracket scan and bisection assumed increasing flux and rejected TC24's
axis-maximum COCOS-3 input. Orienting both by sign(psimax-psi_axis) preserves
the requested boundary for either polarity. The exact circular flux/q oracle
fails for both negative-polarity scan spacings before the fix and passes all
four cases after it. Status: fixed as `a9b6d96`, draft personal-fork
[libneo PR3](https://github.com/krystophny/libneo/pull/3), stacked on the existing
flux-boundary/header-precision prerequisites; no new upstream submission.
The [TC24 exports](phase4/tc24/EXPORTS.md) use this binary; numerical accuracy
qualification remains separate from the signed-boundary defect closure.

## EQ-TC24-3: Wrong absolute-psi TC24 setup

Class: **our setup error**, not an established solver defect. Pinning JINTRAC primitive profiles to
absolute psi while releasing normalized-profile/current constraints selected a different nonlinear
problem and a low-current branch, with a 53.4% Bpol difference. The old cubic-law states remain historical
mathematical controls; they cannot qualify the collaborators' equilibrium. Fixed at the case/adapter
level by selecting modx03 and an explicit normalized-flux/current contract. Exact supplied Istar replay
is kept separate. KIN6D's normalized source path and its current scaling have analytic polynomial,
current-integral and field-scaling oracles. Numerical target gaps remain in the new study's results.

## EQ-TC24-4: CHEASE selector and Leonardo normalization

Class: input/convention distinction. The supplied Edoardo deck has NCSCAL=4, which does not rescale
the equilibrium to CURRT; NSTTP=2 supplies Istar. NCSCAL=2 is the fixed-current option. Treating CURRT
as an enforced constraint in the exact replay was an incorrect assumption, corrected before analysis.
Leonardo's separate January file has R0=6.0 m and F_edge=31.80 T m, versus 6.2 m and 32.86 for modx03.
The native bytes are unchanged and each variant retains its own normalization; no numerical solver
fix or speculative PR follows from either input distinction.

## EQ-TC24-5: Native contour checker loses exterior initial guesses

Class: defect; affected: the Python native Boozer comparison oracle. A first ray guess just outside
a curved finite-element mesh returned NaN, which propagated through Newton updates and rejected an
existing interior contour. A safeguarded bracket retains native field evaluation and both signed
flux branches. Two exact circular q/flux oracles fail before the fix and pass after it. KIN6D TC24
exports now complete; their remaining numerical errors are reported without qualification.

## EQ-TC24-6: GPEC comparison drops the toroidal flux sign

Class: defect; affected: the project's GPEC/DCON readback comparison, not GPEC's solver. Restoring
the declared physical signs to fields and q also requires restoring sign(F_edge) to the full toroidal
flux integral. Negative-F exact constant-q tests reported a false relative error of 2 before the fix;
all four poloidal/toroidal polarity cases now pass. Native reader bytes remain unchanged.

## EQ-TC24-7: GPEC field-line failure diagnostic

Class: defect; affected: GPEC direct_fl_int's error message. Its 65-character formatted output
overflowed a 64-character buffer, hiding the intended integration failure with End of record;
five-digit step counts also exceeded the I4 format. Fork [PR1](https://github.com/krystophny/GPEC/pull/1)
uses a sufficient buffer and unrestricted integer fields. A test executes the production formatter,
failing on both earlier versions and passing at `bb3f02a4`. This repairs diagnostics only.
The same KIN6D export completes with integration tolerance 1e-8 instead of
1e-10 and the unchanged step cap; its measured field/q errors remain above
target. The [consumer study](phase4/tc24/EXPORTS.md) owns this configuration
control. No underlying GPEC solver defect is established.

## EQ-TC24-8: libneo Python EQDSK four-digit dimensions

Class: defect; affected: libneo.eqdsk_base.read_eqdsk. Whitespace splitting cannot read adjacent
four-digit grid dimensions in a valid 3I4 header. Fixed-width parsing with the legacy separated-header
fallback is in fork [PR4](https://github.com/krystophny/libneo/pull/4), `f27ee06`. Generated 1025×9 and
9×1025 numerical round trips fail before and pass after; all 11 reader/writer tests pass. The fixed
reader enables the TC24 1025² export refinement; no source equilibrium or global installation changed.

## EQ-TC24-9: Finite stalled Newton preconditioner rejected

Class: defect; affected: KIN6D nonlinear GS response. Inner diagonal-CG can
reach a roundoff floor before its tolerance, making a usable preconditioner
reject the Newton solve. Fixed on main at
[af84393](https://github.com/itpplasma/kin6d/commit/af84393): retain finite
iteration-limited responses only in preconditioning, and accept stalled outer
GMRES only after an independent physical Jacobian residual check. Other
linear-response callers retain their strict failure behavior. The retained
95k-DOF TC24 reproducer converges; the integrated CPU and Debug presets each
pass all 96 tests. The configurable solve wall limit defaults to 300 s.

<a id="eq-d116"></a>

## EQ-D116: KIN6D reference-triangle guard

Class: defect; affected: KIN6D scalar-jet input validation. Rounded coordinate addition accepts a represented
point just outside the closed reference triangle. [KIN6D PR6](https://github.com/itpplasma/kin6d/pull/6),
`a262675`, compares against the remaining coordinate span after finite/domain checks. Outside-point rejection
and exact-edge acceptance regressions pass. Status: fixed on main through `2e4cd53` integration; the stacked
PR is closed. This validates the input domain and makes no new claim about mapped equilibrium accuracy.

## EQ-EXPORT-1: libneo EFIT Python wrapper kind map

Class: defect; affected: the CMake-built `_efit_to_boozer` Python interface to
`field_eq` and the EQDSK reader. Without an explicit f2py kind map, `real(dp)`
routine arguments become C `float` despite double-precision Fortran storage.
An exactly representable quadratic field returns wrong components. The fork
fix passes the existing `.f2py_f2cmap` explicitly and makes it a generation
dependency. Its field round-trip test fails before and passes after at 2e-13 T.
Status: [upstream PR422](https://github.com/itpplasma/libneo/pull/422) open, commit
`1b867ec`; the Phase 1 export study uses that fixed local build. Native Fortran
executables do not cross this Python ABI. Fork PR1 was closed in favor of PR422.

## EQ-EXPORT-2: Boozer flux boundary and header precision

Class: numerical export limits, improved in [libneo #423](https://github.com/itpplasma/libneo/pull/423)
(`075dd48`, `d5bbe6c`; PR open). The finite-`psimax` boundary was
one or two scan cells inside the requested regular surface, giving first-order
flux/label error; the six-digit header then limited flux serialization. Bisection
of the prescribed flux bracket and a double-precision header remove those limits
while retaining the safety margin for box/separatrix exits. Independent circular
tests fail before and pass after each change. Both exact cases now meet the Boozer
flux/q targets through the actual NEO-RT and NEO-2 readers. Measurement, remaining
norm/consumer limitations and reproducible inputs belong to the
[export results](phase1/results_export/README.md); no new unresolved solver defect
is inferred from the remaining below-target or converging export errors.

## EQ-EXPORT-3: NEO-2 multiple-surface initialization

Class: defect. `neo_magfie_a` allocates `bmod_a` inside its surface loop but
deallocates it after that loop, so a second requested surface aborts. Move the
allocation before the loop; the existing single-surface extrema calculation
and cleanup stay intact. The native two-surface analytic Fourier test fails
before and passes after, checking the sine sign, field pitch and finite vector
and metric outputs. [NEO-2 PR193](https://github.com/itpplasma/NEO-2/pull/193),
`a0b7039`, targets `itpplasma/NEO-2:main`. The full-consumer measurements use
the fix; numerical evidence belongs to [the export table](phase1/results_export/README.md).

<a id="eq-p2-1"></a>

## EQ-EXPORT-4: Boozer geometry serialization

Class: export defect; affected: libneo `efit_to_boozer` surface records and
Fourier geometry coefficients. Eight-digit output loses precision needed by
the consumer's radial derivatives. Six wider formats retain double precision;
an independent analytic-circle Jacobian regression fails before and passes after
for all four boundary/polarity cases. Native file readback and actual NEO-2
accept the format. Status: [fork PR5](https://github.com/krystophny/libneo/pull/5)
open, `08ace36`, with PR3 prerequisites stated. The
[inverse consumer controls](phase3/results/kin6d.md) own measured improvement
and the remaining unexplained geometric determinant residual. This fix does
not close that residual or establish its proposed tracing-tolerance cause.

## EQ-P2-1: circular-ladder radial and stopping limits

Class: discretization and iteration tolerance. The [Phase 2 ladders](phase2/results/README.md)
show VMEC++ field self-convergence consistent with at least first order in radial
resolution. At NS=513 the axis errors remain 6.26e-6 (E1/A3.1), 2.65e-5
(E2/A3.1), and 1.60e-6 (E2/A10), above the 1e-6 target; E2/A3.1 also has
psi/Bpol L2 differences 2.18e-6/1.01e-5. NS=1025 at the declared ftol=1e-18
times out at 300 s for both A3.1 laws. These states are not qualified. High-A
iteration-error plateaus at ftol=1e-16 disappear under tighter tolerance;
overly strict 1e-20 requests can hit the iteration cap. Raw repeats, native
stopping flags and input tolerances remain in the registry. No non-converging
wrong limit is established, and no speculative solver fix is proposed.

<a id="eq-p4a-1"></a>

## EQ-P4A-1: P3 majorant recovery cap

Class: estimator failure/status defect. At E4 boundary_nodes=192, KIN6D's
recovered-flux minimization reaches its 6000-iteration cap and previously
aborted the entire producer although the GS solution was converged. A finite
continuous recovered vector remains admissible in the functional majorant;
the minimum is required for sharpness, not validity. KIN6D lane commit
`1ada383` evaluates the estimate after an iteration cap, exposes recovery
convergence/iteration count, and still rejects breakdown or nonfinite vectors.
The expanded exact Solovev P3 test fails before the fix at n=192 and passes
after, with majorant/exact-energy-error=1.135; the P2 gate also passes.
[The E4 study](phase4/results/README.md) retains the failed attempts and
numerical reference estimates. Status: fixed on main `99fa2c8` (rebased from `1ada383`);
no third-party PR is needed.

## Archive navigation

<a id="eq-d44-public-chease-residual-rise-between-n32-and-n64-is-export-grid-dependence"></a>

[EQ-D44: export-grid and boundary-spline residual controls](ERRATA_ARCHIVE.md#eq-d44-public-chease-residual-rise-between-n32-and-n64-is-export-grid-dependence)
remain archived; force residual has no PLAN accuracy gate.

## EQ-CYL-1: DESC continuation and omitted zero modes

Confirmed input-handling defect in our producer, fixed on main `25d20db2d`:
continuation indexed `rbs`/`zbc` directly although valid symmetric decks omit
these zero Fourier families. The registered Phase 5 native request fails with
`KeyError: rbs`; the extracted stage-input regression fails before and passes
after treating omitted families as empty. Profiles, flux and nonzero boundary
coefficients are preserved. No DESC solver source change or upstream PR.

## EQ-CYL-2: KIN6D coarse P3 readback failures

Class: confirmed axis-search defect, fixed on KIN6D main `bb2ec06` (P3 damped
Newton) and `0e56e29` (shared-entity axes). The coarse Lundquist minimum lies
near a cell corner; the undamped first Newton step left that cell, losing its
valid minimum. The native regression compares the recovered minimum against
an independent P3 polynomial fit and checks refinement. Shared-node/edge
minimum handling has separate behavioral coverage.

Both retained A=100/300, n=16 input/profile requests replay successfully on
main `af84393`, with finite native contour readback and unchanged physical
inputs. [Replay metrics](phase5/results/kin6d_coarse_readback.csv) record source,
binary, wall time and field/q errors. These coarse meshes remain below the
accuracy of the already-delivered fine ladder; solving them closes the reader
failure, not a coarse accuracy claim. Original aborted outputs remain retained.

<a id="eq-oh-1"></a>

## EQ-OH-1: FortNum Brent interpolation fell back to bisection

Class: defect; affected: FortNum `fortnum_roots` (Brent), used by KIN6D contour readback. Wrong secant sign
normalization and inverse-quadratic residual ratios rejected useful interpolation steps, so roots were found
by bisection. A linear root fails a two-iteration budget before the repair; linear and smooth nonlinear
operation-budget tests pass after it (FortNum 149/149; KIN6D CPU/debug 78/78). The GS solution and majorant are
unchanged; KIN6D P3 producer time at n=48 drops from about 0.81 s to 0.42 s, in that control. The Phase 2 committed cost table predates the repair;
a refreshed common table is required for an all-case speed claim. Fixed on FortNum main `5f166bc`, pinned by KIN6D `82d4d1f`.

## EQ-P3X-1: Prescribed-q NOUT record layout

Confirmed reader defect: public CHEASE `NSTTP=5` writes two additional profile
records (`CID3`, `ISTAR_TARGET`) before the boundary. `CheaseNative` used the
forward offsets and failed on every otherwise valid inverse output. Select
the offset from the stored native selector. A generated exact Hermite
quadratic field passes for the forward layout, fails for the inverse layout
before the fix, and recovers the same signed fields from both after it.
`tests/test_phase1_export_check.py` owns the regression; no solver change.

## EQ-P3X-2: Provenance metadata in result collection

Confirmed analysis defect: the broad result JSON glob also selected the list-valued
source provenance index and aborted before writing comparison tables. Restrict
run selection to sampled result objects. The regression supplies analytical
Solovev fields alongside a provenance list: it fails before this check and
recovers zero field/current/geometry error after it. Existing numerical outputs
are unaffected; `tests/test_phase3.py` owns the behavioral test.

## EQ-KINV-1: Exported central field used the nominal input F

Confirmed producer defect, fixed in the KIN6D inverse integration patch:
the EQDSK header used case F_edge although cubic/inverse profiles export the
executed F law. The header now uses the exported edge F divided by R0. An
independent manufactured profile with a deliberately different nominal F
fails before and passes after the change in `tests/test_phase1_kin6d_export.py`.
The prescribed-q producer tests also recover F independently of the nominal
input and preserve both q signs through native and EQDSK round trips.

## EQ-KINV-2: Brent rejected convergence on its last permitted update

Confirmed FortNum status defect: the iteration limit counted the next
convergence check, so a root reached on the last allowed update was returned
with failure. KIN6D's retained inverse Jacobian check encountered this at the
80th root update in a cell quadrature. FortNum `bfea03a` checks the final result
without taking another update or increasing any tolerance. Exact linear-root
tests fail before and pass after; the formerly failing KIN6D Debug inverse
test passes. FortNum Release CTest passes 149/149. The repair is on FortNum main `901aae0` (rebased from `bfea03a`),
pinned by KIN6D main `fde93a9`; current KIN6D main is `f1d1791`.
