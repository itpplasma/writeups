# VMEC++ held-state discrete force and energy

- Source: official VMEC++ `a4150a4e2101bd47868d040f3adee5d0304ce89b`, published0.8.1 binary. Scope: axisymmetric, asymmetric geometry, fixed boundary, prescribed iota (`ncurr=0`), `gamma=0`, `tcon0=0`.
- Actual native first-evaluation checkpoint: TC24 M40/ns129; unchanged native state, one evaluation per fresh model. No equilibrium solve, time step, radial refinement or axis update is called.
- Source/directional evidence: `iter_tc24/equilibrium/data/vmecpp_native_force_checkpoint_20261007/energy_correspondence.json`; [bounded FortSym half-cell identities](cas/vmecpp_native_energy/symbolic_results.json).
- These checks concern the discrete implemented equations. Continuous physical-force admission remains open.

## Actual native chain

- `pybind_vmec.cc:222–319`: `VmecModel.create` initializes one resolution; `evaluate(...precondition=false)` calls `IdealMhdModel::update` and returns at `INVARIANT_RESIDUALS`. `precondition=true` evaluates the full force/preconditioner chain without taking a time step.
- State/force blocks: Rcc,Rsc,Zsc,Zcc,Lsc,Lcc; surface-major, then mode-major. Saved vectors have30960 entries. State change is exactly0 in every retained test.
- `ideal_mhd_model.cc:934–968`: physical forces are multiplied by even/odd decomposition scales; the m1 map uses1/sqrt(2); the constrained gauge force is zeroed. Our directional tests avoid m1 and fix axis/LCFS values.
- `dft_ForcesToFourier_2d_symm` and asymmetric companion project the radial/angle stress terms, including angular derivatives, onto the represented basis. Geometry modes are m0..39; finite-field products can have higher harmonics.
- `fourier_basis.cc`: m0 normalization1, m>0 sqrt(2). `radial_profiles.cc:1242–1249`: even scale1, odd scale1/sqrt(s), with the source axis rule. These scales are part of the dual map, not empirical gains.

## Energy and virtual work

- Native half-cell energy for signed Jacobian J<0 is

\[
 e=-\frac{g_{uu}N_u^2+g_{vv}N_v^2}{2J}+\mu_0pJ,
 \qquad N_u=JB^u,\quad N_v=JB^v.
\]

- At prescribed iota/flux, metric variations hold these numerators fixed; lambda changes N_v through its angular derivative. Native energy is h times angularly normalized quadrature of e, h=1/(ns−1). The SI energy is native energy times4pi²/mu0; physical volume is native volume times4pi².
- FortSym checks the metric/Jacobian derivatives, lambda chain normalization and hybrid difference exactly. These are bounded sectors; full geometry-jet composition, endpoint/gauge and preconditioner derivatives are separate obligations.
- Source R/Z stress assembly: `mhdforce_kernel.h:166–191`; half-grid radial differences, arithmetic/odd-weighted averages and angular test derivatives enter the weak variation. For tested directions, the energy dual is `−signgs*h*dot(raw_force,direction)`; native signgs−1 gives +h.
- Independent scalar-energy central differences use private off-equilibrium probes x+1e−3d, then steps4e−5,2e−5,1e−5. The probe is not a new equilibrium or a change to the archived solution.
- Rcc m0/2/22/38 and Zsc m2 agree with the source-normalized raw force within their measured finite-difference budgets. Wrong-sign controls fail decisively. This tests low/high represented bands, not every direction or a general variational theorem.

## Lambda: finite-stencil qualification

- `lambda_force_kernel.h:77–104` uses G=(1−beta)C+beta A, beta=.1(1−s), C the adjacent-half covariant average and A its local alternative. The existing [hybrid correspondence](vmecpp_hybrid_lambda_correspondence.md) defines the exact stencil and smooth-interior expansion.
- Source lambda projection is `−lamscale*G` paired with the differentiated normalized angular basis. The native scalar `mhd_energy` supplies the C dual; the measured beta(A−C) term must be retained when comparing the implemented raw force to this scalar energy.
- Tested Lsc m2: raw dual0.955196133; energy dual0.955334770; source hybrid correction−0.000138626079; corrected difference1.07e−8.
- Tested Lsc m22: raw dual117.277079458; energy dual117.275011087; source hybrid correction+0.00206831660; corrected difference−5.46e−8.
- Both corrected differences are inside independent FD budgets. Geometry readback agrees with the parent full coefficients to2.22e−16. No fitted gain/sign/offset is used.
- The API comment calling raw force an augmented-Lagrangian gradient is broader than comparison to `mhd_energy` alone supports. This is a possible documentation/functional-definition qualification, **not an established solver defect**. A separate augmented functional may be intended; no general existence/nonexistence claim is made.

## Reconstructed stopping norms

- Source angular weights are1/ntheta for asymmetric axisymmetry. Whole-half-grid replay gives native magnetic energy327.682082054, thermal energy8.139388388, volume20.708078835; energy319.542693667 agrees within1.7e−13.
- `computeForceNorms`: energy density=max(magnetic,thermal)/volume;
  `fNormRZ=1/[energy_density² sum(guu Rhalf² weights)]`;
  `fNormL=1/[lamscale² sum((B_u²+B_v²) weights)]`.
- `lamscale²=h sum(phip_half²)`. Using full points instead is wrong by129/128 for constant phip; the half-grid authority is explicitly tested.
- `FourierForces::residuals` sums squared coefficient forces; fixed-boundary R/Z exclude the LCFS, lambda includes it. Invariant R/Z residuals have an additional1/4; lambda does not.
- Source preconditioned norms use the R/Z state norm with offset modes excluded; lambda uses h. Independent vector/quadrature reconstruction matches raw residuals to1.18e−14 relative and preconditioned residuals to3.78e−15.
- Raw-checkpoint fsqr1/fsqz1/fsql1 are stale initialized values; they become meaningful after preconditioning. The actual freshly evaluated invariant residuals reproduce the archived stopping values to about1e−5 relative; exact equality to a previous solver phase is not assumed.

## Discrete versus continuous virtual work

- Same strict-converged M40/ns129 state; compact even-m test directions supported only on .15<s<.85, with zero value/first jets at endpoints. Continuous weak work uses −mu0 integral mean[R|J|(curl(B)/mu0 cross B−gradp)·deltaX]ds, in native energy units.
- Source-native raw-force energy dual Rcc m2 is6.63e−8. The continuous stored-BSUP dual is−3.47e−4 using native-presf readback, or−3.66e−4 with the exact executed pressure spline. This is a real discrete/readback difference, not a proof of solver error.
- Naive81-point radial trapezoid substantially aliases these cancelling weak moments. Piecewise Gauss4/8/16 splits all270 full/half/profile breakpoints; angular512/1024 and integration order changes agree to about1.5e−15 absolute for five tested directions. Exact-pressure substitution does not close the gap.
- Stored fields are not exactly divergence free; the stress/work identity therefore needs its divB qualification. Other continuum field routes, native metric staggering and radial interpolation are separate model budgets. No continuous moment is relabeled as a native stopping residual.

## Remaining gates

- Native weak stationarity is verified for the discrete coefficient model and tested energy directions. It does not make the interpolated Cartesian curl-force residual vanish.
- Full odd/m1/axis/LCFS virtual-work correspondence; nonlinear live-preconditioner/gauge effects; all directions; actual-state radial-jet bounds; continuum refinement remain open.
- The M40/ns129 parent meets strict native stopping but outer physical force/gradp remains0.04482. M40/ns257 retains a strict stopping failure; it is a diagnostic, not a third admitted resolution.
- Constraint0 continuum closure must keep source/profile/domain and source-axis readback fixed; agreement among shared-genealogy solvers is not an independent proof.
