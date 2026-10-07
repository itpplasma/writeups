# GS and nested ideal-MHD variational correspondence

- Shared derivation belongs in [KIN6D](https://github.com/itpplasma/kin6d/blob/main/theory/derivations/grad-shafranov-variational-bridge.md), with [native expression checks](https://github.com/itpplasma/kin6d/blob/main/test/test_gs_variational_identities.f90).
- The scalar GS stationary functional has a negative F-squared term. It is not the magnetic energy used by nested-surface MHD solvers.
- The axisymmetric bridge proceeds through admissible ideal material variations, physical force balance and the signed GS reduction.
- Weak boundary terms, nonlinear existence/uniqueness, complete variation spaces and discrete solver equivalence require their own evidence.
- Prescribed p-prime/FF-prime, prescribed iota and prescribed enclosed-current profiles define different constraint problems. Matching profile knots alone is insufficient.
- Fresh native evidence: fourteen exact local/source identities, zero probes; wrong physical-field orientation and weak source weight are independently rejected.
- Supported source readback checks actual KIN generated gs_source/gs_field routines. The pinned FortSym named-kind REAL conversion gap remains explicit; no primitive readback proof is claimed.
- This sidecar supplies links and code correspondence, without installing FortSym in third-party solvers.

| Native lane | Source correspondence |
|---|---|
| KIN6D, FreeGS, public/MARS CHEASE | [GS ledgers](gs_solver_source_correspondence.md) |
| Original VMEC and VMEC++ ancestry | [VMEC ledger](vmec2000_equilibrium_source_correspondence.md) |
| DESC force collocation versus Energy objective | [DESC ledger](desc_equilibrium_source_correspondence.md) |
| GVEC nested variation and B-spline discretization | [GVEC ledger](gvec_equilibrium_source_correspondence.md), [discrete force audit](gvec_discrete_force_audit.md) |

- Per-case comparison/admission remains in [TC24 PLAN](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/blob/plan/circular-tokamak-benchmark-20261007/PLAN.md); continuous force, flux, q, current and boundary refinement remain separate from the symbolic identities.
