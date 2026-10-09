# Axisymmetric equilibrium case contract

- Scope: equilibrium only. Perturbations and transport remain later slices in [PLAN.md](../PLAN.md).
- Machine-readable inputs: [cases.json](cases.json). Preserve native outputs; publish explicit canonical maps.
- Reference scale: R0=6.2 m, B_reference=5.3 T, F_reference=32.86 T m. These are scale choices, not an admitted ITER equilibrium.
- All results carry case ID, variant, source commit, input hash, solver settings, boundary representation and convergence evidence.

## Signs, units and selectors

- SI: R,Z in m; B in T; p in Pa; mu0=4*pi*10^-7 H/m.
- Physical phi increases counter-clockwise viewed from +Z; right-handed cylindrical basis (e_R,e_phi,e_Z).
- B=grad(psi) cross grad(phi)+F grad(phi): B_R=-psi_Z/R, B_Z=psi_R/R, B_phi=F/R.
- psi is signed poloidal flux per radian, Wb/rad; full poloidal flux is 2*pi*psi.
- Canonical theta increases counter-clockwise in (R-R0,Z); (r,theta,phi) is left-handed. This convention is COCOS 3; the sign owner documents all native mappings.
- GS: Delta_star psi + mu0*R^2*p_prime + F*F_prime=0; Delta_star=partial_RR-partial_R/R+partial_ZZ.
- Fixed physical LCFS: psi_edge=0; the signed psi_axis is solved, not fitted. E0–E4 and the E5 modx03 reference use an axis minimum; the JINTRAC variant retains its separately declared axis-maximum polarity. s_pol=(psi-psi_axis)/(psi_edge-psi_axis).
- Signed toroidal flux Phi is the full integral of B_phi dR dZ. s_tor=Phi/Phi_edge; published radius rho_tor=sqrt(s_tor).
- q=dPhi/dpsi/(2*pi), equivalently the signed toroidal winding per complete poloidal turn: q=(1/(2*pi))*integral(dphi). Local dphi/dtheta equals q only for a straight-field-line poloidal angle; geometric CCW theta need not have that property. Keep flux, current, q and pressure derivative signs consistent.
- E0–E4 forward cases fix boundary, p_prime(psi), FF_prime(psi), F_edge and pressure_edge. Current, axis flux and q are outputs. E5 instead fixes normalized derivative shapes and signed enclosed current; its common amplitude and axis flux are solved. These are not fixed dimensional primitive profiles. modx03 maps from COCOS 2 to 3 with F<0, q<0, Phi<0 and current<0.
- An inverse prescribed-q case fixes boundary, pressure and a declared flux/current scale, and releases the F/current profile. It is a separate variant.
- q_source_scale=1.5 fixes source amplitude in E1/E2. It does not prescribe q=1.5 on every surface.
- Reject negative pressure in physical plasma cases, F^2<=0, nonnested surfaces or noninvertible radial maps. Manufactured box pressure offsets are not device constraints.

## Cases

| ID | Purpose | Fixed physics | Admission boundary |
| --- | --- | --- | --- |
| C0_gold_hoyle_cylinder | Exact zero-beta periodic cylinder | Gold–Hoyle; independent axial period L, amplitude and signed RH q | Exact analytical reference and sign controls; cylinder ODE and finite-A routes have separate qualification |
| C0_lundquist_cylinder | Exact sheared periodic-cylinder companion | Constant-alpha force-free Bessel field, alpha*a=1.5 | Analytic reference with an isolated rational surface; perturbations remain a later slice |
| E0_solovev_box | Exact PDE and field oracle | Polynomial finite-beta and logarithmic zero-beta GS solutions | Exact Dirichlet trace on rectangular box; independent off-grid error |
| E1_circular_zero_beta | First physical toroidal case | p=0, FF_prime=-2*B_reference/q_source_scale, F_edge fixed | Exact circular LCFS at A=10,20,40; q is solved |
| E2_circular_finite_beta | Separate pressure-supported case | FF_prime=0, p_prime=-2*B_reference/(q_source_scale*mu0*R0^2), p_edge=0 | Same circular LCFS; q is solved |
| E3_finite_aspect_ratio | Controlled toroidicity | E1/E2 source laws, A=3.1 | Circular LCFS; not a perturbation of the cylinder assumed exact |
| E4_shaped_iter_scale | Controlled shaping | E1/E2 laws, A=3.1, kappa=1.7, delta=0.33 | Explicit smooth Miller boundary; not the actual TC24 boundary |
| E5_iter_tc24 | Collaborator modx03 CHEASE reference | [Provenance and exact source/deck](phase4/tc24/EQUILIBRIUM_PROVENANCE.md); COCOS 2→3, reference s_pol=0.995 boundary; normalized pprime/FFprime shapes and enclosed-current constraint for the common forward study | Exact supplied NSTTP=2/NCSCAL=4 replay is separate; source, transfer, native and consumer errors are reported. JINTRAC, gfile_chease and Leonardo are explicit variants |

- C0 in right-handed (r,theta_RH,z): k=1/(q_RH*R0); B_z=B_axis/(1+k^2*r^2), B_theta_RH=k*r*B_z. curl(B)=2*k*B/(1+k^2*r^2), hence j cross B=0.
- Aligning cylinder z with physical +phi gives theta_c=-theta_RH, Btheta_c=-Btheta_RH, psi_c=-psi_RH up to gauge and q_c=-q_RH. Native +1.5 therefore maps to canonical -1.5 in this strict straight limit; retain native outputs.
- A uniform B_z plus B_theta proportional to r is not a zero-pressure force-balanced substitute.
- Physical circular boundaries generally produce nonconcentric flux surfaces. Never prescribe arbitrary circular flux contours and arbitrary q as an exact toroidal equilibrium.
- Constant-q and actual-TC24-q inverse variants are additional cases only after their pressure, flux/current selectors and solver support are specified.

## Periodic cylinder and Freidberg correspondence

- Authority: [periodic-cylinder derivation and reference](data/periodic_cylinder_reference_20261008/CONTRACT_PROPOSAL.md) and its sealed input/data/oracles. The contract is admitted for analytical-reference use; native solver inputs and numerical-error caps remain proposals until reviewed and registered.
- The domain is a disk times an axial circle: r<=a=0.62m, z modulo L=2*pi*6.2m. The period is an independent physical input, not a toroidal major radius. The wall has Br=0; exterior and matching wall current are not prescribed.
- Derive radial force balance, regular axis limits, signed fluxes and winding explicitly from Freidberg's [Ideal MHD, Chapter5, pp85–122](https://www.cambridge.org/core/books/abs/ideal-mhd/equilibrium-onedimensional-configurations/611F4B794D9C6541921CB9DCE17D7A3D) and his open [Lecture5, pp1/4/7](https://ocw.mit.edu/courses/22-615-mhd-theory-of-fusion-systems-spring-2007/a5c962e43b645b825b13715a131166e2_lecture5.pdf). The force equation is d[p+(Btheta²+Bz²)/(2*mu0)]/dr+Btheta²/(mu0*r)=0. Exact book equation numbers have not been verified.
- For Gold–Hoyle set tau=2*pi/(L*q_RH), Bz=Baxis/(1+tau²*r²), Btheta=tau*r*Bz and p=0. Fix amplitude/twist; measure axial flux, meridional flux and current. The primary edge axial flux is6.386248371012646Wb, distinct from CQA10. Test q_RH=±1.5 and global B reversal independently.
- The sheared Lundquist companion has Bz=Baxis*J0(alpha*r), Btheta=Baxis*J1(alpha*r), curl(B)=alpha*B. Its isolated q_RH=1/10 surface is at r=0.5607288380070159m. Constant-q Gold–Hoyle instead has a global resonance and cannot test its localization.
- Exact cylinders and toroidal approximations have separate evidence. Every retained lane needs either a verified cylinder route or a checked finite-A continuation. Use A=10,20,40,80,160 at fixed a,L,p, cylinder flux target and q_RH(s_axial). The inverse toroidal problem releases F/current and finite-A Baxis. Its canonical q_t=-L*q_RH/(2*pi*R_major); holding q_t fixed changes the target cylinder.
- Use the negative-RH-q control for the ordinary positive-canonical-q/axis-minimum toroidal branch. Keep the positive-RH-q and field-reversal controls as explicit signed cases; never pass a negative-canonical-q case through an axis-minimum-only selector silently.
- Numerical boundary/profile/export/derivative error must be smaller than the measured finite-A model difference before interpreting the cylinder limit. Compare signed fields, local pitch, axis shift, flux, current and strong force at fixed physical points; no fitted sign, amplitude or convergence rate.
- Native KIM equilibrium ingress is checked by the [versioned actual-reader/ODE gate](data/periodic_cylinder_native_kim_20261008_v2/README.md): five positive native CTests and two NaN rejection controls pass for signed/reversed GH, Lundquist and its existing integrator oracle; no full response or continuum certificate.
- For later KIM, exp[i*(m*theta_RH-2*pi*n*z/L)] maps to its native plus-sign parallel wavenumber with m_KIM=m,n_KIM=-n and R0_KIM=L/(2*pi). KIM_PERIODIC is radial-window periodicity, not axial periodicity. Positive-radius seeds require B²(r_min), not the on-axis amplitude. No perturbation calculation is admitted here.

## First shared inverse variant: CQA10

- Circular physical boundary: R0=6.2 m, a=0.62 m; p=0; canonical signed q=+1.5 on every surface; full toroidal flux Phi=6.400429545011558 Wb (=pi*a²*5.3 T).
- Authority: the existing [constant-q input](data/ordinary_controls_20261007/constant_q_A10_input.json). Phi is an input scale declared before comparison; Fedge, FFprime and total current are outputs. Circular boundary does not prescribe concentric flux surfaces.
- [Phase 3 definitions](phase3/cases.json) retain this E1 contract, add E2 at the same boundary/q/Phi with p_prime=-146292.26472199883 Pa/(Wb/rad), and prescribe the analytic Phase 1 Solovev q profile at A3. The [results contract](phase3/results/README.md) records pressure amplitudes, signed psi/Phi integration, native selectors and released F/current quantities.
- VMEC-family inputs prescribe iota and Phi with their recorded angle map. Public CHEASE uses NSTTP=5; MARS-associated CHEASE uses NSTTP=4. Those selector numbers have different source meanings and cannot be copied between codes.
- A zero-pressure solve normalized to Fedge can be converted to the declared Phi by the explicit positive homogeneity factor alpha=Phi_target/Phi_native. Scale psi, F, B and j by alpha; q and geometry remain unchanged. Retain raw outputs and the normalization receipt. No comparison error determines alpha.
- Toroidal-field reversal is a physical symmetry of this axisymmetric equilibrium: F and poloidal current reverse, while psi, toroidal current and FFprime remain fixed. It reverses Phi/q and preserves force balance. Declare this input construction separately from COCOS relabeling; global B reversal does not reverse q.
- KIN6D has a native zero-beta constant-q/Phi candidate with reviewed derivative repairs and 45/45 CPU/Debug gates on `3a73515`. Its port to current curved P2/P3 main and Phase 3 refinement/estimator qualification belong to the separate KIN6D lane; forward prescribed-FFprime results do not qualify inverse mode. FreeGS remains withdrawn after its upstream handoff.
- Acceptance requires native stopping, signed q/flux checks, independent force balance and boundary/profile/mesh refinement in every supported lane. TC24-q uses a separate pinned target and pressure/flux contract; it is not yet admitted by CQA10.

## Exact E0 oracles and VMEC++ map

- Polynomial: Psi=C*((R^2-R0^2)^2+4*R^2*Z^2), Delta_star Psi=16*C*R^2; p_prime=-16*C/mu0, F constant.
- C=F/(8*q_axis*R0^3), q_axis=1.5; box values use the exact analytic trace, not a fitted zero-boundary solution.
- Logarithmic: Psi=D*(R^2*log(R/R0)-(R^2-R0^2)/2+Z^2), Delta_star Psi=4*D; p=0, FF_prime=-4*D.
- Logarithmic F^2=F_axis^2+2*FF_prime*Psi; check positivity throughout the actual domain.
- Polynomial analytical LCFS variant: Psi_edge=4*C*R0^2*a^2; R(t)=sqrt(R0^2+2*R0*a*cos(t)), Z(t)=R0*a*sin(t)/R(t).
- Label it `analytic_lcfs_A10`; this exact finite-aspect-ratio LCFS is close to a circle but is not an exact circle.
- On s_pol surfaces replace a by a*sqrt(s_pol). With angular mean over t, q=q_axis*R0^3*mean(R^-3).
- Full toroidal flux: Phi=2*pi*F*R0^2*a^2*s_pol*mean(sin(t)^2/R^3).
- Pressure: p=(16*C/mu0)*Psi_edge*(1-s_pol). Map pressure and iota=1/q to s_tor=Phi/Phi_edge.
- VMEC++ uses this independently derived boundary/profile/flux map. Physical E1–E4 require admitted GS surface maps; a circular constant-iota pilot is not an equal-current comparison.

## Solver contracts

| Solver | Inputs and limitations | Independent check |
| --- | --- | --- |
| KIN6D GS | Native fixed-boundary 2D elliptic solve; forward source law | E0 exact fields, grid/boundary refinement, independent physical-point diagnostics |
| CHEASE public / MARS CHEASE | Freeze actual p/FF_prime or prescribed-q selector and normalization | Native input/output reconstruction and exact/physical case gates |
| FreeGS | Native rectangular fixed-boundary solve admits E0 exact trace | Exact trace and differential-operator convergence |
| FreeGS circle extension | Explicit FreeGS-backed staircase Dirichlet mask; not native exact curved LCFS | Boundary Hausdorff error versus h, manufactured curved-boundary convergence; report edge and interior separately |
| VMEC++ | Fixed-boundary Fourier representation, p(s_tor), iota/current selector and full Phi_edge | E0 exact profile map; mapped physical GS profiles and independent surface/field diagnostics |
| Original VMEC | Same variational family; multiple native profile models, separate auxiliary-table capacity | Exact E0 and explicit profile-approximation budget before TC24 admission |
| DESC | Native Fourier–Zernike equilibrium; Python-native profile classes/extensions | Signed analytical fields, native physical force and common R/Z points; imported VMEC state is a different representation |
| GVEC | Native Fourier/B-spline geometry; several profile/endpoint representations | Signed analytical fields, native projected norms and independently reconstructed force |

- The staircase extension retains FreeGS differential operators, freezes modified matrix rows and mask, and requires a boundary-error gate before physical comparison admission.
- An EQDSK reader that recomputes a coil fit is not an exact fixed-LCFS replay. A reader can inspect a source without establishing solver equivalence.
- Native total-current and total-flux constraints must match before comparing solver accuracy. Do not tune them after examining disagreement.
- E5 native derivative signs and stored field must pass reconstruction before its profiles become cross-code inputs.
- Profile capabilities, selected laws and source references: [profile models](PROFILE_MODELS.md). Table/interface restrictions are not global physics limits.

## Required evidence

- Metric authority: [weighted formulation and observable derivations](../research_notes/Equilibrium%20weak%20formulation%20error%20analysis/foundations.md), [executed metric inventory](../research_notes/Equilibrium%20weak%20formulation%20error%20analysis/metric_inventory.md) and its [source/formula records](../research_notes/Equilibrium%20weak%20formulation%20error%20analysis/metric_inventory.json), and [KIN6D forward bounds with explicit hypotheses](../research_notes/Equilibrium%20weak%20formulation%20error%20analysis/kin6d.md). A proved bound formula and a computed certificate satisfying its premises are separate records.
- Every metric record names its mathematical quantity and formula; discrete or continuum object and trial/test space; units, norm, measure, weights and domain; denominator or reference; reconstruction and derivative regularity; physical model, source/constraint and branch equivalence; bound assumptions/constants; and evidence status. Use explicit statuses: native algebraic correctness, reconstructed diagnostic, conditional estimate, or certified error bound. State missing premises for an uncertified quantity.
- Exact checks: analytical PDE residual, divergence, source derivatives, field components, force balance and q/flux identities under declared domain assumptions.
- Numerical checks: report errors and observed convergence over at least three independently refined resolutions when a convergence study is admitted. An empirical rate is conditional on the same problem/branch, mesh shape regularity and solution regularity, with iteration, source/data, profile-map and quadrature errors controlled. A three-point fit is not a theorem or a certified error bound; theorem-based claims need their actual hypotheses and certified constants.
- Separate geometry/Fourier, PDE mesh, profile-map, contour quadrature and interpolation convergence.
- Each matched case closes with a quantitative discrepancy budget: geometry,
  profile/input transfer, discretization, quadrature, iteration, reconstruction
  and floating-point terms, including coupled effects. Record proved bounds,
  conditional estimates and measured contributions separately. Bound overlap
  establishes compatibility; identifying a cause also requires a source argument
  or a controlled intervention that isolates the claimed mechanism.
- Scaling claims state the refined parameter, fixed physical problem, regularity,
  stability and mesh/representation hypotheses, constants and remainder. Use
  finite refinements to test the claim; an observed slope alone is not its proof.
- Evaluate B, p, j and j cross B-grad(p) at common physical points off the solver grid. Compare axis position, axis/edge flux, full toroidal flux, total current, pressure and q surfaces.
- Identify uniform query RMS separately from physical area/volume norms and contour integrals. A scalar finite-element energy bound controls a weighted volume poloidal-field error; classical current, strong force, contour q and axis/edge traces require their own derivative, level-set or trace bounds. Smooth reconstructed curl is an admissible diagnostic when its regularity is stated; its discrepancy alone does not identify a solver bug.
- Axis limits need regular analytic formulas; exclude coordinate singularities from naive division checks and test the limits separately.
- Curved-boundary approximations report boundary displacement and boundary-layer uncertainty. Interior residual alone cannot establish LCFS accuracy.
- Independently reconstruct source and force balance from output fields; an internal residual alone does not verify adapter signs or profile scaling.
- Native stopping, usable comparison output and physical accuracy are separate dispositions. A finite independent force is a measurement, not a passed accuracy gate.
- Before a metric-specific accuracy claim, use an exact solution or an independently bounded equivalent-problem reference on a common domain and branch. Account for source, model/map, boundary, reconstruction and quadrature errors in the relevant norm. Matched constant-pprime/FFprime forward E1–E4 are linear and unique on the declared fixed domain; mapped nested inverse inputs still require branch/source equivalence. Cross-code differences are bounded by the sum of individual error and transfer/input bounds, not by majority agreement.
- Reintegrate each assembled weak state using independent source quadrature across profile and geometry cuts. Report the executed discrete residual and independent integration discrepancy with their test spaces and norms. A full distributional-current/GS bound retains element, normal-flux jump, boundary/data and integration contributions. A free-basis Gram/Riesz norm measures the restricted dual residual; neither it nor a Euclidean coefficient norm bounds the unresolved test-space complement by itself. Discrete boundary reactions and raw physical normal traces remain separate observables.
- KIN6D mapped physical cells require one geometry identity and common physical
  coordinate/Jacobian path for stiffness, load and readback. Include the Hessian
  connection term and geometry-interface traces. Certified entry errors bound
  the discrete test norm; point quadrature itself is unbounded in the continuum
  energy dual. Actual positive-Jacobian/root and mapped-integral bounds remain
  prerequisites for a new solve. The [reviewed mathematical contract](../archive/equilibrium/dechurn/INDEX.md#certificates)
  admits no PDE execution or unsupported affine inverse/coarea fallback.
- Inverse-q/Phi qualification needs the full augmented state/source/constraint stability and branch/gauge argument; a fixed-source forward bound does not supply it. If a practical bound is unavailable, record the exact missing premise, reconstruction, constant or regularity estimate and the next check. Do not replace it with an arbitrary percentage cap. Native stopping and global invariants remain valid scoped observations while other metrics are uncertified.
- New PDE execution remains on the [PLAN admission hold](../PLAN.md#current-status-and-next-work) until the relevant formulation, metric and case gates are qualified and the controller separately registers/adopts the experiment. Completed records retain their seals and original scopes; native correctness and analysis gates continue. This contract update admits no run.
- Report absolute errors with units and dimensionless errors with an explicit scale. A near-zero quantity needs an absolute criterion.
- No fitted sign, phase, current, flux, radius, smoothing or geometry to obtain agreement.
- An unsupported inverse-q or geometry mode stays open with a specific next gate; no silent substitution.
- Scripts, inputs, compact data and manifests stay in repositories. Generated plots/PDFs are external artifacts linked from reports.
