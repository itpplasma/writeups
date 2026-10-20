# GVEC free-boundary source correspondence

Citations `[@key]` refer to [writeups.bib](../writeups.bib).

- Scope: GVEC's experimental free-boundary loop (plasma energy, BIEST exterior field, coil field, boundary update and termination), our fork's Newton variant, and the axisymmetric TC24 runs. Fixed-boundary conventions are in the [GVEC equilibrium correspondence](gvec_equilibrium_source_correspondence.md) and the [discrete force audit](gvec_discrete_force_audit.md).
- Upstream: [gvec-group/gvec 7da1182fd81b1ba552142bb663319d74c7edfb8b](https://gitlab.mpcdf.mpg.de/gvec-group/gvec/-/tree/7da1182fd81b1ba552142bb663319d74c7edfb8b), branch `free_boundary_three_step` (MR !168, Draft, milestone v1.6), commit date 2026-10-19.
- Fork: [itpplasma/gvec 086b2b25dd1f51acceafbcdc8993c5052b3e462e](https://github.com/itpplasma/gvec/tree/086b2b25dd1f51acceafbcdc8993c5052b3e462e), branch `develop`, commit date 2026-10-20 (previous pin b37d82b3c3c27589061f2bddc00bbb25139e2ffe, an ancestor; changes since then under [Our fork](#our-fork)). It merges upstream 7da1182f (d660cb3b) and the earlier fork line `equilibrium/fb-newton-gtol-20261013` at ca733fe416f0dfda95e3b943a155617e35da63b3 (0065137c). That line branched from upstream 1ac00be4 (2026-10-01); the TC24 runs below used its commit a507bd82e825a2202e7004efb37617ba716131f9. [V]
- Vacuum solver: [fbtools 14a5c4a7c3ff7458780edf7ebb0bd76712b44fbf](https://gitlab.mpcdf.mpg.de/nmpp-mhd-group/fhindenlang/fbtools/-/tree/14a5c4a7c3ff7458780edf7ebb0bd76712b44fbf) with submodule [BIEST 6944d5c0fb1e5e2eb12868749e1a1f829601dc63](https://github.com/dmalhotra/BIEST/tree/6944d5c0fb1e5e2eb12868749e1a1f829601dc63).
- Paths below are relative to these trees. `free_boundary.py` is `python/gvec/core/run/free_boundary.py`; `evalfunc` is `src/functionals/mhd3d/mhd3d_evalfunc.F90`; `mhd3d.F90` is `src/functionals/mhd3d/mhd3d.F90`; `txx` is BIEST `include/biest/vacuum-field.txx`. Line numbers are for 7da1182f unless marked fork (086b2b25) or given with another commit.
- Labels: **[V]** checked against the pinned source, run record or a reference; **[D]** derived here or in the [derivation companion](gvec_free_boundary_derivation.md); **[H]** hypothesis, not tested.
- Status: source correspondence and first-variation algebra checked. Upstream GVEC has no derivation document, no convergence argument and no free-boundary test with assertions. The fork adds free-boundary regressions with physical oracles (below). Nothing here proves that the GVEC iteration converges.
- Native evidence for the convergence questions is KIN6D, not this file. On itpplasma/kin6d `main` at f5420f386bf9e032eec99b0df1f99016a66ac043: the formulation and proof-obligation map `docs/free-boundary-theory.md`; derivations `theory/derivations/free-boundary-first-variation.md`, `free-boundary-gauge-vertical.md`, `free-boundary-iterations.md`, `free-boundary-landreman-benchmark.md`; Lean bordering lemmas B1 and B2 in `proof/Kin6d/Bordered.lean` (`lemma_B1` :103, `lemma_B2` :565); hypothesis diagnostics (`ideal_fb_hypotheses`, slide gauge) in `src/mhd/ideal_free_boundary.f90`; measurements in `docs/ideal-free-boundary.md` and `docs/gs-free-boundary.md`. `docs/ideal-free-boundary.md` has changed since 73891c54a71c3a080826043fd02924779a6e79a3; the numbers cited below are unchanged. Proofs are not repeated here.

## Genealogy

| Stage | Branch, commits | Content |
|---|---|---|
| 2022 experiment | `free_boundary_experiments` 3baf54e4fc62ed4866a215140ea7856a4905a615 (2022-12-07, Hindenlang) | 2D cylinder with a prescribed background B_ext². Commit message: B_ext² "should have a minimum such that the boundary perturbations and the free-boundary iteration are stable"; preconditioning "does not work yet"; m_max=1. [V] |
| 2025 free_boundary | `free_boundary` 84544b74 (2025-03-31, experiment moved onto develop) … e5da31fd (2025-10-24) | Filament Biot–Savart (49d5c779, 2025-08-06), coil save/load; virtual-casing route, later made optional (e5da31fd "Removed requirement for virtual_casing module"). [V] |
| 2026 three_step | `free_boundary_three_step` aaca911354d979ad491e804ad6529c8a4e4171d9 (2026-02-02) "alternative free boundary based on Merkel approach"; 399778b847039257b05df8cb4f461b91bfdb86ba (2026-02-10) "update to a three-step approach" … 7da1182f | Boundary update from a pressure-balance force, blending into the interior, fixed-boundary re-solve; BIEST exterior field; free-boundary minimizer family. 144 commits not on `free_boundary` or `develop`. [V] |

- The "Merkel approach" in aaca9113 is not further specified in code or docs. The frozen-vacuum-pressure boundary force matches the VMEC/NESTOR idea [@hirshman1986; @merkel1986]; the attribution is ours. [H]
- `docs/generators/references.bib` carries the VMEC free-boundary and spectral-condensation entries, but no document cites them. The JOSS paper [@hindenlang2026] does not mention free boundary. [V]

## Continuous model as implemented

| Ingredient | Implemented form | Source | Status |
|---|---|---|---|
| Plasma | Fixed-boundary GVEC energy `W = dthet_dzeta (½ Wmag + mu0/(γ−1) Wpres)`, i.e. μ0×(magnetic + internal) energy at frozen Φ, χ profiles; free boundary adds no term | `evalfunc:539` | [V] |
| Coil field | Filament segments, Hanson–Hirshman formula [@hanson2002] (cited at `src/pygvec/BiotSavart.F90:15–19`); prefactor μ0/(4π) | `python/gvec/coils.py:137` | [V]; `BiotSavart.F90:118` documents μ0/(2π) (#97) |
| Exterior plasma field | `B_ext = B_coil + B_pl`, `B_pl = ∇S[σ] + ∇×S[J0]·I0`, S the Laplace single layer; σ from GMRES on `n·∇S[σ] − σ/2 = (B_coil + B0)·n` (exterior jump) | `txx:120–125`, `:128–129`, `:201` | [V] [@malhotra2019; @malhotra2020] |
| Topology | J0 a harmonic toroidal surface current from a Hodge decomposition, oriented along BIEST's toroidal tangent `Xt_` (first array index; GVEC passes toroidal-first arrays) and normalized so that its field has unit poloidal circulation | `txx:74–79, 133–160` | Normalization not derived in docs [H] |
| Plasma current | `I0 = μ0 I_tor(ρ=1)`, from the `I_tor` profile if set, else evaluated from the state | `free_boundary.py:414–420, 555–561, 925–931` | [V] |
| Toroidal flux | `PhiEdge` prescribed, not matched to coil flux; `coils.get_phi_edge_from_coils` exists but is not called by the run | `coils.py:961` | [V] |
| Boundary condition | Pressure balance `[[B²/2 + μ0 p]] = 0` only; interior B·n=0 by nested surfaces, exterior B·n=0 by BIEST; tangential jump allowed (diagnostic K = n×[[B]]/μ0) | `minimize.py:722`; `free_boundary.py:200` | [V] |
| Vacuum energy | Not evaluated anywhere | — | [V] |

- The method is an indirect single-layer Neumann BIE plus one harmonic field. It is neither NESTOR's scalar potential [@merkel1986] nor virtual casing [@shafranov1972; @drevlak2005]. [V]
- The exterior of a solid torus has first Betti number 1, so B·n on Γ and one poloidal circulation fix the exterior field. The code supplies both. The fbtools docstring (`python/fbtools/exterior_vacuum_field.py:13,30`) writes the circulation without μ0; the code passes μ0 I. [V]
- Related free-boundary codes for comparison of formulations: VMEC/NESTOR [@hirshman1986], SPEC [@hudson2020], DESC [@conlin2024]. No GVEC benchmark against any of them exists. [V]

## Three-step algorithm and termination

`FreeBoundaryRun._run_stage` (`free_boundary.py:265–640`):

1. Initial fixed-boundary solve (`:405`), `I_tor(1)` (`:414–420`), BIEST → B_ext² (`:423`).
2. For each update (`:437`): termination tests (`:469–497`), step-size heuristic (`:510–515`), then `_free_boundary_update` (`:529`; `minimize.py:733–769`):
   - `set_Bext_squared(B2)` stores the latest B_ext² without a size check (`src/pygvec/state.F90:135–144`);
   - `update_boundary_MHD3D` (`mhd3d.F90:1334–1428`) re-evaluates the force with this B_ext² (`:1383`), optionally divides by the boundary diagonal preconditioner, asks the free-boundary minimizer for a step (`:1392`), blends it into the interior with `((1+cos(π(ξ−1)))/2)^m` over s∈[1−depth,1] (`:1312–1330`, depth 0.6), and on detJ<0 scales the step by 0.9 and resets the minimizer, up to 130 times (`:1381–1420`);
   - fixed-boundary re-solve at the ramped `minimize_tol` (`:453–466`).
   Then `I_tor(1)` (`:555–561`) and BIEST again (`:563–572`).
3. Final fixed-boundary solve at `minimize_tol_min` (`:618–624`).

- Minimizers: GD, mGD, aGD, ADAM, BFGS, dBFGS (Powell damping), SR1, lBFGS (`src/free_b_minimize/*.F90`; selection `mhd3d.F90:544–585`). The quasi-Newton family disables the boundary preconditioner (`:561–581`). GD, mGD, aGD, BFGS, dBFGS and lBFGS use positive-definite metrics; SR1 can be indefinite. [V]
- For m=0 the blend is 1 for every s, so m=0 boundary steps move the whole volume including the axis (`mhd3d.F90:1324–1325`). [V]
- Stop tests, in order: target ≤ `tolerance`; `fdelta` ≤ `ftol` (1e-5, absolute); `xnorm_mavg` ≤ `xtol` (1e-5) with `xnorm = xnorm_fb/dt` (`:553`); `gnorm_mavg` ≤ `gtol` (1e-8); resolved-force ratio ≤ limit (`:151–166`). The window is 10 but statistics use from update 1 on (`:224–251`). Defaults `:37–42`. [V]
- Target: Jacobian-weighted mean of `|[[B²/2+μ0p]]|/((B_in²+B_ext²)/2)` on s=1 (`minimize.py:719–730`). The weight is the volume Jacobian, not the area element. [V]

## Equation-to-source table

Derivations are in the [companion](gvec_free_boundary_derivation.md).

| Equation | Code | Source | Status |
|---|---|---|---|
| E1 discrete energy | `W = dthet_dzeta Σ_GP w (½ Σ bgb/J + μ0 p/(γ−1) Σ J)` | `evalfunc:516–539` | [V] |
| E2 full-torus weight | `d_thet = 2π/m_nyq`, `d_zeta = 2π/(n_nyq nfp)·nfp` | `src/base/fbase.F90:300–301, 319`; `evalfunc:132` | [V] |
| E3 dW | `dW = ½ B² + μ0 p` at Gauss points | `evalfunc:615` | [V] |
| E4 radial-derivative test coefficient | X1: `+dW J_h ∂θX2`; X2: `−dW J_h ∂θX1` | `evalfunc:665, 748` | [V] |
| E5 normal | `δx·(x_θ×x_ζ) = J_h(δX1 ∂θX2 − δX2 ∂θX1)`, for any hmap with q3=ζ | algebra | [D] |
| E6 exterior force | X1: `−½B_ext² J_h ∂θX2 − ε_m ∂θX1 I_s`; X2: `+½B_ext² J_h ∂θX1 − ε_m ∂θX2 I_s` | `evalfunc:1626, 1630` | [V] |
| E7 boundary force | `Force_b = F_MHD3D(nBase) + F_b` | `evalfunc:870–874` | [V] |
| E8 sum | `(dW − ½B_ext²) J_h(δX1 ∂θX2 − δX2 ∂θX1)` + condensation + last-element remainder | E4+E6 | [D] |
| E9 first variation of fixed-current vacuum potential | `+½∮ B_ext² ξ_n dA` | Hadamard + envelope | [D] |
| E10 boundary preconditioner | `−½⟨B_ext² ∂J_h/∂q1 ∂θX2⟩`, `+½⟨B_ext² ∂J_h/∂q2 ∂θX1⟩` | `evalfunc:1145–1163, 1289, 1372` | [V]; frozen-B_ext² part only |
| E11 spectral condensation | `I_s = X1_c ∂θX1 + X2_c ∂θX2`, prefactor `m^p(m^q−M)`, p=Q−1, q=1, Q=5, ε=1e-3 | `evalfunc:1584–1619`; `mhd3d.F90:518–519` | [V]; form consistent with [@hirshman1985] [H] |
| E12 pressure-balance target | `(B_in² − B_ext²)/2 + μ0 p` | `minimize.py:722` | [V] |

## Conventions

- Chart: hmap_RZ `x = (R cos ζ, −R sin ζ, Z)`, ζ clockwise seen from above, θ counterclockwise in (R,Z), `J = J_h J_p`, `J_p = ∂sX1 ∂θX2 − ∂sX2 ∂θX1` (`evalfunc:321–324`), `J_h = R`. With J>0, `x_θ×x_ζ = R(Z_θ e_R − R_θ e_Z)` is the outward normal. [D]
- nfp: the angular grid spans one field period with weight ×nfp (E2). BIEST replicates one period by rotations 2πj/nfp about z (`surface_op.txx` `CompleteVecField`); this equals GVEC's ζ→ζ+2π/nfp for hmap_RZ. For other hmaps (G-frame [@hindenlang2025], knots) this is not checked. [H]
- Orientation: `clockwise_zeta` flips the toroidal index before and after BIEST (`free_boundary.py:916–921, 934–935`). The winding-number test replaced an earlier geometric check after review on !168. [V]
- 2π and μ0: GVEC stores `Phi_edge/2π` (`mhd3d.F90:140`), so `Φ′` and `χ′` carry 1/(2π) and B is in tesla. W and all forces are μ0-scaled (units T² m³); B_ext² from BIEST is in T². `mu_0 = 2e-7·2π` (`mhd3d.F90:119`). [V]
- Sign of I: J0 is a toroidal surface current along BIEST's toroidal tangent `Xt_` (`txx:133, 138`; `Xt_` is the derivative along the first, toroidal, index, `:74–79`), with its sign fixed relative to the outward normal (`:141–159`); its field circulates poloidally. BIEST imposes +I along its poloidal index only when (toroidal tangent)×(poloidal tangent) points outward. Upstream passes `I_tor·mu_0` for both ζ orientations (`free_boundary.py:925–931`). This is correct for clockwise ζ (hmap_RZ, with the index flip) and has the wrong sign for counter-clockwise ζ (G-frames): circulation/(μ0 I) = −1.0000 on the N3.471 G-frame before the fork fix 8ffcd68a3c526d26f4e4053c1d49e06beb9188cc, +1.0000 after (fork `free_boundary.py:1731–1737`; regression `test_B2_exterior_counterclockwise_zeta`). [V, fork bug-hunt record]
- Stellarator symmetry: BIEST runs with `half_period=false` (`txx:48,107`); symmetry is retained only through GVEC's sin/cos projection. [V]
- Grid: BIEST source and target grid is GVEC's integration grid at s=1 with a half-cell offset (`free_boundary.py:904–907`); BIEST upsamples internally by `digits` (default 8). [V] The offset is harmless for a Fourier resampling [H].

## Deviations from a variational formulation

The [derivation](gvec_free_boundary_derivation.md#8-vacuum-energy-variation) gives the fixed-coil-current, fixed-circulation potential `Ŵ(Γ) = W_p − m(Γ)`, `m(Γ) = min ½∫_V |B|²`. Its first variation is E8 without the condensation term. The deviations are therefore of a different kind than "the vacuum energy is missing":

| Item | GVEC | Consequence |
|---|---|---|
| First variation | Matches `−dŴ` when B_ext² is from the current boundary; it is: the force is re-evaluated after `set_Bext_squared` (`mhd3d.F90:1383`) | Gradient consistent at each update, up to interior tolerance, BIEST and quadrature error [D] |
| Merit | Ŵ is never evaluated; acceptance uses only detJ>0; dt heuristic on the residual target | No line search or sufficient-decrease test on the functional being descended [V] |
| Second variation | `∂B_ext²/∂Γ` never formed; preconditioner has only the frozen-B_ext² geometric part (E10) | Quasi-Newton and preconditioned steps lack the vacuum stiffness; Newton needs it [V/D] |
| Circulation | `I0` re-evaluated from the state each update when iota is prescribed (`:555–561`) | The functional changes between updates (c_k drifts); not a derivative of one Ŵ [D]. Prescribed `I_tor` keeps c fixed (93d36ae9: "seems to help convergence in some cases") |
| Condensation | Adds `−ε_m X_θ I_s`; pointwise tangential for hmap_RZ, but not after Fourier projection and mode-wise preconditioning (derivation §7) | Fixed point is not the pressure-balance root; fork measured a ~0.4 mm bias (a507bd82 message) [V for the message, not re-run] |
| Interior | Re-solved to a ramped `minimize_tol`, which never increases | Inexact gradients early on; secant pairs mix tolerances [H for the effect] |

- The audit hypothesis "quasi-Newton pairs come from different frozen B_ext², so no single objective is minimized" is narrower than stated: with fixed c and ε=0, all updates use gradients of the same Ŵ at their own iterate. Mixed tolerances, drifting c and the condensation term remain. [D]

## Verified defects and upstream issues

Present at upstream 7da1182f. "Fixed" means a fork commit on itpplasma/gvec `develop` (086b2b25) that adds a regression test, unless noted. Failure of that test on the parent commit was checked for 8ffcd68a, ae4b2662, bfbc57ac, 1813c5a7, 8df39023, 781b4838 and 75fce329 (a strict xfail before); for the others it is not recorded.

| Item | Source (7da1182f) | Status |
|---|---|---|
| Plasma-current sign of the BIEST field for counter-clockwise ζ | `free_boundary.py:925–931` | [V]; fixed 8ffcd68a3c526d26f4e4053c1d49e06beb9188cc |
| Convergence statistics set only in `__init__`; a stage after a gtol stop inherits them and makes 0 updates | `free_boundary.py:69–76` | [V]; fixed ae4b266274021758fe635017914f55d051c3ceb0 |
| `reset_minimizer` can never become True in the step heuristic | `free_boundary.py:357, 518–519` (condition requires it already True) | [V] dead code; fixed bfbc57acf546bd2681074a4750e84c2fc94eb038 (reset when dt is held at `min_dt`; the intended semantics are a judgement call) |
| Statefile check inverted and not raised | `free_boundary.py:672–673`: `if len(...) > 0: FileNotFoundError(...)`; also `fixed_boundary.py:101–102` | [V]; fixed bfbbfdcc07c46234a412584f38d408abbc5f567a (no test) |
| Restart boundary mode left out of the new parameters is kept | `python/gvec/util/geometry.py:144–147` | [V]; fixed 01c5399dc51db9c3ec11ee11b4243e632e3b8013 |
| `save_statefile` writes into the working directory, not the run directory | `python/gvec/core/minimize.py:187–190` | [V]; fixed 057050e1d8129446f197bc7cca58707969b3d024 |
| `update_boundary` discards the step size | `python/gvec/core/minimize.py:699–701` | [V]; fixed 8df39023b120d517dc066ebceff89aacb2fe45ce |
| Resolution proposal reads column `fb_update−1` (off by one after a full loop) | `free_boundary.py:634–638` | [V]; fixed 1813c5a743f6323f4aa07288994bbeb80bc63294 |
| `W_MHD` uses `(γ−1)μ0 p` instead of `μ0 p/(γ−1)` | `python/gvec/quantities.py:1921` | [V]; latent, the two agree at γ=0, the only supported value; fixed 781b48383b1049191cdeac770e8645675bf73927 |
| Current fit: iota(0) ≈ 0 instead of the finite limit of `I_tor·iota_curr_bar` | `python/gvec/core/minimize.py:342` (no axis extrapolation of the product) | [V]; fixed 75fce32918e60e528f53ad48b44fb716423a2968 (independent Ampère/flux oracle, 1e-3) |
| BFGS `M` stored but unused | `free_b_minimizer_BFGS.F90:30, 69–72` | [V]; report only, not changed (classified as a missing feature, hypothesis) |
| Absolute `ftol`/`xtol` on a 2-entry window | `:224–251, 469–471`; defaults `:37–42` | [V]; stops after one update (#99); fork 4e9bb9a52f9e2854469279972d564386cc16b6b1 |
| `xnorm = xnorm_fb/dt` | `:553` | [V]; for GD this is a mode-scaled force norm, not a step length; not changed |
| `"{i}_b_"` key without X prefix | `python/gvec/util/geometry.py:141` | [V] (#98); fork 24ae677d921a56d36314975950733647cde87468 |

Issue states recorded from local GitLab dumps on 2026-10-19 (not re-queried):

- #96 axisymmetric `nzeta=1` (`zeta[1]` IndexError at `:907`; BIEST needs Nt ≥ 6): open; maintainer: "tokamaks are not yet supported"; MR !185 closed.
- #97 Biot–Savart doc prefactor: open, documentation only.
- #98 restart boundary key: open, milestone v1.6.
- #99 absolute ftol/xtol: closed, "still under development"; MR !188 closed; code unchanged at 7da1182f.
- #100 saved parameter files carry the input boundary: closed, "intended to be used in pairs" with the statefile.
- Developers' stated doubts concern step control, termination, resolution, preconditioning and coil quality (MR !168 notes 2026-08-07/12; #86 on the Picard current constraint). No source discusses existence, uniqueness or the choice of variational principle. [V, from the dumps]

## Our fork

All commits below are ancestors of itpplasma/gvec `develop` 086b2b25 (checked with `git merge-base --is-ancestor`).

First fork line (2026-10-12/13, 1ac00be4..ca733fe4, merged at 0065137c), the #96–#100 items and the Newton update:

| Commit | Change | Evidence |
|---|---|---|
| 1c59a5d2b7a406127603138cc53a58a86ec1ab8d | Axisymmetric states (one toroidal point); BIEST on an odd multiple of points when < 6 (#96) | 5 unit tests, `test_free_boundary_axisym.py` |
| 62d3b53e0ab3495ff892206c9bfad852148f1640 | Biot–Savart comment μ0/(4π) (#97) | segment sum agrees to 9e-16 |
| 24ae677d921a56d36314975950733647cde87468 | Restart boundary read with `X{i}_b_` (#98) | `test_util.py` |
| 4e9bb9a52f9e2854469279972d564386cc16b6b1 | `ftol` relative to the moving-average target; ftol/xtol only with a full window (#99) | MR !188 text |
| 8a59ae7902575ca3e3dceeedb743aef7f3c5459f | Saved parameter files carry the moved boundary (#100) | — |
| b298321aaf28623deb00048b59f8b40579967544 | `method="newton"`: solve `g(y) = Pᵀ F_b(x0 + P y) = 0` for normal displacement y; FD Jacobian (interior solve + BIEST per unknown), Broyden, Levenberg–Marquardt, step limit, backtracking on \|g\| | fork `free_boundary.py:779–1117` (current form) |
| c792c3eb0db95f41c9d70fb97636e7bcd3fb7279 | FD workers pinned to CPUs; Broyden rebuild if \|g\| drops by less than 0.5 | — |
| 4d9fb7ae74ccb1d1aa79203dc884f0e9bde284da | Normal basis uses n per field period (was n·nfp² for nfp>1) | nfp=3 helical test |
| a507bd82e825a2202e7004efb37617ba716131f9 | Newton residual with ε_spectral=0 | fork `src/pygvec/state.F90:384–411` |
| ca733fe416f0dfda95e3b943a155617e35da63b3 | `newton_gtol`: small steps do not stop above it; rejected steps rebuild Broyden first | used as the absolute stop in the stellarator regression (12d778df) |

Fixes of fork-introduced defects (2026-10-19/20), each with a regression test:

| Commit | Defect fixed | Evidence |
|---|---|---|
| b979af8cc0e61a01d0ffb5fea10fbb477ef5a87b | Saved parameter files (8a59ae79) repeated the initial boundary perturbation on restart | R00 3.01 → 3.02 m in the test before the fix (commit message) |
| 4b194acf75098884762445687203667510110b58 | Stale in-memory dof checkpoint survived Finalize/Init and corrupted a later state | commit message: first FD column detJ ≤ 0 |
| 22bcccfd45870058e8c39fd2ffbcfa051acf9bc6 | Newton ignored the `totalIter` budget | parent: 50 iterations with budget 0 [V] |
| 64fc486d70163e8b3603e79a703910ba0fd7af63 | Broyden Jacobian kept in the old basis after P was rebuilt | parent fails 2 tests [V]; superseded by 81fe6405, which never rebuilds P within a solve (`_change_jacobian_basis`, fork `free_boundary.py:1263–1268`, is now used only by its unit test) |
| 1991c38feda10944d53ccc3af7012fb8b8e98969 | Normal basis built from X1 modes only (vertical shift unrepresentable with cos-only X1); no tangential gauge | complete X1/X2 normal-trace basis, below [V] |
| 81fe640587e339ccb89f9647b78b057e86427591 | P rebuilt after every step while the Jacobian treated it as frozen, omitting `(∂P/∂y)ᵀ r`; forward differences | P fixed within a solve, central differences, below [V] |
| 12d778df004f1e25494140f2efd6bbc08cdecbb9 | Stellarator regression accepted a state after one Newton update | converged-equilibrium test, below [V] |

Changes after b37d82b3 (2026-10-20), all on `develop` 086b2b25 (checked with `git merge-base --is-ancestor`). Line numbers are fork 086b2b25. Evidence is the fork lane reports of 2026-10-20; not re-run here.

| Commit | Change | Evidence |
|---|---|---|
| 260e6ed1d23e99fb2d0e3e5cfa7ec8a6b318fbb9 | Trial checkpoints also save and restore the fitted iota profile, so a rejected Newton trial no longer leaves its current-fit profile in place (`python/gvec/core/minimize.py:754–768`) | regression in `test_free_boundary_axisym.py` [V, report] |
| 0e92a36893a21550c495e55c8b6ed897408108c3 | Levenberg–Marquardt scaling `diag(JᵀJ)` set to 1 where it vanishes, so null directions are still regularized (`free_boundary.py:940–941`) | same file [V, report] |
| e388d7d9d6e0290b483187eb03c4f6fdd3c35ac0 | A restart whose initial \|g\| is already below `newton_gtol` returns as converged with zero updates (`:874–881`) | same file [V, report] |
| f35d57b164bee26256af5ea0161f7500378d1d4e | A step exceeding `newton_max_step` is no longer scaled as a whole: Cauchy step in displacement units, then a dogleg towards Newton inside the step box (`:977–1002`) | same file [V, report] |
| ef665bd6d749bdbebfef83829dcc34978b2e0299 | With `newton_gtol` > 0 the LM step is damped as strongly as possible while its linear model still predicts \|g + J dy\| ≤ gtol/2 (`:942–955`) | same file [V, report]; changes the return-test results, below |
| a33fa0cace8140857445b499cb27e879d6a51d6a, b1f0727583ce41036438f031bff59ff3afacc9e9 | Stellarator resolution ladder with inner and current targets 1e-9; strict xfail of the 17×17 case on the pressure bound | ladder below [V, report] |
| f7790957b4efd11e8d25654b047a464024757b7a | Fast/slow split: the CI stellarator case starts from a known 9×9 boundary and recomputes interior, current, coil and BIEST fields; the cold 9×9 solve and the 17×17 case are marked slow and deselected in `ci.yml` (`test_free_boundary_realcases.py:157–197`) | hosted case 41 s instead of 640 s; full \|F_b\| 4.99e-6, pressure RMS/max 0.0388 %/0.142 % [V, report] |
| cda656ae7350dc3778b864db3f07472e3b33988a | G-frame test stop 0.03 → 0.02 after a hosted pressure maximum of 0.206 > 0.20 | superseded by 303400f3 [V, report] |
| 216fc5478b3af79abb45c7b95bece90f72fc7af4, 58dea07c9c32573869d0e26aef4e250a695506f3 (merged at 140c50c15b65c1e06d257298e0dbe1a7699fa7ea) | Nightly and dispatchable workflow for the slow tests (`.github/workflows/slow.yml`, cron 02:30 UTC, 90 min timeout) | dispatched run: cold 9×9 passes, 17×17 remains a strict xfail [V, report] |
| 303400f3e0bbbe77338b121589a71dbd2267fbc9 | Robust G-frame fixture: full Fourier coordinates (`newton_space="full"`), inner/iota tolerances 1e-5/1e-7, absolute stop on the full boundary force 1e-4, 40 updates (`test_free_boundary_realcases.py:200–254`) | the old fixture failed with a Nehalem BLAS kernel (pressure max 0.251 > 0.20); now 21/21 local and three hosted runners pass, 14 updates, full force 7.30e-5, pressure RMS/max 2.33 %/5.58 % (bounds 8 %/20 % unchanged) [V, report] |
| 8aa89ea6c761e5b00e0ad3d2a2f3a609d04f5d8a | Canonical, kernel-independent normal basis (`_canonical_range_basis`, `:1578–1601`, applied at `:1659`). Before, the circular and other symmetric starts had repeated singular values, and the BLAS kernel rotated the SVD basis (16 of 18 directions) while its projector agreed to 1.1e-14; the basis sets the FD directions and the coordinate step limits, so the Newton path depended on the kernel | `test_normal_basis_and_newton_across_blas_kernels` (`test_free_boundary_basis.py:37`): Haswell vs Nehalem bases agree to 6.4e-15; fails on 303400f3 (bases differ by 1.21) [V, report] |
| 086b2b25dd1f51acceafbcdc8993c5052b3e462e | Offset-return tests with consistent tight base and return solves and a 20 µm bound (was 500 µm), 2048-point contours | below [V, report] |

- Normal basis at 086b2b25 (`_normal_displacement_basis`, fork `free_boundary.py:1604–1660`) [V]:
  - The sampled normal-trace map A has one column `φ_k n_var` for every allowed X1 and X2 boundary DOF, with `(n_R, n_Z) = (Z_θ, −R_θ)/|·|` per ζ plane, the outward normal of E5.
  - SVD of A; right singular vectors with singular value > 1e-10 × the largest span the independent normal traces (P); the rest (T) are tangential nulls (`:1650–1653`).
  - Slide gauge `Tᵀ D dx = 0`, `D_kk = m_k² + (n_k nfp)²`, applied as a correction of P along T, then QR (`:1654–1658`). D annihilates rigid shifts, so translations stay available, and the correction leaves the normal trace unchanged. `TᵀDT` is positive definite because a constant displacement cannot be tangential everywhere on a closed section (docstring `:1614–1618`) [D in the docstring; not re-derived here].
  - The gauged range is then given a canonical frame from the boundary-DOF axes (`:1659`); only the projector `P Pᵀ` enters, so the FD directions and the step box no longer depend on the SVD rotation (8aa89ea6).
- Newton at 086b2b25 (`_run_newton_loop`, fork `free_boundary.py:779–1117`) [V]:
  - P is built once per solve (`basis()` `:861–866`, called once at `:868`) and not rebuilt after accepted steps, so `x = x_start + P y` and `Dg = Pᵀ (∂F_b/∂x) P` holds also for `F_b ≠ 0` (derivation §10).
  - The FD Jacobian uses central differences with step `newton_fd_step`: two interior solves and two BIEST calls per unknown (`:897–936`, difference quotient `:917`).
  - LM step with unit scaling in null directions (`:938–955`), damped towards the requested `newton_gtol` (ef665bd6), and a Cauchy/dogleg step inside the step box (`:977–1002`).
  - Merit is \|g\| with backtracking; there is no energy merit, and indefinite directions such as the fixed-current vertical saddle are handled by the residual merit only.
  - The circulation c = μ0 I_tor(1) is taken from the state at each residual evaluation (`_boundary_residual`, `:1290–1304`).
- Before 1991c38f/81fe6405 (e.g. at a507bd82, used for TC24) [V by source]: the basis was `{φ_k n : φ_k an X1 boundary function}`, L2-projected onto the X1/X2 coefficients (a507bd82 `free_boundary.py:1255–1288`); the FD Jacobian was a forward difference (`:886–896`); P was rebuilt after each accepted step (`:968`) while the Jacobian and Broyden updates treated it as constant. Its normal traces span only the X1 functions, so with cos-only X1 (up-down symmetric) the odd trace of a vertical shift is missing [D].

### Fork regressions with physical oracles (086b2b25)

Measured by the fork lane reports of 2026-10-20 (fresh or hash-matched editable builds, fbtools 14a5c4a7, headless); not re-run here. Test line numbers are fork 086b2b25.

| Test | Before the fixes (at e2e3011a) | Current | Status |
|---|---|---|---|
| `test_free_boundary_offsets.py` radial return: matched current-controlled axisymmetric polygon-coil equilibrium, rigid +10 mm R start, base and return solves with minimize_tol 1e-10, iota_tol 1e-9, `newton_gtol` 1e-9; acceptance 20 µm contour distance on 2048 points (`:161–201`) | 12.31 mm after two accepted updates (strict xfail) | At 086b2b25: 0.44 µm local (both test orders), 2.95 µm hosted; reference probe at 8aa89ea6 1.78 µm, 5 updates | [V, report] |
| Same, +10 mm Z start (`:204–207`) | 10.00 mm after one update (strict xfail) | 1.52 µm local, 1.38 µm hosted; probe 1.89 µm, 2 updates | [V, report] |
| `test_free_boundary_stellarator_real_coils`, 9×9 integration grid (`test_free_boundary_realcases.py:299–321`) | Accepted after one Newton update (target 1e-2, interior tol 1e-3). Pre-fix (5fe6ba29) and fixed-basis (81fe6405) surfaces differed by 76.8 mm (symmetric max); full \|F_b\| 5.5e-2 / 4.6e-2 | Requires the convergence flag, interior force < 1e-9, Newton \|g\| < 1e-5 and full native \|F_b\| < 2e-5; gauge-invariant volume (±1e-3 m³) and Z=0 ray radii (±0.3 mm) replace R00; pressure-jump RMS/max < 0.06 %/0.18 % on an independent 96×64 grid. CI runs the known-boundary variant (4.99e-6, 0.0388 %/0.142 %, zero Newton updates); the cold solve is slow-marked | [V, report] |
| `test_free_boundary_stellarator_resolution`, 17×17 (`:328–362`, slow, strict xfail) | — | Cold start reaches full \|F_b\| 4.75e-6 in nine updates, but the pressure maximum 0.1840 % exceeds 0.18 %; a warm start from the 13×13 root rejects every step (\|F_b\| 3.67e-3) | Open resolution item, below |
| `test_free_boundary_gframe_nonzero_current` (`:365–375`) | — | 14 updates, full force 7.30e-5, pressure RMS/max 2.33 %/5.58 % (bounds 8 %/20 %), also with a Nehalem BLAS kernel | [V, report] |

- The ~10 µm returns cited at b37d82b3 (radial 10.14 µm, vertical 9.72 µm) were measured with `newton_gtol` 1e-7 and loose inner solves (minimize_tol 1e-8, iota_tol 1e-7); the bisection re-measured 11.86/9.72 µm at b37d82b3. After ef665bd6 the same settings stop at \|g\| < 1e-7 with an incomplete correction: 190.6 µm radial and 40.1 µm vertical (166.4/12.3 µm at 8aa89ea6), with the radial projected residual rising 4.8× and the full residual near 3e-7. Tightening only the return solve shifts the result by about 52 µm against the loosely solved reference; consistent tight base and return solves with `newton_gtol` 1e-9 give 0.4–3.0 µm (local/hosted). The 20 µm bound (was 500 µm) rejects the ef665bd6-era and loose 8aa89ea6 results. [V, report]
- The return attribution to the individual fixes (complete basis, fixed P, central differences, and the five Newton fixes) is not separated; the returns were measured only with all of them in place. [V for the combination, H for the split]
- Stellarator resolution ladder (fixed Fourier/radial space m,n ≤ 2, inner/current 1e-9, FD h = 1e-4, 12 updates): 9, 13, cold 17 and 25 are discrete force roots (full \|F_b\| 8.8e-6, 3.9e-6, 4.7e-6, 7.3e-6; interior force < 1e-9). Volume decreases by 1.9 % from 9 to 25 (13.2465 → 12.9920 m³); Z=0 rays move by up to 28 mm from cold 17 to 25 and by up to 58 mm between 9 and cold 17. On a frozen 9×9 surface the BIEST grid changes the field by 7.3e-4 T against 2.8e-9 T for BIEST digits 8 → 12, so the results depend on the coupled BIEST/quadrature resolution. The existence of a discrete 17×17 root rules out a missing root as the cause of the warm-start stall; a converged geometry limit is not established. [V, report; H for the limiting geometry]
- The physical FD check of `dg/dy` agrees to 2.15e-4 (matrix norm) at test inner tolerances and 7.3e-6 with tightened inner solves; along the softest direction the difference is 98 % and 5.2 % (measured at b37d82b3). The soft-direction sensitivity is attributed to inner-solve/fit noise [H].
- Other oracles kept in the real-case tests: max \|B·n\|/\|B\| < 1e-6 on an independent grid, exterior Ampère circulation = μ0 I_tor with sign (1e-3), stellarator symmetry. [V, report]

### TC24 runs (FB-cut / FB-taper 0.997, ITER, axisymmetric)

| Run | Code | Result as recorded | Status |
|---|---|---|---|
| `/mnt/storage/codex-equilibrium-20261011/gvec/gvec_fb_cut099{5,7}_ladder_20261012_01` | GD, fork 352350f4 | 0.034/0.12 mm vs FreeGS | **Retracted**: one boundary update (absolute ftol/xtol) and the offset start was reset to the contour, so this is the fixed-boundary miss (`WHY_GVEC.md` §1) |
| `.../gvec/whygvec_diag_20261013` | GD, dt 1e-2, m25, ne16, ftol=xtol=gtol=0 | +15 mm R start: 12.30/16.04 mm rms/max from FreeGS after 100 and 400 updates; 2 % elongation: 17.5/44.4 mm; target floor 2.3–2.5e-4 | Stalled (`WHY_GVEC.md` §2A) |
| `.../gvec/gvec_fb_taper_offset_return_20261013_02` (sCluster 3220230) | Newton, a507bd82 | Contour start 0.041/0.224 mm vs KIN6D; dR+15 returns 0.109/0.80 mm; dZ−15 0.148/1.02 mm; elong2 0.46/5.04 mm (\|g\| 2.1e-3 at stop); old K+ start 0.38/4.57 mm; all native stops | dR+15 passes the 1 mm offset-return gate (0.80 mm max); dZ−15, elong2 and the old K+ start fail it (`analysis.json` `_verdict`) |
| `.../gvec3d/gvec3d_fb_rmp_cut0997_20261013_05` (sCluster 3220235) | 3D Newton, a507bd82, m25 n2 ne48 | Both tasks COMPLETED; B0 vs KIN6D 0.041/0.224 mm; +15 mm returns 0.105 mm rms; response per unit amplitude 106–111 mm (phi000), 151–158 mm (phi010) for amplitudes 0.0025–0.01 (`response_per_amp_mm` in `cases/*/result.json` of the copy `/mnt/storage/tc24-parallel-20261015/collect-old-evidence/gvec3d_fb_rmp_cut0997_20261013_05`) | No independent 3D free-boundary reference; `_02`–`_04` cancelled and not results |

- Ip is an output (iota prescribed): 15.25–15.26 MA in the Newton runs. [V]
- All TC24 Newton runs used a507bd82, i.e. the X1-only basis with P rebuilt after each step and a forward-difference Jacobian. Their inputs use `_sincos_` for X1 and X2 with equal `mn_max = (24, 0)` (`cases/*/F/parameter_cut0997_final.ini`), so the X1-only basis contained odd traces and the cos-only vertical gap of the fork regression does not apply directly [V for the inputs, D for the consequence]. The moving-P Jacobian inconsistency and the forward-difference error did apply [V by source].
- The elong2 (5.04 mm max), old K+ (4.57 mm max) and dZ−15 (1.02 mm max) misses are therefore plausibly due to the moving projection and forward-difference Jacobian, which the fork fixed after these runs. The fork's 10 mm return tests went from 10–12 mm to about 10 µm at b37d82b3 only with three fixes together (complete basis, fixed P, central differences), and to 0.4–3.0 µm at 086b2b25 only with tight base and return solves and `newton_gtol` 1e-9 (above); the complete basis does not apply to TC24 (above), and the share of the two fixes that do apply is not measured. KIN6D itself does not converge the +2 % elongation start on ITER FB-cut 0.997 v2 (8.4 mm max, `kin6d/docs/ideal-free-boundary.md:139`), so the elong2 miss may not be specific to GVEC. This is a hypothesis: no TC24 run at 81fe6405 or later exists. The earlier reading "a different root or a flat direction" is not excluded either. [H]
- No GVEC free-boundary stellarator result with an independent reference surface exists in our records. The fork's real-coil stellarator regression (above) is a coarse 9×9 CI case without an independent reference surface; its resolution ladder has discrete roots at 9, 13, 17 (cold) and 25 but does not converge in geometry (volume −1.9 % from 9 to 25, rays up to 28 mm from 17 to 25), and the 17×17 root misses the 0.18 % pressure bound. [V]
- The TC24 report states the GVEC free-boundary lane is stopped as a documented limitation (`equilibrium/tc24/revision_20261013.tex:329–345, 414–416`); the `_05` "running" wording there is stale. [V]

## Convergence of GVEC's scheme

Existence of non-symmetric toroidal MHD equilibria with nested surfaces is no longer the open question [@landreman2026; @issan2026; @gomezserrano2026]. These results do not address a given coil set or the boundary iteration. The open issue is whether and how fast GVEC's boundary iteration reaches the root.

- The axisymmetric analogue has a well-posedness theory [@temam1975; @temam1977], and axisymmetric free-boundary codes solve the coupled plasma–vacuum problem by Newton [@heumann2015; @faugeras2017]. The common statement that Picard iteration fails for vertically unstable equilibria was not checked against a source here.

1. **Descent cannot converge to a saddle of Ŵ.** [D] With fixed coil currents an elongated tokamak is vertically unstable, so its equilibrium is a saddle of Ŵ. KIN6D measures this on the same ITER cases: rigid K_Z = −5.4e6 J/m² per period on FB-cut 0.997 v2 and −5.2e6 on the FB-taper base state; n=0 Schur eigenvalue down to −3.9e-7 (`kin6d/docs/ideal-free-boundary.md`, NL-3a and solver-revision sections). Linearized at a saddle with fixed dt and P, a preconditioned descent step `δ ← (I − dt P⁻¹H)δ` has an eigenvalue `1 + dt|λ| > 1`, λ a negative eigenvalue of `P⁻¹H`. GVEC changes dt, P and the quasi-Newton metric between updates, so the argument that applies is energy decrease (derivation §9): a step `−dt M⁻¹∇Ŵ` with M positive definite decreases Ŵ strictly when `dt λ_max(M^{−1/2} H M^{−1/2}) < 2`, so from any start below the saddle value the iterates cannot converge to the saddle. This covers GD with varying dt and P, and heavy-ball mGD for fixed dt, P and β. For unit-step BFGS, dBFGS and lBFGS (Powell damping keeps dBFGS definite, `free_b_minimizer_dBFGS.F90:158–163`) GVEC has no sufficient-decrease test, so the step bound is a condition, not a guarantee [H]. SR1 and ADAM are not covered. Convergence to the saddle remains possible only from starts that never go below the saddle value, or when the negative curvature is below the iteration's noise and step floor. Whether this, rather than ill-conditioning, explains the GD stalls is **[H]**: the run records cannot separate the two, and WHY_GVEC §3 ranks the [[B²]] target floor first.
2. **Rate on soft modes.** [D] Away from the saddle the descent rate is set by `λ_min/λ_max` of `P⁻¹H`. KIN6D measures `K_R/|K_Z|` ≈ 600 on its gs_free fixture and ≈ 46 on ITER FB-cut 0.997 v2 (`K_R = +2.5e8`). WHY_GVEC estimates the position and shape forces at about 1e-5 of B² per 15 mm, against a target floor of 1–2.5e-4. Both are consistent with the 12 mm stalls [H].
3. **Relabelling nulls.** Full boundary coefficients (X1_b, X2_b) include tangential reparametrizations of the boundary curve. The physical force is normal only (E5, E8), so these directions have zero physical gradient and zero physical stiffness; only condensation gives them stiffness [D]. Descent ignores them; Newton on full coefficients sees a near-singular Jacobian. The fork's normal basis removes them; since 1991c38f it fixes them by a slide gauge that keeps rigid translations (fork `free_boundary.py:1576–1580`), the boundary analogue of KIN6D's slide gauge (`theory/derivations/free-boundary-gauge-vertical.md`; its FB-D4 shows that a normal-only displacement plus a rigid-Z coordinate is not equivalent to stationarity, and FB-D1, with Lean lemmas B1/B2 in `proof/Kin6d/Bordered.lean`, gives nonsingularity and inertia of the bordered gauge system). Whether GVEC's gauge (a weighted least-change condition, not KIN6D's slide moments) is equivalent is not shown [H]. In the interior, the fixed-boundary minimizer handles the relabelling at each solve. KIN6D shows on its gs_free fixture what a missing gauge does to Newton: drift of 1–5 cm along the n=0 slide null, a 7 mm stall when over-constrained, and return in about 3 steps once the gauge is exact (`kin6d/docs/ideal-free-boundary.md`, formulation and "Relabelling (slide) gauge" sections). Whether GVEC's interior λ/θ gauge creates a similar soft direction for the boundary Newton is **[H]**.
4. **What a variational or gauged Newton needs.** [D] (i) The second variation of Ŵ including `D(½B_ext²)[ξ]` (derivation §9); (ii) an exact gauge for tangential and interior relabelling; (iii) a method for indefinite systems (LDLᵀ/LU, or a residual merit) instead of positive-definite quasi-Newton; KIN6D's FB-D4 rules out a normal-only displacement plus rigid-Z coordinate as a substitute; (iv) for a variational merit, fixed circulation or c as an explicit unknown (root finding on the coupled map with c(X) needs neither); (v) ε_spectral=0 in the residual; (vi) an absolute residual target, since relative merit and step tests stop on soft modes. KIN6D implements (i)–(iv) and (vi) natively; on ITER FB-cut 0.997 v2 its ±15 mm R/Z offsets return within about 0.2 mm (in the FB-taper family the returns reach about 1.9 mm and −15 mm Z is not converged, `kin6d/docs/ideal-free-boundary.md:173–174`), while +2 % elongation is not converged (8.4 mm, NL-3a). The fork implements (iii), (v), (vi) (`newton_gtol`) and the boundary part of (ii), with a central-difference FD Jacobian in a fixed projection and root finding with c taken from the state (fork `free_boundary.py:1242–1256`). It does not form (i) analytically, and has no energy merit. On its 10 mm axisymmetric return tests it returns to 0.4–3.0 µm with consistent tight base and return solves and `newton_gtol` 1e-9 (the earlier ~10 µm at b37d82b3 used `newton_gtol` 1e-7 and loose inner solves, which after ef665bd6 stop at 190.6/40.1 µm); the TC24 elongation and K+ misses of about 5 mm predate these fixes and have not been rerun (see TC24 runs). [V for the tests, H for TC24]

## References not verified

Left out of `writeups.bib`: the "Lee & Kim" coil Biot–Savart reference (not identified); Bauer–Betancourt–Garabedian 1978; Blum's 1989 book; Merkel's Varenna 1987 proceedings (local Zotero record only, no DOI); the journal version of [@conlin2024].

## Open

- Rerun the TC24 elong2, old K+ and dZ−15 starts at 086b2b25 (complete basis, fixed P, central differences, the five Newton fixes, `newton_gtol` with tight inner solves) to test the [H] attribution of their 1–5 mm misses.
- Resolve the 17×17 stellarator case (strict xfail at 086b2b25): the cold start converges but misses the 0.18 % pressure bound (0.1840 %), the warm start from 13×13 stalls, and the 9→25 ladder still moves the volume by 1.9 % and the rays by up to 28 mm (17→25); separate BIEST and plasma quadrature resolution.
- Measure the rigid vertical stiffness through GVEC's own boundary force (FD of F_b along a rigid Z shift) and compare its sign with KIN6D.
- Check the 3D/general-hmap force coefficients against EvalEnergy by FD (the 16 local identities cover axisymmetric RZ only).
- Derive the J0 normalization (`txx:150–160`) and the I sign for non-RZ hmaps.
