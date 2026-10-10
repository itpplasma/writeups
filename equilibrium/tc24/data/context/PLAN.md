# ITER benchmark programme

- Updated: 2026-10-10 by Chris&AI. The previous campaign plan at
  `4ff823e1a:PLAN.md` is historical, not instructions.
- Final goal: a reproducible full ITER NTV benchmark with Xingting and colleagues,
  built bottom-up so that every number downstream is understood.
- **Active slice: axisymmetric equilibrium only, not complete.** Stop before
  perturbation and transport.
- Historical ITER torque results: [frozen status](review/ITER_STATUS_20261007.md),
  [merge review](review/MERGE_REVIEW.md), [upstream PRs](review/UPSTREAM_PRS.md).

## Goal of the equilibrium slice

The downstream NTV codes consume B, q, flux labels and flux coordinates. This
slice must deliver:

1. **Trusted equilibria with known accuracy** for the case ladder below, in the
   form the perturbation slice will consume (signed fields, q, psi/Phi maps,
   COCOS-tagged exports).
2. **KIN6D qualified as the main equilibrium code:** on the same problems its
   error matches or beats public CHEASE, MARS CHEASE, VMEC++ and DESC at
   comparable wall time. The deliverable is one plot per case: error versus
   resolution and error versus wall time, with all five codes.
3. **All defects fixed (Chris, 2026-10-09):** every defect in the equilibrium
   codes we use that gives wrong results beyond numerical limitations is
   identified, fixed and covered by a regression test. Fixes for third-party
   codes are PRs on our forks (upstream later, after human review). Fixes for
   our own codes go on `main`. See [Defect closure](#defect-closure-cross-cutting).

Purely numerical discrepancies (correct limit, expected rate) are explained only
as far as they matter for (1) and (2). Their mechanisms are not proved in detail.
Anything that is *not* numerical is a defect candidate and must be closed.

## Defect closure (cross-cutting)

- **Numerical limitation or defect?** A difference counts as a numerical
  limitation only if it converges to the correct answer at the expected rate
  under refinement of the responsible parameter (resolution, quadrature,
  tolerance, export precision, boundary sampling). Anything else is a defect
  candidate. This includes:
  - a wrong limit, or a rate below prediction not explained by regularity
  - sign, unit or COCOS errors
  - wrong exported or derived quantities (q, flux, current, profiles)
  - input or profile mapping errors
  - silent failures, or wrong behaviour in options we use
- **Codes and paths in scope:** KIN6D, FortFEM and other own dependencies;
  public CHEASE and MARS CHEASE; VMEC++; DESC. This covers input/profile
  parsing, solve, q/flux/current computation, and export plus our readers of
  those exports. Dependencies we use (INTERPOS, readers) are included.
  Withdrawn codes keep their upstream issues.
- **Detection:** systematic, not open-ended source reading. Use the Phase 1–5
  convergence studies against exact and converged references, sign/COCOS round
  trips, and export→readback against native values. Each ERRATA entry is
  re-classified as defect or limitation in DC-2.
- **Fix procedure:**
  1. Write a minimal reproducer (local evidence, not committed).
  2. Make the smallest fix, with a behavioral regression where one is
     proportionate; a test must fail without the fix.
  3. Check that the affected convergence result is now correct.
- **Where fixes go:**
  - Third-party code: branch `equilibrium/<topic>` and a PR against our fork's
    `main`, one defect per PR. Upstream PRs only after Chris's review.
  - Own code: commit to `main` with the test.
  - Record every PR in [UPSTREAM_PRS](review/UPSTREAM_PRS.md) and the
    disposition in [ERRATA](equilibrium/ERRATA.md).
- **Defect ledger:** each code gets one row per ERRATA defect, with status
  *open*, *PR open* or *fixed on main/fork*. The slice is not complete while a
  confirmed defect is open, or while an unexplained, non-converging difference
  remains.

### Accuracy targets (provisional working targets, Chris 2026-10-09)

These values are not derived from NTV sensitivity. They are replaced once the full
pipeline to NTV exists and the uncertainty/sensitivity study below sets them.

| Quantity | Norm | Target at reference resolution |
|---|---|---|
| psi | relative L2 over plasma | 1e-6 |
| B_pol, B_tor | relative L2 and max over plasma | 1e-5 (max 1e-4) |
| q(s) | relative max over 0.05 <= s_tor <= 0.98 | 1e-5 |
| Axis position, volume, Phi_edge | relative | 1e-6 |
| Force balance j×B − grad p | relative to B²/(mu0 a), RMS | reported, not a gate |

A code reaching the target is "converged" for that case. A smaller residual
discrepancy does not justify further work unless it shows non-convergence
under refinement.

## Current implementation and phase status

The case contracts and signs are owned by [CASE_CONTRACT](equilibrium/CASE_CONTRACT.md),
[cases.json](equilibrium/cases.json) and plasma-sign-conventions. KIN6D main
`f6a33c9` includes curved P2/P3, cubic profiles, signed current constraints,
prescribed q (`60bef4c`), TC24 assembly/readback improvements (`313cde5`) and
FortNum `901aae0`. Executed studies retain their earlier binary/source pins;
main integration does not relabel their timings. Public/MARS CHEASE, VMEC++
and DESC remain the references; FreeGS, original VMEC and GVEC stay withdrawn.

| Phase | Status | Remaining reason or delivered item |
|---|---|---|
| 0 Dechurn | Done | Archives, PR/status cleanup and the replacement brain section are delivered; raw figure inputs remain preserved. |
| 1 Exact | Open | Five-code curves and P2/P3 rates delivered; DESC reaches all sampled targets by spectral refinement; VMEC++ targets and matched DESC cold cost remain. |
| 2 Circular | Open | Eight-case comparison and current KIN6D cost refresh pass sampled targets; two VMEC++ target gaps and selected consumer exclusions remain. |
| 3 Inverse | Open | Final-stage readback corrected; public E2/Solovev lose psi qualification. MARS failure, VMEC++ targets, nonlinear bounds and consumer geometry remain open. |
| 4a E4 | Open | Two laws, five codes and consumer comparisons delivered; finite-beta DESC accuracy/stopping passes; VMEC++ targets remain. |
| 4b TC24 | Open | KIN6D held-quadrature Bpol rate 3.66 matches prediction; finite-reference uncertainty, target accuracy and converter geometry remain open. |
| 5 Cylinder | Open | Five-code curves and KIM ingress delivered; coarse KIN6D repaired; DESC accuracy/stopping passes at all four aspect ratios; selected consumer paths remain excluded. |
| 6 Report | Done (report) | The 27-page report and ten figures are published in writeups PR1; scientific slice closure remains open. |

## Phase 0 — Dechurn (do first; time-box about 2 working days)

DC-1–DC-10 are delivered. Superseded evidence remains in six LFS tarballs
indexed under `archive/equilibrium/dechurn/`; raw figure inputs are recoverable.
New bulk moves require a reviewable manifest and Chris's approval; preserve
native outputs feeding figures. No further archive campaign is part of this slice.

## Phase 1 — Exact-solution convergence and cost (core milestone)

- Cases: E0 Solovev on its physical LCFS (circular-ish, existing), plus the
  Cerfon–Freidberg ITER-like shaped Solovev (A=3.1, kappa=1.7, delta=0.33,
  finite beta). Both have closed-form psi, B, q. The rectangular box is kept only
  as a KIN6D unit test.
- Codes: all five, same boundary, same source law, same signed flux constraint.
- Measured per run: errors listed in the target table, native iteration count,
  wall time on one fixed core. At least 4 resolutions per code, chosen so that
  at least 3 lie in the asymptotic range.
- Expected rates are stated before the runs, from the literature and
  discretization:
  - KIN6D P2 isoparametric: psi O(h³) L2, B O(h²).
  - CHEASE: bicubic Hermite, with the rate taken from Lütjens 1996 and
    checked against the measurement.
  - VMEC++: radial O(1/ns), spectral in m (Panici 2023).
  - DESC: spectral.
  An observed rate that misses its prediction is a finding to explain. A rate
  that matches it closes the case for that code.
- [Committed comparison](equilibrium/phase1/results/README.md): generic KIN6D
  P2/P3 and both CHEASE variants meet sampled targets. The CSVs supersede the
  older P2-only README. P3 predicts psi O(h⁴), B O(h³); measured exact-case
  rates agree. The axis recovery and field-consistent contour readback are
  fixed on KIN6D main. DESC's shaped boundary truncation is explained;
  VMEC++ near-axis maxima remain a qualification gap.
- KIN6D's recovered-flux estimator has measured exact-case effectivity and
  circular/E4 Richardson comparisons. Continuous nonlinear/inverse reliability remains a
  separate open cell; measured inverse effectivity is delivered. Costs must state whether estimator/export/readback
  are included; historical pre-Brent circular timings remain historical.
- Deliverable: two figures per case (error vs DOF and error vs wall time, all
  codes), a rate table, and a short section in the report. Template: Lee &
  Cerfon 2015 (ECOM vs CHEASE, q error at fixed run time).

### End-to-end accuracy (every phase; Chris, 2026-10-09)

- [Phase 1 export results](equilibrium/phase1/results_export/README.md): two-resolution CHEASE public/MARS and KIN6D P3 now include actual GPEC/DCON and full NEO-2 vectors/Jacobian (NEO-2 PR193); native MARS Fourier/Hamada measured on both exact cases, with second-order Hamada metric error. VMEC++/DESC downstream converters remain unused.

Each phase measures accuracy after export and actual consumer readback.

- Measure the same errors on fields reconstructed from every export path in use:
  - G-EQDSK written by each code and by our converters
  - CHEASE/MARS native outputs used by MARS
  - Boozer/Hamada files used by NEO-2, NEO-RT and GPEC
  - each consumer's own reader where it can be called standalone (the
    NEO-RT/NEO-2/libneo EQDSK and Boozer readers)
- Additional quantities: |B| on flux surfaces, q, the Boozer |B| spectrum
  (B_mn) and the flux-label maps (s_tor, s_pol, rho_tor).
- One extra figure per case: native error versus exported-and-read-back error
  for each code and path. A path whose error does not decrease with the producer's
  resolution (fixed grid, precision, extrapolation, resampling) is a defect
  candidate under the defect closure rule.

## Phase 2 — Circular toroidal ladder without an exact solution

- [Eight-case comparison and export study](equilibrium/phase2/results/README.md) delivered; two VMEC++ target gaps and the stated consumer exclusions remain.
- KIN6D P3 Richardson Bpol errors are 7e-9 to 7e-8; majorant/Richardson 1.3–3.0. Shift/q remainders follow A^-3/A^-4. In 72 matched selected-state calls, KIN6D beats both CHEASE variants in all eight cases; DESC/VMEC++ timings remain historical.
- Self-convergence per code (Richardson estimate of the error at reference
  resolution) plus the KIN6D estimator, then cross-code difference at converged
  resolution. Cross-code differences above target need a cause.
- Physics check: Shafranov shift and q(0) versus the analytic large-A expansion
  (FortSym derivation), with the expansion error scaling as 1/A.

## Phase 3 — Inverse (prescribed-q) cases

- [Three-case inverse study](equilibrium/phase3/results/README.md) and [KIN6D supplement](equilibrium/phase3/results/kin6d.md) deliver F, current, fields, q and cost. KIN6D and public E1 have sampled passing states; public E2/Solovev miss psi after final-stage correction. MARS remains a candidate; VMEC++ target gaps remain and DESC reaches its sampled targets with calibrated stopping.
- KIN6D inverse is on main `60bef4c`; the three contracts have curved-P3
  convergence and signed EQDSK/libneo readback. Inverse estimator diagnostic stability is measured on all three ladders;
  E1/E2 Hamada and actual NEO-2/GPEC field/q/flux readback are delivered; internal geometric consistency remains open.
- CHEASE public and MARS run in their native q modes. Untouched and minimally
  corrected MARS still fail E1; our zero-moment regression and algorithm port
  are excluded. Leonardo's current-profile replay passes ([EQ-D88](equilibrium/ERRATA.md#eq-d88)).
- VMEC++ with a prescribed iota or current profile, mapped through the checked
  psi↔Phi relations.

## Phase 4 — Shaped and TC24

- Phase 4b is pinned to the collaborators' **modx03 CHEASE equilibrium** ([provenance](equilibrium/phase4/tc24/EQUILIBRIUM_PROVENANCE.md)); [five-code convergence/cost, exact-deck replay, three variants and consumer exports](equilibrium/phase4/tc24/README.md) are delivered, with rate/target gaps and converter geometry explicitly unqualified.
- [E4 two-law study](equilibrium/phase4/results/README.md): five codes × four resolutions and 24 consumer chains delivered; VMEC++ target gaps remain; finite-beta DESC stopping is qualified at the sampled physical targets.
- TC24 source equilibrium inputs, COCOS and profile consistency are pinned once
  (EQ-D04). The X-point itself is out of scope for nested-flux codes.
- Output: the equilibrium export package the perturbation slice will consume,
  with its measured accuracy.

## Phase 5 — Periodic cylinder (can run alongside Phase 1)

- [Five-code cylinder study](equilibrium/phase5/results/README.md) now includes KIN6D P3; coarse KIN6D readback failures are repaired and replayed; DESC stopping and accuracy pass at all four aspect ratios.

Gold–Hoyle and Lundquist exact references fix the axial period. The figure
compares error against aspect ratio and resolution and prepares KIM inputs.
No perturbation solve is part of it.

## Phase 6 — Report and close

- [Writeups PR1](https://github.com/itpplasma/writeups/pull/1) owns the report; [ARTIFACTS](equilibrium/ARTIFACTS.md) owns its latest PDF and figure links.
- Deliver case definitions, rate/cost figures, cross-code tables and linked fixes
  in one LaTeX report; publish PDF/plots on slopbox. Close only at the gates below.

## Symbolics, numerics and tests (kept, but proportionate)

- **Symbolic (FortSym first, SymPy replay optional):** GS weak form, exact
  Solovev families, manufactured sources, large-A expansion, cylinder limits,
  COCOS maps. Each derivation feeds a test oracle or a generated kernel. A
  derivation used by neither is not written.
- **Numerics:** a convergence study with predicted rates is the standard
  evidence. Agreement between two unconverged codes is not evidence. Every
  run records commit, input hash, settings and wall time in the
  [registry](results/run_registry.json).
- **Tests (in the owning code):** exact-solution convergence-order tests
  (observed order within a tolerance of the prediction), sign/COCOS round
  trips, one regression test per fixed bug. Do not add tests that only check
  bounds of one frozen state, file hashes or document text.
- **Independent review:** only for claims that enter the report, and one
  review per claim.

## Rules against busywork (binding; mirrored in AGENTS.md)

- Every task names the Phase item and the figure or table cell it fills. A
  task that fills none is dropped.
- Stop investigating a *numerical* discrepancy once it is shown to converge
  correctly at the expected rate, or is below target. Do not prove its
  mechanism in detail. A non-numerical discrepancy (defect candidate) is
  followed until it is fixed with a PR or commit, whatever its size.
- No interval-arithmetic, IEEE floating-point or "certificate" packets unless
  Chris asks for one by name.
- No per-run admission paragraphs. A run is one registry entry with a one-line
  question. PLAN status changes by editing the phase table, not by appending.
- Fo/Fx/fpm tool defects go to their own repositories. No tool evidence here.
- Size budget per increment: one code change with its test, at most one new data
  directory, at most one status line here. If an increment needs more, ask first.
- Stop and report to Chris after each completed Phase item, instead of opening
  new side investigations.

## Completion gates

- Each case: inputs and signs match across codes; each code has a convergence
  curve with stated observed rate; converged codes agree within the target.
  Every remaining disagreement has a cause class in
  [ERRATA](equilibrium/ERRATA.md).
- Defects: every confirmed defect in the in-scope codes is fixed, with a test,
  as a fork PR (third party) or on main (own code). No unexplained
  non-converging difference remains.
- KIN6D: generic curved boundary, measured rates matching prediction,
  a posteriori estimator with measured effectivity, error-versus-cost position
  against the references stated for every case.
- Reproducible: scripts, inputs, run registry, report source. Generated plots and
  PDFs go on slopbox, not into Git.

Current gate assessment (2026-10-10):

| Gate | Status | Evidence or remaining condition |
|---|---|---|
| Each case: matching inputs, rates and agreement | Open | Phase 3 MARS failure; TC24 finite-reference transfer/accuracy; remaining solver target and reader gaps. |
| Defects fixed with behavioral regressions | Open | ERRATA retains unexplained candidates, held repairs and own-code fixes awaiting MR !20. Published scoped PRs alone do not close those gaps. |
| KIN6D accuracy and cost qualification | Partial | Generic P2/P3, expected rates, forward estimator and matched circular CHEASE costs delivered; nonlinear/inverse reliability, remaining current cost comparisons and TC24 accuracy remain open. |
| Reproducibility and publication | Met for delivered studies | Committed inputs/scripts/registry and report source; native latexmk build, source-row indexes and slopbox PDF/figures. |

## Authorities

- Cases: [CASE_CONTRACT](equilibrium/CASE_CONTRACT.md). Signs: plasma-sign-conventions.
  Discrepancies: [ERRATA](equilibrium/ERRATA.md). Runs: [registry](results/run_registry.json),
  [ops/RUNS.md](ops/RUNS.md). Figures: [ARTIFACTS](equilibrium/ARTIFACTS.md).
- Derivations: kin6d (own theory and implementation), writeups (third-party
  correspondence and the report). Upstream fixes: [UPSTREAM_PRS](review/UPSTREAM_PRS.md).
- Literature: [catalogue](equilibrium/references/README.md). Add Lee & Cerfon 2015
  (ECOM, arXiv:1409.3523), Pataki et al. 2013 (arXiv:1210.2113), Palha et al.
  2016 (JCP 316), Cerfon & Freidberg 2010, and VEQ (arXiv:2606.11821, pitfalls
  of unmatched timing comparisons).

## Following slices

1. **Perturbation:** admitted equilibria with simple linear 3D forcing; compare
   fields, spectra and coordinates, including VMEC++ fixed/free-boundary 3D.
2. **Transport:** the same cases and fields, separating model, collision and orbit
   approximations, then NTV (SFINCS, NEO-2, NEO-RT, POTATO, MARS, GPEC, Shaing,
   ARES, KIN6D).
3. **Full ITER benchmark:** converge to Xingting's case and prepare reviewed
   NTVTOK packages and draft messages.
4. **Uncertainty and sensitivity (UQ), once the pipeline reaches NTV:** propagate
   controlled equilibrium/export perturbations (field, q, |B| spectrum, profiles,
   boundary) through perturbation and transport to the NTV torque. Then replace
   the provisional accuracy targets with ones derived from the torque
   sensitivity.

- Later NTV contracts: [programme](review/CIRCULAR_NTV_PROGRAMME.md). Coordinates:
  [converter audit](review/COORDINATE_CONVERTER_BENCHMARK.md).
