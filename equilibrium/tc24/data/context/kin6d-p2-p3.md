# Phase 1 P2/P3 convergence and cost

Exact common-driver Solovev cases; KIN6D `7951c6a`, GNU Fortran 16.2.1,
CMake `cpu` (`-O3`, no fast math), AMD Ryzen 9 5950X, CPU 7, one thread.
The [CSV](p2-p3.csv) contains every measured metric, settings, input/binary
hashes, source revisions and archived raw directories.
The common driver is unchanged. Its KIN6D producer includes the lane patch
`iter_tc24-producer.patch` (SHA-256 `4cd6060261f699d379e80856b7712ef0f31f9a9ef4dcfd136d151e3713cf3259`).

Each time is one mesh/assembly/solve measurement, matching the existing
producer timing contract. Full driver time (including contours, native
export/readback, reference evaluation and force diagnostics) is retained
separately in the CSV; it is not the solver time. These are local timings,
not a matched cross-code speed claim.

The common driver evaluates exported native FE fields at its fixed samples
inside `s_pol <= 0.98`, with R-weighted L2 norms. Maximum field errors use
the maximum reference magnitude; q uses pointwise relative error over
`0.05 <= s_tor <= 0.98`. Axis, volume and edge toroidal flux are relative.
The force RMS is the common finite-difference diagnostic and is not a gate.

Targets: psi L2 1e-6; Bpol/Btor L2 1e-5 and max 1e-4; q max 1e-5;
axis, volume and edge toroidal flux 1e-6. All quantities are candidates
validated against the exact cases. No rigorous-result claim is made.

## A3

| p | n | DOF | solve s | driver s | psi L2 | Bpol L2 | Bpol max | q max | axis | force RMS | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 96 | 5113 | 0.0515 | 3.04 | 5.669e-06 | 2.635e-04 | 7.941e-04 | 5.258e-05 | 4.085e-07 | 3.212e-03 | fail |
| 2 | 192 | 20629 | 0.3495 | 8.57 | 6.842e-07 | 6.431e-05 | 2.346e-04 | 1.702e-05 | 1.259e-08 | 1.150e-03 | fail |
| 2 | 384 | 82977 | 2.9586 | 30.04 | 8.368e-08 | 1.573e-05 | 4.531e-05 | 4.256e-06 | 7.833e-09 | 5.292e-04 | fail |
| 2 | 576 | 187193 | 9.7855 | 66.05 | 2.431e-08 | 6.973e-06 | 2.665e-05 | 3.867e-06 | 4.457e-09 | 2.750e-04 | pass |
| 3 | 48 | 2854 | 0.0315 | 2.34 | 3.175e-07 | 7.830e-06 | 9.011e-05 | 5.397e-06 | 2.297e-08 | 2.008e-04 | pass |
| 3 | 96 | 11575 | 0.2073 | 4.75 | 1.855e-08 | 7.595e-07 | 7.947e-06 | 3.822e-06 | 1.767e-09 | 1.898e-05 | pass |
| 3 | 192 | 46558 | 1.4075 | 13.00 | 1.076e-09 | 7.997e-08 | 6.051e-07 | 3.805e-06 | 2.007e-10 | 2.841e-06 | pass |
| 3 | 384 | 186985 | 11.5432 | 48.02 | 6.578e-11 | 8.604e-09 | 4.728e-08 | 3.794e-06 | 9.981e-12 | 4.733e-07 | pass |

| p | n | Btor L2 | Btor max | volume | Phi edge |
|---|---|---|---|---|---|
| 2 | 96 | 0.000e+00 | 0.000e+00 | 4.385e-08 | 1.047e-07 |
| 2 | 192 | 0.000e+00 | 0.000e+00 | 2.741e-09 | 6.545e-09 |
| 2 | 384 | 0.000e+00 | 0.000e+00 | 1.716e-10 | 4.098e-10 |
| 2 | 576 | 0.000e+00 | 0.000e+00 | 3.415e-11 | 8.149e-11 |
| 3 | 48 | 0.000e+00 | 0.000e+00 | 1.037e-07 | 2.467e-07 |
| 3 | 96 | 0.000e+00 | 0.000e+00 | 6.494e-09 | 1.549e-08 |
| 3 | 192 | 0.000e+00 | 0.000e+00 | 4.058e-10 | 9.686e-10 |
| 3 | 384 | 0.000e+00 | 0.000e+00 | 2.513e-11 | 5.989e-11 |

P2 final two measured orders: psi 3.03, 3.05; Bpol 2.03, 2.01.
P3 final two measured orders: psi 4.11, 4.03; Bpol 3.25, 3.22.

Cheapest measured passing setting: P3, n=48, 2854 DOF, 0.0315 s mesh/assembly/solve, 2.34 s full driver.

## Cerfon

| p | n | DOF | solve s | driver s | psi L2 | Bpol L2 | Bpol max | q max | axis | force RMS | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 96 | 7501 | 0.0831 | 7.29 | 5.114e-06 | 2.486e-04 | 1.054e-03 | 5.575e-05 | 1.091e-07 | 2.648e-03 | fail |
| 2 | 192 | 30241 | 0.6031 | 14.39 | 5.514e-07 | 5.838e-05 | 2.144e-04 | 9.467e-06 | 4.140e-08 | 1.540e-03 | fail |
| 2 | 384 | 121529 | 4.7005 | 43.89 | 6.800e-08 | 1.470e-05 | 4.169e-05 | 4.792e-06 | 2.137e-08 | 5.774e-04 | fail |
| 2 | 576 | 273725 | 22.3795 | 105.62 | 1.986e-08 | 6.578e-06 | 1.946e-05 | 4.900e-06 | 1.639e-08 | 2.790e-04 | pass |
| 3 | 48 | 4078 | 0.0495 | 6.36 | 2.159e-06 | 2.846e-05 | 3.479e-04 | 1.181e-05 | 5.054e-08 | 2.100e-04 | fail |
| 3 | 96 | 16948 | 0.3304 | 9.69 | 1.120e-07 | 2.124e-06 | 3.069e-05 | 5.220e-06 | 7.346e-09 | 2.125e-05 | pass |
| 3 | 192 | 68185 | 2.4217 | 21.74 | 7.181e-09 | 8.865e-08 | 1.350e-06 | 4.836e-06 | 1.413e-09 | 4.634e-06 | pass |
| 3 | 384 | 273727 | 24.0892 | 78.88 | 4.461e-10 | 7.884e-09 | 4.373e-08 | 4.809e-06 | 3.410e-11 | 6.928e-07 | pass |

| p | n | Btor L2 | Btor max | volume | Phi edge |
|---|---|---|---|---|---|
| 2 | 96 | 2.536e-08 | 1.807e-07 | 4.152e-07 | 5.625e-07 |
| 2 | 192 | 2.666e-09 | 1.418e-08 | 2.603e-08 | 3.528e-08 |
| 2 | 384 | 3.247e-10 | 1.057e-09 | 1.630e-09 | 2.210e-09 |
| 2 | 576 | 9.558e-11 | 3.505e-10 | 3.242e-10 | 4.396e-10 |
| 3 | 48 | 1.212e-08 | 1.274e-07 | 9.533e-07 | 1.288e-06 |
| 3 | 96 | 6.247e-10 | 4.934e-09 | 6.120e-08 | 8.291e-08 |
| 3 | 192 | 4.023e-11 | 2.863e-10 | 3.848e-09 | 5.216e-09 |
| 3 | 384 | 2.501e-12 | 1.729e-11 | 2.384e-10 | 3.231e-10 |

P2 final two measured orders: psi 3.02, 3.04; Bpol 1.99, 1.98.
P3 final two measured orders: psi 3.96, 4.01; Bpol 4.58, 3.49.

Cheapest measured passing setting: P3, n=96, 16948 DOF, 0.3304 s mesh/assembly/solve, 9.69 s full driver.

The common-driver field rates use interior samples; the whole-domain CTest
below supplies the asymptotic P3 order gate. In these fixed radial grids,
q levels off near 4e-6 to 5e-6, below its 1e-5 target. The mesh sweep does
not refine the radial interpolation used for q.

## Reproduction and validation

Build with `cmake --preset cpu && cmake --build --preset cpu --target gs_phase1`.
The TC24 producer must include degree selection. From that checkout, set
`KIN6D_BINARY` to this build and invoke its unchanged common driver:

```sh
KIN6D_BINARY=/path/to/kin6d/build/gs_phase1 uv run python -m equilibrium.phase1.driver \
  --case solovev_lcfs_A3 --code kin6d \
  --res '{"degree":3,"boundary_nodes":48,"max_area":0.036592167551878364}' \
  --workdir /disk/unique-run --output-dir /disk/results
```

Use the CSV resolution and max_area for each repeat. Here max_area is
`(2*pi*a/n)^2/2`, with a=R0/3 for A3 and a=eps*R0=1.984 m for Cerfon.
Retained defaults: curved geometry, radial_points=257, angular_points=128.
Register each repeat through TC24 `results/run_registry.json` and regenerate
its table with `uv run python ops/run_registry.py`. Raw runs belong on disk.

Validation: all 31 Grad-Shafranov CTests pass in both cpu and debug; the
producer suite passes 3/3. The P3 curved A3 CTest checks both refinement
pairs on n=96,192,384 against psi order 4 and B order 3, each within 0.3.
P3 contour sensitivities, nonlinear profiles and the P2 majorant are
explicitly unsupported. Fixed-source equation responses use the primal operator.
