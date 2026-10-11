# Prescribed-q fixed-boundary equilibrium

`solve_gs_prescribed_q` solves the current Phase 3 contract on curved P2/P3:
constant physical pprime, a signed q(s_pol) table, and signed total toroidal
Phi. The boundary gauge is psi=0. q and Phi have the same nonzero sign;
the supported branch has an interior minimum of psi and nonnegative pressure.
Reversing both q and Phi reverses F and Bphi while preserving psi and FFprime.
The input F_edge is not an inverse constraint. The solver recovers it.

The current cubic-profile forward engine supplies the weak GS equation.
Continuous cubic B-splines represent FFprime(s_pol); their exact polynomial
primitive defines F squared, anchored at the solved F_edge. FortNum supplies
the spline basis and derivatives. The outer equations set the native area
integral of F/R to Phi and the weighted moments of (q_native/q_input - 1) to
zero. The weights are B_i(s)*s*(1-s): axis Hessians and one-sided boundary
values receive zero measure. The residual is sampled uniformly in sqrt(s).
This avoids feeding pointwise Hessian error into the recovered source law.
The full off-moment profile is checked separately, including the endpoints.

FortNum's numerical root solver proposes the profile coefficients; its central
secant Jacobian is a solver approximation, not a sensitivity product. The
forward state's fixed-law tangent/adjoint remains the equation-level cubic
Jacobian. Full inverse-input and curved/P3 contour sensitivities are explicitly
unavailable; the legacy affine-P2 response oracles below remain supported.
No derivative of an iteration sequence is reported.

`gs_phase1` selects this mode with `q_file` and `phi_target`, along with the
ordinary `pprime`, `mu0`, boundary and mesh options. `q_file` contains a row
count followed by ascending `s_pol q` pairs, at least four rows, spanning 0..1.
Local four-point cubic interpolation defines the input q law. `profile_file`
and `q_file` are mutually exclusive. `inverse_intervals` (default 2) is the
number of cubic FFprime spline intervals; `nonlinear_tolerance` controls the
outer residual (default 1e-9), and `q_tolerance` controls the independent
relative q defect (default 1e-3). Radial/angular budgets have the same meaning
as forward readback. Refine both mesh and profile budgets when needed.

After convergence, an interleaved radial grid and doubled angular budget
check q independently of the fitted moments. Status 9 retains the physical
candidate but rejects its q accuracy. Source, contour, boundary geometry and
profile truncation errors remain numerical errors measured by refinement.
The nonlinear recovered-flux diagnostic has status 4: it controls the frozen
source defect, without an inverse-equilibrium stability bound.

`profile-law.dat` contains the recovered pprime/FFprime law and signed F_edge.
The native field reader consumes that file; `profiles.dat` contains the actual
q, p, F, pprime and FFprime. NetCDF retains the literal/resolved namelist,
input q table, Phi constraint, solved law and provenance. The iter_tc24
producer extension uses the Phase 3 `prescribed_q` schema without using the
case's forward FFprime or nominal F_edge as constraints.

The behavioral CTests cover an independent Phase 1 Solovev q integral, P3
psi/field/source convergence, constant-q zero/finite-pressure self-convergence,
signed mesh/profile round trips, off-profile rejection, and the CLI/NetCDF
contract. They contain no frozen solution snapshots.

## E1 continuous coupled linear estimate

A continuous linear estimate separates coupled q-profile stability from the
frozen-source residual diagnostic. This estimate applies to smooth solutions
of the linearized equations at one constructed E1 forward state. It does not
establish existence of the prescribed-q/Phi target or change the solver's
status-4 inverse-equilibrium diagnostic.

### Physical-disk state and hypotheses

Use the exact disk `(R-6.2)^2+Z^2<0.62^2`, zero boundary flux and zero pressure.
Put `X=(R-6.2)/0.62`, `Y=Z/0.62` and define the comparison polynomial
`p=(1-X^2-Y^2)Q`, where

```text
Q = -0.6790006140025554 - 0.0017770331708278058 Y^2
    - 0.000007398162010552908 Y^4 - 0.01696288407071555 X
    - 0.000028102526808112354 X Y^2 - 0.0009254066813575565 X^2
    - 0.000014918763351629 X^2 Y^2 - 0.0000816198051169326 X^3
    - 0.0000037684611922780744 X^4.
a_v = -0.67910666625417071,
g(t) = c0+c1 s+c2 s^2+c3 s^3,  s=1-t/a_v,
(c0,c1,c2,c3) = (-7.0559048663098558,-0.06500580748754814,
                 -0.00050826590225128143,-0.0000017952327766579401).
```

These decimals define exact rational comparison/profile data. They were
selected from the retained E1 inverse run
`kin6d-inverse-20261009-ccabcc5_kin6d_E1_constant_q_A10_03_t0`; agreement with
its sampled finite-element state is not used in the estimate. Define the smooth
forward state by `-Delta*psi=g(psi)`, with zero boundary flux, in the local
neighborhood of p constructed below. Set
`H(t)=F_edge^2/2+integral_0^t g(z) dz`,
`F(t)=sqrt(2H(t))`, with `F_edge=32.704097175474018`.
The normalization a_v is part of g; the actual axis value `a=min psi` is a
separate quantity. This forward state need not have the requested constant
q=1.5 or total Phi.

Let T be the disk Dirichlet inverse of `-Delta`. The forward construction
uses `psi=sqrt(R)u`, `P=-Delta+3/(4R^2)` and
`rho=(R*(p_RR+p_ZZ+g(p))-p_R)/R^(3/2)`. The disk Green inverse gives
`||P^-1 f||inf<=0.097||f||inf`, `||D P^-1 f||inf<=2.49||f||inf` and
`||D2 P^-1 f||inf<=0.66||f||inf+2.48 Lip(f)`.
Absolute polynomial coefficient sums, after clearing the R factor, give
`||rho||inf<0.0002`, `Lip(rho)<0.0015`,
`lambda_min(D2p)>3.09`, `||D2p||op<3.961` and `Lip(p)<4.6`.
On the full flux ball `[-0.72,0.01]`, the profile obeys
`|g|<7.13`, `|g'|<0.1`, `|g''|<0.003`, `|g'''|<0.00004`, with `g'<0`.
The map
`delta u=P^-1((g(p+sqrt(R)delta u)-g(p))/sqrt(R)+rho)`
has C0 contraction factor below 0.0097 and a self-mapped ball within that
flux range. Differentiation of the same equation yields
`||psi-p||inf<0.000052`, `||D(psi-p)||inf<0.00132` and
`||D2(psi-p)||op<0.011`.

The smooth state is negative in the interior, strictly convex, with one
nondegenerate axis and regular nested contours. Conservative bounds are
`0.67<|a|<0.7`, `3I<D2psi<4.1I` and `32<F<34`.

### Coarea endpoint control

All derivatives here use outward-increasing physical flux `t in [a,0]`.
Define
`K(t)=integral_{psi=t} 1/(R|grad psi|) dl`; endpoint values are smooth limits.
Let `d=0.62` be the physical disk radius. All spatial derivative tensor
bounds in this section use the full multilinear operator norm. Higher
disk-Green derivatives, after subtracting respectively linear and quadratic
source Taylor polynomials, give

```text
||D3 Tf|| <= 0.75||Df||+4d||D2f||,
||D4 Tf|| <= 1.25||D2f||+4d||D3f||.
```

The polynomial loads supply the 0.75 and 1.25 terms. Applying these to
`-Delta u=R^(-1/2)g(psi)-3u/(4R^2)` gives
`||D3psi||<5.3`, `||D4psi||<6.5`, in full multilinear operator norm.
To retain the axis cancellation, use signed rays from the axis x0:

```text
J(r)=e^T D2psi(x0+r e)e,
B_ray(r)=integral_0^1 J(ur) du,
A_ray(r)=2 integral_0^1 (1-u)J(ur) du,
psi=a+r^2 A_ray/2,  v=sign(r)*sqrt(t-a),
C_ray(r)=1/(R(r)B_ray(r)),  K(v)=integral_0^(2pi) C_ray(r(v,theta)) dtheta.
```

Opposite rays make the integrated K(v) even, so `K_v(0)=0`. With
`lambda=3`, `Lambda=4.1`, `D3=5.3`, `D4=6.5`, `Rmin=5.58`, set

```text
C1=1/(Rmin^2 lambda)+D3/(2 Rmin lambda^2),
C2=2/(Rmin^3 lambda)+D3/(Rmin^2 lambda^2)
   +D3^2/(2 Rmin lambda^3)+D4/(3 Rmin lambda^2).
```

The ray derivatives satisfy
`r_v^2<=2Lambda/lambda^2` and
`|r_vv|<=4Lambda D3/(3lambda^3)`.
Consequently the endpoint-inclusive bound is
`||K'||inf<=pi*((2Lambda/lambda^2)*C2+(4Lambda D3/(3lambda^3))*C1)<0.7`.
The same state bounds give `0.2<K<0.4`.

### Linear a-priori bound with axis residual

Let `A=-div(grad/R)`, `B=A-H''(psi)/R`, `b=delta H`,
`w=K/F^2`, `c=2pi delta q/F`, and
`M_h(t)=integral_{psi=t} h/(R|grad psi|) dl`.
The actual derivative equations are

```text
B h-b'(psi)/R=r,
w b-M_h'=c,
h|boundary=0,  h(x0)=alpha.
```

Here r is a spatial residual functional, delta q is the physical-flux q
variation and alpha is the axis-value variation. Define
`||h||_a^2=integral |grad h|^2/R`,
`||h||_B^2=||h||_a^2-integral H''(psi)h^2/R`, and
`||b||_w^2=integral_a^0 w b^2 dt`.
The norm `||r||_{a,*}` is dual to `||h||_a` on zero-trace functions.
Since `H''=g'<0`, `||h||_B>=||h||_a`.

For alpha=0, smoothness gives `M_h(a)=M_h(0)=0`.
Testing the spatial equation by h and integrating by parts in physical flux
therefore gives

```text
||h||_B^2+||b||_w^2=r(h)+integral_a^0 b c dt.
```

Cauchy-Schwarz bounds its square root by
`sqrt(||r||_{a,*}^2+||c||_{1/w}^2)`.
For nonzero alpha, use `l=psi/a`, `h0=h-alpha l`,
`r0=r-alpha B l` and `c0=c+alpha M_l'`, where `M_l=tK/a`.
The constructed state supplies

```text
1/6000<w<1/2500,
||c||_{1/w} <= 15||delta q||L2(dt),
||l||_a<1.56,  ||B l||_{a,*}<1.6,
||M_l'||_{1/w}<40+70||K'||inf<89.
```

Thus every smooth solution of the displayed linearized equations obeys

```text
N0^2=(||r||_{a,*}+1.6|alpha|)^2
     +(15||delta q||L2(dt)+89|alpha|)^2,
||h-alpha l||_B^2+||b||_w^2 <= N0^2,
||M_(h-alpha l)'||_{1/w} <= 2N0,
||h||_a <= N0+1.56|alpha|,
||b||L2(dt) <= 78N0.
```

Phi variation retains its actual coupling:
`delta Phi=integral_disk (b(psi)/F(psi)+g(psi)h/F(psi))/R dA`.
It cannot be discarded by assuming the forward base state already satisfies
the prescribed q/Phi constraints.

The remaining implication is a smooth coupled inverse estimate controlling
profile curvature and axis-position derivatives. The constraint differentiated
again requires bounds on `M_h''`, and higher derivatives for `b''`, from
differentiated GS/q data. The bound on K' alone supplies no such estimate.
Graph-space coercivity and profile L2 control therefore establish neither
smooth linearized solvability nor a nonlinear inverse remainder bound.
Finite-element-to-disk comparison additionally needs full-domain geometry
transport or a proved extension. The estimate above establishes none of these
three prerequisites for inverse-equilibrium reliability.

## Retained affine-P2 constant-q entry point

The public inverse solves fixed-boundary, axisymmetric Grad–Shafranov with
zero pressure, constant signed canonical q, and signed total toroidal flux.
It uses the native affine P2 state, contour coarea K, and F=q·2π/K. The
continuous FF′ profile is piecewise linear in normalized poloidal flux;
F² follows its exact integral. A coupled profile Newton solve differentiates
the converged weak GS equation and the native cell-arc contour equation.

Positive zero-beta homogeneity leaves q unchanged. The normalized-flux mean
FF′ is fixed to −1 during the profile solve, then the requested physical Phi
selects the positive amplitude. Fixing a single edge coefficient instead is
poorly conditioned on a refined profile. The exact piecewise-linear mean
eliminates the last coefficient; its primal/JVP/VJP algebra comes from
`gen/gen_gs_inverse.f90`. Finite pressure does not permit this normalization.

The F² domain check covers the complete closed axis-to-edge interval,
including every quadratic minimum where linear FF′ crosses from negative
to positive. Positive knot values alone are insufficient. Signed q must be
finite and nonzero. The native q/Phi signs must agree; reversal changes F
and toroidal flux while retaining the poloidal state and FF′.

Convergence requires a weak source residual, independent off-knot q probes,
coarea quadrature refinement, and physical Phi quadrature refinement. The
default q gate remains 0.1%; development fixtures with a looser declared
threshold do not establish comparison accuracy. A converged source with a
failed q gate returns status 9 and retains the physically normalized candidate.
Newton or contour failures retain their raw unnormalized states.

This candidate supports only zero pressure and constant q. Finite-pressure
and variable-q coupling, full inverse-input JVP/VJP, shape derivatives, and
rigorous whole-contour or field/current/force certificates are unavailable.
The native representation and contour domain restrictions in
`gs-coarea.md` apply. Native derivative/oracle tests are separate from
registered physical comparison runs.

The continuous piecewise-linear FFprime law is integrated on native quadratic
flux cuts. The implicit response caches the source-slope weak mass and the
stationary-axis flux response on the same cut geometry before GMRES. Its
matrix products reuse those caches; they do not repeat adaptive integration.
Numerical paired quadrature estimates and per-cell work limits fail closed.
They are not rigorous source, derivative or physical equilibrium bounds.
The independently integrated source residual is required before any
constant-q candidate is accepted. Historical candidates solved with the
seven-point profile-source rule require a new solve and cannot inherit the
corrected source residual.

Each profile Jacobian prepares one immutable response context and reuses it
for its coefficient directions. The context owns the numerical state, weak
operator, preconditioner and FFprime knots; any changed input is rejected.
It is local to that Jacobian and is prepared again for a new state. Sharing
this context changes neither integration tolerances nor response equations.

`gs_profile_response` is a primal Picard map with the affine fixed-Dirichlet
load. `gs_profile_implicit_response` differentiates coefficient forcing at
fixed boundary data: that boundary offset has zero tangent and is omitted.
The coefficient forcing follows the native source JVP with zero state,
profile-knot, pressure and mu0 directions.

The same response context integrates every nodal FFprime derivative column
in one vector traversal of the fixed native quadratic cuts. Each column
retains the original load tolerance and global estimator check. A coefficient
direction contracts those columns; if its conservative combined estimator
exceeds the original relative budget through cancellation, the original
directional source JVP reintegrates it. Fixed Dirichlet data has zero tangent.
That reintegration accumulates directional quadrature estimates separately
from primal estimates and checks them against the directional load norm.
Cancellation can therefore return failure even with zero base profiles;
the exact zero-load pressure fixture exercises this case. These estimates
remain numerical error indicators, not rigorous enclosures.
The source JVP differentiates the same locally shifted flux and profile knots
as the primal. A common gauge direction therefore produces zero source
activity before quadrature; fixed boundary derivatives retain their original
direction. The existing gauge and all-active pairing controls cover this map.
The hat basis and source composition use the existing interpolation adjoint
and generated GS source definition.
