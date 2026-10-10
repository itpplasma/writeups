# TC24 modx03 candidate equilibrium exports

Status: **measured candidates, not qualified perturbation inputs**. The
collaborator reference is `ngfile_p1_run_eq_modx03_20260527`. Native convergence
and consumer accuracy still have open targets; see the main TC24 README.

The archive contains `chease_public/`, `chease_mars/` and `kin6d/`, each with
`equilibrium_cocos3.g`, `equilibrium_boozer_lhs.bc`, the converter input,
producer/converter manifests and measured accuracy. `inputs/` contains the
four normalized-current case contracts, profiles and boundaries; `received/`
preserves all four original gfiles. `accuracy/` contains the numerical tables,
`scripts/` the study entry points (imports require iter_tc24).
`vmecpp_native_only/` and `desc_native_only/` contain native solver states;
their downstream export chains have not been measured in this study.

## Coordinates and resolution

G-EQDSK is SI, COCOS 3: physical phi increases CCW viewed from +Z,
BR=-psi_Z/R, BZ=psi_R/R, Bphi=F/R. The reference has edge psi=0, negative
axis psi (about -11.826 Wb/rad), F<0, current<0 and q<0. The boundary is the
128-mode curve at received s_pol=0.995; the separatrix and X-point are excluded.
This is the derived derivative-shape/current problem documented in the README,
distinct from replaying the collaborator's supplied Istar namelist.

Boozer uses the libneo/NEO left-handed `(s_tor,theta_B,phi_B)` chart, with CCW
poloidal theta, negative physical toroidal flux (about -119.302 Wb), iota=1/q,
s_tor=Phi/Phi_edge and rho_tor=sqrt(s_tor). Geometry and fields are metres and
tesla. The converter uses CGS internally; psimax=(psi_edge-psi_axis)*1e8.
Public/MARS baseline exports use 513² EQDSK grids, converter radial-map resolution
nlabel=512, 2048 integration angles, 2000 output surfaces and m<=128, n=0.
Public CHEASE refinements retain that producer and EQDSK, with nlabel=1024/2048,
4096/8192 integration angles, 2048/4096 output surfaces and m<=256/512.
KIN6D's selected
candidate uses a 1025² grid, nlabel=1024, 4096 angles, 2048 output surfaces and
m<=256. nlabel is not the output surface count. File hashes are in manifest.json.

The independent Boozer oracle fixes its phase at the outboard ray and
integrates B²/Bpol along the native contour. Both Fourier parities and all
retained modes are compared. No phase, gain, radius, smoothing or sign is fitted.
Scalar NEO-RT/NEO-2 readers sample 12 surfaces over 0.05<=s_tor<=0.98 with
256 angles each. Actual GPEC/DCON and full NEO-2 vector/label readers are also
executed; the latter use 512 angular spline knots at baseline, refined to
1024/2048 for the public m<=256/512 files. Their raw output remains unmodified.

## Measured accuracy

These export-only errors compare each reader with its native producer.
EQDSK uses the fixed 1200-point interior sample; Boozer uses contour-volume
norms. Maxima are sampled, not continuous-domain bounds. Axis and outer-edge
regions are excluded. CSVs retain psi, Bphi, full B, labels, flux and spectra
as well as Bpol. Full-consumer field norms use R-weighted reader samples:
GPEC samples 0.05<=s_pol<=0.98; NEO-2 samples 0.05<=s_tor<=0.98.
Columns prefixed `total_` compare exported fields with the
finite public CHEASE 128×256 comparator and include producer disagreement.

| Finest export-only error | Public CHEASE | MARS CHEASE | KIN6D P3 n96 |
|---|---:|---:|---:|
| libneo EQDSK Bpol relative L2 | 9.110e-5 | 5.224e-5 | 1.445e-4 |
| libneo EQDSK Bpol relative max | 1.111e-3 | 7.038e-4 | 1.657e-3 |
| Boozer Bpol relative L2 | 8.128e-5 | 3.201e-4 | 5.067e-4 |
| Boozer Bpol relative max | 1.416e-3 | 7.477e-3 | 1.134e-2 |
| Scalar reader q relative max | 2.766e-5 | 9.509e-6 | 6.557e-5 |
| Full NEO-2 Bpol relative L2 | 8.801e-5 | 5.096e-4 | 5.555e-4 |
| Full NEO-2 q relative max | 2.937e-5 | 4.759e-4 | 3.097e-3 |
| NEO-2 Jacobian / native relative max | 2.094e-5 | 2.853e-4 | 4.609e-4 |
| Geometric Jacobian / native relative max | 1.744e-2 | 3.529e-1 | 2.382e-1 |
| GPEC/DCON Bpol relative L2 | 8.748e-5 | 8.073e-5 | 9.347e-4 |
| GPEC/DCON q relative max | 3.101e-5 | 3.043e-6 | 7.720e-4 |

GPEC's positive internal flux-span/F convention is mapped to the declared
physical signs from the input header, including toroidal flux. The KIN6D
1025² input at driver etol=1e-10 exhausts GPEC's 16384 field-line steps at
ipsi=512. Its STOP path
returns zero without output; the wrapper detects the missing fields/profiles.
The diagnostic used to crash while formatting this failure; the tested fix is
[GPEC fork PR1](https://github.com/krystophny/GPEC/pull/1), commit bb3f02a4.
It reports the integration failure. With the same input, outer chart surface,
solver and step cap, etol=1e-8 completes the reader in 1.69 s and gives the
KIN6D table values above. This is a recorded integration configuration change;
field/q targets remain unmet and no GPEC solver defect is established.

Full NEO-2's geometric Jacobian identity relative maximum is 0.0177 (precision-refined
public), 0.261 (MARS), and 0.313 (fine KIN6D), so vector/geometry consistency
remains unqualified. The native Jacobian oracle uses independent native contour
quadrature for signed I, F and q, with J=-Phi_edge*(F+I/q)/(2*pi*B_native²).
It compares both reader Jacobians with the producer, separately from the
reader's internal identity. Native-reference and sample-domain uncertainty
remain part of the export budget.

At a fixed public CHEASE producer/EQDSK, coupled map/angle/mode refinement
reduces the internal Jacobian mismatch 0.263→0.0289→0.0175 and Bpol L2
5.103e-4→1.618e-4→8.801e-5. Doubling only NEO-2 angular knots leaves the
baseline mismatch unchanged (0.263→0.264). Direct Fourier/radial reconstruction
of the baseline file independently reproduces the 0.264 mismatch, locating it
in exported geometry rather than a global chart sign. The final refinement
does not establish an asymptotic rate or close the geometric residual.
A frozen-settings control using sixteen-digit Fourier output leaves the
residual unchanged (0.0175→0.0177), ruling out output rounding as its dominant
cause. The remaining TC24 radial/Fourier geometric derivative map is unresolved;
retained 513² field interpolation and q errors also remain above target.

Two additional controls sample the same public128 NOUT Hermite solution
inside the native plasma (`rho<=1`) at 513² and 1025², keeping the final precise
converter, map2048/angles8192/m512/4096 output surfaces and reader2048 fixed.
Both retain the original delivered metadata and normalized-profile splines.
Outside the plasma both sample the same original EQDSK cubic continuation;
there is no far-exterior NOUT extrapolation. Libneo constructs quintic splines
across whole rows and columns, so this continuation participates in the
coefficients, particularly near the outer measurement surface. These are held
sampler controls, not a claim of isolated native-only interpolation stencils.

| Native-sampler control | 513² | 1025² |
|---|---:|---:|
| libneo EQDSK Bpol relative L2 | 4.498e-5 | 6.274e-6 |
| libneo EQDSK Bpol relative max | 5.687e-4 | 4.730e-5 |
| Boozer Bpol relative L2 | 5.830e-5 | 1.874e-4 |
| Scalar reader q relative max | 2.569e-6 | 8.317e-7 |
| Full NEO-2 Bpol relative L2 | 6.923e-5 | 6.131e-5 |
| Full NEO-2 q relative max | 1.537e-5 | 2.738e-4 |
| Internal geometric Jacobian relative max | 2.071e-2 | 3.038e-2 |
| NEO-2 Jacobian / native relative max | 1.420e-5 | 2.315e-5 |
| Geometric Jacobian / native relative max | 2.029e-2 | 2.948e-2 |

The EQDSK Bpol error decreases by a factor 7.17 and passes its targets at 1025,
but downstream chart geometry and q-label errors worsen. This does not establish
expected-rate convergence for the converter chart. Its tracing/radial-map
reconstruction remains an unresolved defect candidate; no global sign or
normalization mismatch was found. The previous precise 513 result remains frozen
in the main table rather than being replaced by this mixed improvement.

Refining only KIN6D's EQDSK grid gave a 5.59e-2 Bpol readback
error; refining the Boozer map/angles/modes together reduced it to 5.56e-4.
This demonstrates resolution sensitivity, not target closure. The intermediate
files and failures remain in the execution inventory. No OUTRMAR/Hamada chain
or downstream perturbation/torque solve is included.

## Reproduction and retained history

The converter is libneo a9b6d9674f82e6e1bdac5146fddc732097bece9d, with the
signed-boundary correction in [fork PR3](https://github.com/krystophny/libneo/pull/3).
The Python EQDSK preparation reader needs
[fork PR4](https://github.com/krystophny/libneo/pull/4), f27ee06, for four-digit
fixed-width dimensions; the 1025² runs retain that exact source copy.
The precision control changes only converter surface/geometry output to
sixteen-digit precision; its copied source and binary hashes are retained.
The Fortran field reader is unchanged. Actual NEO-2 uses the retained
PR193 vector-reader build; source/build hashes are recorded with every job.

Use the commands in the TC24 README and fresh execution tags. For the fine
KIN6D export add `--grid 1025 --nlabel 1024 --ntheta 4096 --mpol 256
--eqdsk-reader <fixed-eqdsk_base.py>`. Actual vector readers use
`reference_exports --consumer gpec|neo2 --producer <run> --export <export-run>
--tag <unique-tag>`; `--reader-directory` selects the fixed GPEC build.
Rebuild that reader with the current `gpec_readback.f90` before using
`--gpec-tolerance 1e-8`; the default remains 1e-10. The override rejects old
reader builds that ignore the fourth argument. Requests and manifests retain
the selected tolerance.

The old top-level package index and figures describe the superseded absolute-psi
JINTRAC experiment. They are preserved as history. The archive retains baseline
candidates; new refinement roots are in the accuracy CSVs. Archive and figure
URLs are in `reference/export_package.json` and `reference/artifacts.json`.

Chris&AI
