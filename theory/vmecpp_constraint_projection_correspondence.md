# VMEC++ auxiliary constraint and projection

- Source: VMEC++ `a4150a4e2101bd47868d040f3adee5d0304ce89b`, `ntor=0`, fixed boundary. [Source receipts and replay](cas/vmecpp_constraint_projection/provenance.json); [native symbolic checks](cas/vmecpp_constraint_projection/symbolic_results.json).
- This checks actual local constraint kernels, harmonic support and conditional weak variations. It does not reconstruct the live TC24 multiplier or prove native stopping equals continuous MHD force balance.

## Executed lifecycle

- `ideal_mhd_model.cc:183–188`: `P_m=m(m-1)`; scalar filter gain is `-signgs/[4*m²*(m+1)²]`.
- Lines499–503 and1576–1601: at startup/soft reset with vacuum state Off/Initializing, offsets are `RCon0=s*(P R)_LCFS`, `ZCon0=s*(P Z)_LCFS`.
- Lines653–703: multiplying those offsets by0.9 occurs inside the **free-boundary** branch, when vacuum pressure is on. Fixed-boundary offsets remain inherited from the boundary; do not assume they decay to zero.
- Lines2430–2488: radial multiplier uses live R/Z preconditioner entries divided by angular tangent norms, the declared tcon0 and radial grid. Those live entries and offsets are absent from wout.
- With `h=1/(ns-1)`, its explicit geometric factor is `64*h²*(1+ns/60+ns²/24000)`, tending to `1/375`. This is conditional algebra: the live preconditioner/tangent ratio may scale too. Neither a vanishing nor a persistent continuum constraint is proved.

## Scalar support versus assembled weak force

- Define `C=(P R-RCon0)*R_theta+(P Z-ZCon0)*Z_theta`.
- The actual header `constraint_force_kernel.h` keeps scalar harmonics `1<=m<mpol-1`, excluding m0 and the highest geometry harmonic. At MPOL24 it keeps1..22.
- Then it multiplies the filtered `g=L C` by geometry/tangents. `brmn/bzmn` multiply **derivative** test functions; `frcon/fzcon` multiply `P_m` in the final Fourier force assembly. These are not pointwise R/Z SI force components.
- For fixed self-adjoint L and fixed offsets, the constraint variation is

\[
\delta E_C=\langle g,(P\delta R)R_\theta+(P R-RCon0)\delta R_\theta
 +(P\delta Z)Z_\theta+(P Z-ZCon0)\delta Z_\theta\rangle.
\]

- This equals `delta[0.5<C,L C>]` under those predicates. The live multiplier depends on geometry; no fixed global penalty functional is established.
- `ideal_mhd_model.cc:912–1001` projects MHD plus constraint forces, applies the m1 gauge/allowed-mode constraints, then forms invariant residuals; preconditioning follows. A residual criterion is a discrete projected statement, not a bound on unrepresented continuous force.

## Exact manufactured harmonic example

- Take `R=R0+a*cos(theta)+e*cos(k*theta)`, `Z=a*sin(theta)`, zero offsets; set `P=k(k-1)`.

\[
C=-\frac{aPe}{2}[\sin((k+1)\theta)-\sin((k-1)\theta)]
  -\frac{kPe^2}{2}\sin(2k\theta).
\]

- For k23 at MPOL24, C contains22,24,46; the filter keeps22. Multiplication by geometry can subsequently generate harmonics through45. High-harmonic strong force is therefore possible without a filter defect.
- A geometry containing only m0/m1 has `P R=P Z=0`; its constraint is zero **only when offsets are also zero**, as for an m0/m1 boundary and its initialized offsets.
- For maximum geometry harmonic K, scalar C has degree at most2K when offsets share that support. A `C²` energy can reach4K. At K23, ntheta256 resolves these finite polynomial products; rational metric/field products have no such finite degree bound.

## Checked evidence and remaining gaps

- Native CMake/CTest compiles the actual pinned constraint header:27 sine/cosine/manufactured support cases, symmetric and asymmetric charts; gain/support error below2.9e-16.
- Actual effective-force and AddConstraintForces kernels match exact scalar-energy derivatives for k2/12/23, with zero and nonzero fixed offsets; odd radial factors checked. tcon0 disabled and excluded upper-band modes are negative controls.
- Native FortSym verifies seven exact amplitude/chain/offset/scaling identities and rejects the omitted derivative-test-function term. Fourier orthogonality is an explicit assumption, independently exercised by native harmonic tests.
- The tests exclude copied-kernel and wrong derivative-basis interpretations. They do not establish a solver defect, quantify live TC24 cancellation, or prove complete projection/preconditioning equivalence.
- Remaining discriminator: same historical law, fixed MP24/tcon0, ns65/129/257 on identical physical queries, then a separately converged angular control. Shared interpolation/model error must be tested alongside a native-code defect.
