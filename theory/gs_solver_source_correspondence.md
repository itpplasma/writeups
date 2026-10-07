# Grad–Shafranov: examined source correspondence

- Scope: static axisymmetric scalar-pressure equilibria; fixed boundary. No flow, anisotropic pressure, free-boundary qualification, perturbation or transport claim.
- Shared theory and independent analytical checks: [KIN6D derivation](https://github.com/itpplasma/kin6d/blob/5d75dfc/theory/derivations/grad-shafranov.md). The cited derivation includes the C0 orientation correction.
- Physics/constraints: [TC24 case contract](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/blob/plan/circular-tokamak-benchmark-20261007/equilibrium/CASE_CONTRACT.md). Numerical disagreements and closure gates: [equilibrium errata](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/blob/plan/circular-tokamak-benchmark-20261007/equilibrium/ERRATA.md).
- Conventions: [axisymmetric sign contract](https://gitlab.tugraz.at/plasma/proj/plasma-sign-conventions/-/blob/main/docs/AXISYMMETRIC_COCOS_CONTRACT.md). Native arrays remain native; comparisons apply the declared map, never a fitted sign.
- These are examined routine paths, not proofs of every code/mode. Exact file hashes and this document's base/patch digest are in `gs_source_correspondence_manifest.json`.

## Common physical equation and conditions

- SI; physical phi is CCW viewed from +Z, `(e_R,e_phi,e_Z)` is RH. Canonical theta is CCW in `(R-R0,Z)`, so `(r,theta,phi)` is LH.
- Canonical signed flux per radian: `B=grad(psi)×grad(phi)+F grad(phi)`, `BR=-psi_Z/R`, `BZ=psi_R/R`, `Bphi=F/R`.
- `Delta_star psi = psi_RR - psi_R/R + psi_ZZ = -mu0 R^2 pprime - FFprime`; `mu0 jphi=-Delta_star psi/R`; `mu0 jpol=Fprime Bpol`.
- For smooth surface functions, `j×B=-(Delta_star psi+FFprime) grad(psi)/(mu0 R^2)`. Equality to `grad(p)` gives GS away from critical points; the axis needs a regular limit.
- With fixed Dirichlet trace and zero-boundary test function v: `integral grad(psi)·grad(v)/R = integral (mu0 R pprime+FFprime/R) v`.
- Stationary functional: `integral [|grad(psi)|^2/(2R)-mu0 R p(psi)-F(psi)^2/(2R)] dR dZ`. This is not a full dynamical MHD energy principle; nonlinear convexity/branch uniqueness are unproved.
- Forward cases prescribe boundary, derivative laws and edge p/F. Current, axis flux and q are outputs. Prescribed q requires a different inverse constraint; `q_seed`, `QSPEC` and an actual q profile are not interchangeable.

## KIN6D: native weak equation and exports

- Pin: [`f26b8df7969484152e54ad495d0231cc26b8c2ad`](https://github.com/itpplasma/kin6d/tree/f26b8df7969484152e54ad495d0231cc26b8c2ad).
- `src/grad_shafranov.f90::initialize_gs`: FortFEM polygon mesh/P1 basis, physical `(R,Z)` gradients, three barycentric Gauss points `(2/3,1/6,1/6)` and permutations. Element stiffness is quadrature of `grad(Ni)·grad(Nj)/R`; the supplied polygon is its boundary.
- `solve_gs`, `solve_gs_profiles`: constant-source equation or relaxed Picard evaluation of derivative laws at quadrature psi. FortNum matrix-free preconditioned CG solves the interior equation; Dirichlet degrees are constrained. Relative weak residual is not a continuous curl/force error.
- `gs_profile_value`, `gs_profile_integral`: ascending signed-psi knots, piecewise-linear derivatives, exact segment primitives; constant derivative extension outside the table. This is the executed law, including extrapolation.
- `app/grad_shafranov_demo.f90`: reconstructs `p=p_edge+integral_edge^psi pprime` and `F=sign(F_edge)*sqrt(F_edge^2+2 integral_edge^psi FFprime)`. Rejects nonpositive square or zero-edge branch; retains received p/F columns separately. Nodal pressure/F interpolation in a comparison is an output representation, not the executed derivative law.
- Native NetCDF has nodal psi, pressure/F, connectivity, centroid physical fields and weak residual. `write_gs_mesh` exports node/triangle tables; profile companion exports the executed p/F samples. Signed q/current/total-flux comparison is independently reconstructed by TC24 adapters, not a native GS diagnostic.
- `gen/gen_grad_shafranov.f90` generates physics primal/JVP/VJP leaves. Fixed-geometry constant-source tangent/adjoint solves are implemented; nonlinear/profile/shape implicit derivatives remain unsupported.
- Native physical-point route uses affine P1 psi/gradients. Smoothed gradients, bicubic grids and VMEC field reconstruction have different error budgets; compare their provenance explicitly.

## FreeGS: native finite differences versus external LCFS adapter

- Base pin: [`5b41fe5565ff8077bf8139051c80c69416fc9b86`](https://github.com/freegs-plasma/freegs/tree/5b41fe5565ff8077bf8139051c80c69416fc9b86). Fork q repair: [`378763074204ceee2ef5bfd6b62309e07bc1de55`](https://github.com/itpplasma/freegs/tree/378763074204ceee2ef5bfd6b62309e07bc1de55), [PR 1](https://github.com/itpplasma/freegs/pull/1).
- `freegs/gradshafranov.py::GSsparse` implements the physical rectangular-grid operator. Radial neighbours have weights `1/dR^2 ± 1/(2R dR)`, vertical neighbours `1/dZ^2`, diagonal `-2(1/dR^2+1/dZ^2)`. Outer rows are identity. This is second-order centred Delta_star, not a bicubic/variational solver.
- `GSsparse4thOrder` is another native stencil. Our recorded masked-LCFS cases use order 2; no order-4 accuracy claim follows from its presence.
- `equilibrium.py::Equilibrium.solve` (436–493): computes profiles/Jtor when needed, applies native boundary callback, sets RHS `-mu0 R Jtor`, copies outer boundary values, calls `_solver`; computes plasma current by nested Romberg quadrature of Jtor.
- `jtor.py::ProfilesPprimeFfprime.Jtor` (461–502): finds critical points/core, clips normalized psi to `[0,1]`, uses `Jtor=R pprime+FFprime/(mu0 R)`, and applies core mask when present. Callable inputs have normalized-flux arguments but return derivatives with respect to physical psi; no missing flux-span factor may be inferred from argument names alone.
- Native `plasmaBr`, `plasmaBz` use `-psi_Z/R`, `psi_R/R`; `Equilibrium.Br/Bz` add machine coil fields. `_updatePlasmaPsi` installs SciPy `RectBivariateSpline`; field derivatives and critical-point diagnostics inherit that interpolation.
- `critical.find_safety` (460–560 in fixed source) uses positive arc length and `|Bpol|`: `q=integral F dl/(2pi R^2 |Bpol|)`. Its sign follows F alone, not oriented poloidal circulation. The fixed-boundary fallback repair does not repair general signed-q semantics.
- Our curved-LCFS cases replace outside-polygon rows by identity and use external Picard/source callbacks. Staircase Dirichlet geometry and exact derivative primitives belong to TC24 adapters; they are not native arbitrary-LCFS capabilities.
- Older circle/shaped executions used base 5b41fe55 plus the retained q patch; E5 LCFS runs used committed 37876307. Execution manifests, not later source promotion, identify each binary.

## CHEASE: native Hermite equation, profiles and geometry

| Lane | Exact source | Examined paths |
|---|---|---|
| Public | [EPFL fb4636631ac6be62eefc73b1a420508a40e7ea13](https://gitlab.epfl.ch/spc/chease/-/tree/fb4636631ac6be62eefc73b1a420508a40e7ea13) | `src-f90/{setupa,setupb,curent,matrix,pprime,ppspln,surface,psibox,cocos_module}.f90` |
| MARS-associated | [8824bb18e1514b4a27f6357d5fe859d4fe690542](https://github.com/gafusion/MARS-Q/tree/8824bb18e1514b4a27f6357d5fe859d4fe690542/CheaseMerge) | `CheaseMerge/chease.f::{SETUPA,SETUPB,SURFACE,PPRIME,PPSPLN,PSIBOX}` |

- Native CHEASE coordinates/normalizations differ from canonical SI. COCOS2→3 in the executed lane keeps psi, pprime, FFprime and reverses toroidal chart, F, q and Iphi. Public `SIGNB0XP=-1` supplies the canonical-F-positive control; MARS native positive TMF maps to canonical F-negative. Do not reverse F alone to declare a matched problem.
- Public `cocos_module.f90::COCOS`, `COCOS_values_coefficients` encode sign/2pi factors; `psibox` exports physical lengths. COCOS constants do not establish that an arbitrary imported tuple is internally consistent.
- Native direct-source mode `NSTTP=1,NPROFZ=0`: `CURENT` calls `PPRIME/PRFUNC` and forms normalized `Jphi=-R*pprime-TTprime/R`. The negative sign is native convention/normalization, not a discrepancy with FreeGS canonical current. Profile/current-constrained branches differ; no audit of every `NSTTP` mode is claimed.
- Public `SETUPA` calls `BASIS2`, forms transformed angular/radial gradients and assembles Gaussian weighted products with `ZCOEF=ZW*RSINT/R`; `MATRIX` calls `SETUPA` and banded LDLT. `SETUPB` evaluates prior-iterate Hermite psi, calls `CURENT`, and assembles its negative weighted source. These examined paths match the fixed-boundary weak/Picard architecture, not a compiler-level equivalence proof.
- MARS monolithic anchors: `SETUPA` 6680, `SETUPB` 6988, `SURFACE` 9466, `PPRIME` 17043, `PSIBOX` 21147. Assembly/source genealogy is shared with public CHEASE; they are one algorithm family for independence assessment.
- `NPPFUN=4` calls cubic `PPSPLN`; public pressure paths additionally depend on `NPP`, current/profile-coordinate selectors. `NFUNC=4` is tabulated PRFUNC input. Cubic derivative profiles on normalized flux are not our exact piecewise-linear law on absolute signed psi.
- Executed forward controls use `NCSCAL=4` to preserve source profiles; `QSPEC` is not silently promoted to a q constraint. The physical source/F normalization and each deck are retained in TC24 manifests.
- E5 needs a source-map fixed point as the solved psi span changes. Matching knots alone does not match between-knot laws; executed NISO/selector/output sampling and derivative discrepancies remain explicit admission gates.

## q, current and output routes must remain separate

- CHEASE `SURFACE` differentiates Hermite coefficients through basis routines. It forms `ZINT2=rho*boundary_radius/(R*psi_sigma)`, Gauss-integrates CHIO, then `QPSI=TMF*CHIO/(2pi)` (MARS line 9827). Native q therefore retains a signed derivative route; it is not the FreeGS unsigned-arc estimator.
- Current-source and surface-integral paths in `CURENT`, `SETUPB`, `SURFACE` have been inspected. A complete SI current normalization/output correspondence for every export mode has not been proved; use per-run native Iphi and declared conversion alongside independent Ampere/current integrals.
- `PSIBOX` constructs rectangular exports from the native FEM solution. Public exterior selector `NEQDXTPO=1` is linear; selector 4 uses derivative-based cubic continuation. Changing that selector can change reconstructed diagnostics while native equilibrium/q remain unchanged.
- Public shifted-default-box defect: a dimensional/native-length mix moved the export box. The [fork PR 1](https://github.com/itpplasma/chease/pull/1), commit `9ac358d`, fixes geometry; independent shifted analytical controls fail before/pass after. It does not establish improved continuous GS accuracy.
- Public thin-flux postprocessing defect: GLOQUA uses an absolute 0.001 cutoff, selecting too few spline knots in A20/A40; bundled INTERPOS clears a failed factorization status. [CHEASE #2](https://github.com/itpplasma/chease/pull/2) and owner [INTERPOS !1](https://gitlab.tugraz.at/plasma/libs/interpos/-/merge_requests/1) repair the selector/error path. Six controls retain identical psi/profile/q; current headers match the exact constant-FFprime area integral after repair. Interior current/li accuracy remains open.
- MARS E0 LCFS endpoint controls: independent field-gradient integration reproduces native q error, so isolated q-table assembly is insufficient. At NS256 the endpoint worsens while interior improves. Last-cell derivatives/boundary/export precision and tolerance remain open.
- KIN native P1 gradients, FreeGS/CHEASE bicubic exported-grid gradients and native VMEC fields are distinct representations. Common-point error is neither truth-relative error nor a substitute for each code's mesh/boundary convergence.

## C0 orientation erratum: retain native values, qualify their meaning

- Native Gold–Hoyle C0 is a **RH straight cylinder**: axial period `2pi R0`, `Btheta_RH=k*r*Bz`, `q_RH=1/(k R0)`, `dpsi_RH/dr=R0 Btheta_RH`.
- If z aligns physical +phi, canonical CCW-RZ poloidal angle satisfies `theta_c=-theta_RH`: `Btheta_c=-Btheta_RH`, `psi_c=-psi_RH` up to gauge, `F=R0 Bz`, `q_c=-q_RH`. Thus retained native +1.5 means canonical -1.5 in this straight-limit alignment.
- Independent basis derivation: `e_r=cos(theta_c)e_R+sin(theta_c)e_Z`, `e_theta_c=-sin(theta_c)e_R+cos(theta_c)e_Z`, `e_r×e_theta_c=-e_phi`. This establishes handedness without reading a q header or fitting a field sign.
- Physical `curl(B)=alpha B`, `alpha=2k/(1+k^2 r^2)`, is invariant under the chart change. RH curl formulas applied to LH components give a spurious sign. Finite-R curvature is a different physical model.
- Corrected KIN theory and readable companion accompany this file. Native arrays/generator/CAS identities stay unchanged. Cartesian orientation/field/curl numerical check is retained in KIN `test/check_cylinder_orientation.py`; it is not a ninth CAS proof.

## Literature correspondence and evidence status

| Primary source | Examined bridge | Status / next review |
|---|---|---|
| [Lütjens, Bondeson, Sauter (1996), DOI 10.1016/0010-4655(96)00046-X](https://crppwww.epfl.ch/~sauter/chease/Lutjens_CHEASE_CPC96_OS.pdf) | §2.1 static isotropic GS; §5.2 equations 26–28 weak equation, Hermite expansion, Gauss quadrature and Picard | Public SETUPA explicitly cites eq.27; examined source architecture agrees. Paper stopping norm is not automatically the executed modern deck's criterion. Every selector and SI-normalization bridge remains unproved. |
| [Sauter, Medvedev (2013), DOI 10.1016/j.cpc.2012.09.010](https://crppwww.epfl.ch/~sauter/cocos/Sauter_COCOS_Tokamak_Coordinate_Conventions.pdf) | Separate toroidal/poloidal handedness, flux sign and 2pi factors | Public COCOS module cites its transformation rules. Individual physical ingress and polarity gates are required; a global COCOS change cannot fix inconsistent received derivatives. |
| [Vandas, Romashets (2017), DOI 10.1051/0004-6361/201731412](https://doi.org/10.1051/0004-6361/201731412) | Uniform-twist cylindrical reference and toroidal distinction | Gold–Hoyle identities are checked directly in KIN. The native-to-canonical embedding correction is our explicit chart derivation, not a claimed paper erratum. |

- Literature PDFs stay in the external archive; this document references/hashes source, imports no third-party routines or private material, and inserts no FortSym dependency upstream.
- Eight registered native FortSym identities use exact zero decisions under nonzero-denominator/domain assumptions. They prove the selected algebraic identities, not weak-form boundary arguments, existence, uniqueness, all code paths or compilers.
- Weak functional, integration by parts, axis limits, flux map and embedding argument are hand derivations. Surface-map/Cartesian/PDE-refinement tests are numerical evidence; no formal-proof claim.
- Existing independent controls include exact polynomial/log operators, native Solovev refinement, Cartesian field/orientation checks and shifted-box oracle. Large native residual reduction alone is not physical admission.
- Confirmed defects: FreeGS fixed-boundary q fallback, public CHEASE dimensional box/thin-flux current postprocessing, INTERPOS lost factorization status, original VMEC axis-storage alias, and unspecified C0 embedding. No demonstrated error in the cited physics papers is asserted here.
- Separatrix scope: at an X-point grad(psi)=0, so a nested flux-coordinate inverse loses rank. The physical GS operator stays regular for R>0 and smooth sources. Exact-X topology and a regularized inner/Fourier boundary are distinct mathematical problems; retain both before interpreting convergence failures.
- Open questions: signed-q handling for reversed poloidal circulation; complete CHEASE normalization/constraints and nonlinear stopping paths; absolute-psi/source-spline equivalence; near-axis/endpoint derivatives; current/flux/force reconstruction; nonlinear branch uniqueness.
- Review both outlier-defect and shared-error hypotheses. Public/MARS CHEASE share genealogy; mapped VMEC profiles share source reconstruction; matching p/F laws share input assumptions. Count independent operators/oracles, not agreeing votes. Closure belongs to TC24 ERRATA.

Chris&AI
