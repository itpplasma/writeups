# TC24 fixes and PRs

- **KIN6D current main:** [`f1d1791`](https://github.com/itpplasma/kin6d/commit/f1d1791) includes cubic profiles `2d8142a`, TC24 performance `313cde5`, inverse `60bef4c` and FortNum main [`901aae0`](https://github.com/lazy-fortran/fortnum/commit/901aae0) via `fde93a9`. The inverse export-header repair is in iter_tc24 [MR !20](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/merge_requests/20), with a manufactured-profile regression.
- **TC24 normalized-current capability:** KIN6D own main [`5dfb9df`](https://github.com/itpplasma/kin6d/commit/5dfb9df), on curved cubic profiles `2d8142a`; exact current/field scaling oracles and full CPU/Debug 81/81 each. The [reference study](../equilibrium/phase4/tc24/README.md) owns numerical qualification.
- **GPEC failure diagnostic:** draft personal-fork [PR1](https://github.com/krystophny/GPEC/pull/1), `bb3f02a4`, branch `equilibrium/fieldline-error-message` against fork main (baseline `e68d7ac2`). Executes the actual Fortran formatter; fixes its buffer overflow and five-digit step counts. The underlying TC24 field-line failure remains unresolved; this change affects diagnostics only.
- **libneo four-digit EQDSK reader:** draft personal-fork [PR4](https://github.com/krystophny/libneo/pull/4), `f27ee06`, branch `equilibrium/eqdsk-four-digit-grid` against fork main. Both 1025-point dimension round trips fail before; 11 reader/writer tests pass after, including legacy whitespace headers. The copied fixed reader is used for the 1025² TC24 preparation; no global installation changed.
- **iter_tc24 completion branch, [MR !20](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/merge_requests/20):** safeguarded native contour roots, signed GPEC toroidal flux and explicit CHEASE final-stage readback. Seven behavioral cases pass; ERRATA EQ-TC24-5/6 and EQ-D103 own the causes. No numerical alignment or sign was fitted.

- **libneo signed TC24 boundary, draft [personal-fork PR3](https://github.com/krystophny/libneo/pull/3), `a9b6d96`:** orient the prescribed-flux bracket and bisection for either poloidal polarity. Two negative-polarity circular oracles fail before; all four polarity/scan cases pass after. Branch `equilibrium/tc24-signed-boozer-boundary` targets `krystophny/libneo:main`, with `075dd48` / `d5bbe6c` prerequisites stated in the PR. No new upstream submission. [EQ-TC24-2](../equilibrium/ERRATA.md#eq-tc24-2-boozer-converter-signed-prescribed-boundary).
- **iter_tc24 own code, `lane/cylinder`:** [EQ-CYL-1](../equilibrium/ERRATA.md#eq-cyl-1-desc-continuation-and-omitted-zero-modes) fixed with a failing-before/passing-after continuation input test. Integrated on main; no third-party PR.
- **KIN6D lane `phase4a`, `1ada383`:** retain the functional majorant when finite flux recovery reaches its iteration cap; expose recovery convergence and iterations. The exact Solovev P3 n=192 effectivity test fails before and passes after (effectivity 1.135); P2/P3 convergence gates pass 2/2. Integrated on own main as [`99fa2c8`](https://github.com/itpplasma/kin6d/commit/99fa2c8). [EQ-P4A-1](../equilibrium/ERRATA.md#eq-p4a-1).

- **libneo Boozer flux accuracy, [personal-fork PR2](https://github.com/krystophny/libneo/pull/2), `075dd48` / `d5bbe6c`:** refine the prescribed regular flux boundary inside the scan bracket and retain double precision in the flux header. Independent circular flux/q and native-to-file flux tests fail on the original/intermediate versions and pass after the changes. These remove numerical export limits; box/separatrix exits retain their margin. Personal-fork PR2 closed in favor of open [libneo PR423](https://github.com/itpplasma/libneo/pull/423). [Results](../equilibrium/phase1/results_export/README.md), [EQ-EXPORT-2](../equilibrium/ERRATA.md#eq-export-2-boozer-flux-boundary-and-header-precision).
- **libneo export reader, [personal-fork PR1](https://github.com/krystophny/libneo/pull/1), `1b867ec`:** pass the double-precision kind map to f2py when generating the EFIT wrapper. The exact quadratic EQDSK→field test fails on the unmodified build and passes after the fix. Personal-fork PR1 closed in favor of open [libneo PR422](https://github.com/itpplasma/libneo/pull/422). [ERRATA EQ-EXPORT-1](../equilibrium/ERRATA.md#eq-export-1-libneo-efit-python-wrapper-kind-map).
- **Dropped-handoff formulation recheck:** [FreeGS audit](../research_notes/Equilibrium%20weak%20formulation%20error%20analysis/freegs_upstream_audit.md) confirms the analytical diagnostic/parser controls; signed winding remains a legacy API decision. [Original VMEC/GVEC audit](../research_notes/Equilibrium%20weak%20formulation%20error%20analysis/dropped_vmec_gvec_upstream_audit.md) confirms the component and mathematical-documentation controls. Live [FreeGS155](https://github.com/freegs-plasma/freegs/issues/155) and [VMEC512](https://github.com/PrincetonUniversity/STELLOPT/issues/512) wording is corrected; full reproducer code is preserved. Unexplained numerical accuracy stays open without a solver patch.

- **FreeGS upstream transfer authorized by Chris on2026-10-08:** [PR152](https://github.com/freegs-plasma/freegs/pull/152) fixes known-edge/no-X q, [PR153](https://github.com/freegs-plasma/freegs/pull/153) fixes contour-root/tangent integration, [PR154](https://github.com/freegs-plasma/freegs/pull/154) proposes signed poloidal circulation. Independent heads/base, portable scripts and issues149/150/151/155 are in the [handoff receipt](../archive/equilibrium/dechurn/INDEX.md#entry-216). Earlier fork PRs1/2/3 closed as superseded. No further local FreeGS follow-up; upstream convention/accuracy discussion remains open.


- Current equilibrium PR states reconciled: 2026-10-09; older sections retain historical scope. [Results/questions](MERGE_REVIEW.md); [next experiments](../PLAN.md).
- Fix, diagnostic and proposal remain distinct; curve agreement alone does not admit a physical change.

## Upstream submissions (2026-10-09)

- iter_tc24 lane/phase4bx: own-code signed Boozer comparison fix
  [EQ-TC24-1](../equilibrium/ERRATA.md#eq-tc24-1-signed-boozer-comparison-readback).
  Three analytic polarity cases fail before and pass after; no third-party PR.

Tier 1 defects only; tier 2 (robustness, performance) awaits review.

- DESC metadata: [PlasmaControl/DESC#2348](https://github.com/PlasmaControl/DESC/pull/2348), combined signed labels and units (fork #4/#5 closed).
- DESC: [PlasmaControl/DESC#2347](https://github.com/PlasmaControl/DESC/pull/2347), failed `map_coordinates` inversions return NaN (fork #3 closed).
- MARS-Q: [gafusion/MARS-Q#6](https://github.com/gafusion/MARS-Q/pull/6), ISOFUN cubic FF' integral (fork #30 closed); [gafusion/MARS-Q#7](https://github.com/gafusion/MARS-Q/pull/7), SMOOTH fourth Hermite slot (fork #31 closed). MARS-only `tests/` target.
- CHEASE: upstream requires a signed CLA and EPFL GitLab access, and asks for no public forks; `itpplasma/chease` is private since 2026-10-09. Signed CLA and four patches (box units, smoothing slot, current cutoff, interpolation status; fork #1, #4, #16, #17) drafted by e-mail to O. Sauter; `make test_chease_ci_short` passes with all four applied.

The 2026-10-09 block below supersedes the older CHEASE, DESC and MARS CHEASE equilibrium entries further down; the dechurn pass removes those.

## Equilibrium fork PRs — DC-8 checked 2026-10-09

The scoped cleanup targeted our fork main; later upstream handoffs above
supersede closed fork PRs. No fork main was merged by that cleanup. CHEASE main remains `fb463663`, DESC `6296faa6`, and MARS-Q `8824bb18`.
Readiness below records the scoped tests; live supersessions are marked in place. Shared test bases are
[CHEASE #19](https://github.com/itpplasma/chease/pull/19) and
[MARS-Q #46](https://github.com/krystophny/MARS-Q/pull/46), one flat test directory/CTest
regression target per repo. DESC tests now live in the existing equilibrium/compute modules.

Every ready defect test fails on its source parent and passes after; every ready performance
PR passes exact native output equality. Native Make plus an existing deck smoke pass for
CHEASE/MARS; DESC's focused pytest cases pass. All executions were capped at 300 seconds,
one thread. Ready diffs contain no per-test READMEs, copied baseline routines, timing programs
or detached diagnostic/input-generator scripts. Ready descriptions contain commands/results,
performance timings, result-change scope and `Chris&AI` signatures. Hold heads are unchanged;
their descriptions now state the unresolved qualification. Readiness here is for the scoped
fork review, not Phase 3 equilibrium or downstream MARS Pair A/B acceptance.

| Review | State / scope | Head | Verification | Prerequisite |
|---|---|---|---|---|
| [CHEASE #1](https://github.com/itpplasma/chease/pull/1) | ready — Fix the SI units of the default vertical export box | `b7dfde60` | fail → pass: 4 translated/explicit box controls | #19 |
| [CHEASE #2](https://github.com/itpplasma/chease/pull/2) | closed — superseded by #16 + #17 — Fix current smoothing for equilibria with a small flux span | `b5fc1c8d` | retired; not rerun | none |
| [CHEASE #3](https://github.com/itpplasma/chease/pull/3) | ready — Use 64-bit band storage counts and addresses | `f4d8b775` | fail → pass: count, zeroing, dense solves | #19 |
| [CHEASE #4](https://github.com/itpplasma/chease/pull/4) | ready — Preserve the fourth smoothed Hermite component | `8ebe4bb1` | fail → pass: four Hermite components | #19 |
| [CHEASE #5](https://github.com/itpplasma/chease/pull/5) | ready — Use contiguous tiles for native band factorization | `600b6b36` | parent + PR pass: exact native byte equality; dense factors too | #18 → #5 |
| [CHEASE #6](https://github.com/itpplasma/chease/pull/6) | hold — opt-in ordering — Reduce anisotropic solve bandwidth with opt-in folded angle ordering | `b244c04e` | not rerun; hold unchanged | none |
| [CHEASE #7](https://github.com/itpplasma/chease/pull/7) | hold — optional BLAS backend — Allow optional installed LP64 BLAS in the existing Make build | `9a128ae0` | not rerun; hold unchanged | none |
| [CHEASE #8](https://github.com/itpplasma/chease/pull/8) | ready — Clear only active band-matrix columns | `88e04655` | parent + PR pass: exact native byte equality | #19 |
| [CHEASE #9](https://github.com/itpplasma/chease/pull/9) | ready — Compute each spline-query radius once | `098ef94c` | parent + PR pass: exact native byte equality | #19 |
| [CHEASE #10](https://github.com/itpplasma/chease/pull/10) | ready — Validate quadrature and boundary inputs | `97eb0f74` | 9 failing subcases → all pass | #19 |
| [CHEASE #11](https://github.com/itpplasma/chease/pull/11) | closed — consolidated into #10 — Reject the singular radial endpoint quadrature rule | `231a4259` | retired; not rerun | none |
| [CHEASE #12](https://github.com/itpplasma/chease/pull/12) | closed — consolidated into #10 — Reject unmatched boundary angles before spline indexing | `dc2cd39d` | retired; not rerun | none |
| [CHEASE #13](https://github.com/itpplasma/chease/pull/13) | hold — scoped PR cleanup pending — Use native interpolation for zero-tension prescribed q | `72046b42` | combined Phase 3 exact/native/consumer convergence passes; flat-PR parent retest pending | none |
| [CHEASE #14](https://github.com/itpplasma/chease/pull/14) | closed — consolidated into #10 — Reject unsupported Gaussian quadrature orders before writes | `4f908476` | retired; not rerun | none |
| [CHEASE #15](https://github.com/itpplasma/chease/pull/15) | hold — scoped PR cleanup pending — Keep the magnetic axis consistent with the smoothed flux field | `2f83bc08` | combined Phase 3 exact/native/consumer convergence passes; flat-PR parent retest pending | none |
| [CHEASE #16](https://github.com/itpplasma/chease/pull/16) | ready — Use a relative flux cutoff for current smoothing | `297d28bd` | fail → pass: 3 flux spans | #19 |
| [CHEASE #17](https://github.com/itpplasma/chease/pull/17) | ready — Propagate failed current interpolation status | `fde5a12f` | fail → pass: failed status + affine control | #19 |
| [CHEASE #18](https://github.com/itpplasma/chease/pull/18) | ready — Define band factorization edge cases | `0c053683` | fail → pass: edge/status + dense controls | #19 |
| [CHEASE #19](https://github.com/itpplasma/chease/pull/19) | ready — Add one shared native CHEASE regression target | `bb29c950` | shared base: native smoke passes (no defect) | none |
| [DESC #1](https://github.com/itpplasma/DESC/pull/1) | closed — callback feature; no scoped dependency (defects retained in #3/#4/#5) — Expose accepted-step callbacks in least-squares wrapper | `22aff5f1` | retired; not rerun | none |
| [DESC #2](https://github.com/itpplasma/DESC/pull/2) | closed — superseded by #4 + #5 — Correct helical basis component labels and norm units | `c3fe2957` | retired; not rerun | none |
| [DESC #3](https://github.com/itpplasma/DESC/pull/3) | closed — superseded by upstream #2347; tested scope: Return NaN for failed physical coordinate inversions | `ea635b48` | 2 fail → 2 pass | none |
| [DESC #4](https://github.com/itpplasma/DESC/pull/4) | closed — superseded by upstream #2348; tested scope: Correct the sign of helical basis labels | `822605d9` | 3 fail → 3 pass | none |
| [DESC #5](https://github.com/itpplasma/DESC/pull/5) | closed — superseded by upstream #2348; tested scope: Correct Jacobian-weighted helical basis units | `acb6daf1` | 1 fail → 1 pass | none |
| [MARS-Q #30](https://github.com/krystophny/MARS-Q/pull/30) | closed — superseded by upstream #6; tested scope: Correct CHEASE cubic profile integration in both directions | `0a423887` | 4 fail → all 8 polynomial/direction controls pass | #46 |
| [MARS-Q #31](https://github.com/krystophny/MARS-Q/pull/31) | closed — superseded by upstream #7; tested scope: Preserve the fourth CHEASE smoothing component | `84167df9` | fail → pass: four Hermite components | #46 |
| [MARS-Q #32](https://github.com/krystophny/MARS-Q/pull/32) | ready — Use contiguous tiles for CHEASE band factorization | `fa8fd09a` | parent + PR pass: exact native byte equality; dense factors too | #45 → #32 |
| [MARS-Q #33](https://github.com/krystophny/MARS-Q/pull/33) | hold — folded ordering/axis-q qualification — CHEASE: opt-in folded band ordering with a center Schur border | `154292d7` | not rerun; hold unchanged | none |
| [MARS-Q #34](https://github.com/krystophny/MARS-Q/pull/34) | ready — Clear only active CHEASE band-matrix columns | `2ae67699` | parent + PR pass: exact native byte equality | #46 |
| [MARS-Q #35](https://github.com/krystophny/MARS-Q/pull/35) | hold — axis-F result change — CHEASE: use radial coordinate in axis-field interpolation | `0e129cf9` | not rerun; hold unchanged | none |
| [MARS-Q #36](https://github.com/krystophny/MARS-Q/pull/36) | ready — Compute each CHEASE spline-query radius once | `81a69b56` | parent + PR pass: exact native byte equality | #46 |
| [MARS-Q #37](https://github.com/krystophny/MARS-Q/pull/37) | ready — Validate CHEASE quadrature inputs | `fc47045c` | 6 failing subcases → all pass | #46 |
| [MARS-Q #38](https://github.com/krystophny/MARS-Q/pull/38) | closed — consolidated into #37 — Reject CHEASE radial endpoint quadrature at the polar axis | `94f789f0` | retired; not rerun | none |
| [MARS-Q #39](https://github.com/krystophny/MARS-Q/pull/39) | ready — prescribed-q current sign | `6d954d9` | 24 signed/pressure kernel controls fail → pass; Make + native smoke pass | #46 |
| [MARS-Q #40](https://github.com/krystophny/MARS-Q/pull/40) | closed — superseded by #42 — Initialize missing inner coarea in CHEASE prescribed-q profiles | `5ecc6ae0` | retired; not rerun | none |
| [MARS-Q #41](https://github.com/krystophny/MARS-Q/pull/41) | ready — axis normalization follows the smoothed field | `67c9e34` | whole NONLIN polynomial controls fail → pass; Make + native smoke pass | #46 |
| [MARS-Q #42](https://github.com/krystophny/MARS-Q/pull/42) | ready — trace missing inner coareas about the axis | `a288ebe` | independent circle/ellipse integrals, 3 angular grids, invalid controls fail → pass; Make + smoke pass | #46 |
| [MARS-Q #43](https://github.com/krystophny/MARS-Q/pull/43) | recommend close — source interpolant and continuous field remain inconsistent; retain defect in #44 | `ff639e23` | 48 source + 32 PROFILE + 4 legacy controls pass; combined inverse solves still fail | none |
| [MARS-Q #45](https://github.com/krystophny/MARS-Q/pull/45) | ready — Define CHEASE factorization status and edge cases | `459a4c0a` | fail → pass: edge/status + dense controls | #46 |
| [MARS-Q #46](https://github.com/krystophny/MARS-Q/pull/46) | ready — Add one shared native CHEASE regression target | `dc20a4bc` | shared base: native smoke passes (no defect) | none |

CHEASE #10 consolidates #10/#11/#12/#14 with one validation test module; MARS #37
consolidates #37/#38. Each rejected input was demonstrated to cause an overrun, undefined
arithmetic or silently wrong state. CHEASE #2 and DESC #2 retain signed redirects to their
atomic replacements. DESC #1 is a feature with no dependency from #3–5. MARS #40 redirects
to ready #42. MARS #44 remains an untouched issue for the unresolved inverse iteration.

CHEASE #9 and MARS #36 now satisfy the small, result-preserving exception to hold: native
bytes match their parents, and only query-local spline bracket work is hoisted. CHEASE
#5 / MARS #32 have performance-only deltas over the separate #18 / #45 edge-contract fixes.
CHEASE #3's arithmetic oracle crosses 2^31 entries; no full high-address solve was run.

Recommended upstream review order after human review:

- CHEASE #19 → #1, #3, #4, #10, #16, #17, #18 → #5; then #8, #9.
- MARS-Q #46 → #30, #31, #37, #45 → #32; then #34, #36.
- DESC #3, #4, #5, independent on fork main.

VMEC++ still has no open PRs. The DESC `equilibrium/phase1-v0173-backports` branch remains
an existing environment pin, not a PR; it was not changed. The callback feature's closure
does not remove that historical pin. The [Phase 3 study](../equilibrium/phase3/results/README.md)
qualifies the combined public prescribed-q path in its sampled domains; held public #13/#15
still need scoped PR cleanup. MARS inverse qualification remains open. MARS-K #5–29 is outside this cleanup.

Commands, exact final file inventories, parent/after logs and measured timings:
`/home/ert/code/worktrees/_lanes/pr-tidy/REPORT.md` and its adjacent evidence files.

## Dropped solver upstream handoff

Chris explicitly authorized transfer to actual upstreams on2026-10-08, for dropped codes only. No merges were performed; retained solver PRs remain on their forks. Original VMEC/GVEC/FreeGS local development and comparison are withdrawn until upstream questions are resolved and Chris explicitly readmits them. KIN6D is the future main code; accuracy/speed parity remains a requirement to demonstrate.

- Original VMEC/STELLOPT: [PR510 geometry storage](https://github.com/PrincetonUniversity/STELLOPT/pull/510), [PR511 lambda restart](https://github.com/PrincetonUniversity/STELLOPT/pull/511), [PR515 build failure status](https://github.com/PrincetonUniversity/STELLOPT/pull/515), [PR516 non-MPI compile](https://github.com/PrincetonUniversity/STELLOPT/pull/516). All independently target actual upstream develop. Fork PR2/3 closed with redirects.
- Original VMEC unresolved/math reports: [issue512 stopping/physical force](https://github.com/PrincetonUniversity/STELLOPT/issues/512), [issue513 reset truncation](https://github.com/PrincetonUniversity/STELLOPT/issues/513), [issue514 B-squared theory equation](https://github.com/PrincetonUniversity/STELLOPT/issues/514). Complete generic scripts; no speculative solver patch.
- GVEC: [MPCDF upstream MR183](https://gitlab.mpcdf.mpg.de/gvec-group/gvec/-/merge_requests/183), mathematical lambda/component correction with exact independent oracle, numerical code unchanged. [MPCDF issue94](https://gitlab.mpcdf.mpg.de/gvec-group/gvec/-/work_items/94), revised after independent mathematical/reproducer review, reports two circular/shaped runs capped before convergence. It defines the absolute constrained/preconditioned coefficient norm and reports the demonstrated iteration-cap/success-footer ambiguity and inaccurate relative-tolerance wording. All four answerable questions have been removed and answered locally; unfinished minimization versus representation/quadrature remains unmeasured, without a speculative solver fix. Complete generated scripts and signed analytic controls are retained; finite force in these unconverged states is not a demonstrated numerical bug or paper error. [Question-free publication receipt](../research_notes/Equilibrium%20weak%20formulation%20error%20analysis/gvec94_question_closure/publication_receipt.json). Target develop, source calbert/gvec; GitHub fork PR1 closed.
- FreeGS: upstream PR152/153/154 and issues149/150/151/155 remain the original completed q handoff. Added [issue156](https://github.com/freegs-plasma/freegs/issues/156) for actual native-reader flux/derivative inconsistency inherited from [FreeQDSK issue28](https://github.com/freegs-plasma/FreeQDSK/issues/28); owner issue updated with complete generated input bytes.
- [Coverage, exclusions and verification](../archive/equilibrium/dechurn/INDEX.md#entry-212); [18-item receipt](../archive/equilibrium/dechurn/INDEX.md#entry-212). Circular/Miller controls and exact component oracles are embedded in public bodies; no received equilibrium or private project paths. Paper/code questions are distinguished from demonstrated mathematical-documentation errors; no verified paper error is asserted.

## Verified retained-code repairs on 2026-10-08

- [KIN6D PR1](https://github.com/itpplasma/kin6d/pull/1): quadratic GS elements, physical derivative/current/axis diagnostics, explicit six-node export and flux-gauge-stable derivatives. Twenty-four native GS tests pass in Release and checked Debug, plus the affected I/O contract in each. Independent frozen-patch review passes. Whole-cell P2 certification and prescribed-q inverse qualification remain separate.
- [FortFEM generated reference repair25975b3](https://github.com/lazy-fortran/fortfem/commit/25975b30d7740f27b1b918cfd3ce16e6d9980469): independent quadratic reconstruction fails15/18 on old handwritten Hessians and passes after generation. [Typed dependency pin91a7](https://github.com/lazy-fortran/fortfem/commit/91a7eb72563e67141411421b6c38820967fb9ed5) remains the equilibrium consumer pin.
- Subsequent owning FortFEM migrations cover arbitrary scalar jets1fc790f, tetrahedral Whitney kernels8ed540e and triangle Piola products6cb3d4c. They remain background library work; consumer pin unchanged. Independent native polynomial/conservation gates and canonical generation pass.
- [Fo2b97566](https://github.com/lazy-fortran/fo/commit/2b97566526198b67e4efffe7bcb7beb6dde7cd20): propagate invalid/missing selected-test verdicts to public failure status. [Fo2974209](https://github.com/lazy-fortran/fo/commit/2974209): eliminate silent64-dependency truncation from scanner, serialized scan cache and source/test build keys. Native128-module cold/warm/edit/restore oracle, scan110/DAG18 and original pinned FortFEM eight-job consumer pass. Exact private driver used; global installation provenance remains separate.

Independent correctness reviews against the review repositories' unchanged main bases:

| Review | Defect and independent reproducer |
|---|---|
| [CHEASE10](https://github.com/itpplasma/chease/pull/10) | Selector1 expands to2; reserve effective capacity and recompute tensor count |
| [MARS-Q37](https://github.com/krystophny/MARS-Q/pull/37), draft | Reject unsupported/over-capacity quadrature before writes, recompute effective count; capacity4 retained |
| [CHEASE11](https://github.com/itpplasma/chease/pull/11) / [MARS-Q38](https://github.com/krystophny/MARS-Q/pull/38), draft | Radial endpoint rule evaluates the singular polar-axis operator; fail early |
| [MARS-Q39](https://github.com/krystophny/MARS-Q/pull/39), draft | Prescribed-q toroidal-current term has the opposite sign to native F/FFprime and GS chain rule |
| [CHEASE12](https://github.com/itpplasma/chease/pull/12) | Unmatched/NaN boundary angle dereferences an unset interval index; whole native circular/elongated boundary controls |
| [CHEASE13](https://github.com/itpplasma/chease/pull/13) | Zero-tension prescribed-q call asks INTERPOS for an unsupported boundary combination and ignores NaNs; native interpolation branch |
| [CHEASE14](https://github.com/itpplasma/chease/pull/14) | Unsupported Gaussian order halves uninitialized weights; reject before writes |

- [MARS-Q40](https://github.com/krystophny/MARS-Q/pull/40), draft, superseded by [42](https://github.com/krystophny/MARS-Q/pull/42): independently repair undefined prescribed-q inner coarea in whole native PROFILE. Twelve circular/elongated/legacy controls pass, including the ordinary-clone relative-path command; current-sign39 and primitive30 remain separate full-validation prerequisites. The full rerun still fails at a later NaN axis; no complete nonlinear repair is claimed.
- [Fo8292321](https://github.com/lazy-fortran/fo/commit/8292321): preserve registered CTest failures with missing/forbidden regex reasons and passes with WILL_FAIL. Actual native CTest process/verdict controls fail the parent and pass the repair; exact private driver used.
- [FortNum471c288](https://github.com/lazy-fortran/fortnum/commit/471c2888d1d4e24a5491fe8156b84d7cd9c758f2): remove an unused tracked absolute source alias; standalone native quadrature passes. KIN6D cbb5101 pins the portable source with fifteen native GS gates passing; FortFEM remains91a7.

All eight standalone native parent/fixed oracles pass under the controller. Prescribed-q reviews include complete generated circular and elongated native inputs, without external equilibrium data. MARS downstream Pair A/B gates remain pending. The current-sign fix alone does not repair full inverse convergence: its bounded circular pilot stops during remapping and retains empty final outputs. These retained-code reviews await human review before actual upstream transfer. [Frozen reviews/publication receipt](../research_notes/Retained%20equilibrium%20discrepancy%20closure/chease_correctness_publication.json).

## Active equilibrium fixes

- VMEC++: the existing [itpplasma fork](https://github.com/itpplasma/vmecpp)
  has no open PRs (live check 2026-10-09). PR2 is merged; the other historical
  PRs are closed feature/autodiff work. No defect PR needs splitting or
  superseding. Phase 1 uses release 0.8.1 / `a4150a4`; no native defect fix is
  established. The canonical-flux reader correction is own-code commit
  `35583217c` (EQ-D57), with a failing-before chart-reversal regression.

- [CHEASE #1](https://github.com/itpplasma/chease/pull/1): default vertical export box mixes normalized/SI units; shifted exact-case regression. PR open against unchanged fork main.
- [CHEASE #2](https://github.com/itpplasma/chease/pull/2): superseded for correctness review by [#16](https://github.com/itpplasma/chease/pull/16) (flux-relative current cutoff, `018afb4`) and [#17](https://github.com/itpplasma/chease/pull/17) (interpolation failure propagation, `23d03a0`). Each isolated native test fails on the parent and passes after its fix; both Make builds pass. Leave #2 open for controller action.
- [CHEASE #3](https://github.com/itpplasma/chease/pull/3): 64-bit band counts/addresses prevent NT1024 overflow. Three native gates and exact E0 interior preservation pass; high-address execution open. Reworked independently against fork mainfb46366, excluding export PR1; head2650e04.
- [DESC #1](https://github.com/itpplasma/DESC/pull/1) **open**: expose accepted-step callbacks. Rechecked: three tests fail before and pass on the PR head; trajectories, projected snapshots and graceful stopping are covered. One defect, based on fork main.
- [DESC #2](https://github.com/itpplasma/DESC/pull/2) **superseded; left open**: split its two independently failing metadata defects into [#4](https://github.com/itpplasma/DESC/pull/4) (signed labels; three vector tests) and [#5](https://github.com/itpplasma/DESC/pull/5) (T*m units; one length-scaling test). Each replacement is based directly on fork main and fails before/passes after. The controller closes #2 after review.
- [DESC #3](https://github.com/itpplasma/DESC/pull/3) **open**: return NaNs for failed physical-coordinate inversions instead of finite boundary coordinates. Both default/full-output regression cases fail before and pass after.
- DESC 0.17.3 qualification environment: branch `equilibrium/phase1-v0173-backports`, commit `2888389`, based on `fcc29be`; includes #1/#3/#4/#5. All nine owning regression cases pass. Pushed as a [fork branch](https://github.com/itpplasma/DESC/tree/equilibrium/phase1-v0173-backports); it is an environment pin, not a PR against fork main.

- [INTERPOS !1](https://gitlab.tugraz.at/plasma/libs/interpos/-/merge_requests/1): stop after failed spline factorization so later interpolation cannot clear INFO. Independent singular/affine oracles. Private research fork main, official base b7380de; EPFL transfer after human review.
- [INTERPOS !2](https://gitlab.tugraz.at/plasma/libs/interpos/-/merge_requests/2): locate fixtures in the source tree during out-of-tree tests; native make check 4/4 without copied files. Stacked on !1; both target fork main. Harness fix only.
- Benchmark follow-ups: [physical-input admission #2](https://github.com/itpplasma/benchmark_vmec/issues/2), [source/input seals #3](https://github.com/itpplasma/benchmark_vmec/issues/3). Historical rows remain unchanged; fixes not yet implemented.
- [CHEASE #4](https://github.com/itpplasma/chease/pull/4): correct fourth smoothed-jet permutation slot. Native four-component/cubic/sine baseline-fail oracle;1/1 passes; headd0e4b3d. Cache repair does not explain retained physical-force errors.
- [CHEASE #5](https://github.com/itpplasma/chease/pull/5): mixed correctness/tiling review. [#18](https://github.com/itpplasma/chease/pull/18), `591e654`, now isolates the empty/singleton/zero-pivot contract with original regular-matrix arithmetic. Parent bounds-check failure, fixed independent dense/edge oracle and native Make pass. Tiling remains performance work; #5 is not a single-defect correctness handoff.
- [MARS-Q #31](https://github.com/krystophny/MARS-Q/pull/31), draft: same CHEASE smoothing permutation repair, native baseline-fail1/1 oracle; heade14c6d1. Pair A/B pending.
- [MARS-Q #32](https://github.com/krystophny/MARS-Q/pull/32), draft: mixed correctness/tiling review. [#45](https://github.com/krystophny/MARS-Q/pull/45), `3828c7d`, isolates native factorization status and edge inputs, with parent failure, fixed dense/edge CTest and full Make success. Pair A/B remains pending; #32 retains the optional tiling work.
- [CHEASE #6](https://github.com/itpplasma/chease/pull/6): opt-in folded angular bulk/three-variable center border; independent against fork mainfb46366, headb244c04, with inactive/map guards; historical head0dfd639 remains frozen. Native Make and independent periodic/center/boundary matrix oracle pass. Integrated exact-E0 physical fields pass; no dependency.
- [CHEASE #7](https://github.com/itpplasma/chease/pull/7): optional installed LP64 BLAS in existing Make, default native; independent head9a128ae. Both Make builds and vector/stride/inner-product CTest oracles pass; system symbol resolution confirmed. It is not the principal performance repair.
- [MARS-Q #33](https://github.com/krystophny/MARS-Q/pull/33), draft: independent opt-in folded angular band with center Schur border, head154292d against fork main8824bb18. Native matrix oracle and full Make pass; combined E0 timing/core fields retained, axis-q diagnostic and Pair A/B gates remain open.
- [CHEASE #8](https://github.com/itpplasma/chease/pull/8): active matrix-column clearing, independent headfa72085. Exact-E0 output-byte oracle and native Make pass.
- [MARS-Q #34](https://github.com/krystophny/MARS-Q/pull/34), draft: same active-column clearing, independent head57f72f2. NS64/NT2569.370→6.174s, seven native files byte-identical; Pair A/B pending.
- [MARS-Q #35](https://github.com/krystophny/MARS-Q/pull/35), draft: axis-F coordinate typo, independent head0e129cf. Actual native-call baseline2/8→8/8; ordinary source-integral gate repaired with unchanged psi/q/nonaxis profiles. Pair A/B pending.
- Case/force/sign and alternative explanations: [equilibrium errata](../equilibrium/ERRATA.md). Fork fixes await human review before merge/upstream transfer.

## MARS delivery candidates

- Fork: **krystophny/MARS-Q**; #5–29 open, some drafts. Compatibility features exist in executed lineage; PR heads are divergent histories.
- Before upstream delivery: exact base/patch and pinned `mars_mastu_validate` Pair A/B gates.

- [#5](https://github.com/krystophny/MARS-Q/pull/5) **open** — native frozen-field B/X ingress; delivery foundation.
- [#12](https://github.com/krystophny/MARS-Q/pull/12) **open** — rebuild passive operator before output; final DWK/torque consistency.
- [#7](https://github.com/krystophny/MARS-Q/pull/7) **open** — preserve F=R B_phi (`KEEPTFUN=1`); accepted compatibility.
- [#8](https://github.com/krystophny/MARS-Q/pull/8) **open** — rebuild BPK after filtering; small measured correction.
- [#9](https://github.com/krystophny/MARS-Q/pull/9) **open** — physical-field passive pressure carrier; required partner of #7.
- [#17](https://github.com/krystophny/MARS-Q/pull/17) **draft** — authoritative experimental Ti/Te (`KPROFTAUTH=1`); accepted profile setting, delivery gates pending.

## MARS scoped fixes and diagnostics

- No established repair of the remaining magnitude discrepancy in this group.

- [#6](https://github.com/krystophny/MARS-Q/pull/6) **open** — periodic/Hamada projection; Shaing route, outside KNTV=21.
- [#13](https://github.com/krystophny/MARS-Q/pull/13) **open** — electric numerator-sign control; not a coordinate conversion.
- [#14](https://github.com/krystophny/MARS-Q/pull/14) **open** — electron diamagnetic edge initialization; tested deck inert; overlaps #25.
- [#15](https://github.com/krystophny/MARS-Q/pull/15) **draft** — full trapped bounce/drift singular extraction; finite-birth/energetic review needed.
- [#16](https://github.com/krystophny/MARS-Q/pull/16) **open** — X3 orbit-average normalization; diagnostic, incomplete physical action.
- [#20](https://github.com/krystophny/MARS-Q/pull/20) **draft** — kinetic-pressure mass solve; small sensitivity, unadmitted repair.
- [#21](https://github.com/krystophny/MARS-Q/pull/21) **draft** — NDB thermal fast denominator; inactive at accepted KFASTRUN=0.
- [#25](https://github.com/krystophny/MARS-Q/pull/25) **draft** — electron boundary rotation; consolidate overlap with #14.
- [#10](https://github.com/krystophny/MARS-Q/pull/10) **open** — opt-in DWK contractions; verify diagnostic-off parity.
- [#11](https://github.com/krystophny/MARS-Q/pull/11) **open** — torque boundary stages; distinguish assembly, masks and smoothing.
- [#18](https://github.com/krystophny/MARS-Q/pull/18) **draft** — exact work ledger; reconstruction, not physical-action proof.
- [#19](https://github.com/krystophny/MARS-Q/pull/19) **draft** — selected pressure-response traces; localize cancellation.
- [#22](https://github.com/krystophny/MARS-Q/pull/22) **draft** — trapped quadrature response components; not a collisionless production fix.
- [#26](https://github.com/krystophny/MARS-Q/pull/26) **draft** — VI0 energy-factor export from KI0; no allocation repair.
- [#27](https://github.com/krystophny/MARS-Q/pull/27) **draft** — KI0 coverage/response traces; expose omitted support.
- [#29](https://github.com/krystophny/MARS-Q/pull/29) **open** — KI0 endpoint-drift export; no zero-node interval repair.
- [#28](https://github.com/krystophny/MARS-Q/pull/28) **draft** — runtime tests default to in-tree executable; harness only.
- [#23](https://github.com/krystophny/MARS-Q/pull/23) **draft** — replacement history for closed upstream #4; prefer exact-base #5.
- [#24](https://github.com/krystophny/MARS-Q/pull/24) **draft** — replacement history for closed upstream #5; compare with #9.

- Earlier fork attempts: [#1](https://github.com/krystophny/MARS-Q/pull/1), [#2](https://github.com/krystophny/MARS-Q/pull/2), [#3](https://github.com/krystophny/MARS-Q/pull/3), [#4](https://github.com/krystophny/MARS-Q/pull/4) **closed** (carrier/filter/BPK/normalization).
- Upstream [gafusion #4](https://github.com/gafusion/MARS-Q/pull/4), [gafusion #5](https://github.com/gafusion/MARS-Q/pull/5) **closed, unmerged**.
- Unfiled: KI0 nonempty-interval allocation (tested torque effect 0.028474%); wrapped RUU endpoint moments (diagnostic, not torque clock).
- Physical adjoint, passing-drift and historical canonical-embedding corrections remain unadmitted.

## GPEC and PENTRC

- [#294](https://github.com/PrincetonUniversity/GPEC/pull/294) **open** — four-line observer-grid precision repair at `e338152093fe0a7bc1cccf0cec3598b5c5b4927d`; snapping, evaluator and output formats retained. Independent grid/base-failure and two-sided surface-trace controls pass; downstream resampling lives in `rmp_torque`, with unsupported samples masked.

- [#280](https://github.com/PrincetonUniversity/GPEC/pull/280) **merged** — contour OpenMP race and nested tolerance coupling.
- [#281](https://github.com/PrincetonUniversity/GPEC/pull/281) **merged** — remove spurious major-radius factor in GAR drift.
- [#282](https://github.com/PrincetonUniversity/GPEC/pull/282) **merged** — correct rotation/harmonic documentation; no delivered-output flip.
- [#268](https://github.com/PrincetonUniversity/GPEC/pull/268) **merged** — sign-convention documentation.
- [#269](https://github.com/PrincetonUniversity/GPEC/pull/269) **merged** — positive-q documentation.
- #280/#281 already in executed Fortran PENTRC `e68d7ac2`; general stored-torque covector test remains open.
- [#391](https://github.com/OpenFUSIONToolkit/GPEC/pull/391) **merged** — Julia GAR radius-factor repair; separate from Fortran runs.
- [#392](https://github.com/OpenFUSIONToolkit/GPEC/pull/392) **merged** — Julia energy-specific tolerances; no retrospective Fortran change.
- [Issue #275](https://github.com/PrincetonUniversity/GPEC/issues/275) **open** — artificial 1e-9 zero-rotation frequency; exact-zero serializer gate needed.

## Conversion and NEO

- [#39](https://github.com/itpplasma/rmp_torque/pull/39) **merged** — strict MARS readers/native Boozer conversion; pin executed converter.
- [#40](https://github.com/itpplasma/rmp_torque/pull/40) **merged** — MARS interoperability and Pair A/B delivery gates.
- [#41](https://github.com/itpplasma/rmp_torque/pull/41) **merged** — strict GPEC ASCII/field interface validation; no full-volume equivalence.
- [#34](https://github.com/itpplasma/rmp_torque/pull/34) **merged** — adversarial field checks and DWK reconstruction; no action proof.
- [#35](https://github.com/itpplasma/rmp_torque/pull/35) **merged** — booz_xform coordinate maps; historical physical embedding still conditional.
- [#37](https://github.com/itpplasma/rmp_torque/pull/37) **merged** — measured toroidal orientation maps RNTOR=-3 to n=+3.
- [#38](https://github.com/itpplasma/rmp_torque/pull/38) **merged** — reject inconsistent whole Boozer charts.
- [#44](https://github.com/itpplasma/rmp_torque/pull/44) **merged** — plot displacement contribution; fix b_lag+b_eul double counting, plotting only.
- [#169](https://github.com/itpplasma/NEO-2/pull/169) **merged** — prescribed Om_tE flux/torque output; sealed D-matrix reconstruction retained.
- [NEO-2 #193](https://github.com/itpplasma/NEO-2/pull/193) **open** — allocate the full magnetic reader's temporary once for multiple surfaces; `a0b7039`, branch `equilibrium/magfie-multiple-surfaces`, against `itpplasma/NEO-2:main`. Native analytic two-surface test fails before and passes after; full-vector Phase 1 measurements use the fix. No merge.
- [#90](https://github.com/itpplasma/NEO-RT/pull/90) **open** — per-resonance native torque ledger; root/measure diagnostic.
- [#94](https://github.com/itpplasma/NEO-RT/pull/94) **closed draft** — passing-drift control; historical raw outputs uncollected.
- [#102](https://github.com/itpplasma/NEO-RT/pull/102) **merged** — validated POTATO input adapters; no TC24 torque admission.
- [#105](https://github.com/itpplasma/NEO-RT/pull/105) **open** — POTATO signed modes; reflection/root-support gates needed.
- [#107](https://github.com/itpplasma/NEO-RT/pull/107) **open** — POTATO representation invariance; convergence still required.
- [#108](https://github.com/itpplasma/NEO-RT/pull/108) **merged** — fixed-energy POTATO contour diagnostics.
- [#122](https://github.com/itpplasma/NEO-RT/pull/122) **merged** — EQDSK flux gauge for NEO-2 profile import.
- [#127](https://github.com/itpplasma/NEO-RT/pull/127) **merged** — ITER POTATO domain support; no convergence claim.
- [#80](https://github.com/itpplasma/NEO-RT/pull/80) **closed** — broad historical experiment; no accepted all-in-one fix.
- [Sign/serializer issue ledger](https://gitlab.tugraz.at/plasma/proj/plasma-sign-conventions/-/blob/main/docs/SIGN_CONVENTION_ISSUE_LEDGER.md).

## ARES main and legacy proposals

- New work on **main**. #1–11 remain open; heads not contained in main; review exact patches/oracles before reuse.
- Full-density parity approximate; half-density parity fails. NEO functional is the same physical model, not an independent reference.

- [#1](https://github.com/itpplasma/ares/pull/1) **draft** — source/cell/mask binding; reject unbound outputs.
- [#2](https://github.com/itpplasma/ares/pull/2) **draft** — closed-form trapped harmonic oracle.
- [#3](https://github.com/itpplasma/ares/pull/3) **draft** — elliptic-nome trapped drive oracle.
- [#4](https://github.com/itpplasma/ares/pull/4) **draft** — resonance sign-selectivity tests.
- [#5](https://github.com/itpplasma/ares/pull/5) **draft** — ell=0 drift-reversal pitch oracle.
- [#6](https://github.com/itpplasma/ares/pull/6) **draft** — finite-width/Plemelj residue limit tests.
- [#7](https://github.com/itpplasma/ares/pull/7) **draft** — circular trapped scaling/residue oracle.
- [#8](https://github.com/itpplasma/ares/pull/8) **open** — source binding and cell weights in every trace.
- [#9](https://github.com/itpplasma/ares/pull/9) **open** — signed mode/momentum leg in circular torque.
- [#10](https://github.com/itpplasma/ares/pull/10) **open** — report skipped Python tests as SKIP.
- [#11](https://github.com/itpplasma/ares/pull/11) **open** — build the tested drift CLI; reject stale/missing executables.

- Next: half-density profiles/collisions/assembly, complete species/partition coverage and root/support bounds.
- Owners: [ARES PLAN](https://github.com/itpplasma/ares/blob/main/PLAN.md), [modes and admission](https://github.com/itpplasma/ares/blob/main/docs/MODES_AND_FIXES.md).

- [MARS-Q fork #30](https://github.com/krystophny/MARS-Q/pull/30) **draft** — correct CHEASE cubic-profile integration in both directions; native polynomial baseline8/12→fixed12/12. Registered equilibrium pair and downstreamMARS PairA/B remain open. Forkmain aliases existingmaster8824bb18; no upstream transfer.

## Additional CHEASE profile lookup repairs, 2026-10-08

- [Public CHEASE #9](https://github.com/itpplasma/chease/pull/9) **open** — independent query-first PPSPLN bracket loop, head6f9a9ce againstfb463663. Native48-case cubic/byte controls, Debug/Release CTest and native Make pass; combined NS128/NT51230.993s.
- [MARS-Q fork #36](https://github.com/krystophny/MARS-Q/pull/36) **draft** — same independently based native fixed-form optimization, head3863df3 against8824bb18. Native gates pass; combined NS64/NT2565.322s. Downstream Pair A/B remains open.

## Audit 2026-10-07 (read-only)

- **Citations:** 42 PR and issue citations across eight repositories match live state on open, draft or closed, and on cited commits.
- **Corrections to make:** CHEASE #3 is based on main, not stacked on #1, though it shares one of two commits with #1. MARS-Q #23 and #24 need full URLs, because krystophny/MARS-Q #5 is open. `itpplasma/chease` is not a GitHub fork (`isFork=false`), so do not call it one.
- **Unverified:** INTERPOS !1 and !2 (GitLab, not covered by gh). The DESC 0.17.3 backport is now reproducible at the local branch/commit recorded above.
- **Historical fork audit:** issue settings on our forks are not the upstream issue settings. Actual FreeGS/STELLOPT/GVEC upstream issue trackers are enabled and now own the dropped-code handoff; GVEC uses MPCDF GitLab. Retained solver workflow is unchanged.
- **Remotes:** see EQ-D45 in `equilibrium/ERRATA.md`.

## Retained correctness reviews and owning-tool handoffs, 2026-10-08

- [Public CHEASE15](https://github.com/itpplasma/chease/pull/15) and [MARS-Q41](https://github.com/krystophny/MARS-Q/pull/41), draft: move existing SMOOTH before MAGAXE so current uses the actual axis normalization. Whole-native NONLIN parent fails; eight physical-polynomial controls pass per variant; smoothing0 packet byte parity. The full MARS pilot avoids immediate singularity but later source-map growth still aborts.
- **Merged to own main:** [KIN6D2](https://github.com/itpplasma/kin6d/pull/2): cell-arc P2 coarea and moving-interface JVP, stacked on [P2/gauge PR1](https://github.com/itpplasma/kin6d/pull/1). Twenty-six registered tests pass Release/Debug; independent relocated-contour finite differences and deliberately omitted interface-term failure establish derivative behavior. Coupled inverse solver excluded.
- [VMECerror1](https://github.com/dpanici/VMECerror/pull/1), actual upstream master: include general physical-force norm cross term. Standalone circular/sheared/elongated/reversed signed controls: parent12failures, fixed16pass over1536points, independent Cartesian curl. No historical paper ranking-impact claim.
- FPM actual-upstream [absolute-path1336](https://github.com/fortran-lang/fpm/issues/1336), [cross-command freshness1337](https://github.com/fortran-lang/fpm/issues/1337), and [include reproducer358](https://github.com/fortran-lang/fpm/issues/358#issuecomment-6060152609): current-main parent/fixed behavioral evidence and independent review branches published. Three atomic PRs are prepared; CONTRIBUTING requires community scope consensus before opening them. [Handoff and complete scripts](../archive/equilibrium/dechurn/INDEX.md#entry-310).

- [MARS-Q42](https://github.com/krystophny/MARS-Q/pull/42), draft: integrate actual axis-centred inner contours for prescribed-q PROFILE. Native56 controls and four legacy byte guards pass; same-held-field inner error falls from62.7% to below3.4e-13. Full same-input pilot still fails in the next mapping stage; no equilibrium acceptance. Prerequisites30/39/41 are separate; this supersedes q4 continuation in40.
- **Merged to own main:** [KIN6D3](https://github.com/itpplasma/kin6d/pull/3): evaluate known native face endpoints directly in the cell-arc JVP. Parent false rejection becomes valid amplitude identity;26 registered Release/Debug gates pass. Stacked on2; coupled inverse accuracy remains open.
- Fo owner-main repairs43d0115 (version substitution) and ac9704a (package preprocessing/cache semantics) are published with full standalone reproducers and original-consumer rechecks.

- **KIN6D own-main integration:** PRs1/2/3/4 are merged; main `f073eba` pins latest verified FortFEM `44897b4`, retaining17 exact periodic-cylinder identities and publishing affine P2 reference enclosures. Eleven affected native checks pass in both profiles; three historical P1 outputs remain byte-identical. Inverse accuracy remains under qualification.
- [MARS draft43](https://github.com/krystophny/MARS-Q/pull/43): finite F²(x=rho²) source/current and primitive knots, with48 whole-native source controls,32 PROFILE controls and4 legacy byte guards. Direct API/knots scope only; continuous TMF field interpolation and full iteration remain separate. [Review issue44](https://github.com/krystophny/MARS-Q/issues/44) retains the unresolved prescribed-q iteration with a complete generated circular/shaped shell reproducer. Both remain on our review repository pending human upstream review.
- Fo owner-main27f1f22/c59b2e2/4684809 repairs native CMake preset/output inventory and failed zero-random test selection. Native/public cold/warm/edited/restored fixtures and original KIN6D consumer rechecks pass; no global driver installation.

- [Actual Jonquil issue39](https://github.com/toml-f/jonquil/issues/39) and [PR40](https://github.com/toml-f/jonquil/pull/40): geometric JSON output buffers. At upstream review request, benchmark/run/README artifacts were removed; the PR now contains only the serializer fix and unit-test integration. Exact buffer-growth coverage for arrays/objects passes with37 native FPM cases and4 CMake/CTest gates. Earlier scaling/consumer evidence remains archived locally. [Minimal publication receipt](../archive/equilibrium/dechurn/INDEX.md#entry-267); no review comment was posted.
- Fo own-main993d9ba/00e6400 independently repair test-helper module-interface cache invalidation and declared test dependencies. Separate preserved-mtime integer oracles and original Jonquil native test recheck pass; no global install.

- **Merged atomic [KIN6D4](https://github.com/itpplasma/kin6d/pull/4):** integrate continuous piecewise-linear profile sources across P1/P2 flux-level cuts, with consistent state/profile/parameter JVP/VJP and explicit work/error failure. Exact pressure-load parent error10.60% becomes correct rational moments;34 independent checks and27 registered Release/Debug gates pass. The inverse-cache/mean-source solver is excluded; saved equilibrium accuracy remains unqualified.
- **Published [FortFEM5af7291](https://github.com/lazy-fortran/fortfem/commit/5af7291d1dae8abf991ff228450700668f64853a):** generic vector triangle level-cut integration and generated geometry. Independent cut moments, retained positive traces, derivative/failure controls and canonical regeneration pass. Embedded estimates are not rigorous enclosures. Latest-main consumer pin verified; broader generation inventory remains explicit.
- **MARS draft43 input follow-up:** actual native parser now checks generated circle/shaped q4 and forward headers; five valid/two malformed controls pass. The independent forward32×32 control succeeds; q4 robustness issue44 remains unresolved. [EQ-D102](../equilibrium/ERRATA.md#eq-d102-mars-standalone-reproducer-generates-invalid-native-expeq-headers).

KIN6D inverse transfer checkpoint: own repository branch [`equilibrium/inverse-integration`](https://github.com/itpplasma/kin6d/tree/equilibrium/inverse-integration), `7d1e836`, based on main `f073eba` and verified FortFEM main `44897b4`. Combined Debug45/45 passes; CPU/review and physical qualification remain pending. No upstream issue/comment or completion claim accompanies this branch.

- **KIN6D draft [5](https://github.com/itpplasma/kin6d/pull/5), `1308d22`:** geometry-only Solovev smooth-domain callback with generated Cartesian Jacobian/Hessian and point JVP/VJP. Independent source review and native CPU36/36, Debug36/36 pass. Geometry predicates, root/Jacobian roundoff and native assembly/readback remain uncertified; no scientific PDE run. Fo infrastructure failure selected no tests and remains an owning-tool repair.

- **Fo draft [212](https://github.com/lazy-fortran/fo/pull/212), `cd84b7b`:** prevent recursive native-CMake fixture launches when PATH supplies bare `cmake`/`ctest` names, including `.exe` forms. The actual compiled fixture rejects all four aliases with the expected marker and failing exit. Exact-path cleanup removed the runaway fixture copies that exhausted local process capacity; scientific jobs were untouched. Full native-backend verification remains open: the pinned public driver still delegates generation to CMake after the owning controller's pending provider/platform repairs. Those repairs are excluded from this commit; shared main and its pre-existing edits are preserved. Reproducer, logs and cleanup receipt are retained in `/Users/ert/tmp/iter-equilibrium-20261009/`.

- **KIN6D draft [6](https://github.com/itpplasma/kin6d/pull/6), `a262675`, stacked on5:** explicit affine/nonlinear geometry composition and scalar Hessian connection through verified FortFEM `de4245c5`. The owning reference-triangle guard now rejects exact outside dyadics whose sum rounds to one; its subtraction comparison is exact by Sterbenz. Original adapter CPU/Debug37/37 evidence remains pinned to `3cf0aeb`; final stacked tree passes38/38 per profile. Floating candidate only; mapped physical qualification remains open. [Original evidence](../archive/equilibrium/dechurn/INDEX.md#certificates), [guard and final evidence](../archive/equilibrium/dechurn/INDEX.md#certificates).
- **KIN6D draft [7](https://github.com/itpplasma/kin6d/pull/7), `41db837`, stacked on6:** finite-node mapped P2 stiffness/load with one shared geometry sample per node, authoritative generated source and complete failure clearing. Independent exact forward-chart/Vandermonde oracle reproduces36 stiffness entries and6 loads at two distinct nodes. CPU38/38, Debug38/38, independent focused2/2 per profile and named Fo1/1 pass. Supplied quadrature remains uncertified; extra underintegration null modes, global assembly and PDE accuracy remain open. [Reviewed sources, counterexample and receipts](../archive/equilibrium/dechurn/INDEX.md#certificates).
- **Fo owning main repairs `204192f` / `94c89c0`:** confined chained library aliases pass4 native gates and actual SymEngine inventory controls; deep-lint cold/warm JSON equality passes5 native lint gates with UTF-8/int64 preserved. The combined published-source private driver plus approved bootstrap passes original callback and adapter named consumer gates1/1 each, with source unchanged. Full native suites remain separate; no global install or shared resident restart.

- **KIN6D draft [8](https://github.com/itpplasma/kin6d/pull/8), `2e4cd53`, stacked on7:** value-only polygon-to-physical positions and physical-to-polygon location through one owning ray-root helper and a generated forward scale. The position type exposes no J/H; existing jet cut rejection and clearing remain strict. Independent36 rational ray pairs/144 generated derivative identities/three mutants, affected CPU3/3 and Debug3/3 in both runs, and final-source named Fo1/1 pass. Historical44 lint findings unchanged. No inherited arithmetic certificate or mapped PDE admission. [Published source joins and review](../archive/equilibrium/dechurn/INDEX.md#certificates).

## Own-main integration, 2026-10-09

Chris reaffirmed main-only development for own codes. KIN6D checkpoint `2e4cd53`
contains the exact reviewed PR5–8 commits, fast-forwarded without source edits.
PR5 is merged; stacked drafts6–8 are closed as superseded by own-main integration.
All historical review/source hashes remain valid. The mapped state change is now
published on own main `fd3700a` after frozen source and mathematical review.
Third-party solver PR policy is unchanged; scientific qualification stays open.

- **KIN6D own main `fd3700a`:** mapped P2 state, shared assembly/CG and physical jet/field readback; CPU39/39, Debug39/39, independent source/math review and focused Fo1/1 pass. Final repaired-driver lint preserves53 parent findings, adds none. No full-mesh accuracy or scientific PDE admission.
- **Fo own main `3049a03`:** dynamically retry filesystem inventory collection on an overflow-only status, preserving hard/alias errors and negative-capacity rejection. Existing native regression17/2 becomes19/0; original KIN consumer inventory resolves. Seven unrelated owner edits remain preserved; no global driver installation.
