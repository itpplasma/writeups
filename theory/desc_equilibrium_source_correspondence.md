# DESC equilibrium source correspondence

This companion serves colleagues comparing the axisymmetric equilibrium solvers in the TC24 programme. DESC solves ideal magnetohydrodynamic force balance using a global spectral geometry and a collocation residual. Matching that residual requires the same physical boundary, signed flux and continuous profiles; matching profile samples alone is insufficient.

- **Source correspondence** means a statement read from the pinned implementation, or an explicitly derived identity under stated assumptions. It establishes implemented equations, not convergence.
- **Probe** means a recorded numerical or visual observation. It has only the stated scope.
- **Unresolved** means evidence required for admission remains absent. Runtime sections below belong to the controller.

## Frozen sources

| Evidence | Pin and access | Status |
|---|---|---|
| DESC equilibrium solver | Official release `v0.17.3`, commit `fcc29be36f0b36b1b667df4b1f8891a9b633f5d1`; local `/tmp/tc24-desc-source-v0173-20261007`; [pinned source](https://github.com/PlasmaControl/DESC/tree/fcc29be36f0b36b1b667df4b1f8891a9b633f5d1) | Source correspondence; clean source checkout inspected on 2026-10-07 |
| Runtime dependency contract | Isolated `desc-opt==0.17.3`, Python 3.12.12, `jax==jaxlib==0.9.2`; five installed physics files match the release | Probe: TC24 `equilibrium/data/desc_20261007/environment.txt` and pre-execution receipts |
| Primary equilibrium paper | Panici, Conlin, Dudt, Unalmis and Kolemen; arXiv title *The DESC Stellarator Code Suite Part I: Quick and accurate equilibria computations*; [arXiv:2203.17173v3](https://arxiv.org/abs/2203.17173v3), 31 March 2023; journal *The DESC stellarator code suite. Part 1. Quick and accurate equilibria computations*, J. Plasma Phys. **89**, 955890303 (2023), [DOI](https://doi.org/10.1017/S0022377823000272) | Probe: both archived arXiv v3 and published journal typesetting inspected |
| Archived paper | `/mnt/files/archive/literature/iter_tc24-equilibrium-20261007/panici2023_desc_part1.pdf`; SHA-256 `aaab8fe33af8361a247c925b2917912844137ba3c1c3e743436fa323767ce9a1` | Probe: pages 9–10 rendered in memory and read; text `/tmp/panici_desc_part1_20261007.txt` |
| Published paper | `/mnt/files/archive/literature/iter_tc24-equilibrium-20261007/PaniciEtAl2023Published.pdf`; SHA-256 `067d9b11b0e763bfa2c1a0bc38211d7ae4c598465c249648d446fefa22ac30ca` | Probe: typeset page 7 and Appendix A pages 23–27 inspected; text `/tmp/panici_desc_published_20261007.txt` |
| VMEC++ spline comparator | Commit `a4150a4e2101bd47868d040f3adee5d0304ce89b`, `/tmp/tc24-vmecpp-source-20261007` | Source correspondence; clean source checkout inspected |
| Literature catalogue | Controller reports unavailable Zotero Web API credentials and no exact DESC-paper match from read-only local title queries | Unresolved: catalogue membership; archived paper supplies present evidence |
| Writeups integration base | `fff012776a0ffe0f94925e9658269e861a1a513f` | Source correspondence; worker writes this path only and does not promote |

## Ideal MHD and the geometric chart

**Source correspondence — assumptions.** Restrict this lane to static, scalar-pressure, nested-flux-surface equilibria with a fixed boundary. Set toroidal spectral resolution `N=0` for axisymmetry. DESC's three-dimensional representation remains useful for stating the coordinate and field identities. There is no perturbation or transport claim here.

The governing physical equations are

\[
\mathbf J\times\mathbf B-\nabla p=0,\qquad
\mu_0\mathbf J=\nabla\times\mathbf B,\qquad
\nabla\cdot\mathbf B=0,\qquad p=p(\rho).
\]

**Source correspondence — chart.** For the standard `Equilibrium` parameterization, `desc/compute/_core.py::_omega` returns zero and `_phi` sets \(\phi=\zeta\). Thus

\[
\mathbf x=(R\cos\zeta,R\sin\zeta,Z),\quad
\mathbf e_i=\partial_i\mathbf x,\quad \mathbf e^i=\nabla\alpha^i,
\quad \alpha=(\rho,\theta,\zeta),
\quad \mathcal J=\mathbf e_\rho\cdot(\mathbf e_\theta\times\mathbf e_\zeta).
\]

The native quantity `sqrt(g)` is this signed Jacobian (`desc/compute/_metric.py::_sqrtg`), not a separately evaluated positive square root. The admitted chart is right handed, so \(\mathcal J>0\) away from the axis. `desc/geometry/core.py::Surface._compute_orientation` identifies clockwise poloidal orientation as right handed; `_flip_orientation` reverses sine coefficients when required. This low-mode orientation check does not prove nesting throughout a solved volume.

**Source correspondence — derivatives and regularity.** `desc/basis.py::FourierZernikeBasis.evaluate` multiplies radial Zernike, poloidal Fourier and toroidal Fourier factors. Its `derivatives=(d_r,d_t,d_z)` argument differentiates the factors themselves. `desc/compute/_core.py` applies these transform matrices to the geometry and stream-function coefficients. No radial finite-difference approximation enters these native geometry derivatives.

\[
u(\rho,\theta,\zeta)=\sum_{lmn}u_{lmn}\,
\mathcal R_l^{|m|}(\rho)\,\mathcal F_m(\theta)\,\mathcal F_n(N_{FP}\zeta),
\quad u\in\{R,Z,\lambda\},
\quad \mathcal R_l^{|m|}=\rho^{|m|}P_{(l-|m|)/2}(\rho^2).
\]

Admissible modes obey \(l\geq |m|\) and even \(l-|m|\). Consequently each poloidal harmonic has the disk-regular form \(\rho^{|m|}\) times a polynomial in \(\rho^2\). This proves the basis' axis regularity under the chart assumptions; finite resolution and a folded coordinate map remain separate accuracy concerns. `_psi_r_over_sqrtg` and current routines implement explicit axis limits for otherwise indeterminate ratios.

## Native flux, magnetic field and current

**Source correspondence — signed flux.** `desc/compute/_profiles.py::_psi`, `_psi_r` and `_psi_rr` implement

\[
\psi_t(\rho)=\frac{\Psi_a}{2\pi}\rho^2,
\qquad \psi_t'=\frac{\Psi_a}{\pi}\rho,
\qquad \psi_t''=\frac{\Psi_a}{\pi}.
\]

Here native `psi` is toroidal flux per radian; `Psi` is the full signed toroidal flux through the boundary. The subscript \(t\) in this companion prevents confusion with a Grad–Shafranov solver's poloidal-flux variable. Neither quantity supplies a universal COCOS identifier by itself.

**Source correspondence — field construction.** Let \(\vartheta=\theta+\lambda\) denote the straight-field-line poloidal angle and define \(\chi'=\iota\psi_t'\). With \(\zeta=\phi\), the implemented field is

\[
\mathbf B=\nabla\psi_t\times\nabla\vartheta+
\nabla\zeta\times\nabla\chi,
\quad B^\rho=0,
\quad B^\theta=\frac{\psi_t'}{\mathcal J}(\iota-\lambda_\zeta),
\quad B^\zeta=\frac{\psi_t'}{\mathcal J}(1+\lambda_\theta).
\]

These are `_B_sup_rho`, `_B_sup_theta`, `_B_sup_zeta` and `_B` in `desc/compute/_field.py`, after substituting the standard chart's zero toroidal stream function. Thus \(\mathbf B\cdot\nabla\rho=0\), solenoidality follows from the cross-gradient representation, and \(d\vartheta/d\zeta=\iota\) along a field line. Covariant components are \(B_i=\mathbf B\cdot\mathbf e_i\).

**Source correspondence — current and force.** `desc/compute/_equil.py::_J_sup_rho`, `_J_sup_theta_sqrt_g` and `_J_sup_zeta` implement the right-handed curvilinear curl:

\[
\mu_0\mathcal J(J^\rho,J^\theta,J^\zeta)=
(B_{\zeta,\theta}-B_{\theta,\zeta},\,
B_{\rho,\zeta}-B_{\zeta,\rho},\,
B_{\theta,\rho}-B_{\rho,\theta}).
\]

Writing \(H=(B_{\zeta,\theta}-B_{\theta,\zeta})/\mu_0=\mathcal J J^\rho\) gives the actual residual decomposition

\[
F_\rho=\mathcal J(J^\theta B^\zeta-J^\zeta B^\theta)-p',
\quad F_\theta=-B^\zeta H,\quad F_\zeta=B^\theta H,
\quad \boldsymbol\beta=B^\zeta\nabla\theta-B^\theta\nabla\zeta,
\quad \mathbf F=F_\rho\nabla\rho-H\boldsymbol\beta.
\]

`_F_rho` reads `(curl(B)xB)_rho/mu_0-p_r`; `_F_helical` returns \(H\). The signed helical coefficient of \(\boldsymbol\beta\) in the physical force is therefore \(-H\), although the optimizer stores \(+H\). Its zero-target squared objective is invariant under this isolated sign change.

**Source correspondence — axisymmetric reduction.** For `N=0`, \(\chi=\chi(\rho)\) yields \(B_R=\chi_Z/R\), \(B_Z=-\chi_R/R\). Force balance makes \(F_B=RB_\phi\) a flux function, where \(F_B\) is distinct from the force residual. At regular points with nonzero \(\nabla\chi\), eliminating current gives

\[
\Delta^*\chi+F_B\frac{dF_B}{d\chi}+\mu_0R^2\frac{dp}{d\chi}=0,
\qquad \Delta^*=\partial_R^2-R^{-1}\partial_R+\partial_Z^2.
\]

This is a local mathematical correspondence with Grad–Shafranov force balance. It does not imply that a solver prescribing \(p(\psi_{pol})\) and \(F_B(\psi_{pol})\) solves the same boundary-value problem as DESC prescribing \(p(\rho)\) and \(\iota(\rho)\). If an external GS chart uses \(\mathbf B_{pol}=\nabla\psi_{pol}\times\nabla\phi\), its poloidal flux is \(\psi_{pol}=-\chi\), up to an additive constant.

**Checked signed GS bridge.** [Native FortSym source](cas/desc_gs_strong_correspondence.wl), [raw output](cas/desc_gs_strong_correspondence.native.txt), and [replay gate](cas/run_desc_gs_strong_native.sh) check ten exact identities. For smooth derivative jets, \(R>0\), \(\mu_0>0\), \(p=p(\psi)\), \(F_B=F_B(\psi)\), and canonical \(\psi=-\chi\):

\[
G=\Delta^*\psi+F_BF_B'+\mu_0R^2p',\qquad
\mathbf J\times\mathbf B-\nabla p=-\frac{G}{\mu_0R^2}(\psi_R,0,\psi_Z).
\]

- Also checks \(J_\phi=-\Delta^*\psi/(\mu_0R)\), the signed flux integral and a nonzero least-squares residual with zero objective gradient.
- Scope: conditional continuum algebra. No claim about executed source selection, numerical convergence, the axis or a folded chart.
- Shared GS/ideal-variation theory belongs to [kin6d](https://github.com/itpplasma/kin6d/tree/main/theory); this companion records the third-party correspondence without an upstream CAS dependency.

## Discrete force objective and constraints

**Source correspondence — default solve.** `Equilibrium.solve` defaults to `objective="force"`, `optimizer="lsq-exact"`; `objectives/getters.py::get_equilibrium_objective` selects `ForceBalance`. The unknowns include the spectral coefficients of \(R,Z,\lambda\). The scalar objective below assumes target zero, user weight one, no custom loss, normalization enabled and the standard constraints.

| Stage | Executed expression or constraint | Pinned routine |
|---|---|---|
| Collocation | Default `ConcentricGrid(L_grid,M_grid,N_grid,NFP,sym,axis=False)`; \(n\) nodes and \(2n\) residual entries | `objectives/_equilibrium.py::ForceBalance.build` |
| Raw radial entry | \(r_{\rho i}=F_{\rho i}|\nabla\rho|_i\mathcal J_i\) | `ForceBalance.compute` |
| Raw helical entry | \(r_{hi}=H_i|\mathcal J\boldsymbol\beta|_i\) | `ForceBalance.compute`; `_e_sup_helical_sqrtg` in `compute/_equil.py` |
| Grid factor | \(w_i=\sqrt n\,\omega_i\), \(\omega_i=\texttt{grid.weights}_i\), tiled over both residual blocks | `objectives/objective_funs.py::_Objective.build` |
| Normalized entry | \(\widehat r_i=w_i r_i/f_0\), multiplied by explicit user `weight` when supplied | `_Objective._scale` |
| Minimized scalar | \(\mathcal L=\tfrac12\sum_i(\widehat r_{\rho i}^2+\widehat r_{hi}^2)\) | `_Objective.compute_scalar` |
| Fixed physical inputs | `FixBoundaryR`, `FixBoundaryZ`, `FixPsi`, every assigned profile constraint, `FixSheetCurrent` | `get_fixed_boundary_constraints` |
| Internal consistency | Boundary and axis coefficient consistency; `FixLambdaGauge` when applicable | `maybe_add_self_consistency`; `linear_objectives.py` |
| Profile choice | Supplying both `iota` and `current` raises an error | `Equilibrium.__init__` |

**Source correspondence — quadrature.** `grid.weights` contains coordinate integration weights. `ConcentricGrid` uses `_scale_weights` to account for duplicate nodes and scale their sum to \(4\pi^2\), including full-torus accounting for field periods. Physical volume contributes the Jacobian already present in the raw residual. Thus the least-squares cost uses \(\omega_i^2\mathcal J_i^2\), not a plain quadrature of \(|\mathbf F|^2\mathcal J\). The radial and helical basis vectors also need not be orthogonal. This objective vanishes at exact force balance, but its finite residual is not a physical volume RMS of the full vector force.

**Source correspondence — normalization.** `objectives/normalization.py::compute_scaling_factors` defines

\[
a_0=\sqrt{|R_{\max}Z_{\max}|},\quad A_0=\pi a_0^2,
\quad V_0=2\pi R_{00}A_0,\quad B_0=1.25|\Psi_a|/A_0,
\quad f_0=\frac{B_0^2}{2\mu_0a_0}V_0.
\]

\(R_{\max},Z_{\max}\) are the largest-magnitude nonconstant boundary coefficients selected by the code. Numerically near-zero scaling factors are replaced by one. This boundary-derived force scale is an optimization normalization; pressure normalization and an independent physical residual need separate reporting.

**Source correspondence — variational distinction.** This force collocation lane has no Galerkin weak form obtained by integrating force balance against trial functions. DESC also provides `Energy`, implementing \(\int[B^2/(2\mu_0)+p/(\gamma-1)]\,dV\), with default `gamma=0` (`_W_B`, `_W_p`, `_W` in `compute/_equil.py`). Selecting that scalar objective changes the discrete problem. An ideal-MHD variational derivation additionally needs admissible magnetic-flux and thermodynamic variations; equating an arbitrary prescribed-profile energy minimization to those variations remains unresolved unless its constraints are derived. Energy-objective availability does not turn the default force least-squares solve into VMEC's discrete variational algorithm.

## Input and convention correspondence

**Source correspondence — scoped VMEC map.** Assume the same cylindrical toroidal angle, a VMEC geometric poloidal angle increasing counterclockwise, and the right-handed DESC chart. Preserve the signed physical toroidal flux and reverse the poloidal angle:

\[
\theta_D=-\theta_V,\quad \zeta_D=\zeta_V,\quad \rho_D=\sqrt{s_V},
\quad \iota_D=-\iota_V,\quad \Psi_D=\Phi_V.
\]

For a consistent straight-angle map, \(\lambda_D(\rho,\theta_D,\zeta)=-\lambda_V(s,-\theta_D,\zeta)\). The geometry is \(R_D(\rho,\theta_D)=R_V(s,-\theta_D)\), with the same expression for \(Z\); poloidal sine coefficients change sign. These are coordinate relabelings, not a physical reversal of \(\mathbf B\). A physical-field reconstruction probe is still required for each executed adapter.

**Source correspondence — native profile representations.** The complete class inventory at this pin is below. Here \(x=\rho\) for radial profiles; Fourier–Zernike profiles additionally support angular dependence. For the scalar-pressure nested-surface case, use flux-function profiles, with `M=N=0` when choosing the latter representation.

| Class | Function and stored parameters | Source in `desc/profiles.py` |
|---|---|---|
| `_Profile` | Extension interface: `params` getter/setter and `compute(grid,params,dr,dt,dz)`; `IOAble` serialization metadata | line 25 |
| `ScaledProfile` | \(a f(x)\); scale and wrapped profile parameters | line 266 |
| `PowerProfile` | \(f(x)^a\); exponent and wrapped profile parameters | line 356 |
| `SumProfile` | \(\sum_j f_j(x)\); concatenated constituent parameters | line 478 |
| `ProductProfile` | \(\prod_j f_j(x)\); concatenated constituent parameters | line 565 |
| `PowerSeriesProfile` | \(\sum_l a_lx^l\); coefficients, modes and even/all-power selection | line 662 |
| `TwoPowerProfile` | \(a_0(1-x^{a_1})^{a_2}\); three parameters | line 839 |
| `SplineProfile` | Interpolated values at knots; nearest, linear, local cubic, natural C2 cubic or Catmull–Rom method | line 942 |
| `HermiteSplineProfile` | Piecewise cubic in \(x\); knot values and first derivatives | line 1041 |
| `MTanhProfile` | Modified-tanh pedestal plus core polynomial; height, offset, location, width and polynomial coefficients | line 1136 |
| `FourierZernikeProfile` | Global Fourier–Zernike expansion; coefficients, `(l,m,n)` modes, symmetry and `NFP` | line 1378 |

**Source correspondence — composition and derivatives.** The first four concrete classes combine profile values evaluated on the same grid; `PowerProfile` raises values to a power and does not replace the argument by \(\rho^2\). `PowerProfile` and `MTanhProfile` implement radial derivatives through order two; `PowerProfile` and `ProductProfile` reject angular derivatives. Other representations have their own derivative implementation and regularity conditions. Native fitting/conversion routes include `PowerSeriesProfile.from_values`, `FourierZernikeProfile.from_values`, `MTanhProfile.from_values` and `_Profile` conversion helpers.

**Source correspondence — Python API and text CLI.** `desc/equilibrium/utils.py::parse_profile` accepts any `_Profile` subclass unchanged. It converts scalars and one-dimensional coefficient arrays to `PowerSeriesProfile`, and two-column arrays to specified power-series modes/coefficients. `Equilibrium` constructors and profile setters use this ingress. The native text reader `desc/input_reader.py::InputReader.parse_inputs` instead reads `l`, `p`, `i` and `c` coefficients into power-series tables; `desc/__main__.py` constructs equilibria from those parsed inputs. Its `parse_vmec_inputs` path reads `AM/AI/AC`, maps their \(s\) powers to even \(\rho\) powers, and warns for non-`power_series` profile types. It does not import the executed `AM_AUX_S/F` and `AI_AUX_S/F` spline contracts. These CLI choices do not restrict the Python API's profile types.

**Source correspondence — exact case contract.** The pinned VMEC++ `radial_profiles.cc::BuildCubicSecondDerivatives` clamps endpoint slopes using quadratics through the nearest three samples; `RadialProfiles::evalCubic` evaluates the spline in \(s\). The prepared TC24 deck has 129 pressure knots and 129 transform knots, giving 128 intervals each. A cubic \(P(s)\) becomes a piecewise even sextic \(P(\rho^2)\). Native cubic `SplineProfile` or `HermiteSplineProfile` in \(\rho\) generally differs even when knot values match. A finite global `PowerSeriesProfile`, or radial `FourierZernikeProfile`, exactly represents global polynomial cases, but generally cannot equal a spline whose polynomial coefficients change across intervals.

**Source correspondence — chosen extension.** The external [`StoredFluxCubicProfile`](/home/ert/proj/iter_tc24/equilibrium/adapters/desc_profile_contract.py) uses the supported `_Profile` interface to evaluate the original interval coefficients at \(s=\rho^2\). Its `compute` method uses JAX arrays and supports radial orders zero through three; `_io_attrs_` and `_static_attrs` retain coefficient/knot state for the established I/O and tracing path. It supplies \(p_D'=2\rho P_s\), \(p_D''=2P_s+4\rho^2P_{ss}\), and the signed map \(\iota_D(\rho)=-I_V(\rho^2)\). This extension was chosen to preserve one fixed continuous input contract directly; it is not a missing DESC physics feature or a general limitation to splines.

**Probe — exact extension admission.** Retained gates check an independently specified quadratic in \(s\), its chain derivatives through order three, JAX tracing and all four literal boundary parities. The E0 signed physical fields and profiles pass both native-chart and independently selected physical-point oracles. Both executed states retain exact adapter and input hashes. Native fitted profiles remain an alternative if their value and required-derivative errors against the frozen law are measured and accepted; matching knots alone supplies no such bound. Alternative composite representations and TC24 convergence remain unresolved.

## Paper and code ledger

The paper describes force collocation and Fourier–Zernike geometry in arXiv equations 19–31, corresponding to journal equations 3.16–3.28. This ledger covers both archived versions and the pinned implementation. All potential paper errata remain provisional candidates; correspondence with the historical evaluator and any additional metric assumptions remains unresolved. [Panici et al., published article](https://doi.org/10.1017/S0022377823000272)

| Item | Qualified finding and consequence | Evidence status |
|---|---|---|
| ArXiv 25; journal 3.22 | Candidate missing flux factor: both print \(\nabla\rho\times\nabla\vartheta\). Under their normalized-radius definition, multiplying by \(\psi_t'\) recovers the subsequent field components. | Probe: typeset arXiv page 9 and journal page 7; source correspondence: `_psi_r` and `_B_sup_theta/_B_sup_zeta`; historical evaluator unresolved |
| ArXiv 27a; journal 3.24a | Both print \(\mathbf B\cdot\mathbf e^\rho=0\), using the reciprocal basis correctly. Text extraction obscures the superscript. | Probe: typeset arXiv page 10 and journal page 7 |
| ArXiv 28–30; journal 3.25–3.27 | Candidate inconsistent residual convention: both reconstruct \(\nabla p-\mathbf J\times\mathbf B\), opposite arXiv 2, journal 1.2 and native `_F_rho`. Appendix A8a explicitly adopts that reversed residual. Zero-target squared residuals are unaffected. | Probe: typeset equations; source correspondence: signed curl/force identities with SI \(\mu_0\); no implementation defect established |
| ArXiv 31; journal 3.28 | Jacobian/basis norms enter `ForceBalance.compute`; coordinate weights and \(\sqrt n\) enter `_Objective.build`. Raw entries miss final weighting. | Source correspondence: exact current cost above; historical-code identity unresolved |
| Journal A18 | Candidate missing metric cross term under the printed A10–A11 definition of \(\boldsymbol\beta\). The two-term expression applies when that term vanishes. | Probe: journal pages 25–26 and counterexample below; derived source correspondence: metric identity; historical evaluator/extra assumptions unresolved |
| Native helical labels | `e^helical` and its Jacobian-weighted label print the opposite signed vector to their functions. Actual \(\boldsymbol\beta=B^\zeta\nabla\theta-B^\theta\nabla\zeta\). | Confirmed metadata defect at benchmark `fcc29be` and official tip `6296faa`; independent Cartesian \(\mathbf B\times\mathbf e_\rho\) oracle; numerical formulas unchanged |
| Native weighted-basis units | `e^helical*sqrt(g)` and its norm advertise `T*m²`; actual units are `T*m`. Uniform physical-length scaling gives one power, not two. | Confirmed metadata defect at both pins; direct-function scaling oracle; [sign errata](https://gitlab.tugraz.at/plasma/proj/plasma-sign-conventions/-/blob/main/docs/DESC_HELICAL_METADATA_ERRATA.md); focused fork patch pending controller review |

## Physical force reconstructed from VMEC geometry

**Source correspondence — reconstruction route.** Published Appendix A supplies an independent field-and-force calculation from VMEC's \(R,Z,\lambda\) Fourier coefficients and flux/pressure profiles. It does not require native `bsupu`, `bsupv` or `bsub*` field arrays. It constructs its own field components and derivatives from geometry (A2–A7, A12–A16). It is an independent evaluator of the exported solution, not an independent equilibrium solution.

**Source correspondence — required state.** Read full-mesh geometry coefficients, half-mesh \(\lambda\) coefficients, signed toroidal and poloidal flux derivatives or their equivalent signed transform profile, and pressure. Include the sine/cosine families present in the executed symmetry mode. Retain native radial meshes and Fourier phase/mode conventions, including whether toroidal mode numbers already contain `NFP`. Native processed field-component arrays can be omitted entirely.

For \(\alpha=(s,u,v)\), \(v=\phi\), reconstruct a Cartesian position \(\mathbf x=(R\cos v,R\sin v,Z)\). Then compute

\[
\mathbf e_i=\partial_i\mathbf x,\quad
\mathcal J=\mathbf e_s\cdot(\mathbf e_u\times\mathbf e_v),\quad
\mathbf e^s=\frac{\mathbf e_u\times\mathbf e_v}{\mathcal J},
\quad\mathbf e^u=\frac{\mathbf e_v\times\mathbf e_s}{\mathcal J},
\quad\mathbf e^v=\frac{\mathbf e_s\times\mathbf e_u}{\mathcal J}.
\]

**Source correspondence — derivative requirements.** Evaluate \(R,Z\) and their first/second derivatives, \(\lambda_u,\lambda_v\) and the mixed/angular second derivatives \(\lambda_{su},\lambda_{sv},\lambda_{uu},\lambda_{uv},\lambda_{vv}\), together with \(p_s,\psi_s,\psi_{ss},\chi_s,\chi_{ss}\). For an independently enforced \(\chi_s=\iota\psi_s\), use \(\chi_{ss}=\iota_s\psi_s+\iota\psi_{ss}\). Under Appendix A1's exact \(s=\psi/\psi_a\), \(\psi_s=\psi_a\) and \(\psi_{ss}=0\); verify that the executed export uses this radial label before imposing it.

**Source correspondence — implementation identities.** Define \(a=\chi_s-\psi_s\lambda_v\), \(b=\psi_s(1+\lambda_u)\). Then

\[
B^s=0,\quad B^u=a/\mathcal J,\quad B^v=b/\mathcal J,
\quad\mathbf B=B^u\mathbf e_u+B^v\mathbf e_v,
\quad B_i=\mathbf B\cdot\mathbf e_i.
\]

For \(k\in\{s,u,v\}\), differentiate the signed Jacobian by the triple-product rule and use

\[
\partial_k B^u=\frac{a_k-B^u\mathcal J_k}{\mathcal J},\qquad
\partial_k B^v=\frac{b_k-B^v\mathcal J_k}{\mathcal J},
\quad\partial_k B_i=(\partial_k\mathbf B)\cdot\mathbf e_i+
\mathbf B\cdot\partial_k\mathbf e_i,
\]
\[
(a_s,a_u,a_v)=(\chi_{ss}-\psi_{ss}\lambda_v-\psi_s\lambda_{sv},
-\psi_s\lambda_{uv},-\psi_s\lambda_{vv}),
\quad(b_s,b_u,b_v)=(\psi_{ss}(1+\lambda_u)+\psi_s\lambda_{su},
\psi_s\lambda_{uu},\psi_s\lambda_{uv}).
\]

The curvilinear curl then reconstructs the physical current and residual directly:

\[
\mu_0\mathcal J(J^s,J^u,J^v)=
(B_{v,u}-B_{u,v},B_{s,v}-B_{v,s},B_{u,s}-B_{s,u}),
\quad\mathbf J=\sum_iJ^i\mathbf e_i,
\quad\mathbf F_{native}=\mathbf J\times\mathbf B-p_s\mathbf e^s.
\]

Cartesian differentiation automatically includes rotation of the cylindrical basis. A cylindrical implementation must explicitly include \(\partial_v\widehat{\mathbf e}_R=\widehat{\mathbf e}_\phi\), \(\partial_v\widehat{\mathbf e}_\phi=-\widehat{\mathbf e}_R\); differentiating only cylindrical component triples loses those terms. Retain the signed \(\mathcal J\) in field and curl identities; use \(|\mathcal J|\) in physical volume integrals.

**Source correspondence — axisymmetric specialization.** With all scalar \(v\)-derivatives zero, the same route simplifies to

\[
\mathcal J=R(Z_sR_u-R_sZ_u),\quad
(B_R,B_\phi,B_Z)=(B^uR_u,B^vR,B^uZ_u),
\]
\[
B_s=B^u(R_uR_s+Z_uZ_s),\quad
B_u=B^u(R_u^2+Z_u^2),\quad B_v=B^vR^2,
\quad \mu_0\mathcal J(J^s,J^u,J^v)=
(\partial_uB_v,-\partial_sB_v,\partial_sB_u-\partial_uB_s).
\]

These equations keep coordinate components distinct from the physical cylindrical components. The latter are reconstructed as \((J_R,J_\phi,J_Z)=(J^sR_s+J^uR_u,J^vR,J^sZ_s+J^uZ_u)\), with \(\nabla s=(Z_u,0,-R_u)/(Z_uR_s-R_uZ_s)\). This supplies a direct cylindrical-vector residual at each regular chart point without assuming the solution already satisfies Grad–Shafranov force balance.

**Source correspondence — full force norm.** With Appendix A's reversed force convention, \(F_s=\mathcal J(J^vB^u-J^uB^v)+p_s\), \(F_\beta=J^s\), \(\boldsymbol\beta=\mathcal J(B^v\mathbf e^u-B^u\mathbf e^v)\), and \(g^{ij}=\mathbf e^i\cdot\mathbf e^j\), the general identity is

\[
|\mathbf F|^2=F_s^2g^{ss}+F_\beta^2|\boldsymbol\beta|^2
+2F_sF_\beta\mathcal J(B^vg^{su}-B^ug^{sv}),
\quad |\boldsymbol\beta|^2=\mathcal J^2[(B^v)^2g^{uu}+(B^u)^2g^{vv}-2B^uB^vg^{uv}].
\]

The original printed definition obeys \(\boldsymbol\beta=\mathbf B\times\mathbf e_s\), with the covariant vector \(\mathbf e_s=\partial_s\mathbf x\). It is perpendicular to \(\mathbf e_s\); it generally differs from \(\mathbf B\times\nabla s\) and need not be perpendicular to \(\nabla s\). The cross term persists in an axisymmetric chart when \(g^{su}\ne0\). It vanishes if either force coefficient is zero or \(\nabla s\cdot\boldsymbol\beta=0\). Direct Cartesian evaluation produces the same norm for either global force sign. Whether the historical evaluator imposes a condition that makes A18 valid remains unresolved.

**Probe — A18 counterexample.** At one point choose \(\mathbf e_s=(1,0,0)\), \(\mathbf e_u=(1,1,0)\), \(\mathbf e_v=(0,0,1)\), so \(\mathcal J=1\), \(\mathbf e^s=(1,-1,0)\). Let \(B^u=1,B^v=2\), \(\mathbf J=(1,0,0)\), \(p_s=1\). Then \(\boldsymbol\beta=(0,2,-1)\), \(F_s=F_\beta=1\). Independently evaluating \(\nabla p-\mathbf J\times\mathbf B=(1,1,-1)\) gives squared norm 3; A18's two terms give 7 and the missing cross term is −4. This is an algebraic local counterexample, not a global equilibrium fixture.

**Probe — retained exact algebra.** The controller's [native FortSym source](cas/desc_force_correspondence.wl), [runner](cas/run_desc_force_native.sh) and [raw output](cas/desc_force_correspondence.native.txt) retain ten zero-valued exact checks. They cover straight-field-line differentiation, toroidal-flux normalization, curl/Lorentz correspondence, helical signs, zero-target sign invariance, the complete metric norm, angle reversal and the cubic \(s=\rho^2\) chain rule. Its separate positive-definite-metric example gives full squared norm 3 versus omitted-cross norm 4. These checks establish conditional algebra; they do not establish equilibrium convergence or execution of the solver's source path.

**Source correspondence — inherited numerical state.** The route inherits VMEC's solved Fourier geometry, stream function, truncation and radial resolution. Appendix A notes that \(\lambda\) is stored on a half mesh and interpolated to the main mesh; all radial derivatives of \(R,Z,\lambda\) are numerical. Its implementation therefore needs an explicit interpolation/differentiation contract. A continuous spline evaluator changes the reconstructed derivatives even when all original samples match. It also inherits whatever pressure/transform values are taken from exported data; using executed prescribed profiles avoids substituting a different interpolated law. These dependencies remain after eliminating processed magnetic-field arrays.

- **Unresolved — reconstruction convergence:** compare at least two radial differentiation/interpolation orders, refine the exported solution independently, and report near-axis/edge handling. Appendix A's derivation supplies no unique radial interpolation contract.
- **Unresolved — physical evaluation:** use explicit physical sampling points, invert the reconstructed chart as needed, and retain mapping errors separately from force errors. Exclude singular points only with a stated domain and additional axis/edge checks.
- **Unresolved — historical reproducer:** the paper names a [Zenodo data/scripts archive](https://doi.org/10.5281/zenodo.6539680); its exact force-evaluator implementation has not been audited here.

## Runtime admission evidence

| Controller-owned evidence | Required disposition | Present status |
|---|---|---|
| Exact E0 oracle | L=18, M=17; 20 iterations, native gtol termination | Probe: field RMS error 1.98e-12, Bpol 2.68e-11, pressure 6.95e-12; independent force/grad(p) 4.98e-9 |
| Frozen coarse TC24 boundary | L=24, M=23; complete four-parity boundary, signed flux and exact retained pressure/iota laws | Probe: stopped at 80 iterations; force/grad(p) 0.22456. **Unconverged diagnostic; not an admitted reference.** |
| Physical-field convention | Native E0 fields match the signed polynomial oracle; full-B and toroidal-only fixed-state reversals | Probe: exact reversal relations and unchanged geometry; these are native field controls, not solver replays |
| Refinement | Independent spectral and collocation refinement; off-grid residuals; distinguish profile, boundary and numerical errors | Unresolved; no convergence claim in this correspondence |
| Run provenance | Source/deck/command/output hashes and PID/time receipts retained under TC24 `equilibrium/data/desc_20261007` | Probe: E0 registry 771 and TC24 registry 773; failed E0 r01 retained with honest registry sequencing correction |

Independent continuous validation must evaluate the physical vector residual on points outside the solve grid and report the pressure-gradient and Lorentz-force scales used for normalization. Agreement of two unconverged outputs is not an error bound. The controller owns numerical admission and cross-code discrepancy dispositions.

- Controller10/10 native signed-GS replay passed2026-10-07; [metadata fork PR2](https://github.com/itpplasma/DESC/pull/2) corrects labels/units without changing numerical bodies. [Callback fork PR1](https://github.com/itpplasma/DESC/pull/1) and the separately pinned0.17.3 backport retain accepted diagnostics; they do not certify convergence.
