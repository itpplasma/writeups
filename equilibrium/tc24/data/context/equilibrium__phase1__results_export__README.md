# Phase 1: accuracy delivered by equilibrium exports

PLAN cell: **End-to-end accuracy**, `solovev_lcfs_A3` and
`solovev_cerfon_iter`. The two-resolution study now includes KIN6D P3 and
both CHEASE variants through G-EQDSK, libneo Boozer, NEO-RT and NEO-2.
The previous Boozer **flux/q target gap is closed** on both cases.
GPEC/DCON's reconstruction, native MARS Fourier/Hamada and NEO-2's full
vector/Jacobian path are now measured below. VMEC++/DESC have no deployed
NTV conversion in the retained lanes.
This is export-path evidence, not closure of the whole equilibrium slice.

[Figure](https://box.sloppy.at/93509.png), SHA256
`349380c90950c3cf131ed1d4cfcf6afd1a68b70bdb21a693c9666f6ee6d27936`.
[summary.csv](summary.csv) preserves the 164 earlier rows and adds 32 full-consumer
rows. The figure above predates these new rows. [inputs.json](inputs.json) identifies the raw numerical
results, hashes and manifests. Generated images are not committed.
The [previous figure](https://box.sloppy.at/e9cad.png) is retained as historical
scan-limited evidence; its conclusions are superseded by this table.

## Native versus exported fields

Relative Bpol L2. Native and EQDSK use the same 40 exact flux surfaces and
128 geometric angles. The Boozer column uses the same combined R-weighted
normalization over 12 file surfaces at their reconstructed R,Z positions
(2048 angles each). The sampling grids differ, not the norm formula.
`n` means CHEASE NS=NT or KIN6D boundary nodes.

| Case / producer | n | Native FE / NOUT | EQDSK Python | EQDSK actual Fortran | Boozer reconstructed field |
|---|---:|---:|---:|---:|---:|
| A3 / public CHEASE | 64 → 128 | 5.48e-6 → 6.41e-7 | 5.21e-6 → 4.77e-7 | 5.23e-6 → 4.84e-7 | 2.79e-7 → 1.85e-7 |
| A3 / MARS CHEASE | 64 → 128 | 5.48e-6 → 6.41e-7 | 5.45e-6 → 6.06e-7 | 5.46e-6 → 6.20e-7 | 2.93e-7 → 1.82e-7 |
| A3 / KIN6D P3 | 48 → 96 | 1.05e-5 → 9.42e-7 | 9.98e-6 → 9.03e-7 | 1.01e-5 → 9.10e-7 | 9.87e-6 → 7.98e-7 |
| Cerfon / public CHEASE | 128 → 256 | 1.88e-6 → 2.41e-7 | 1.39e-6 → 1.87e-7 | 1.41e-6 → 1.89e-7 | 6.22e-7 → 3.37e-7 |
| Cerfon / MARS CHEASE | 128 → 256 | 1.88e-6 → 2.41e-7 | 1.78e-6 → 2.28e-7 | 1.83e-6 → 2.33e-7 | 4.93e-7 → 3.30e-7 |
| Cerfon / KIN6D P3 | 48 → 96 | 3.67e-5 → 2.29e-6 | 3.11e-5 → 2.26e-6 | 3.12e-5 → 2.28e-6 | 6.72e-5 → 3.50e-6 |

KIN6D's generic P3 native output is sampled by `gs_phase1 --evaluate`.
No EQDSK writer was found in that solver. The producer-side
[writer](../kin6d_export.py) uses the FE values, native q/psi profiles and
supplied constant source law. It integrates signed current on the cubic
geometry and writes SI COCOS 3 without an exact-solution dependency.
Exterior rectangular padding uses a local cubic nodal continuation; it is
**not a qualified vacuum field**. Consumers are qualified inside the supplied
LCFS. Grid refinement is 257² → 513²; native readback uses 513 radial and
512 angular points. The four final solves have 2,215–9,784 DOF and take
0.025–0.167 s for mesh/assembly/solve; contour evaluation and export cost are
separate, and their elapsed times are retained in the manifests.

Public/MARS EQDSK grids are 257² for A3 and 257² → 513² for Cerfon.
The Python column uses libneo's actual parser plus the repository cubic
reconstruction; the Fortran column uses actual `field_eq` through the fixed
f2py interface. Neither is mislabeled as the other's interpolation.
NOUT is a native numerical baseline, not MARS's Fourier/metric consumer.
Its F comes from the delivered EQDSK profile; native CHEASE q/flux are not
claimed as independent measurements.

At the finer resolution, actual Fortran EQDSK readback gives:

| Case / producer | psi L2 | \|B\| L2 | max relative q | relative Phi_edge |
|---|---:|---:|---:|---:|
| A3 / public | 1.08e-8 | 1.72e-9 | 2.97e-9 | 1.99e-9 |
| A3 / MARS | 1.23e-8 | 1.90e-9 | 3.01e-9 | 1.90e-9 |
| A3 / KIN6D | 2.47e-8 | 2.18e-8 | 4.14e-7 | 6.67e-9 |
| Cerfon / public | 1.91e-9 | 2.31e-9 | 4.08e-10 | 2.67e-10 |
| Cerfon / MARS | 2.08e-9 | 2.56e-9 | 4.05e-10 | 2.61e-10 |
| Cerfon / KIN6D | 1.20e-7 | 6.28e-8 | 5.33e-7 | 1.02e-7 |

## Boozer spectrum, flux and actual consumers

Both actual readers are invoked without a transport solve. NEO-RT uses
`read_boozer_file`, `set_s`, `init_magfie_at_s` and `do_magfie`.
[NEO-2 harness](neo2_readback.f90) calls unchanged `neo_read`,
`neo_init_spline` and `splint_horner3`, using `inp_swi=9`, `lab_swi=10` and
cubic radial interpolation. It evaluates the signed cosine/sine spectrum;
its standalone test has independently known radial harmonics and sine sign.
That original harness did not invoke `neo_magfie`; the separate full-path
measurement below now does. Vector-field and label errors in the original
table use the libneo file reconstruction.

All final conversions use 1,000 scan points with boundary refinement,
256 radial mapping points, 512 mapping angles, 2,000 file surfaces and
m=0..40. Reader queries use 12 fixed labels in 0.05..0.98 and 256 angles,
generally between file surfaces. NEO-RT and NEO-2 agree at displayed precision.

| Case / producer | NEO-RT and NEO-2 B_m0 error, lower → higher n | q error, lower → higher n | Phi_edge error, lower → higher n |
|---|---:|---:|---:|
| A3 / public | 1.64e-8 → 2.32e-8 | 3.13e-8 → 5.40e-8 | 4.96e-9 → 3.18e-9 |
| A3 / MARS | 1.75e-8 → 1.47e-8 | 3.13e-8 → 8.63e-8 | 9.66e-9 → 5.66e-10 |
| A3 / KIN6D | 1.05e-6 → 1.09e-7 | 5.65e-6 → 6.42e-7 | 1.29e-7 → 2.92e-8 |
| Cerfon / public | 5.49e-8 → 2.61e-8 | 5.99e-8 → 2.29e-8 | 1.15e-8 → 1.36e-10 |
| Cerfon / MARS | 3.75e-8 → 2.15e-8 | 2.09e-7 → 2.28e-8 | 1.16e-8 → 1.15e-9 |
| Cerfon / KIN6D | 8.06e-6 → 6.85e-7 | 2.81e-5 → 1.80e-6 | 1.02e-6 → 2.89e-8 |

Phi_edge here is the signed file-header flux, not an independent consumer
volume integration. Below-target CHEASE fluctuations are not treated as
convergence-rate evidence. Two native resolutions measure export degradation;
they do not establish an asymptotic FE convergence rate.

The limiting steps and their controlled refinements are:

| Step | Evidence and disposition |
|---|---|
| Boundary scan | Original 10,000 → 40,000 scans reduced B_m0 error 6.8× / 4.4× on A3/Cerfon, consistent with first-order scan spacing. At 40,000 points, flux errors were 8.80e-5 / 1.47e-4 and q errors 4.90e-5 / 8.59e-5. The converter discarded one or two scan cells below the requested `psimax`. PR2 refines the regular flux-boundary bracket; box/separatrix exits retain the old margin. |
| File precision | After bracket refinement, the analytic circular test still lost 2.3e-6 relative flux in the six-digit header. PR2 writes that header at double precision; native-to-file flux round trip now passes at 2e-14 relative tolerance. |
| Radial sampling | With refined boundary on A3 public n=128, 40 → 400 → 2,000 file surfaces gives actual-reader B_m0 error 3.08e-4 → 2.52e-8 → 2.32e-8. Cubic interpolation has reached the numerical floor by 400; no further diagnosis is needed below target. |
| Harmonics | Previous m=20 → 40 reduced maximum per-surface reconstructed Bpol errors from 2.56e-4 → 5.09e-7 (A3) and 9.47e-5 → 8.58e-7 (Cerfon). Final combined norms with the refined boundary are in the table above. |
| Mapping grid / quadrature | Previous 256×512 → 1024×2048 mapping refinement made no material change while the scan error dominated. At 256×512 with the refined boundary, both flux and q now meet target. The independent analytic-circle test also checks converter flux/q without fitting. |

The oracle [exact_boozer](../export_check.py) integrates the exact field-line
ODE from [exact.py](../exact.py), using `d(R,Z)/dt=(-psi_Z,psi_R)` and
`dphi/dt=Bphi`. Integrating `R*B² dt` constructs theta_B independently of
libneo's symmetry-flux chart. Theta_B=0 is the outboard midplane; up/down
symmetry closes the orbit. Analytic circular B_m0 and independent exact q
checks validate that construction. No phase, amplitude, radial or sign fit is
used. B_mn is cosine-minus-i-sine, with no factor two for m=0; its norm includes
B00. Nonaxisymmetric content is reported, not discarded.

Flux labels are s_pol, s_tor and rho_tor=sqrt(s_tor). All native files remain
unchanged. The explicit CHEASE COCOS 2→3 map is used; MARS additionally has
the declared physical F/q partner reversal to the common positive toroidal
field. Psi is Wb/radian, zero at the supplied LCFS, and B is tesla.
Norms use R-weighted samples, not a volume quadrature over the whole plasma.
Boozer psi comes from integrating file iota with endpoint extrapolation.
The CSV retains both `combined_*` norms and the old `physical_*` surface
maxima. Normalizing psi separately on each near-zero edge surface amplifies
gauge/geometry errors: at fine KIN6D resolution that maximum is 1.12e-5 /
4.60e-5 (A3/Cerfon), while combined psi L2 is **1.31e-7 / 4.97e-7**.
For public/MARS CHEASE the fine combined psi L2 is 4.35e-8 / 4.48e-8 on A3
and 1.01e-7 / 9.18e-8 on Cerfon. All six fine combined psi norms are below
1e-6. These sampled norms still exclude the axis and outermost flux shell;
they are not whole-plasma volume bounds. The physical field/label columns
and full complex spectra remain in the raw JSON.

## Full consumer coverage

The `lane/readers` extension uses actual project consumer code, without
transport or perturbation solves. Every run has a pre-execution manifest,
input/build hashes, raw outputs and a registry entry. Both exact cases and
two producer resolutions are covered for all three retained exporters.

| Case / producer | n | GPEC/DCON Bpol L2 | Full NEO-2 Bpol L2 |
|---|---:|---:|---:|
| A3 / public CHEASE | 64 → 128 | 6.81e-6 → 1.22e-6 | 2.80e-7 → 1.86e-7 |
| A3 / MARS CHEASE | 64 → 128 | 7.21e-6 → 1.40e-6 | 2.93e-7 → 1.81e-7 |
| A3 / KIN6D P3 | 48 → 96 | 9.50e-6 → 4.92e-6 | 1.00e-5 → 8.07e-7 |
| Cerfon / public CHEASE | 128 → 256 | 2.24e-6 → 4.25e-6 | 6.11e-7 → 3.44e-7 |
| Cerfon / MARS CHEASE | 128 → 256 | 2.75e-6 → 2.24e-6 | 4.91e-7 → 3.36e-7 |
| Cerfon / KIN6D P3 | 48 → 96 | 4.04e-5 → 4.92e-6 | 6.87e-5 → 3.68e-6 |

GPEC `e68d7ac` is the local production source. Its equilibrium modules and
LSODE were built directly with gfortran; no prebuilt library was required.
[The driver](gpec_readback.f90) calls unchanged `read_eq_efit` → `direct_run`,
including surface tracing and the final `rzphi`, `sq` and `eqfun` splines.
It evaluates the delivered Hamada chart (`mpsi=256`, `mtheta=512`,
`etol=1e-10`), not merely the rectangular input spline. The chart uses
positive q/F, psi increasing outward, and unit-period angles; its Jacobian
comparison accounts for those units. Forty surfaces over 0.05–0.98 in
s_pol and 128 angles offset from spline knots are sampled. Public Cerfon's
below-target Bpol fluctuation is not claimed as an asymptotic convergence rate.

[Full NEO-2 driver](neo2_vector.f90): unchanged `neo_read`, `neo_prep`,
`neo_init_spline`, `neo_magfie_a` and angular spline evaluation, with
`inp_swi=9`, `lab_swi=10`, cubic radial splines, 513×9 angular nodes,
12 s_tor labels and 256 off-knot angular queries. Native contravariant unit
vectors and geometry derivatives reconstruct cylindrical B; covariant
components are checked independently against that vector. Centimetres and
cm³ are converted to metres and m³ explicitly. The signed Jacobian uses
the delivered `(s,theta_B,phi_B)` ordering and is negative. Its independent
exact oracle uses `J=-Phi_edge/(2*pi)*(F+iota*I)/B²`, with
`I=(2*pi)^-1 integral Bpol dl` on the exact contour.

At fine resolution, GPEC psi L2 is 1.15e-8–1.25e-7 and maximum relative q
error is 1.96e-8–9.15e-7; full NEO-2 gives psi L2 3.80e-8–4.98e-7, q
1.11e-7–3.28e-6 and Jacobian error 1.36e-7–3.32e-6. GPEC's Jacobian error
is 9.99e-9–5.13e-7 at fine resolution. CSV rows also retain
|B|, full-vector and component errors, all three flux labels, signed edge
flux, and spectra. These are sampled plasma norms, excluding axis/LCFS;
they are not whole-domain bounds. The NEO-2 `jacobian_geometry_max_rel`
column is a separate consistency diagnostic using radial derivatives of
the rounded file geometry; it is not the error of the returned Jacobian
against the exact solution (that is `jacobian_max_rel`).

The full NEO-2 call exposed an allocation defect for multiple surfaces.
The one-allocation fix and independent analytic two-surface regression are
in [NEO-2 PR193](https://github.com/itpplasma/NEO-2/pull/193), `a0b7039`.
The test aborts before and passes after. This study links that module with
the existing `cefb20b` COMMON build; it does not claim the PR is merged.
Disposition belongs to [EQ-EXPORT-3](../../ERRATA.md#eq-export-3-neo-2-multiple-surface-initialization).

MARS uses `OUTRMAR` and `OUTVMAR`, not the old `OUTMAR` or CHEASE's
approximate `RMZM_F`. [Native exporter](mars_native_study.py) reuses each
frozen EXPEQ/source law and the pinned `104053d` CHEASE binary, setting
`NIDEAL=0,NFFTOPT=0,NPSI=2*n,NCHI=min(2*n,512),NV=32`.
`MSMAX=1` saves unused legacy `OUTMAR` transforms; the full real-space
`OUTRMAR` grid is unchanged and MARS performs its own Fourier transform.
The four one-thread solve/export times are 3.2, 8.9, 8.8 and 57.0 seconds.
The previous NAG-stub exclusion was incorrect: the non-NAG path calls
`GIJREA` and writes both consumer files.

[MARS driver](mars_readback.f90) extracts unchanged `READTOR`, `GETQPLS`,
`READVAC`, `INPUTV` and `FOURIER_VACUUM` from MARS-Q `8824bb18`, links its
actual `FFTDRIVER`, and reconstructs plasma B from the read flux jet,
metric Jacobian and Fourier derivatives of R/Z. The equilibrium-only
`NTV_pre` routines `get_RZ`, `cal_metric`, `coord_trans` and `coord_map`
also run. Optional `NCONVCS` conversions are disabled and guarded by
abort-only stubs; MPI declarations are retained without MPI initialization.
Compile with MARS's required default-real-8/default-double-8 flags. The
signed analytic circular-field regression detects their omission.
`OUTRMAR` F/q are already positive for these cases; the legacy EQDSK-only
F/q partner reversal must **not** be applied here. MARS retains its positive
metric-Jacobian magnitude; the negative NEO-2 chart determinant is a separate
coordinate convention.

| Case | n | Native MARS Bpol L2 | Hamada B_m0 error | Hamada Jacobian max relative error |
|---|---:|---:|---:|---:|
| A3 | 64 → 128 | 1.25e-5 → 1.51e-6 | 5.09e-6 → 1.51e-6 | 9.66e-5 → 2.41e-5 |
| Cerfon | 128 → 256 | 4.37e-6 → 5.79e-7 | 5.67e-6 → 1.42e-6 | 2.60e-5 → 6.50e-6 |

Native MARS fine psi L2 is 9.17e-9 / 2.12e-9, |B| L2
3.25e-8 / 1.45e-8, q error 1.94e-8 / 3.76e-9 and edge-flux error
1.34e-9 / 2.90e-10 (A3 / Cerfon). Hamada finite-difference metrics are
expected to be second order; the Jacobian errors decrease by factors
4.00 and 4.00, so this is a numerical limitation, not an unresolved
non-converging defect. No higher-resolution solve is needed to explain it.
Vacuum files are read and their interface coordinates retained; no vacuum
field accuracy is claimed outside the exact plasma domain.

Hamada spectra use a separate exact volume-angle integral
`dtheta_H proportional to R*dl/|grad psi|`, with theta_H=0 at the outboard
midplane, checked against an analytic circular-angle/Jacobian oracle.
GPEC `hamada_bmn_rel` and NEO-2 `boozer_bmn_rel` use independent exact
angle maps; ordinary `bmn_rel` also retains the spectrum comparison at the
consumer's actual R/Z positions. No angle or phase fit is used. NEO-2's
known query offset is removed analytically when taking its Fourier transform.
Their fine-resolution spectrum errors are at most 3.51e-7 and 6.85e-7,
respectively.

The extension's focused tests pass **14 checks**, with one optional Python
libneo parser test skipped in the validation environment; the separate native
NEO-2 regression fails before/passes after. Development failures and outputs
are retained, including the MARS harness sign/build corrections. Final MARS
rows use the `_r8` readbacks. GPEC's registry code is `PENTRC` (the allowed
GPEC-family label), but only its equilibrium library ran.

Raw roots are `phase1/{gpec,neo-2}/runs/readers_*_final`, the four
`phase1/chease-mars/runs/readers_mars_*_final*` producers and
`phase1/mars-k/runs/readers_mars_hamada_*_r8`. The final derived table is
`phase1/mars-k/runs/readers_summary_final/summary.json`.

```bash
python -m equilibrium.phase1.results_export.build_consumers gpec --source <GPEC> --output <disk>/gpec_readback
python -m equilibrium.phase1.results_export.build_consumers mars --source <MARS-Q> --output <disk>/mars_readback
python -m equilibrium.phase1.results_export.build_consumers neo2 --source <NEO-2-build> --neo2-override <PR193>/COMMON/neo_magfie.f90 --output <disk>/neo2_vector
python -m equilibrium.phase1.results_export.consumer_study --help
python -m equilibrium.phase1.results_export.mars_native_study --help
python -m equilibrium.phase1.results_export.collect_consumers --data <phase1-raw-root> --output <fresh-derived-root>
```

## Consumer inventory and bounded gaps

| Path | Actual use / disposition |
|---|---|
| CHEASE/MARS G-EQDSK → libneo / direct NEO-RT | Both cases, two resolutions; parser, FluxConverter and actual Fortran `field_eq` measured. |
| KIN6D FE → producer EQDSK → libneo Boozer → NEO readers | Newly implemented and measured here; no KIN6D source changes and no native KIN6D Boozer writer found. |
| Boozer `.bc` → NEO-2 | Actual COMMON reader, radial/angular splines and full vector/Jacobian path measured on both cases and all three producers at two resolutions; PR193 fixes multiple-surface initialization. |
| GPEC EQDSK | Used by `GPEC/old_equil/prepare_input.py` and `rmp_torque.gpec.set_eqdsk_path`; actual `read_eq_efit/direct_run` reconstruction now measured through final Hamada splines. |
| VMEC++ `wout.nc` | Used by Phase 1's own diagnostic reader (`producers/vmecpp.py`, `VmecWOut.from_wout_file`), already measured in [common results](../results/README.md). No retained NTV lane invokes wout→EQDSK/Boozer; libneo's available `vmec_to_efit.py` is unused here. No additional downstream conversion claimed. |
| DESC HDF5 / DESC-to-EQDSK | Native HDF5 readback is in the common Phase 1 comparison. No DESC-to-EQDSK or DESC-to-Boozer invocation in retained NEO-RT, NEO-2, GPEC or BOOZER lane scripts. Record as unused, not qualified. |
| CHEASE/MARS native metrics → MARS | `NIDEAL=0,NFFTOPT=0` exports `OUTRMAR/OUTVMAR` without NAG. Actual `READTOR`, `READVAC`, `GETQPLS`, `FFTDRIVER` and equilibrium Hamada routines are exercised on both exact cases at two producer resolutions. |
| GPEC/MARS perturbations / historical boozmn | Matching common-case perturbation outputs do not exist. The axisymmetric Hamada geometry is covered; perturbation spectra and transport remain outside this slice. Historical artifacts remain intact. |

## Changes, validation and reproduction

- Previous defect: libneo f2py float/double ABI, `1b867ec`,
  [fork PR1](https://github.com/krystophny/libneo/pull/1); still used for the
  EQDSK field wrapper. Owner: [EQ-EXPORT-1](../../ERRATA.md#eq-export-1-libneo-efit-python-wrapper-kind-map).
- Numerical export improvements: `075dd48` (finite flux boundary) and
  `d5bbe6c` (header precision),
  [fork PR2](https://github.com/krystophny/libneo/pull/2), against
  `krystophny/libneo:main`. Independent circular tests fail on the original
  and intermediate builds and pass after the changes. No upstream PR or merge.
- Own producer: `ade9cb8ac`; consumer runner/harness: `10cff550c`;
  reproduction helper, analytic NEO-2 test and figure: `f65eab296` on
  `lane/export-e2e2`; combined norms and replay: `4ce3e0304`, `9adfa4695`.
  No own-code push or merge.

There are 33 distinct passing focused checks and two skipped opt-in CHEASE
solve checks. The first full check encountered a Git LFS pointer in one
existing COCOS fixture; materializing that 127 KB fixture and rerunning its
six checks passed without a code change. The seven export checks also pass
after adding the common-norm behavioral oracle. The fixture was not committed.
Ruff and diff whitespace checks pass. Final runs reuse all native CHEASE
solutions and run four bounded KIN6D P3 solves; one development KIN6D solve
is also retained. No cluster, long CHEASE or transport runs.

Raw final runs are `.../phase1/{neo-rt,kin6d}/runs/export_e2e2_final_*`, with
radial controls under `neo-rt/runs/export_e2e2_radial_*`. The registry includes
development runs and `export_e2e2_validation_v1/v2`; the failed fixture check
is retained as aborted. `export_e2e2_combined_v1` derives the combined norms
from those immutable exports without a new solve. Validation tools preserve failing/passing libneo logs,
source snapshots and the exact NEO-2 library/module hashes and build command.
KIN6D pin: `3c851d7`; public/MARS CHEASE: `b942066` / `104053d`;
NEO-RT: `8411537`; NEO-2 checkout: `cefb20b`. Converter pin: `d5bbe6c` on
fork base `e533f4d`; the separately hashed f2py wrapper retains PR1.

```bash
python -m equilibrium.phase1.results_export.build_neo2_reader --build <NEO-2-build> --output <disk-scratch>/neo2_readback
python -m equilibrium.phase1.results_export.extend_study --help
python -m equilibrium.phase1.results_export.combine_metrics <source-results.json>... --output <new-raw-root>
python -m equilibrium.phase1.results_export.plot <results.json>... --table equilibrium/phase1/results_export/summary.csv --figure <disk-scratch>/export_accuracy.png
uv run python ops/run_registry.py
```

`extend_study` accepts `--variant kin6d --n 48/96 --grid 257/513`, or
`--variant public/mars --producer <native-root>`. It records requests and
hashes before executing, archives binaries and outputs, and applies a
300-second subprocess cap. Converter build flags remain those of the previous
study (Release, SKBUILD, OpenMP off); `efit_to_boozer.x` is sufficient for the
new converter. Preserve the PR1 wrapper separately when that fix is unmerged.
Set TMPDIR to disk and numerical thread counts to one. Use a fresh output
root for every repeat. The archived request.json files provide all exact CLI
settings; inputs.json provides every numerical input to the figure/table.

Controller decisions: integrate the `lane/readers` own-code commit and review
NEO-2 PR193; previous libneo integration decisions remain with the controller.
The three requested axisymmetric consumer paths no longer need a build handoff.

Chris&AI
