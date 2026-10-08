# RMP model and implementation correspondence

This is a proposed extension of the source-correspondence programme. It specifies
coverage and evidence for complete resonant magnetic perturbation models; no new
derivation, implementation equivalence or solver result is certified here.
Programme order and case admission remain with the TC24 controller.

## Ownership

- Shared basic theory, reductions and independent analytical validation remain
  with kin6d under the existing programme ownership.
- Derivations of our own implemented models and numerics stay in each code's
  repository. This repository links them and owns their readable companions.
- Third-party source correspondence and readable model comparisons belong here.
  Pin external revisions and switches; do not insert an algebra dependency upstream.
- Signs and reversible convention maps belong in plasma-sign-conventions.
- Case inputs, execution and cross-code run evidence belong in TC24.
- Project-specific derivations, contracts, interpretation and evidence stay in
  the requesting project's repository. They are not copied into shared theory.

## Whole-model coverage

For every code variant, account for every source module and configuration branch
as covered, auxiliary with a specified contract, excluded from the selected build
with a reason, or unresolved. Catalogue the continuum equations and closures,
coordinates and boundary conditions, discrete residuals and quadrature,
interpolation, linearizations, solver/time-integration algorithms, stopping
rules, input defaults and switches, dependencies, and scientific diagnostics.
This is broader than checking a paper's final formula or comparing output plots.

The comparator catalogue includes KIM/KAMEL, MEPHIT, GPEC/SLAYER, TJ FourField,
EPEC, MARS-F/K/Q, JOREK, NEO-2, NEO-RT/POTATO and GORILLA. Include publication
models for GYRO, TM1 and Kaveeva–Rozhansky even where an implementation or exact
driver remains unavailable. Unavailable source receives explicit open coverage.

Each obligation records a stable ID, model/build/source commit, routine and
switch predicates, original paper version/page/equation, native and canonical
expressions, dimensions, assumptions, boundary/domain conditions, dependencies,
owner, independent oracle and evidence/review status. Preserve three separate
expressions: printed, independently derived and implemented.

## Symbolic and native evidence

Derive common limits only under explicit hypotheses. Cover geometry and metrics,
species/field closure, response kernels, matching, orbit theory, momentum and
energy balances, nonlinear evolution, and stability. Retain omitted terms and
boundary contributions. Incompatible closures are compared as different models.

A reproducible symbolic record needs assumptions, nonzero denominators,
integration/convergence conditions, branches and limit prescriptions. It must
reject sign, factor, metric, Jacobian, omitted-term or boundary-term mutants.
Independent engines and derivations should corroborate the algebra. Numeric
sampling supplements an identity check; it does not prove an identity or bound.

Native source correspondence adds independent kernel/residual/tangent oracles,
manufactured solutions, conservation checks and refined quadrature. Numerical
stability, consistency, convergence, finite precision and library/compiler
contracts remain explicit obligations. Exact local identities do not certify
the whole floating-point program or all build configurations.

Suspected paper/code discrepancies retain a minimal counterexample and possible
notation, transcription, branch, parameter or figure explanations until review.
Published numerical thresholds and empirical fits require data/input evidence;
symbolic algebra verifies their mathematical consequences, not their measured value.

## Existing shared material

Begin with the existing [GS correspondence](gs_solver_source_correspondence.md),
[variational bridge](gs_variational_bridge.md),
[admission obligations](equilibrium_admission_obligations.md),
[CHEASE primitive](chease_cubic_profile_primitive.md),
[VMEC++ constraint projection](vmecpp_constraint_projection_correspondence.md),
[VMEC++ hybrid lambda](vmecpp_hybrid_lambda_correspondence.md), and
[DESC source correspondence](desc_equilibrium_source_correspondence.md).
Use exact commit/content hashes and each record's current scope; these links
are reuse candidates, not fresh validation of all equilibrium or RMP modes.
Historical withdrawn-code records preserve their evidence and disposition.

## TC24 handover

The downstream comparison consumes TC24's owner-admitted cylinder case and
operator evidence. Keep its geometry oracle separate from an isolated sheared
response case, and the full-cylinder operator separate from local reductions.
Admit signs/units, forcing and observable conversions before a response campaign.
Direct-cylinder and asymptotic-torus routes require separate evidence.

Publish a scoped handover receipt with case/source hashes, reviewed identities,
operator and forcing contracts, outstanding obligations and destination owners.
A shared-file request is not an acknowledged handover. No simulation, solver
build or change to the active equilibrium programme is authorized by this note.

Chris&AI
