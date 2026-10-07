# DESC TC24 cubic-inverse closure checks

- Scope: axisymmetric isotropic `ForceBalance`, fixed smooth Fourier boundary, prescribed p/iota/signed full toroidal flux; F and current are outputs.
- Execution pin: DESC 0.17.3 `fcc29be36f0b36b1b667df4b1f8891a9b633f5d1`, with the separately sealed accepted-step callback backport. The callback observes copies; no optimizer is reimplemented in TC24.
- Checked theory: [source correspondence and native algebra](desc_equilibrium_source_correspondence.md). Basic GS theory/independent fixtures belong to kin6d.
- Status: both first checkpoint repeats reached cap160; no native-convergence claim. Same-resolution warm repeats again reached cap160; radial repeats reached the wall cap with complete accepted states. None meets native convergence.

## Continuous field and signs

- Native rho=sqrt(s_tor), poloidal theta clockwise; physical toroidal phi is CCW.
- Common CCW-poloidal iota reverses sign in DESC. Signed full toroidal flux is retained.
- Canonical edge-zero poloidal flux:

\[
\psi_c(s)=-\frac{\Phi}{2\pi}\int_1^s\iota_D(u)\,du.
\]

- Store profiles as literal quadratic-endpoint-clamped piecewise cubics in s_tor. A spline in rho, natural endpoints or zero-slope endpoints define different inputs.
- Native spectral R/Z/lambda and their derivatives are evaluated directly. No VMECIO fit or shared imported state supplies an independent solver vote.
- Physical force: cylindrical curl(B)/mu0 × B − gradp. Retain inverse-map errors, domains and fixed/reference normalization separately.

## Native collocation versus physical force

| Quantity | Pinned code |
|---|---|
| Radial coefficient a=F_rho | `compute/_equil.py::_F_rho` |
| Helical coefficient h=F_helical | `compute/_equil.py::_F_helical` |
| Radial dual vector u=grad(rho) | Native metric/dual-basis routines |
| Helical vector v=−B^zeta e^theta+B^theta e^zeta | Negative of executed `compute/_equil.py::_e_sup_helical` |
| Full force a u+h v | `compute/_equil.py::_F` |
| Raw residuals a\|u\|J, h\|v\|\|J\| | `objectives/_equilibrium.py::ForceBalance.compute` |
| Weight sqrt(n) × coordinate grid weight | `objectives/objective_funs.py::_Objective.build` |

\[
|\mathbf F|^2=a^2|u|^2+h^2|v|^2+2ah(u\cdot v),
\qquad S=a^2|u|^2+h^2|v|^2.
\]

- Pinned `e^helical` executes the opposite sign to its label. Use the actual function and v=−e^helical; metadata fork PR2 repairs the label without changing native fields. A direct Cartesian J×B oracle checks all four signed tangential-field combinations in an oblique chart.
- This native dual-basis decomposition is not automatically the literature basis β=B×grad(rho), which is orthogonal to grad(rho). No missing-cross-term paper erratum follows without mapping the original definitions.
- Complete vector norm retains the metric cross term. The native zero-target cost uses separately weighted radial/helical magnitudes.
- For nonzero basis vectors, c=(u·v)/(\|u\|\|v\|) gives (1−|c|)S ≤ \|F\|² ≤ (1+|c|)S. This is a local algebraic bound, not a volume-error or convergence theorem.
- Native `rtz` scaling multiplies residuals by coordinate weight×sqrt(node count), not the square root of that weight. The stored force residual has units N after multiplication by the volume Jacobian. It is not a volume-L2 norm of force density.
- Native force scale is f_ref=(B_ref²/(2mu0 a_ref))V_ref, with B_ref=1.25|Phi|/(πa_ref²), V_ref=2πR0πa_ref² and a_ref from the largest boundary R/Z Fourier coefficients (`objectives/normalization.py`). This scale is unchanged for these fixed-boundary/flux controls.
- Native cost additionally squares coordinate weights/Jacobians and applies a boundary-derived force normalization. Its small value is not an unweighted physical-force RMS.
- At regular nondegenerate charts both residual coefficients vanish at exact force balance. Different finite residual norms do not establish a source defect.
- Existing [native FortSym metric identities](cas/desc_force_correspondence.wl) and [signed GS identities](cas/desc_gs_strong_correspondence.wl) retain twenty conditional checks; numerical source/metric probes must still verify the actual execution path and state.
- No new symbolic check is counted from the numerical probes below.

## Radial sampling and controls

- Default grid: `ConcentricGrid`, Jacobi radial nodes; L_grid56 has29 rings, L_grid72 has37. Profiles have129 knots.
- Source-only reference: three-point Gauss integration per interval exactly integrates the squared quadratic p_s or iota_s derivative.
- L_grid56 pressure-derivative squared-integral midpoint error: CHEASE −2.02%, Pigatto +0.407%; L_grid72: −1.00%, −0.362%.
- This source-only diagnostic excludes physical metrics, magnetic cancellation and native squared quadrature weights. Node counts alone do not explain the measured force error.
- Compare same L28/M23 warm restart with L36/M23 and L_grid72. The latter jointly changes radial basis/collocation; it does not isolate basis error.
- Warm restart retains the equilibrium but resets native optimizer history. It is not a resumed trust-region checkpoint.
- Hold literal profiles, signed flux, Fourier boundary and stopping criteria fixed. Record exact parent H5/source/runtime hashes and full-state prolongation controls.

## Bounded physical comparison

| Family | Parent L28 | Warm L28 | Radial L36 accepted state |
|---|---:|---:|---:|
| CHEASE | 17.6769% | 17.6119% | 4.32077% |
| Pigatto | 4.87792% | 4.80625% | 1.73975% |

- Observable: unweighted vector force RMS / gradp RMS on the identical outer1024 physical points; every inverse-map point passes. Input profiles, signed flux and boundary remain fixed.
- CHEASE warm optimality falls from 3.272e−6 to 1.825e−8 while this force changes only 0.37%. A small objective gradient is not a physical-force certificate.
- Radial states are accepted93/136 before timeout. Their lower errors support a resolution-dependent contribution; optimizer history, basis and collocation effects remain distinct open questions.
- Full-query physical derivatives pass all429/426 inner and1024 outer-inclusive points at three step sizes. Finest observed force discrepancy/gradp spans 1.44e−8…7.88e−7; discrepancy is below6e−6 of the measured residual. This is an observed derivative budget, not a rigorous error bound.
- Twelve native directional-JVP probes pass the preset1e−6 threshold after resolving FD truncation with smaller steps; largest best error 4.13e−8. Full Gram/vector and native cost reconstruction pass roundoff. These probes do not prove the whole Jacobian, optimizer convergence or global accuracy.

## Required evidence and open questions

- Complete H5/JSON pairs only: initial/accepted/terminal roles; accepted states assert no optimizer convergence.
- Native stopping, profile/flux/boundary fidelity and independent physical-force refinement are separate gates.
- Use both frozen inner and outer physical queries; retain every validity mask and mapping error.
- Physical finite differences: independent R/Z centered stencils with step refinement. Piecewise-C2 input profiles can reduce the nominal convergence order when a stencil crosses a knot.
- Preserve inherited source/export-force, derivative-transfer and Fourier-boundary budgets. A common cubic inverse problem is not the historical exact forward-source problem.
- Open: warm-history versus radial representation; actual collocation/metric conditioning; outer physical-force refinement; axis/edge/global chart certification.
- No numerical optimizer defect, source-law equivalence or physical model limitation follows merely from an iteration cap.

## Evidence owners

- [TC24 programme and admission](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/blob/plan/circular-tokamak-benchmark-20261007/PLAN.md).
- [Checkpoint controls](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/blob/plan/circular-tokamak-benchmark-20261007/review/DESC_TC24_CHECKPOINT_CONTROLS_20261007.md): complete states, common queries and sampled derivative checks.
- TC24 adapters: `desc_checkpoint_restart.py`, `desc_checkpoint_trajectory.py`, `desc_profile_radial_sampling.py`, `desc_checkpoint_force_bridge.py`, `desc_checkpoint_full_fd.py`.
- [Pinned native source](https://github.com/PlasmaControl/DESC/tree/fcc29be36f0b36b1b667df4b1f8891a9b633f5d1); [callback fork PR1](https://github.com/itpplasma/DESC/pull/1); [metadata fork PR2](https://github.com/itpplasma/DESC/pull/2).
