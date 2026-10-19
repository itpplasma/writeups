# GVEC free-boundary source correspondence

Citations `[@key]` refer to [writeups.bib](../writeups.bib).

- Scope: GVEC's experimental free-boundary loop (plasma energy, BIEST exterior field, coil field, boundary update and termination), our fork's Newton variant, and the axisymmetric TC24 runs. Fixed-boundary conventions are in the [GVEC equilibrium correspondence](gvec_equilibrium_source_correspondence.md) and the [discrete force audit](gvec_discrete_force_audit.md).
- Upstream: [gvec-group/gvec 7da1182fd81b1ba552142bb663319d74c7edfb8b](https://gitlab.mpcdf.mpg.de/gvec-group/gvec/-/tree/7da1182fd81b1ba552142bb663319d74c7edfb8b), branch `free_boundary_three_step` (MR !168, Draft, milestone v1.6), commit date 2026-10-19.
- Fork: [calbert/gvec ca733fe416f0dfda95e3b943a155617e35da63b3](https://gitlab.mpcdf.mpg.de/calbert/gvec/-/tree/ca733fe416f0dfda95e3b943a155617e35da63b3), branch `equilibrium/fb-newton-gtol-20261013`. It branches from upstream 1ac00be4 (2026-10-01) with 11 commits (one merge); it does not contain upstream 93d36ae9 (I_tor profile for BIEST) or 7da1182f.
- Vacuum solver: [fbtools 14a5c4a7c3ff7458780edf7ebb0bd76712b44fbf](https://gitlab.mpcdf.mpg.de/nmpp-mhd-group/fhindenlang/fbtools/-/tree/14a5c4a7c3ff7458780edf7ebb0bd76712b44fbf) with submodule [BIEST 6944d5c0fb1e5e2eb12868749e1a1f829601dc63](https://github.com/dmalhotra/BIEST/tree/6944d5c0fb1e5e2eb12868749e1a1f829601dc63).
- Paths below are relative to these trees. `free_boundary.py` is `python/gvec/core/run/free_boundary.py`; `evalfunc` is `src/functionals/mhd3d/mhd3d_evalfunc.F90`; `mhd3d.F90` is `src/functionals/mhd3d/mhd3d.F90`; `txx` is BIEST `include/biest/vacuum-field.txx`. Line numbers are for 7da1182f unless marked fork.
- Labels: **[V]** checked against the pinned source, run record or a reference; **[D]** derived here or in the [derivation companion](gvec_free_boundary_derivation.md); **[H]** hypothesis, not tested.
- Status: source correspondence and first-variation algebra checked. GVEC has no derivation document, no convergence argument and no free-boundary test with assertions. Nothing here proves that the GVEC iteration converges.
- Native evidence for the convergence questions is KIN6D, not this file: `kin6d/docs/ideal-free-boundary.md` and `kin6d/docs/gs-free-boundary.md` (itpplasma/kin6d at 73891c54a71c3a080826043fd02924779a6e79a3). Their proofs are not repeated here.

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
| Topology | J0 a harmonic surface field from a Hodge decomposition, normalized to unit poloidal circulation and oriented along ∂_θx | `txx:132–160` | Normalization not derived in docs [H] |
| Plasma current | `I0 = μ0 I_tor(ρ=1)`, from the `I_tor` profile if set, else evaluated from the state | `free_boundary.py:414–420, 555–561, 924–930` | [V] |
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
   Then `I_tor(1)` and BIEST again (`:555–566`).
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
- Orientation: `clockwise_zeta` flips the toroidal index before and after BIEST (`free_boundary.py:916–933`). The winding-number test replaced an earlier geometric check after review on !168. [V]
- 2π and μ0: GVEC stores `Phi_edge/2π` (`mhd3d.F90:140`), so `Φ′` and `χ′` carry 1/(2π) and B is in tesla. W and all forces are μ0-scaled (units T² m³); B_ext² from BIEST is in T². `mu_0 = 2e-7·2π` (`mhd3d.F90:119`). [V]
- Sign of I: J0 is oriented along ∂_θx relative to the outward normal (`txx:142–160`); a positive circulation then corresponds to current along the orientation fixed by θ and the normal. Correct for hmap_RZ with the ζ flip [H]; the fork's Ampère circulation oracle on #96 supports it, at about 1e-3.
- Stellarator symmetry: BIEST runs with `half_period=false` (`txx:48,107`); symmetry is retained only through GVEC's sin/cos projection. [V]
- Grid: BIEST source and target grid is GVEC's integration grid at s=1 with a half-cell offset (`free_boundary.py:903–907`); BIEST upsamples internally by `digits` (default 8). [V] The offset is harmless for a Fourier resampling [H].

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

| Item | Source | Status |
|---|---|---|
| `reset_minimizer` can never become True in the step heuristic | `free_boundary.py:357, 518–519` (condition requires it already True) | [V] dead code |
| Statefile check inverted and not raised | `free_boundary.py:672–673`: `if len(...) > 0: FileNotFoundError(...)` | [V] |
| BFGS `M` stored but unused | `free_b_minimizer_BFGS.F90:30, 69–72` | [V] |
| Absolute `ftol`/`xtol` on a 2-entry window | `:224–251, 469–471`; defaults `:37–42` | [V]; stops after one update (#99) |
| `xnorm = xnorm_fb/dt` | `:553` | [V]; for GD this is a mode-scaled force norm, not a step length |
| `"{i}_b_"` key without X prefix | `python/gvec/util/geometry.py:141` | [V] (#98) |

Issue states recorded from local GitLab dumps on 2026-10-19 (not re-queried):

- #96 axisymmetric `nzeta=1` (`zeta[1]` IndexError at `:907`; BIEST needs Nt ≥ 6): open; maintainer: "tokamaks are not yet supported"; MR !185 closed.
- #97 Biot–Savart doc prefactor: open, documentation only.
- #98 restart boundary key: open, milestone v1.6.
- #99 absolute ftol/xtol: closed, "still under development"; MR !188 closed; code unchanged at 7da1182f.
- #100 saved parameter files carry the input boundary: closed, "intended to be used in pairs" with the statefile.
- Developers' stated doubts concern step control, termination, resolution, preconditioning and coil quality (MR !168 notes 2026-08-07/12; #86 on the Picard current constraint). No source discusses existence, uniqueness or the choice of variational principle. [V, from the dumps]

## Our fork

Commits 1ac00be4..ca733fe4 (merge 352350f4 omitted), all 2026-10-12/13:

| Commit | Change | Evidence |
|---|---|---|
| 1c59a5d2 | Axisymmetric states (one toroidal point); BIEST on an odd multiple of points when < 6 | 5 unit tests, `test_free_boundary_axisym.py` |
| 62d3b53e | Biot–Savart comment μ0/(4π) | segment sum agrees to 9e-16 |
| 24ae677d | Restart boundary read with `X{i}_b_` | `test_util.py` |
| 4e9bb9a5 | `ftol` relative to the moving-average target; ftol/xtol only with a full window | MR !188 text |
| 8a59ae79 | Saved parameter files carry the moved boundary | — |
| b298321a | `method="newton"`: solve `g(y) = Pᵀ F_b(x0 + P y) = 0` for normal displacement y; FD Jacobian (interior solve + BIEST per unknown), Broyden, Levenberg–Marquardt, step limit, backtracking on \|g\| | fork `free_boundary.py:804–1027` |
| c792c3eb | FD workers pinned to CPUs; Broyden rebuild if \|g\| drops by less than 0.5 | — |
| 4d9fb7ae | Normal basis uses n per field period (was n·nfp² for nfp>1) | nfp=3 helical test |
| a507bd82 | Newton residual with ε_spectral=0 | fork `src/pygvec/state.F90:388–408` |
| ca733fe4 | `newton_gtol`: small steps do not stop above it; rejected steps rebuild Broyden first | No run uses it [V] |

- The normal basis is `(n_R, n_Z) = (Z_θ, −R_θ)/|·|` per ζ plane (fork `free_boundary.py:1280–1314`), the outward normal of E5. It removes the tangential reparametrization directions, whose only stiffness in GVEC is the condensation weight (fork docstring `:813–822`). [V]

### TC24 runs (FB-cut / FB-taper 0.997, ITER, axisymmetric)

| Run | Code | Result as recorded | Status |
|---|---|---|---|
| `/mnt/storage/codex-equilibrium-20261011/gvec/gvec_fb_cut099{5,7}_ladder_20261012_01` | GD, fork 352350f4 | 0.034/0.12 mm vs FreeGS | **Retracted**: one boundary update (absolute ftol/xtol) and the offset start was reset to the contour, so this is the fixed-boundary miss (`WHY_GVEC.md` §1) |
| `.../gvec/whygvec_diag_20261013` | GD, dt 1e-2, m25, ne16, ftol=xtol=gtol=0 | +15 mm R start: 12.30/16.04 mm rms/max from FreeGS after 100 and 400 updates; 2 % elongation: 17.5/44.4 mm; target floor 2.3–2.5e-4 | Stalled (`WHY_GVEC.md` §2A) |
| `.../gvec/gvec_fb_taper_offset_return_20261013_02` (sCluster 3220230) | Newton, a507bd82 | Contour start 0.041/0.224 mm vs KIN6D; dR+15 returns 0.109/0.80 mm; dZ−15 0.148/1.02 mm; elong2 0.46/5.04 mm (\|g\| 2.1e-3 at stop); old K+ start 0.38/4.57 mm; all native stops | Fails the 1 mm offset-return gate (`analysis.json` `_verdict`) |
| `.../gvec3d/gvec3d_fb_rmp_cut0997_20261013_05` (sCluster 3220235) | 3D Newton, a507bd82, m25 n2 ne48 | Both tasks COMPLETED; B0 vs KIN6D 0.041/0.224 mm; +15 mm returns 0.105 mm rms; response/a 106–111 mm (phi000), 151–158 mm (phi010) | No independent 3D free-boundary reference; `_02`–`_04` cancelled and not results |

- Ip is an output (iota prescribed): 15.25–15.26 MA in the Newton runs. [V]
- No GVEC free-boundary result exists for stellarators in our records. [V]
- The TC24 report states the GVEC free-boundary lane is stopped as a documented limitation (`equilibrium/tc24/revision_20261013.tex:329–345, 414–416`); the `_05` "running" wording there is stale. [V]

## Convergence of GVEC's scheme

Existence of non-symmetric toroidal MHD equilibria with nested surfaces is no longer the open question [@landreman2026; @issan2026; @gomezserrano2026]. These results do not address a given coil set or the boundary iteration. The open issue is whether and how fast GVEC's boundary iteration reaches the root.

- The axisymmetric analogue has a well-posedness theory [@temam1975; @temam1977], and axisymmetric free-boundary codes solve the coupled plasma–vacuum problem by Newton [@heumann2015; @faugeras2017]. The common statement that Picard iteration fails for vertically unstable equilibria was not checked against a source here.

1. **Descent cannot converge to a saddle of Ŵ.** [D] With fixed coil currents an elongated tokamak is vertically unstable, so its equilibrium is a saddle of Ŵ. KIN6D measures this on the same ITER cases: rigid K_Z = −5.4e6 J/m² per period on FB-cut 0.997 v2 and −5.2e6 on the FB-taper base state; n=0 Schur eigenvalue down to −3.9e-7 (`kin6d/docs/ideal-free-boundary.md`, NL-3a and solver-revision sections). Linearized at a saddle, a preconditioned descent step `δ ← (I − dt P⁻¹H)δ` has an eigenvalue `1 + dt|λ|/p > 1` along the negative direction. GD, heavy-ball mGD and the positive-definite quasi-Newton updates (Powell damping keeps dBFGS definite, `free_b_minimizer_dBFGS.F90:158–163`) all amplify that direction (derivation §9); SR1 and ADAM are not covered. So convergence is possible only from the stable manifold, or because the negative curvature is below the iteration's noise and step floor. Whether this, rather than ill-conditioning, explains the GD stalls is **[H]**: the run records cannot separate the two, and WHY_GVEC §3 ranks the [[B²]] target floor first.
2. **Rate on soft modes.** [D] Away from the saddle the descent rate is set by `λ_min/λ_max` of `P⁻¹H`. KIN6D measures `K_R/|K_Z|` ≈ 600 on its gs_free fixture and ≈ 46 on ITER FB-cut 0.997 v2 (`K_R = +2.5e8`). WHY_GVEC estimates the position and shape forces at about 1e-5 of B² per 15 mm, against a target floor of 1–2.5e-4. Both are consistent with the 12 mm stalls [H].
3. **Relabelling nulls.** Full boundary coefficients (X1_b, X2_b) include tangential reparametrizations of the boundary curve. The physical force is normal only (E5, E8), so these directions have zero physical gradient and zero physical stiffness; only condensation gives them stiffness [D]. Descent ignores them; Newton on full coefficients sees a near-singular Jacobian. The fork's normal basis removes them. In the interior, the fixed-boundary minimizer handles the relabelling at each solve. KIN6D shows on its gs_free fixture what a missing gauge does to Newton: drift of 1–5 cm along the n=0 slide null, a 7 mm stall when over-constrained, and return in about 3 steps once the gauge is exact (`kin6d/docs/ideal-free-boundary.md`, formulation and "Relabelling (slide) gauge" sections). Whether GVEC's interior λ/θ gauge creates a similar soft direction for the boundary Newton is **[H]**.
4. **What a variational or gauged Newton needs.** [D] (i) The second variation of Ŵ including `D(½B_ext²)[ξ]` (derivation §9); (ii) an exact gauge for tangential and interior relabelling; (iii) a method for indefinite systems (LDLᵀ/LU or bordered vertical coordinate) instead of positive-definite quasi-Newton; (iv) for a variational merit, fixed circulation or c as an explicit unknown (root finding on the coupled map with c(X) needs neither); (v) ε_spectral=0 in the residual; (vi) an absolute residual target, since relative merit and step tests stop on soft modes. KIN6D implements (i)–(iv) and (vi) natively; on ITER FB-cut 0.997 v2 its ±15 mm R/Z offsets return within about 0.2 mm, while +2 % elongation is not converged (8.4 mm, NL-3a). The fork implements (iii) and (v) with an FD Jacobian and root finding with c taken from the state (fork `free_boundary.py:1173–1187`); elongation and K+ starts still miss by 5 mm. The fork's hypothesis that these stop at a different root or along a flat direction is untested.

## References not verified

Left out of `writeups.bib`: the "Lee & Kim" coil Biot–Savart reference (not identified); Bauer–Betancourt–Garabedian 1978; Blum's 1989 book; Merkel's Varenna 1987 proceedings (local Zotero record only, no DOI); the journal version of [@conlin2024].

## Open

- Run the fork's `newton_gtol` (ca733fe4) on elong2/K+; compare \|g\| floor with the contour start's 2.3e-4.
- Measure the rigid vertical stiffness through GVEC's own boundary force (FD of F_b along a rigid Z shift) and compare its sign with KIN6D.
- Check the 3D/general-hmap force coefficients against EvalEnergy by FD (the 16 local identities cover axisymmetric RZ only).
- Derive the J0 normalization (`txx:150–160`) and the I sign for non-RZ hmaps.
