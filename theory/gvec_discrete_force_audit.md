# GVEC discrete force and canonical sign bridge

- Source: [GVEC c0dc66fe2b9faa147c76a728e5cd053ce693d472](https://gitlab.mpcdf.mpg.de/gvec-group/gvec/-/tree/c0dc66fe2b9faa147c76a728e5cd053ce693d472).
- Scope: fixed-boundary, nested-surface, axisymmetric RZ equilibria, fixed pressure (`gamma=0`), fixed iota and toroidal flux. This is neither a stability test nor a proof of full 3D assembly.
- Evidence: [16 native exact local identities](cas/gvec_native/gvec_local_identities.f90), registered CMake/CTest; retained independent analytical E0 and physical cylindrical-curl probes in the TC24 repository.
- The integration-by-parts bridge below is derived explicitly; a full discrete-to-continuous convergence theorem remains open.

## Signed geometry and field

- Define covariant tangents `e_a=partial_a x`, reciprocal gradients, and signed `Jac=e_rho·(e_theta×e_zeta)`.
- Native RZ map: `x=(R cos(zeta),−R sin(zeta),Z)`; hence physical counterclockwise `phi=−zeta`.
- `Jp=R_rho Z_theta−R_theta Z_rho`, `Jac=R Jp>0` away from the axis; `g_theta_theta=R_theta²+Z_theta²`, `g_zeta_zeta=R²`, `g_theta_zeta=0` in axisymmetry.
- Flux-density components: `btheta=chi′−Phi′ lambda_zeta`, `bzeta=Phi′(1+lambda_theta)`; `B=(btheta e_theta+bzeta e_zeta)/Jac`.
- `Phi=PHIEDGE*rho²/(2*pi)` in Wb/radian; `chi′=iota_G Phi′`. The input PHIEDGE is total signed toroidal flux in Wb.
- Canonical scalar flux: `psi=chi−chi_edge`, not `−chi` and not `chi/(2*pi)`.
- At axisymmetry, `psi_R=chi′ Z_theta/Jp`, `psi_Z=−chi′ R_theta/Jp`.
- Consequently `B_R=−psi_Z/R`, `B_Z=psi_R/R`, `B_phi=−Phi′(1+lambda_theta)/Jp`. Canonical `F=R B_phi` must retain this sign.
- Straight angle `theta*=theta+lambda` satisfies `dtheta*/dzeta=iota_G`; therefore canonical `q=dphi/dtheta*=−1/iota_G`.
- Opposite toroidal-chart orientation maps `Phi_G=−Phi_V`, `iota_G=−iota_V`, with unchanged theta. This preserves physical B only when all components and basis vectors are transformed together.
- In the ordinary positive-F lane, Phi_G is negative. The retained TC24 negative-F lane instead has Phi_G positive. Never take absolute flux to compare them.

## Energy derivative actually assembled

- Write `E=mu0 W`; the local integrand is `L=−mu0 p Jac+(btheta² gtt+2 btheta bzeta gtz+bzeta² gzz)/(2 Jac)`.
- Define `D=mu0 p+(btheta² gtt+2 btheta bzeta gtz+bzeta² gzz)/(2 Jac²)`.
- Geometry variations keep the prescribed flux/profile functions fixed; `−delta E=D delta Jac−(b^a b^b delta g_ab)/(2 Jac)`.
- For the axisymmetric RZ map, the five native negative-derivative coefficients are:

| Test coefficient | Negative derivative |
|---|---|
| `Y_R` | `D Jp−bzeta² R/Jac` |
| `partial_rho Y_R` | `D R Z_theta` |
| `partial_theta Y_R` | `−D R Z_rho−btheta² R_theta/Jac` |
| `partial_rho Y_Z` | `−D R R_theta` |
| `partial_theta Y_Z` | `D R R_rho−btheta² Z_theta/Jac` |

- Exact native identities 1–9 check the determinant and these five coefficients independently by differentiating L; identities 10–12 check canonical B/q.
- Lambda variations: `delta btheta=−Phi′ partial_zeta Lambda`, `delta bzeta=Phi′ partial_theta Lambda`.
- Thus `−delta_lambda E=Phi′(B_theta partial_zeta Lambda−B_zeta partial_theta Lambda)`; covariant `B_a=B·e_a`.
- Identities 13–16 check both signs directly. The pinned documentation's delta-b signs describe the opposite variation, while executed negative-energy force assembly has the correct signs.
- Source: `mhd3d_evalfunc.F90:382–395` field densities, `:589–596` D/magnetic coefficients, `:625–649` R coefficients, `:717–737` Z coefficients, `:796–797` lambda projection; `:517` mu0-scaled energy.

## Weak-to-strong force bridge

- Use `j=curl(B)/mu0`, reserving Jac for the coordinate Jacobian.
- Covariant curl gives `j^rho=(partial_theta B_zeta−partial_zeta B_theta)/(mu0 Jac)`.
- Periodic integration by parts yields `−D_lambda W[Lambda]=integral Phi′ Jac j^rho Lambda dρdθdζ`.
- It imposes radial-current stationarity in the test-function span. It does not impose a pointwise bound when that span or quadrature is insufficient.
- Physical force `f=j×B−grad(p)` has tangential covariant components `f_theta=−Jac j^rho B^zeta=−j^rho bzeta`, `f_zeta=Jac j^rho B^theta=j^rho btheta` because pressure is a flux function.
- Once the lambda equation removes radial current, tangential force vanishes; geometry variations supply the remaining force condition.
- For a smooth admissible displacement xi vanishing at the fixed boundary, the magnetic-flux-preserving geometric variation gives `−D_geometry W[xi]=integral f·xi dV`. Pressure is advected with the flux label, not fixed at physical R,Z.
- Assumptions: periodic angles, nondegenerate positive Jac away from the axis, regular axis limit, nested flux surfaces, fixed physical boundary and sufficiently smooth profiles/fields.
- This continuum identity does not equate a finite preconditioned coefficient norm with `||f||` in SI.

## Discrete operator and stopping measure

| Stage | Source authority | Meaning |
|---|---|---|
| Trial/test basis | theory.md; radial and Fourier base modules | Tensor-product B-splines in rho and sin/cos(m theta−n*nfp*zeta) |
| Evaluation | `EvalAux` | Geometry and derivatives at radial Gauss/angular nodes; nonlinear metric and inverse Jac |
| Weak projection | `EvalForce:651–676,740–764,795–815` | Weighted angular projection then radial value/derivative basis contraction |
| Constraints | `:849–871,896–919,948–979` | Axis/edge BC applied before preconditioning; fixed geometry at edge, lambda free |
| Preconditioner | `BuildPrecond`; `ApplyPrecond:1481` | Mode-wise matrix solve; changes residual metric and optimizer direction |
| Norm | `sol_var_mhd3d.F90:261–263`; `mhd3d_minimize.F90:507` | Euclidean square-root coefficient norm for each of R/Z/lambda after those operations |
| Stop | `mhd3d_minimize.F90:489` | All three norms <=abstol; printed “relative tolerance” does not define SI force normalization |

- Nonpolynomial `1/Jac` means finite Gauss/trapezoidal quadrature is not generally exact, even when the trial functions are polynomial/Fourier.
- Exact differentiation of the discrete quadrature energy, quadrature refinement and aliasing bounds remain separate gates. The 16 local identities do not certify every basis projection or preconditioner.
- Positive, invertible preconditioning preserves a zero unconstrained gradient; finite tolerance values are basis/preconditioner dependent.
- Boundary and axis constraints change the admissible variation space. A low constrained norm cannot establish omitted modes or boundary-force conditions.

## Retained TC24 interpretation and next control

- Existing 32-element continuation hit 40000 steps; projected norms approximately 4.2e−9,6.17e−9,4.93e−9 exceed 1e−10. Native convergence failed.
- Independent cylindrical-curl force and producer Cartesian force agree closely; both retain force/gradp near 0.25 on the declared interior sampling grid. This rejects a large checker-only error for that state, not every input/numerical hypothesis.
- Frozen coarse Fourier boundary differs from the received polygon and avoids the original X point. Nested-surface incompatibility and unresolved harmonics remain hypotheses, not conclusions.
- Native CHEASE q plus independently specified exact p/F can describe inconsistent source equilibria; corrected source-law/mapping admission precedes another purported matched TC24 run.
- Next radial control: retain the exact admitted physical law/boundary/sign and continue the 32-element state at 64 elements, degree5, unchanged M23. Next angular control: unchanged radial space, larger interior M while retaining the same boundary coefficients.
- These are proposed separate controls, not executed jobs. Each requires fresh tags, sealed deck/source/state/binary hashes and controller registry ACK before execution.
- Missing ordinary E1/E2 aspect ratios and E4 zero/finite beta await the CHEASE-source native-q/Phi mapper. No noisy P1 profile deck is recycled as a matched input.
