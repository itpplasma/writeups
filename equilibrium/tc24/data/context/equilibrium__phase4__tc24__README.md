# Phase 4b: actual ITER TC24

**Blocked at the KIN6D P3 reference.** The source problem is pinned below;
the five-code forward convergence/cost study, comparison of a converged solve
with the source, and accuracy-qualified perturbation exports are not delivered.
The native profile-table solve rejects P3 with status 20. A constant-source
P3 solution or an old CHEASE equilibrium would solve a different problem.

This directory owns the E5 variant `E5_iter_tc24_stored_profiles_psiN0995`.
[case.json](case.json) records the received paths, hashes and declared maps.
The original JINTRAC file is authoritative for the stored flux field and
profile values. The received MARS and Leonardo CHEASE equilibria, CHEASE log,
MARS input and MATLAB input structure are pinned as historical context.
They are not interchangeable inputs: their boundaries, profiles and native
normalizations differ. No received bytes were changed.

## Conventions and the forward problem

SI; COCOS 3; physical phi increases CCW viewed from +Z;
`B_R=-psi_Z/R`, `B_Z=psi_R/R`, `B_phi=F/R`;
`Delta*psi + mu0 R² pprime + FFprime = 0`.

For JINTRAC, **COCOS 7 is an adopted declaration**, following the retained
source-conversion precedent documented in
[the existing source investigation](../../../research_notes/Remaining%20equilibrium%20discrepancy%20causes/contracts.md).
The original exporter/deck and an authoritative producer declaration are
unavailable. The 7→3 map leaves psi, F, Ip and derivatives unchanged and reverses
q. A constant flux gauge then places this boundary at zero. This is not a
derivative-sign correction. Under this declaration the source has F>0,
Ip>0, a positive axis flux (a maximum), and q<0. Its physical polarity differs
from the COCOS-2→3 supplied CHEASE fields. No global field reversal is applied.
The Phase 1 axis-minimum convention must not be imported into this case.

| Fixed input | Value / definition |
|---|---|
| Source cutoff | source s_pol=0.995; native psi=0.35897409022399884 Wb/rad |
| Flux gauge | psi = psi_native − psi_native_at_cutoff |
| Source axis label in that gauge | +11.869883349776002 Wb/rad; the forward axis is an output |
| Pressure at the new edge | 14174.557967725552 Pa |
| F at the new edge | +32.85217660204595 T m |
| Source law | Cubic p(psi), G(psi)=F²/2 through all 513 stored values |
| Derivative law | pprime=dp/dpsi, FFprime=dG/dpsi, exactly from those cubics |
| Global constraints | Boundary, absolute-psi source law, edge p and F; q, current and flux span are outputs |

[profile_coefficients.csv](profile_coefficients.csv) is the authoritative
piecewise polynomial: on `[psi_left,psi_right]`, use powers 3,2,1,0 of
`psi-psi_left` for p and G. It is the not-a-knot C2 interpolant, with no
smoothing or fitted normalization. [profiles.csv](profiles.csv) retains all
knots, derivative evaluations and both discarded received derivative arrays.
It includes the thin source shell outside the new boundary to preserve the
interpolant's endpoint definition; that shell is not part of the solve domain.
For psi above the source axis, continue the last interval polynomial. Reject
negative pressure or nonpositive F². Do not renormalize knots to a solved axis.

EQ-D04 is resolved **as an explicit choice of a new consistent forward
problem**, not a repair of the unknown exporter. Independent Simpson integrals
over the full received flux span give:

| Source | integral(pprime)/Δp | integral(FFprime)/Δ(F²/2) |
|---|---:|---:|
| JINTRAC | −1.013007167219742 | −1.013007167300012 |
| MARS CHEASE | 1.000275593069282 | 1.000106567315072 |
| Leonardo CHEASE | 1.001720880161872 | 0.997827847900975 |

The JINTRAC mismatch includes opposite sign and 1.3007% amplitude; a COCOS map
cannot change these ratios. [source_consistency.csv](source_consistency.csv)
also keeps the dimensional changes and integrals. The original producer cause
remains unresolved. EQ-D13 still requires measuring each solver's interpolation
of this common law; sampling a derivative table does not establish equivalence.

## Common smooth boundary

[boundary_coefficients.csv](boundary_coefficients.csv) defines R(theta),Z(theta)
by the listed sine and cosine coefficients, modes 0..128. Both parities are
required: TC24 is vertically asymmetric. The coefficients come from 4096
uniform source-axis polar rays intersecting the source's s_pol=0.995 contour,
using a quintic tensor spline of the received flux grid. This finite Fourier
curve is the common boundary itself; consumers must refine their representation
of it. [boundary.csv](boundary.csv) is a convenience sample, including closure.

On 4096 independent angular samples its source labels are
0.9949885469..0.9950137983, its displacement from the extracted contour is at
most 22.4 micrometres, and source Bpol is at least 0.113697 T. Its minimum
sampled distance from the lower X-point is 0.201301 m. The original X-point
and the historical CHEASE boundaries are not part of this domain.
[boundary_convergence.csv](boundary_convergence.csv) records modes 16..256.
Cubic/quintic source reconstructions differ by at most 12.2 micrometres on
the sampled contours. These are reconstruction/representation differences on
one source grid, not an uncertainty bound on the original equilibrium.

## Blocker and remaining work

[capability.csv](capability.csv) records the existing native
`test_gs_profile_domain valid <degree>` oracle against KIN6D `5d17831`:

| Profile-table path | Native result | Wall time |
|---|---|---:|
| Affine P2 control | finite positive-source oracle passed | 0.331 s |
| P3 | rejected, status 20 (`GS_UNSUPPORTED_GEOMETRY`) | 0.113 s |

Both executions, PIDs, binary/source/input hashes and raw logs are registered.
These timings are capability diagnostics, not TC24 equilibrium costs. The
executed binary is retained beside each log under the CSV's raw-root paths.
Source `profile_load_products` also explicitly rejects mapped geometry.
The qualified `gs_phase1` solve, majorant and F/q readback take constant source
coefficients. This is a missing capability, not evidence of a wrong numerical
limit, and does not reopen the fixed affine-P2 quadrature defect EQ-D99.

Resume after generic nonlinear curved-P3 profile integration, consistent
primal/JVP/VJP, estimator and signed profile readback are available. Then run
the Richardson/majorant ladder; map its p/q/Phi to asymmetric VMEC++/DESC
inputs; check both CHEASE laws and boundary representations; and measure
native and consumer-readback errors. The source comparison must keep input
selection, boundary representation and source reconstruction separate.
No G-EQDSK or Boozer file here is promoted for perturbation use. Controller
integration of these lane changes and scheduling that prerequisite remain open.

## Reproduce

From the repository root, with NumPy/SciPy/Matplotlib and a disk TMPDIR:

```sh
python -m equilibrium.phase4.tc24.prepare --plot-dir "$TMPDIR/plots"
python -m pytest tests/test_phase4_tc24.py
python -m equilibrium.phase4.tc24.probe  # fresh registered diagnostic runs
uv run python ops/run_registry.py
```

Six analytic behavioral tests cover derivative/integral consistency, extension
domain, signed COCOS/field reconstruction, exact ellipse intersections and
asymmetric Fourier geometry. No test compares repository hashes or frozen
case values. Together with the existing GEQDSK/profile-map and registry tests,
34 targeted checks pass; one existing LFS fixture was materialized from its
matching local object for its test and the original pointer restored. Ruff
passes and the regenerated registry validates 1536 entries. The input figure is [PDF](https://box.sloppy.at/a6099.pdf) /
[PNG](https://box.sloppy.at/734a0.png); uploaded bytes were checked against
[artifacts.json](artifacts.json). Plots/PDFs are not committed.

Chris&AI
