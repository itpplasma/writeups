# Writeups revival plan

- Updated: 2026-10-07. Global programme order and completion gates belong to [TC24 PLAN](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/blob/plan/circular-tokamak-benchmark-20261007/PLAN.md).
- Active slice: axisymmetric equilibrium from a force-free cylinder and exact GS oracles to circular, finite-aspect-ratio, shaped and actual ITER TC24 cases.
- Solvers: kin6d, FreeGS, public CHEASE, MARS-associated CHEASE, VMEC++ and targeted original VMEC/DESC/GVEC lanes. Stop before perturbations/transport.

## Task order

1. Inventory existing writeups and archive/brain sources with exact partners, hashes, attribution, pairing status and duplicate relations.
2. Collect eligible source packages; keep unknown-rights/private material indexed in local receipts. Preserve archives and file notices.
3. Produce the readable GS derivation: signed field/flux, current and force balance, weak form/energy, profiles/constraints and cylinder/torus limits.
4. Link checked canonical theory/analytical fixtures in kin6d; retain each claim's assumptions and evidence status.
5. Add source correspondence for CHEASE variants, FreeGS, VMEC++, original VMEC, DESC and GVEC, including discrete equations, normalizations and code/literature errata.
6. Incorporate actual independent residuals/convergence and comparison interpretations; publish writeup PDFs/plots on slopbox with reproducible source/data.
7. Extend the same evidence structure in later perturbation and transport slices; NTV remains a catalogue and roadmap now.

## Ownership

- kin6d: shared basic theory, reductions and independent validation.
- Own codes: implemented-model and numerical derivations, retained generators and regressions.
- writeups: readable companions, historical intake and third-party source correspondence; solvers acquire no FortSym dependency.
- Sign repository: native sign/COCOS contracts and checked physical maps.
- TC24: case inputs, orchestration, evidence and cross-code comparison.
- FortSym/FortGen: generic algebra, derivation recording, runnable SymPy export and neutral computational interchange.

## Status

- GS companion and KIN/FreeGS/CHEASE source correspondence published; C0 RH-to-canonical embedding corrected with independent Cartesian checks.
- [GVEC discrete force/sign bridge](theory/gvec_discrete_force_audit.md): 16 exact local identities; weak projection, quadrature, constraints and stopping norms explicitly separated. Full discrete convergence proof remains open.
- GVEC, DESC and original VMEC source ledgers published. DESC retains ten exact native FortSym identities; broader discrete-solver equivalence remains unproved.
- Smooth circular A10 constant-q matches DESC/GVEC/original VMEC/VMEC++ at 216 physical points (max Bpol RMS difference 0.0254%). Native convergence, reconstruction and full refinement admission are separate.
- Original VMEC TC24 storage repair now converges with unchanged input; physical force/gradp remains about 1.63. Odd-mode reconstruction and CHEASE thin-flux current defects have owner reviews.
- Original TC24 has a true X-point; executed regularized boundaries avoid it. Source correspondence distinguishes this coordinate/model limit from other failures.
- Ordinary benchmark: [benchmark_vmec](https://github.com/itpplasma/benchmark_vmec), physical-input/provenance issues #2/#3. mhd-differentiable owns complementary derivative/optimization checks.
- Physics admission/next experiments belong to TC24 PLAN/ERRATA; literature candidates remain provisional.
- Existing repository: 43 tracked files at revival base 22b60a4b89a7d2822fcd6315abdd67d954c36206; numerical Hamiltonian examples, no existing CAS replay suite found.
- Targeted intake: 19 source families across the geometry and NTV inventories. Same-stem/co-located partners do not establish equation correspondence.
- Collected: libneo's licensed EFIT/Boozer/Hamada writeup and near-axis symbolic source; Chris's Boozer/Hamada draft. Fresh replay/accuracy qualification remains open.
- Source inventories cover 92 file receipts, including duplicate paths/copies and rendered references. These are not 92 independent derivations.
- Historical Hamiltonian/nonlinear notebooks, Shaing comparisons and NEO-2 collision writeups are indexed. Current private proof collections remain linked at their owners.
- No numerical equilibrium/NTV result is promoted by collection alone.

## Artifacts

- Upload new plots and rendered writeup PDFs to slopbox; never commit generated plots/PDFs.
- Keep producing source/scripts, input/numerical data, source/command hashes and timestamped artifact links.
- Slopbox links expire after three days. Regenerate and re-upload from retained evidence.
