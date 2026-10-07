# Equilibrium admission: missing mathematical bridges

- Scope: axisymmetric static scalar-pressure benchmark; examined modes only. Exact source/case matrix and proof receipts: [TC24 closure audit](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/blob/plan/circular-tokamak-benchmark-20261007/review/EQUILIBRIUM_CLOSURE_MATRIX_20261007.md).
- Shared GS/ideal-MHD theory remains in KIN6D. This sidecar records obligations for [source correspondences](gs_solver_source_correspondence.md), [VMEC constraint](vmec2000_constraint_force_source_correspondence.md), [hybrid lambda](vmecpp_hybrid_lambda_correspondence.md), [DESC](desc_equilibrium_source_correspondence.md) and [GVEC](gvec_discrete_force_audit.md).

## Exact inference counterexample

- On x∈[−1,1], r=x³−3x/5. Its moments against 1,x,x² vanish, but integral r²=8/175>0.
- Therefore a finite projected residual of zero does not by itself bound the strong residual. This is an inference counterexample, not evidence that any specific equilibrium code produced r.
- A strong-error bound needs the actual approximation space, consistent quadrature/constraints, normalization/preconditioner, coercivity/stability, completeness and refinement/domain hypotheses.
- DESC weighted collocation least-squares stationarity has a separate issue: zero cost gradient need not mean zero residual. Its available Energy objective is not the executed ForceBalance objective.

## Signed flux and profiles

- For a geometric poloidal angle, q is winding average `(1/2pi)*integral dphi/dtheta dtheta`. Only a straight-field-line angle makes the local pitch equal to q.
- Kinematic circular-flux oracle: psi=C*r², constant F, R0>|r|. Local pitch `F/[2C(R0+r*cos(theta))]`; q=`F/[2C*sqrt(R0²−r²)]`; Phi=`2pi*F*(R0−sqrt(R0²−r²))`.
- Differentiating Phi gives `dPhi=2pi*q*dpsi`. The half-angle substitution yields integrand `2/[(R0+r)+(R0−r)*t²]`; integration over the real line gives the winding mean. This is not an arbitrary exact finite-R force-balanced equilibrium.
- An affine nonzero flux/unit conversion scales derivative inconsistencies by a nonzero reciprocal factor. It cannot turn inconsistent stored pprime/FFprime columns into consistent derivatives.
- Values, derivatives, endpoint conditions and invertible radial maps require separate admission. Matching knots or source labels is insufficient.

## Declared CQA10 symmetries

- Fixed geometry, alpha>0: psi/F/B/j→alpha times their original values; p→alpha²p; pressure derivative and FFprime→alpha times their original values. q is unchanged. CQA10 has p=0.
- Scaling from the predeclared full-flux target is an explicit input normalization. It is not chosen from comparison error; retain raw/native outputs and receipts.
- F-only reversal also reverses poloidal current, Phi and q, preserving psi/toroidal current/FFprime/force. Global B reversal instead leaves q unchanged.
- Prescribed pprime/FFprime/edge-F forward cases and p/iota/Phi inverse cases have different constraints. Source equivalence can be tested on the final native solution; it does not follow from copying its sampled profile map.

## Remaining code bridges

- KIN P1: distributional cell/jump/boundary current; a smooth recovered force is another representation.
- FreeGS: external one-shot masked linear equation versus staircase geometry/export derivatives; native Picard predicates were not executed in those ordinary cases.
- CHEASE: actual SI source/current/export selectors and endpoint derivatives; public/MARS share genealogy.
- VMEC family: auxiliary force and hybrid fields followed by Fourier projection/preconditioning/stopping; local exact stencil checks do not prove that complete composition.
- GVEC: constrained weak energy gradient, absolute coefficient norm and physical strong-force norm need a stability/completeness bridge.
- Exact-X loss of flux-chart rank does not make the real-space GS operator singular for R>0. Smooth-boundary discrepancies remain in scope; unsupported nested exact-X cases need disposition rather than impossible repair.
- Existing named-kind REAL readback limitation belongs to historical pinned KIN/FortSym proof generation. The owner repair has a separate 16/16 source-readback receipt; preserve both pins and link the repaired evidence.

- Native FortSym candidate: 20 exact conditional identities and five nonzero rejection witnesses, no probes or third-party upstream dependency. These verify selected algebra, not every source path, compiler or continuum error.
- Primary reading and external PDF hashes remain in the [TC24 reference catalogue](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/blob/plan/circular-tokamak-benchmark-20261007/equilibrium/references/README.md). Possession or a matching paper equation is not production-code validation.

Chris&AI
