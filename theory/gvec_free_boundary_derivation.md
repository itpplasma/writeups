# GVEC free-boundary residual: derivation

Citations `[@key]` refer to [writeups.bib](../writeups.bib). Source pins, paths and labels as in the [source correspondence](gvec_free_boundary_source_correspondence.md): upstream gvec 7da1182fd81b1ba552142bb663319d74c7edfb8b, `evalfunc` = `src/functionals/mhd3d/mhd3d_evalfunc.F90`, `mhd3d.F90` = `src/functionals/mhd3d/mhd3d.F90`; fork itpplasma/gvec `develop` b37d82b3c3c27589061f2bddc00bbb25139e2ffe for §10.

- Scope: fixed pressure (γ=0), frozen Φ and χ profiles, nested surfaces, J>0, maps with q3=ζ. §1–§7 derive the residual GVEC assembles; §8 gives the vacuum-energy variation a variational formulation would use; §9 the second variation and the linear descent analysis; §10 the Jacobian of the fork's projected Newton residual.
- Labels: **[V]** read from the pinned source; **[D]** derived here; **[H]** not shown. Continuum identities are derived for smooth fields; discrete statements say which quadrature they use.
- Native KIN6D theory (itpplasma/kin6d `main` f5420f386bf9e032eec99b0df1f99016a66ac043): formulation and obligation map `docs/free-boundary-theory.md`, first variation `theory/derivations/free-boundary-first-variation.md`, gauge, bordering and vertical saddle `theory/derivations/free-boundary-gauge-vertical.md`, Newton/descent/Picard `theory/derivations/free-boundary-iterations.md`, Lean lemmas B1/B2 `proof/Kin6d/Bordered.lean`, measurements `docs/ideal-free-boundary.md`. Not repeated here; §8 reaches the same first variation independently.

## 1. Unknowns

- `X1(s,θ,ζ) = Σ_i Σ_j X1_ij N_i(s) φ_j(θ,ζ)`, the same for X2 and λ. N_i are B-splines, φ_j are `sin/cos(mθ − n nfp ζ)`. [V]
- Boundary coefficients `b = (X1_{nBase,j}, X2_{nBase,j})`. The last B-spline is interpolatory: `N_nBase(1) = 1` and `N_i(1) = 0` otherwise (code comment `evalfunc:1563`, clamped knot vector). [V]
- Interior coefficients `u`: all other rows not fixed by axis constraints.

## 2. Discrete energy

`evalfunc:516–539`:

```text
W_h(u,b) = Δθ Δζ Σ_g w_g Σ_k [ ½ b^α g_αβ b^β / J + μ0 p(s_g)/(γ−1) J ]   at nodes (s_g, θ_k, ζ_k)
```

- `Δθ = 2π/m_nyq` and `Δζ = (2π/(n_nyq nfp))·nfp` (`src/base/fbase.F90:300–301, 319`). The nodes cover one field period and the weight covers the full torus. [V]
- With γ=0, `1/(γ−1) = −1` (`mhd3d.F90:121`), so `W_h ≈ ∫(½B² − μ0 p) dV = μ0 W_phys`. Units T² m³. [V]
- `b^θ = χ′ − Φ′ ∂ζλ`, `b^ζ = Φ′(1 + ∂θλ)` (`evalfunc:403–404`), so `B² = b·g·b/J²`. [V]
- `J = J_h J_p`, `J_p = ∂sX1 ∂θX2 − ∂sX2 ∂θX1` (`evalfunc:321–324`). [V]

## 3. Discrete gradient

At each node the integrand `L` depends on the coefficients only through the nodal values of `(X, ∂sX, ∂θX, ∂ζX, ∂θλ, ∂ζλ)`, and these are linear in the coefficients. The chain rule gives exactly [D]

```text
−∂W_h/∂X1_ij = Δθ Δζ Σ_g w_g Σ_k [ c0 N_i φ_j + cθ N_i ∂θφ_j + cζ N_i ∂ζφ_j + cs N_i′ φ_j ],
c0 = −∂L/∂X1,  cθ = −∂L/∂(∂θX1),  cζ = −∂L/∂(∂ζX1),  cs = −∂L/∂(∂sX1).
```

- `EvalForce` assembles exactly this sum. It projects coefY, coefY_thet, coefY_zeta, coefY_s with weight `w_g Δθ Δζ` (`evalfunc:672–681`) and contracts them with `N_i` and `N_i′` (`:686–697`). [V]
- Radial coefficient. g_ss does not enter because b^s = 0, so `∂sX1` enters L only through J. With `∂L/∂J = −b·g·b/(2J²) − μ0 p = −(½B² + μ0 p)` and `∂J/∂(∂sX1) = J_h ∂θX2`:

  ```text
  cs(X1) = (½B² + μ0 p) J_h ∂θX2 = dW J_h ∂θX2,      cs(X2) = −dW J_h ∂θX1.
  ```

  This matches `evalfunc:615` (dW), `:665` and `:748`. [D, V]
- The pointwise identity `coef = −∂L/∂(·)` is checked exactly for all coefficients only in axisymmetric RZ (16 native identities, [discrete force audit](gvec_discrete_force_audit.md)). For general 3D hmaps it is [H]. Where it holds, `F_MHD3D = −∇W_h` exactly, up to roundoff.

## 4. Boundary row and reduced plasma functional

- The fixed-boundary solve drives `∂_u W_h(u, b) → 0` to `minimize_tol`. Define the reduced functional `Ŵ_p(b) = W_h(u*(b), b)`. [D]
- Envelope theorem: `dŴ_p/db = ∂_b W_h(u*, b) + ∂_u W_h · du*/db = ∂_b W_h`, so `−dŴ_p/db = F_MHD3D(nBase, ·)`, the row used at `evalfunc:872–873`. [D]
- Blending (`mhd3d.F90:1312–1330, 1400`) changes u together with b. Since `∂_u W_h = 0` at u*, this has no first-order effect on Ŵ_p. It only changes the starting point of the next interior solve. [D]
- This reading needs no claim about pressure balance. Its errors are the interior tolerance and, for general hmaps, §3's [H].

## 5. Strong form of the boundary row

The code comment (`evalfunc:1559–1563`) interprets the row as a pressure jump. In continuous s with exact angular integrals:

```text
F(nBase, j) = ∮ cs(s=1) φ_j dθdζ + ∫_0^1 N_nBase(s) ∮ R1 φ_j dθdζ ds,
R1 = c0 − ∂θcθ − ∂ζcζ − ∂s cs.
```

This follows from `∫ cs N′ ds = cs(1)N(1) − ∫ ∂s cs N ds` and periodic integration by parts in θ and ζ. [D]

- R1 is the strong X1 Euler–Lagrange residual. The interior solve makes it orthogonal to `N_1 … N_{nBase−1}`, not to N_nBase.
- The remainder is supported on the last element, width h. It vanishes only when R1 = 0 pointwise there. Gauss quadrature does not reproduce the integration by parts exactly, because `1/J` is not polynomial.
- So the boundary row equals the pressure-jump term plus an O(h·R1) last-element remainder and a quadrature defect. Their size is not measured. [H]

## 6. Normal vector for a general hmap

Write `x = h(q1, q2, q3)` with `q3 = ζ`. The covariant basis `a_i = ∂h/∂q_i` has `J_h = a1·(a2×a3)`. On s=1:

- `x_θ = X1_θ a1 + X2_θ a2`
- `x_ζ = X1_ζ a1 + X2_ζ a2 + a3`
- a boundary variation with `δq3 = 0`: `δx = δX1 a1 + δX2 a2`

```text
δx·(x_θ × x_ζ) = J_h det[[δX1, δX2, 0], [X1_θ, X2_θ, 0], [X1_ζ, X2_ζ, 1]]
              = J_h (δX1 ∂θX2 − δX2 ∂θX1).
```

[D]

- For hmap_RZ, `x_θ×x_ζ = R(Z_θ e_R − R_θ e_Z)`, the outward normal when θ runs counterclockwise and J>0.
- Hence `J_h(δX1 ∂θX2 − δX2 ∂θX1) dθdζ = ξ_n dA`, with `ξ_n = δx·n`, n the outward unit normal and `dA = |x_θ×x_ζ| dθdζ`. [D]

## 7. Assembled boundary force

Exterior term (`evalfunc:1626, 1630`), projected with the same `Δθ Δζ` (`:1628, 1632`):

```text
F_b,X1(j) = Δθ Δζ Σ_k [ −½ B_ext² J_h ∂θX2 − ε_m ∂θX1 I_s ] φ_j
F_b,X2(j) = Δθ Δζ Σ_k [ +½ B_ext² J_h ∂θX1 − ε_m ∂θX2 I_s ] φ_j
```

- `I_s = X1_c ∂θX1 + X2_c ∂θX2`, with `X_c` the boundary series weighted by `m^p(m^q − M)`, q=1, p=Q−1=4, and `ε_m = ε/Σ m^p (X_mn)²` (`:1584–1619`). [V]

Sum with §5 (`Force_b = F_MHD3D(nBase) + F_b`, `evalfunc:872–873`). For a boundary variation `δX_b = Σ_j δX_j φ_j`:

```text
Force_b · δb = ∮ (dW|_{s=1} − ½ B_ext²) ξ_n dA − ∮ ε_m I_s (∂θX1 δX1 + ∂θX2 δX2) dθdζ + (last-element remainder).
```

[D]

- The two pressure terms carry the same normal and the same full-torus weight. The 2π in `Phi_edge/2π` sits in Φ′, so B, B_ext and dW are in T² consistently. B_ext is computed on one period by BIEST and replicated nfp times. [V]
- Condensation term. For hmap_RZ, `∂θX1 δX1 + ∂θX2 δX2 = x_θ·δx` restricted to the poloidal plane. It is therefore tangential pointwise. [D]
  - It enters the Fourier coefficients through the projection onto the truncated basis, and through the mode-wise preconditioner when that is on.
  - So the update it produces is not exactly tangential. The fork measured a ~0.4 mm shift when it was left in the Newton residual (commit a507bd82). The mechanism through the normal-basis projection P is [H].

## 8. Vacuum-energy variation

Setup [D]:

- V is the exterior of the plasma, with boundary Γ and unit normal n pointing out of the plasma into V.
- The coil currents are fixed. They have smooth density supported in V away from Γ, and free-space field `B_c`.
- The plasma's net toroidal current I is fixed, so `c = μ0 I` is the period of ψ around poloidal loops.
- Admissible exterior fields are `B = B_c + ∇ψ`, with ψ multivalued with period c and `∇ψ → 0` at infinity.
- Define

  ```text
  G(Γ, ψ) = ½ ∫_V |B_c + ∇ψ|² dV,      m(Γ) = min_ψ G(Γ, ψ).
  ```

- G is finite: the coil density is smooth, PF and plasma currents are dipoles at infinity, and the TF field is confined. G is strictly convex in ∇ψ.
- Its Euler–Lagrange equations are `Δψ = 0` in V and `B·n = 0` on Γ. Variations δψ are single valued, so the cut contributes nothing.
- This is the problem BIEST solves: `B_pl = ∇S[σ] + ∇×S[J0] I0` is curl-free in V with circulation I0 and `B·n = 0` (`vacuum-field.txx:120–215`). [V for the code, D for the equivalence]

Potential at fixed currents [D]:

```text
L(X, ψ) = W_p(X) − G(Γ(X), ψ),     Ŵ(Γ) = max_ψ L = W_p − m(Γ).
```

- L is a minimum in the plasma and a maximum in ψ. This matches the KIN6D Lagrangian `W_p − E_v/μ0` at fixed coil currents and fixed circulation (`kin6d/docs/ideal-free-boundary.md`, Formulation).
- The variational principle with vacuum goes back to Kruskal–Kulsrud [@kruskal1958].

Shape derivative [D]:

- Let `Γ_ε = {x + ε ξ}`. G is stationary in ψ at ψ*, so the envelope (Céa) argument applies with a smooth extension of ψ*, and only the domain change contributes.
- V loses the layer `ξ_n dA` where `ξ_n > 0`. The Hadamard formula, with V's outward normal `−n`, gives

```text
dm[ξ] = −½ ∮_Γ |B_ext|² ξ_n dA,      so   d(−m)[ξ] = +½ ∮_Γ B_ext² ξ_n dA.
```

Plasma side: §4–§5 give `dŴ_p[ξ] = −∮ (½B_in² + μ0 p) ξ_n dA` at the interior equilibrium. Hence

```text
−dŴ[ξ] = ∮ (½B_in² + μ0 p − ½B_ext²) ξ_n dA,
```

and stationarity is `[[B²/2 + μ0 p]] = 0`. [D]

What the vacuum-energy variation adds to GVEC's residual:

1. **At first order, nothing.** GVEC's `−½B_ext² N·δq` (E6) is exactly `d(−m)` evaluated with the current B_ext.
   - `update_boundary_MHD3D` re-evaluates the force after `set_Bext_squared` (`mhd3d.F90:1383`; `python/gvec/core/minimize.py:764–766`), so B_ext is current at every update.
   - "Frozen B_ext²" is not a missing first-order term. It means the dependence `B_ext(Γ)` is absent from the step metric and from any merit function. [D, V]
2. **The value −m(Γ).** GVEC never evaluates it, so no update can test decrease of Ŵ. [V]
3. **A circulation term, when c is not fixed.** Write `ψ = c w + φ̃`, with w a fixed multivalued function of unit period. The envelope argument in φ̃ gives `∂m/∂c = ∫_V B·∇w dV`. Integrating by parts (`∇·B = 0`, `B·n = 0` on Γ, decay) gives `∂m/∂c = ±Ψ_Σ`, the flux of B through a cut surface Σ that every poloidal loop crosses once; the sign depends on how Σ is oriented. [D]
   - With prescribed iota, GVEC resets `c = μ0 I_tor(1)[X]` from the state at every update (`free_boundary.py:555–561`). A gradient of one functional would carry `∓Ψ_Σ dc[ξ]`; GVEC drops it, so successive steps descend different functionals `Ŵ(·; c_k)`. [D]
   - With a prescribed `I_tor` profile, c is constant and the term is absent.
4. **The second variation**, §9. This is the one that matters for Newton.

## 9. Second variation and descent near a saddle

Linearization of the vacuum term in a normal direction `η = η_n n` [D]:

- Exterior field. Differentiate `B·n = 0` along `Γ_ε`. Use `n′ = −∇_Γ η_n`, and `∂_n B_n = −∇_Γ·B_t` from `∇·B = 0` with `B_n = 0`. The Eulerian derivative `B′ = ∇ψ′` then solves

  ```text
  Δψ′ = 0 in V,    ∂_n ψ′ = ∇_Γ·(η_n B_t) on Γ,    ψ′ single valued, decaying.
  ```

  B_c does not depend on Γ.
- On the moving surface, `D(½B_ext²)[η] = B_ext·∇ψ′[η] + η_n n·(B_ext·∇)B_ext`. The second term uses `∇(½B²) = (B·∇)B` for curl-free B.
- Symmetrization by Green's identity in V gives `∮ ξ_n B_t·∇_Γψ′[η] dA = ∫_V ∇ψ′[ξ]·∇ψ′[η] dV`.
- Hessian of `−m`, in the normal directions:

  ```text
  D²(−m)[ξ,η] = ∫_V ∇ψ′[ξ]·∇ψ′[η] dV + ∮ ξ_n η_n n·(B_ext·∇)B_ext dA + (geometric variation of dA and n at frozen B_ext²).
  ```

  - The first term is nonlocal and positive semidefinite (vacuum stiffening).
  - The second is local and carries the curvature and decay index of the external field. It has either sign.
- GVEC's boundary preconditioner contains only part of the geometric term: `½ B_ext² ∂J_h/∂q ∂θX`, mode-diagonal (`evalfunc:1145–1163, 1289, 1372`). [V]
- Neither of the first two terms is formed anywhere in upstream GVEC. The fork's Newton obtains all of them by finite differences of the full residual: central differences since 81fe6405 (two interior solves and two BIEST calls per normal coordinate, fork `free_boundary.py:887–926`, difference quotient `:907`), forward differences before. [V]

Rigid vertical shift in axisymmetry [D]:

- For hmap_RZ, a rigid Z translation leaves W_p unchanged (`J_h = R`; the metric does not depend on Z). So the reduced Hessian along this direction is the vacuum part only.
- Its sign is set by the coil field. KIN6D measures `K_Z = −5.4e6` (FB-cut 0.997 v2) and `−5.2e6 J/m²` per period (FB-taper base) on the ITER cases, i.e. a negative direction of Ŵ (`kin6d/docs/ideal-free-boundary.md`, NL-3a and solver-revision sections). [V for the record]

Linear descent near a stationary point b* with reduced Hessian Ĥ [D]:

- GD step `b ← b − dt P⁻¹∇Ŵ`, P positive diagonal (`Precond_b`). Error map `e ← (I − dt P⁻¹Ĥ) e`. The eigenvalues of `P⁻¹Ĥ` have the signs of Ĥ's (Sylvester). A negative eigenvalue λ gives an amplification `1 + dt|λ| > 1`.
- BFGS, dBFGS, lBFGS step `−B_k⁻¹∇Ŵ` with `B_k` symmetric positive definite; Powell damping keeps it so (`free_b_minimizer_dBFGS.F90:158–163`). `B_k⁻¹Ĥ` is similar to `B_k^{−1/2} Ĥ B_k^{−1/2}`, which has Ĥ's inertia, so again an eigenvalue `> 1`.
- Heavy-ball momentum (mGD): the characteristic roots of `μ² − (1 + β − dt λ)μ + β = 0` include one `> 1` for λ < 0, 0 ≤ β < 1.
- So these methods converge to a saddle only from its stable manifold, or when the negative growth stays below the step and noise floors.
- SR1 updates can be indefinite and are not covered. ADAM is nonlinear and not covered. [H]
- On the positive subspace, GD converges with factor `max(|1 − dt λ_i/p_i|)`, at best `(κ−1)/(κ+1)` for condition number κ of `P⁻¹Ĥ`. For a stiff toroidal-field/area mode and a soft position or shape mode, this is slow even without a saddle. [D]
  - Which of the two limits GVEC's 12 mm stalls on TC24 is [H]. The run records do not separate them (`/mnt/storage/codex-equilibrium-20261011/gvec/WHY_GVEC.md` §2–3).

## 10. Projected Newton Jacobian

The fork's Newton solves `g(y) = P(x)ᵀ r(x) = 0`, `x = x_start + P y`, with r the boundary residual (§7 with ε=0) and P the normal-coordinate basis. [V for the form, fork `free_boundary.py:779–1068`]

- If P depends on the current boundary, the chain rule gives [D]

  ```text
  Dg[δy] = Pᵀ Dr P δy + (DP[P δy])ᵀ r.
  ```

  The second term is first order in r. Before 81fe6405 the fork rebuilt P after each accepted step (a507bd82 `free_boundary.py:968`) but used `Pᵀ Dr P` (FD) and Broyden updates as if P were constant, so it omitted this term. An independent FD probe on the 10 mm radial-return fixture found it, largest difference 9.55e-5 in the probed column. [V, fork lane report]
- With P fixed for a whole solve (81fe6405, P built once at `:866`), `DP = 0` and `Dg = Pᵀ Dr P` exactly, also for r ≠ 0. A rectangular regression with nonzero residual and an indefinite mode checks the FD `dg/dy` to 7.35e-15. [D, V]
- The roots differ only through range(P): `Pᵀ r = 0` is the weak pressure balance tested on the normal traces in range(P). A basis spanning only the X1 functions (before 1991c38f) tests fewer traces; with cos-only X1 the odd trace of a rigid vertical shift is absent, so `g = 0` does not imply vertical force balance and the vertical coordinate is not an unknown. [D]
- Whether the omitted term or the incomplete basis caused the 12.3 mm radial and 10.0 mm vertical stalls of the fork's return fixture is not separated: the 10 µm returns were measured only with both fixes and central differences in place, and no single-fix run exists. [H for the split]
- The residual merit `|g|` has no energy-descent requirement, so the indefinite fixed-current vertical direction of §9 is admissible for the Newton step; descent methods remain covered by §9. [D]

## 11. Open derivation items

- FD check of `F_MHD3D = −∇W_h` for a 3D, non-RZ hmap (§3).
- Size of the last-element remainder and of the quadrature defect in §5, under radial refinement.
- Normalization `J0 ← J0·NFP·Nt·Np/Jtor_flux·orientation` (`vacuum-field.txx:150–160`) giving unit poloidal circulation, and the sign of I for non-RZ hmaps.
- Sign convention of `∂m/∂c = ±Ψ_Σ` fixed against an exact filament oracle.
