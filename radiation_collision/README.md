# Relativistic radiation collisions

A readable rederivation of the radiation-mediated collision operator of
Kasilov and Kernbichler, Phys. Plasmas 3, 4115 (1996), Sec. IV, in their
notation: the closed diffusion tensor, the two-electron kernel as a convergent
special-function series, its absorption-threshold cusps, a conservative
two-mode (temperature/drift) closure with Bessel-function constants, and the
optically thin radiation-drag propagator.

- `radiation_collision.tex`: the writeup. Render with
  `./render.sh OUTPUT_DIR` (needs `pdflatex`). The PDF is not committed.
- `cas/`: exact checks in [fortsym](https://github.com/lazy-fortran/fortsym)'s
  native Wolfram-language runner, one script per part of the derivation
  (128 bindings, each must reduce to 0). Run
  `FORTSYM_WL_RUN=/path/to/fortsym_wl_run cas/run_cas.sh [OUT_DIR]`.
  Checked with fortsym `4a04213`, which contains the fixes these checks
  needed (series of removable singularities, rational power merging,
  improper exponential integrals, parse-failure reporting).
- `cas/gen_angular_antiderivatives.py`: SymPy proposes the antiderivatives of
  the photon-angle integrals; `cas/angular_integrals.wl` verifies them in
  fortsym by differentiation and evaluates the end points exactly.
- `numeric_checks.py`: independent mpmath checks of the non-algebraic
  statements (harmonic sums, angle quadrature of the unsummed tensor,
  absorption series, Bessel moments, the harmonic-tail bound, the broadened
  cusp, the drag propagator). `numeric_results.json` records the last run.

What is and is not established is stated in the text: the threshold cusp is
proved locally, the global obstruction to a finite kernel is conditional on a
derivative estimate that is not proved, and the closure is exact for the
specified two-mode photon model, with its distance to the original operator
given by an exact identity.
