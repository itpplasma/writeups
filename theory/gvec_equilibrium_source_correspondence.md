# GVEC equilibrium source correspondence

- Scope: targeted axisymmetric E0/TC24 investigation; no perturbation or transport claims.
- Source: [official GVEC c0dc66fe](https://gitlab.mpcdf.mpg.de/gvec-group/gvec/-/tree/c0dc66fe2b9faa147c76a728e5cd053ce693d472); [release mirror](https://github.com/gvec-group/gvec/tree/c0dc66fe2b9faa147c76a728e5cd053ce693d472).
- Status: source correspondence inspected; run and independent-field gates belong to TC24 evidence. No symbolic proof of the full discrete solver is claimed.
- Genealogy: nested-surface ideal MHD energy minimization follows VMEC; radial B-splines provide numerical independence within the same equilibrium model.

## Coordinates and profiles

- Native `rho=sqrt(Phi/Phi_edge)`; profile interpolation acts on `rho²`, not rho.
- RZ map: `(x,y,z)=(R cos zeta,−R sin zeta,Z)`; zeta clockwise, theta counterclockwise.
- [Conventions](https://gitlab.mpcdf.mpg.de/gvec-group/gvec/-/blob/c0dc66fe2b9faa147c76a728e5cd053ce693d472/docs/user/coordinate-conventions.md) and `src/hmap/hmap_RZ.F90` define the map.
- Frozen VMEC chart transformation: theta unchanged; zeta_G=−phi_V, iota_G=−iota_V, Phi_edge_G=−Phi_edge_V. Independently check Cartesian B after applying these input transformations.
- Input PHIEDGE is total signed flux in Wb; `src/functionals/mhd3d/mhd3d.F90:137–138` divides by `2*pi` internally.
- Preserve pressure in Pa and iota as functions of normalized toroidal flux; GS derivative tables define a different input contract.
- `InitProfile`, `mhd3d.F90:477–582`, supports polynomial, B-spline coefficients and cubic interpolation; default interpolation uses not-a-knot endpoint conditions.
- VMEC++0.8.1 clamps endpoint first derivatives to quadratic fits through the nearest three knots. GVEC supports these exact slopes via native `*_BC_type_axis/edge=1st_deriv` and `*_BC_vals`.
- Identical knots do not establish identical profiles. Compare values and derivatives independently, including endpoint neighborhoods.

## Magnetic field and force

- `theta_star=theta+lambda`, `zeta_star=zeta`, with flux functions satisfying `chi′=iota Phi′`.
- Vector potential: `A=Phi grad(theta_star)−chi grad(zeta)`.
- Field: `B=Phi′ grad(rho)×grad(theta+lambda)−chi′ grad(rho)×grad(zeta)`.
- Components: `B^theta=Phi′(iota−lambda_zeta)/J`, `B^zeta=Phi′(1+lambda_theta)/J`, `B^rho=0`.
- Signed Jacobian, vector bases and components transform together.
- Fixed-pressure (`gamma=0`) energy integrand: `−p J + b^alpha g_alpha_beta b^beta/(2 mu0 J)`.
- [Theory and first variation](https://gitlab.mpcdf.mpg.de/gvec-group/gvec/-/blob/c0dc66fe2b9faa147c76a728e5cd053ce693d472/docs/user/theory.md); native assembly: `src/functionals/mhd3d/mhd3d_evalfunc.F90`.
- Python `quantities.py:687–689` reconstructs Cartesian B; `:900–908` computes current through covariant curl; `:921–922` evaluates `J_current×B−grad(p)`.
- Native optimization residual, producer force diagnostic and independent physical GS residual measure different errors. Projected stationarity does not bound unresolved force harmonics.

## Targeted discrimination

| Case/check | Oracle | Interpretation |
| --- | --- | --- |
| Exact Solovev LCFS | Analytical psi, Cartesian B, axis, q, flux | Admit translation before actual ITER |
| Coarse TC24 Fourier LCFS | Frozen VMEC++ boundary, p(s), iota(s), total flux | Separate from original 299-point received LCFS |
| Force balance | Native residual plus independent curl/GS | Separate stationarity, input mismatch and physical residual |
| Refinement | Radial degree/elements and angular harmonics | Numerical limit without fitting another solver |

- Shared-error checks: exact physical fields; implemented profile derivatives; independent Cartesian curl or axisymmetric GS reconstruction.
- Open: axis regularity, high-harmonic residual, signed flux reconstruction, and nested-surface compatibility of the prescribed boundary/profiles.
- Historical GLISS GVEC1.5 CAS3D patches are not applied here. Export wrappers do not provide independent equilibrium votes.

## Documentation errata

- Pinned theory line53 calls `B^alpha=B·grad(alpha)` covariant; this definition is contravariant. Diagnostic component formulas use the latter definition.
- Pinned theory lines189–190 label `delta btheta=+Phi′Lambda_zeta`, `delta bzeta=−Phi′Lambda_theta`; direct differentiation of its field definition gives opposite signs.
- Native lambda force assembly (`mhd3d_evalfunc.F90:796–797`) uses positive zeta and negative theta test derivatives for **−DW**, consistent with the actual differentiated field. The documentation mixes variation and negative-force signs; no native solver defect follows.
- Current pinned Jacobian variation line175 has the correct positive `X2_theta*Y1_rho` term. The version1.3 document's opposite sign cannot be attributed to current source without a separate historical pin.
- Exact Solovev native E0 test verifies physical B/psi; it does not prove every 3D discrete assembly term.

## Native profile variants

| Native selector | Definition | Matched-problem use |
| --- | --- | --- |
| `pres_type/iota_type=polynomial` | Coefficients in s=rho²; `_scale` multiplies coefficients | Exact polynomial functions, or a separately bounded polynomial approximation |
| `pres_type/iota_type=bspline` | `_knots`, `_coefs`; degree inferred from endpoint knot multiplicity | Can encode the same clamped cubic exactly without native interpolation |
| `pres_type/iota_type=interpolation` | Cubic through `_rho2`, `_vals` on s | Selected here with explicit endpoint slopes |
| `_BC_type_axis/edge=not_a_knot` | Native interpolation default | Different endpoint function unless independently shown negligible |
| `_BC_type_axis/edge=1st_deriv` | Prescribed `_BC_vals` first derivatives | Selected quadratic endpoint slopes match frozen VMEC++ cubic |
| `_BC_type_axis/edge=2nd_deriv` | Prescribed second derivatives; zero gives natural spline | Different derivative law; label as a separate input control |

- Native `InitProfile` supports all three families; each evaluates in rho² and supplies radial chain-rule derivatives. Direct B-spline coefficients are an equally valid exact representation, not an unavailable capability.
- Fixed-iota native minimization and Python `I_tor`/`picard_current` prescribed-current optimization are different constraints. The latter iterates iota; it is not used here and cannot also preserve prescribed iota arbitrarily.
- VMEC-state initialization can retain received profiles or explicitly replace them via `init_with_profile_iota/pressure`; this run instead initializes from independent native parameters.
- Current source hardcodes Phi=Phi_edge*s and integrates chi from iota. The legacy `flux_label=phi` line in these decks is not a current selectable radial-label model; no poloidal-label capability is inferred from it.
- Alternative-spline input budget: TC24 not-a-knot changes maximum pressure values by 0.124%, but pressure derivatives by 26.45%; iota values by 0.280%, derivatives by 74.84%, relative to the source-matched clamped functions. This matters for force balance even when knots agree.
- E0 not-a-knot changes pressure/iota values by 3.73e-11/1.06e-12 relative; derivatives by 2.70e-8/2.04e-8. The correction has a tiny E0 budget, while still establishing the exact same input function.
- Natural-spline alternatives and exact normalizations are retained in `equilibrium/data/GVEC_profile_models_20261007.json`. These are function comparisons, not fresh solver runs or evidence of a solver bug.
