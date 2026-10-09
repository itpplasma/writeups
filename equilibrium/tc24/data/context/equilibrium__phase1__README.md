# Phase 1 common comparison

This package supplies the two exact references, fixed physical query points,
metrics, and plotting pipeline for the PLAN Phase 1 error-versus-DOF and
error-versus-wall-time figures. Solver producers consume the same case entry
and return SI fields in COCOS 3. It contains no native equilibrium solver.

## Cases and normalization

`cases.json` maps case IDs to entries. Both use R0=6.2 m, B0=5.3 T,
F_edge=R0*B0=32.86 T m, zero edge pressure and psi_edge=0 Wb/rad.
The magnetic axis is a flux minimum. See the sign definitions in
[CASE_CONTRACT.md](../CASE_CONTRACT.md#signs-units-and-selectors).

- `solovev_lcfs_A3` retains the E0 polynomial, C=0.011489767603191118 T/m²,
  p'=-146292.2647219988 Pa/(Wb/rad), FF'=0, and q_axis=1.5. The case name
  selects a=R0/3; this is a different physical LCFS of the same family as the
  historical a=R0/10 runs. Its exact parametric boundary is recorded in JSON.
- `solovev_cerfon_iter` uses the seven symmetric homogeneous solutions and
  smooth-boundary constraints in Cerfon & Freidberg, *Physics of Plasmas* 17,
  032502 (2010), [equations 8–11](https://doi.org/10.1063/1.3328818).
  eps=0.32, kappa=1.7, delta=0.33 and A=-0.155. Its free flux amplitude is
  fixed by q_axis=1.5, matching the E0 reference; finite beta follows from
  the source law and is not prescribed to the paper's 5% example. The exact
  boundary is the connected zero contour of the analytic flux. A Miller
  curve supplies only the seven shaping constraints, not the full LCFS.

Each boundary contains 2048 distinct samples and a repeated closing point.
`source.terms` stores `[coefficient, x_power, y_power, log_x_power]` with
x=R/R0, y=Z/R0 and psi=`source.psi_scale` times the sum. The Cerfon function
includes logarithms. `source.coefficients` are its seven homogeneous-basis
coefficients in paper order. Sources `p_prime` and `FF_prime` are constant SI
values. F(psi)=sqrt(F_edge²+2*FF_prime*psi) takes the positive branch.

`derive_cerfon.py` constructs and differentiates the equations symbolically,
then solves the seven linear constraints at 70 digits. SymPy is a development
dependency; an installed FortSym Python package was unavailable. Regenerate:

```sh
uv run python -m equilibrium.phase1.derive_cerfon
uv run python -m equilibrium.phase1.points
uv run pytest tests/test_phase1_common.py
```

## Exact reference and measurement

`Exact(case)` exposes vectorized `psi(R,Z)`, `evaluate(R,Z)`, `s_pol(R,Z)`,
`surface(s_pol,theta)`, `q(s_tor)`, `q_pol(s_pol)`, and `poloidal_label(s_tor)`;
`axis`, `psi_axis`, `volume`, `phi_edge`, and `toroidal_flux(s_pol)` supply
geometry and full toroidal flux. Derivative arguments `dx,dy` on `psi` support
all partials through order two. Fields extend analytically outside the LCFS.

The primary q quadrature adaptively doubles periodic contour samples and
requires two successive refinements. The independent `method="ode"` traces
half a flux surface with DOP853 and integrates its toroidal winding. Tests
compare both at all 40 toroidal levels to relative 1e-12. Toroidal flux comes
from direct area quadrature. A converged Chebyshev integral of q accelerates
label inversion and is checked against that independent flux integral.

The committed NPZ files contain 4000 seeded points uniform in poloidal area
with 0<=s_pol<=0.98, plus 40 equally spaced s_tor levels from 0.05 to 0.98.
L2 metrics weight those points by R, estimating physical-volume norms on that
interior domain. Relative max means max absolute error divided by max exact
magnitude, avoiding division by a vanishing poloidal field at the axis.
B_pol and total B use vector magnitudes; B_tor and psi use scalar magnitudes.
q_max is max pointwise relative error. Axis error is Euclidean displacement
divided by the exact axis position's Euclidean norm; volume and Phi use their
exact magnitudes. No gauge, sign, scale, or coordinate alignment is fitted.
Nonfinite samples produce infinite errors and fail the accuracy gate.

`accuracy_passed` requires native convergence and the PLAN target norms on the
specified samples. It is an interior sample gate; it does not measure the
excluded outer 2% poloidal-flux shell. Force balance is reported, not gated:
fourth-order centered differences of the returned fields and psi, step
1e-4 times the LCFS half-width, give RMS(j×B-grad p) / RMS(B²/(mu0*a)).
This reconstruction diagnostic is separate from native solver residuals.

## Producers and command line

A producer exports `run(case: dict, resolution: dict, workdir: Path) -> Result`.
The result provides `evaluate(R,Z)` with arrays `psi,BR,BZ,Bphi`; `q(s_tor)`;
`axis` as `(R,Z)`; scalar `volume,phi_edge`; integer `dof`; `wall_s` including
native setup/solve; boolean `native_converged`; and `meta` with `code_commit`,
`binary_path`, `settings`, and `input_hash`. Record native iteration counts in
`meta` when available. Map native signs and units in the producer and cite the
sign ledger entry used. Return NaN outside the producer's evaluation domain.
The driver fixes thread environment variables before importing the producer.

```sh
uv run python -m equilibrium.phase1.driver --case solovev_cerfon_iter \
  --code exact_interp --res '{"n":129}' \
  --output-dir /tmp/phase1-results --workdir /tmp/phase1-interp-129
uv run python -m equilibrium.phase1.plot \
  /tmp/phase1-results/solovev_cerfon_iter.csv --output-dir /tmp/phase1-plots
```

The driver appends one locked CSV row per run, defaulting to
`equilibrium/phase1/results/<case>.csv`, and retains the producer metadata and
work directory path. Supply a unique work directory for each native solve;
the default creates one under the system temporary directory. Native run
registration remains the controller's responsibility.

`exact_interp` independently interpolates psi and the three field components
on an n×n rectangular grid, with DOF=4*n². Expected field-value error is O(h⁴),
hence O(DOF⁻²). Differentiating a psi spline would have a different field rate.
Its q and geometric scalars use the exact reference; this producer exercises
the infrastructure and does not qualify a native solver. Use n=65,129,257,513
and fit the final three for the asymptotic demonstration. E0's quadratic
poloidal field is represented to roundoff.

Plots show ten PLAN-related error panels against DOF and total native solve
wall seconds; legends give the fitted exponent in error proportional to x^slope
for the last three distinct abscissae with errors above 32 machine epsilons.
Smaller errors are labeled as roundoff. A rate CSV records those fits. Native
unconverged, nonfinite, and zero errors are omitted explicitly. Zero exact
observable errors and interpolation timing do not establish solver rates or
performance. PNG/PDF outputs belong in scratch and are uploaded to slopbox,
never committed here.
