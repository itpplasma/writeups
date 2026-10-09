# ITER benchmark programme

- Updated: 2026-10-09 (rewritten by Chris&AI after review of the 2026-10-06..09
  GPT Sol campaign). The previous 375-line plan with its run-by-run admissions is
  commit `4ff823e1a:PLAN.md`; it is historical, not instructions.
- Final goal: a reproducible full ITER NTV benchmark with Xingting and colleagues,
  built bottom-up so that every number downstream is understood.
- **Active slice: axisymmetric equilibrium only, not complete.** Stop before
  perturbation and transport.
- Historical ITER torque results: [frozen status](review/ITER_STATUS_20261007.md),
  [merge review](review/MERGE_REVIEW.md), [upstream PRs](review/UPSTREAM_PRS.md).

## Goal of the equilibrium slice

The downstream NTV codes consume B, q, flux labels and flux coordinates. This
slice must deliver two things, and nothing that does not serve them:

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
  1. Write a minimal reproducer and a failing behavioral test.
  2. Make the smallest fix.
  3. Check that the test fails before the fix and passes after it, and that
     the affected convergence result is now correct.
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

## Status carried over (established, useful)

- Case contract, selectors and profile models: [CASE_CONTRACT](equilibrium/CASE_CONTRACT.md),
  [cases.json](equilibrium/cases.json), [PROFILE_MODELS](equilibrium/PROFILE_MODELS.md).
  The signs and COCOS maps are checked, with 128 symbolic identities in
  [plasma-sign-conventions](https://gitlab.tugraz.at/plasma/proj/plasma-sign-conventions).
- Solvers: KIN6D, public CHEASE, MARS CHEASE, VMEC++ and DESC. FreeGS, original
  VMEC and GVEC have been handed upstream and stay withdrawn unless Chris readmits them.
- KIN6D main `fa5c388` (2026-10-09): generic curved boundary with P2 and P3. P3 orders
  psi 4.0, B 3.2–3.3; all PLAN targets met at E0 A3 n=48 (2.9k DOF, 0.03 s solve)
  and Cerfon n=96 (17k DOF, 0.33 s), versus public CHEASE NS=NT=64/128 at 6.3/20 s.
  P2 needs n=576 (10–22 s). Fixed: shaped CG stagnation (Cerfon n=384 4.7 s), axis
  recovery by local quartic fit. Recovered-flux majorant effectivity 1.03–1.05 (P2).
  kin6d `fa5c388`: q/Phi/volume readback now converges with the mesh (q orders
  P2 2.1, P3 2.7; P3 n=384 q 2.3e-9) and costs 12–15% of the finest P3 solve.
  Inverse-q branch `3a73515` is not yet on main.
- CHEASE: build/run of both variants. Fork PRs cover the box-unit export,
  smoothing, the 64-bit band and folded ordering (NS128/NT512 157 s → 31 s).
  Finest-grid under-relaxation was found and controlled (RELAX=0). An export
  precision floor and a boundary spline floor were measured for A10–A40.
- VMEC++: tcon0 and resolution dominate the TC24 force residual (1.17 → 0.063
  force/grad p). Radial convergence is first order (consistent with Panici 2023).
- DESC: refinement reduces the force residual. Accepted-step callbacks and the
  helical-basis sign fix are on the fork.
- Exact references exist: E0 Solovev polynomial and logarithmic families, and the
  periodic cylinder (Gold–Hoyle, Lundquist).
- What does **not** exist yet: a single convergence/cost study per case with all
  five codes on identical problems. This is the main gap.

## Phase 0 — Dechurn (do first; time-box about 2 working days)

Purpose: make the repository and the codes readable again before new work.
Nothing is lost: git history and sealed archives keep every byte. Produce a
reviewable manifest first; Chris approves moves and deletions in bulk.

| ID | Item | Action | Done when |
|---|---|---|---|
| DC-1 | PLAN, HANDOFF, README, ARTIFACTS | This plan replaces the old one. Fold HANDOFF into one short "published revisions" table; fix stale README (FreeGS/GVEC listed as active) | Each file under ~150 lines and contradiction-free |
| DC-2 | ERRATA (118 entries, 837 lines) | Keep demonstrated defects and explained differences that change a number above target. Move the rest to an archived appendix. One paragraph per entry | Under ~40 live entries, each with cause class and fix/PR |
| DC-3 | `review/` (94 files, 161 MB) | Archive the dated 2026-10-07 equilibrium review files, JSON receipts and decision TSVs. Keep the owners named in AGENTS | Live `review/` lists only owners of current facts |
| DC-4 | `research_notes/` (2,364 files) | Move Fo/fpm/CMake tool evidence (~2,000 files) out: to the fo repo issues or a sealed tarball. Condense the weak-formulation notes into one derivation note per code | No tool-debugging evidence in this repository |
| DC-5 | `equilibrium/data/` (162 dirs, 1.7 GB) | Classify each dir as *feeds a planned figure*, *raw run worth keeping* or *superseded diagnostic/certificate replay*. Keep the first two. Tar and LFS-archive the third with one index line each, including `solovev_certified_budgets_20261009` | Index file. Live dirs map to Phase 1–5 items |
| DC-6 | `equilibrium/adapters/` (~18k lines Python) | Keep one adapter per code (run + export to the common format) plus one common comparison module. Archive one-off assess/observer/budget scripts | Adapters per code, shared metrics module, tests pass |
| DC-7 | KIN6D code | Replace the Solovev-specific geometry with a generic curved-boundary map (Phase 1). Remove certificate-only tests that check bounds of one frozen state rather than behaviour. Keep exact-identity and convergence tests | kin6d has no case-specific geometry in `src/` |
| DC-8 | Forks and PRs | Re-check open fork PRs (CHEASE 1–3+, DESC 1–2, VMEC++). Each PR must fix one defect and include a test that fails without the fix. Close superseded PRs and split or squash stacks. Start the defect ledger | `review/UPSTREAM_PRS.md` current |
| DC-10 | Open GitLab MRs | !15 (MARS torque evidence): main merged in on 2026-10-09 (`f047adf03`), conflicts resolved to the curated main. Classify its ~2,400 branch-only files (1.4M lines) as keep / archive / drop against the curated main, then merge the remainder or close it as superseded. !4, !9, !13, !14, !16, !17, !18 (August) conflict in PLAN/registry or are stale: merge main, or close as superseded with a note | Every open MR is merged, rebased or closed with a reason |
| DC-9 | Brain | One concise project-status section replaces the accumulated campaign bullets | Brain note matches this plan |

Run DC-5 through the `storage-triage` manifest pattern: list, classify, get
approval, then move. Do not delete raw native outputs of runs that feed a figure.

## Phase 1 — Exact-solution convergence and cost (core milestone)

Question: how does each code's error depend on resolution and wall time on
problems with exactly known solutions, and does KIN6D reach the observed rate
that theory predicts?

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
- Preliminary [results](equilibrium/phase1/results_prelim/): VMEC++ Bpol L2 order
  0.9–1.2 (first order, as predicted), finest 1.3e-4 (E0 A3) / 3.2e-4 (Cerfon) at
  24–56 s; near-axis maximum error converges slower (open).
  DESC: exponential on E0 (1.2e-8 at A10; 1.7e-6 at A3, 200 s); shaped Cerfon
  irregular, 3.6e-3 at L=M=14 (defect candidate, open).
  CHEASE public/MARS: Bpol order 3.2–3.5, psi 4.8; all targets met at NS=NT=64
  (E0 A3, 6.3/2.9 s) and 128 (Cerfon, 1.7e-6/2.2e-6 Bpol, 20/15 s).
- KIN6D work needed:
  1. **Generic curved boundary:** isoparametric P2 (optionally P3) with boundary
     nodes on a parametrized curve R(t), Z(t) (analytic, Miller or spline
     LCFS). This replaces the Solovev-specific maps. Literature: Palha et al.
     2016 (p+1 rates on curved meshes), Howell & Greenwald 2014.
  2. Field readback: B and q from the FE solution on flux contours, with q
     convergence measured.
  3. **One a posteriori estimator** (equilibrated flux / Prager–Synge,
     Repin–Sauter–Smolianski already in Zotero) computed inside KIN6D. Its
     effectivity index is measured on both exact cases. This estimator is
     the error budget for later cases without an exact solution. Rigorous
     interval/IEEE certification is not required.
  4. Timing: total wall time including mesh, assembly and solve. Profile only
     if KIN6D is slower than the best reference at matched error.
- Deliverable: two figures per case (error vs DOF and error vs wall time, all
  codes), a rate table, and a short section in the report. Template: Lee &
  Cerfon 2015 (ECOM vs CHEASE, q error at fixed run time).

### End-to-end accuracy (every phase; Chris, 2026-10-09)

- [Phase 1 export results](equilibrium/phase1/results_export/README.md): two-resolution CHEASE public/MARS and KIN6D P3 now include actual GPEC/DCON and full NEO-2 vectors/Jacobian (NEO-2 PR193); native MARS Fourier/Hamada measured on both exact cases, with second-order Hamada metric error. VMEC++/DESC downstream converters remain unused.

Downstream codes never read native solutions. They read exported files. Each phase
therefore also measures the accuracy that arrives at the consumers, not only native
accuracy.

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

- [Eight-case comparison and export study](equilibrium/phase2/results/README.md) delivered; three VMEC++ target gaps and the stated consumer exclusions remain.
- KIN6D P3 reference error (Richardson, Bpol) 7e-9 to 7e-8; majorant/Richardson 1.3–3.0. Shafranov-shift and q-axis remainders scale as A^-3/A^-4 as predicted. Cost: KIN6D P3 needs ~2 s per case almost independent of difficulty (mesh, solve, estimator, export, readback), public CHEASE 1.2–2.5 s: the fixed per-run overhead, not the solve, is the next KIN6D speed target.

Question: do all codes converge to the same equilibrium for E1 (zero beta) and
E2 (finite beta) at A=40, 20, 10 and E3 at A=3.1, and does the result
match large-aspect-ratio theory?

- Self-convergence per code (Richardson estimate of the error at reference
  resolution) plus the KIN6D estimator, then cross-code difference at converged
  resolution. Cross-code differences above target need a cause.
- Physics check: Shafranov shift and q(0) versus the analytic large-A expansion
  (FortSym derivation), with the expansion error scaling as 1/A.
- Reuse existing E1/E2 runs where their inputs match the frozen case. Rerun only
  what the convergence curves need.

## Phase 3 — Inverse (prescribed-q) cases

Question: given boundary, p and q (instead of FF'), do the codes return the same
F, current and fields?

- Integrate KIN6D `3a73515` into main, then qualify by convergence on E1/E2 constant-q
  and an analytic q-profile case built from Phase 1 Solovev q(psi).
- CHEASE public and MARS run in their native q modes. The MARS prescribed-q
  failure (negative TMF²) is fixed only if a small, demonstrated defect
  remains. Otherwise it is documented as a variant limitation.
- VMEC++ with a prescribed iota or current profile, mapped through the checked
  psi↔Phi relations.

## Phase 4 — Shaped and TC24

- TC24 [inputs are pinned](equilibrium/phase4/tc24/README.md); the forward/export study is blocked by KIN6D's unsupported curved-P3 profile-table path.
- [E4 two-law study](equilibrium/phase4/results/README.md): five codes × four resolutions and 24 consumer chains delivered; VMEC++ target gaps and finite-beta DESC stopping remain documented.

Question: the same convergence and cross-code study on the E4 Miller boundary
and on TC24 with one common smooth boundary just inside the separatrix.

- TC24 source equilibrium inputs, COCOS and profile consistency are pinned once
  (EQ-D04). The X-point itself is out of scope for nested-flux codes.
- Output: the equilibrium export package the perturbation slice will consume,
  with its measured accuracy.

## Phase 5 — Periodic cylinder (can run alongside Phase 1)

Gold–Hoyle and Lundquist exact references. KIN6D and the other codes run the
exact cylinder route where one exists, or a finite-A limit at fixed axial period.
One figure: error versus aspect ratio and resolution. This prepares KIM inputs.
No perturbation solve is part of it.

## Phase 6 — Report and close

- One LaTeX report (writeups repository): case definitions, rate and cost
  figures, cross-code tables, errata summary, code fixes with PR links. Upload
  the PDF and plots to slopbox.
- Close the slice when every case has a converged result or a documented
  domain/model limitation, and the KIN6D accuracy/cost position is stated.

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
