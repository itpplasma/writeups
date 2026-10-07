# VMEC++ hybrid lambda: checked local correspondence

- Scope: pinned VMEC++ `a4150a4e2101bd47868d040f3adee5d0304ce89b`, axisymmetry (`ntor=0`, `lthreed=false`), smooth interior radial chart. This is local source/algebra evidence, not full solver convergence.
- Native covariant toroidal component is `B_v = B·e_v = R Bphi`; axisymmetric lambda stationarity targets its angular derivative. Jacobian and flux-density signs remain native.
- [Replay, source hashes and numerical receipt](cas/vmecpp_hybrid_lambda/provenance.json); [native FortSym checks](cas/vmecpp_hybrid_lambda/symbolic_results.json).

## Lifecycle

- `vmec.h:188`: compile-time `Vmec::kPDamp=0.05`.
- `vmec.cc:752–753`: passes that constant to every new `RadialProfiles`; `radial_profiles.h:202` stores a `const double`.
- `vmec.cc:824`: profile evaluation follows radial initialization. `radial_profiles.cc:1232–1239` assigns `beta(s)=2*pDamp*(1-s)=0.1*(1-s)`.
- The time step `delt` and its restart reductions are separate. They do not update this constant. A pDamp-only solver experiment needs a separately pinned source/binary change; none was run here.
- `IdealMhdModel::update`: raw instantaneous metric lowering (`computeBCo`, line545) precedes the hybrid kernel (line592); effective constraint/de-aliasing follows at912–914. The kernel does not consume force/current-corrected exported BCOV.
- The same initialization path handles fixed/free boundaries; the checked oracle uses interior points only. The 3D mixed-metric/toroidal-force terms are not covered.

## Exact native stencil

- Let `h` be full-grid spacing, `K=gvv/J`, `x` the even normalized lambda density and `y` its regular odd density. The density is `x+sqrt(s)*y`; native flux-density normalization is already included.
- Subscripts `-`, `+` denote half points `s±h/2`; subscripts `j-1`, `j`, `j+1` denote full points.
- The stored half-field interpolation gives

\[
C=\tfrac14\{K_-[x_{j-1}+x_j+\sqrt{s_-}(y_{j-1}+y_j)]
             +K_+[x_j+x_{j+1}+\sqrt{s_+}(y_j+y_{j+1})]\}.
\]

- `lambda_force_kernel.h:77–102` additionally constructs

\[
A=\tfrac12(K_-+K_+)x_j+\tfrac12(K_-\sqrt{s_-}+K_+\sqrt{s_+})y_j,
\qquad G=(1-\beta)C+\beta A.
\]

- The kernel outputs `-lamscale*G` on interior full points, plus the odd `sqrt(s)` factor; native Fourier projection/preconditioning/stopping are subsequent operations.
- **Checked smooth-interior jet identity:**

\[
A-C=-\frac{h^2}{4}\left[\partial_s(K\partial_s x)
                         +\partial_s(K\sqrt{s}\,\partial_s y)\right]+O(h^4).
\]

- Thus the difference is generally nonzero at finite spacing. For fixed `s>0` and bounded smooth jets it decreases quadratically; taking the angular derivative needs the same angular smoothness. Radially constant density jets make it exactly zero; beta0 gives the ordinary average exactly.
- FortSym proves one generic sector, then exact linear composition. Eleven identities pass and an intentionally wrong coefficient is rejected. The combined21-indeterminate probe returns **UNKNOWN** at the native polynomial limit12; it is retained separately. Capacity expansion is adjacent work, not required for the checked composition.

## Independent actual-kernel oracle

- Compiles the pinned header itself through CMake/CTest; no copied implementation and no solver dependency change.
- Exact circles `R=R0+a*sqrt(s)*cos(theta)`, `Z=a*sqrt(s)*sin(theta)`, with R0=6.2m,a0.62m; exact vacuum field `Bphi=F/R`, F32.86Tm, iota0, p0. Physical curl/force are zero; this is a manufactured field/kernel test, **not a tokamak q benchmark**.
- Exact normalized density `L=F/K`; its even/regular-odd parts are rational in s. Angular mean reproduces the known toroidal-flux derivative `-a²F/(2*sqrt(R0²-a²s))`; no input deck equivalence is asserted.
- At s0.25/0.5/0.75, h1/32→1/512: angular derivative RMS and stencil differences decrease by factor4. Angular2048→4096 changes the finest result by1.4e-6 relative. No nonvanishing offset or gross aliasing was found in this oracle.
- First interior point s=h: exact analytical axis jets give quadratic decrease; applying the native m1-axis closure gives h^(3/2), ratio2.830 at the finest doubling. Predicted leading RMS `F*a³*(1-beta)*h^(3/2)/(32*R0³)` agrees within0.033%. Axis closure acts on lambda before multiplication by the flux density.
- A deliberately nonstationary angular field retains derivative0.22846Tm/rad under refinement; it is correctly rejected as a stationary field. Zero-weight/constant-density controls pass.

## Open bridges

- This does not explain the TC24 core force plateau: no native state, profile, damping constant or geometry was modified.
- Full finite-Fourier lambda projection, its residual normalization, weak geometry/constraint balance, and error bounds for the actual TC24 radial jets remain unproved.
- Axis/LCFS endpoint equations require their own predicates; the smooth-interior expansion is not uniform at s0. The tested first-interior closure is a separate result.
- A pDamp/source-only counterfactual is a possible later discriminant after registered review. It must preserve tcon, source laws, initialization and stopping criterion.
