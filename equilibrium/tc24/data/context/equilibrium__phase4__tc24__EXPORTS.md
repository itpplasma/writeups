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
Public/MARS use 513² EQDSK grids, converter radial-map resolution nlabel=512,
2048 integration angles, 2000 output surfaces and m<=128, n=0. KIN6D's selected
candidate uses a 1025² grid, nlabel=1024, 4096 angles, 2048 output surfaces and
m<=256. nlabel is not the output surface count. File hashes are in manifest.json.

The independent Boozer oracle fixes its phase at the outboard ray and
integrates B²/Bpol along the native contour. Both Fourier parities and all
retained modes are compared. No phase, gain, radius, smoothing or sign is fitted.
Scalar NEO-RT/NEO-2 readers sample 12 surfaces over 0.05<=s_tor<=0.98 with
256 angles each. Actual GPEC/DCON and full NEO-2 vector/label readers are also
executed; the latter use 512 angles. Their raw output remains unmodified.

## Measured accuracy

These export-only errors compare each reader with its native producer.
EQDSK uses the fixed 1200-point interior sample; Boozer uses contour-volume
norms. Maxima are sampled, not continuous-domain bounds. Axis and outer-edge
regions are excluded. CSVs retain psi, Bphi, full B, labels, flux and spectra
as well as Bpol. Columns prefixed `total_` compare exported fields with the
finite public CHEASE 128×256 comparator and include producer disagreement.

| Finest export-only error | Public CHEASE | MARS CHEASE | KIN6D P3 n96 |
|---|---:|---:|---:|
| libneo EQDSK Bpol relative L2 | 9.110e-5 | 5.224e-5 | 1.445e-4 |
| libneo EQDSK Bpol relative max | 1.111e-3 | 7.038e-4 | 1.657e-3 |
| Boozer Bpol relative L2 | 3.199e-4 | 3.201e-4 | 5.067e-4 |
| Boozer Bpol relative max | 7.376e-3 | 7.477e-3 | 1.134e-2 |
| Scalar reader q relative max | 3.059e-5 | 9.509e-6 | 6.557e-5 |
| Full NEO-2 Bpol relative L2 | 5.103e-4 | 5.096e-4 | 5.555e-4 |
| Full NEO-2 q relative max | 4.879e-4 | 4.759e-4 | 3.097e-3 |
| GPEC/DCON Bpol relative L2 | 8.748e-5 | 8.073e-5 | failed integration |
| GPEC/DCON q relative max | 3.101e-5 | 3.043e-6 | no result |

GPEC's positive internal flux-span/F convention is mapped to the declared
physical signs from the input header, including toroidal flux. The KIN6D
1025² input exhausts GPEC's 16384 field-line steps at ipsi=512. Its STOP path
returns zero without output; the wrapper detects the missing fields/profiles.
The diagnostic used to crash while formatting this failure; the tested fix is
[GPEC fork PR1](https://github.com/krystophny/GPEC/pull/1), commit bb3f02a4.
It reports the integration failure and does not repair that unresolved path.

Full NEO-2's geometric Jacobian identity relative maximum is 0.263 (public),
0.261 (MARS), and 0.313 (fine KIN6D), so vector/geometry consistency remains
unqualified. Refining only KIN6D's EQDSK grid gave a 5.59e-2 Bpol readback
error; refining the Boozer map/angles/modes together reduced it to 5.56e-4.
This demonstrates resolution sensitivity, not target closure. The intermediate
files and failures remain in the execution inventory. No OUTRMAR/Hamada chain
or downstream perturbation/torque solve is included.

## Reproduction and retained history

The converter is libneo a9b6d9674f82e6e1bdac5146fddc732097bece9d, with the
signed-boundary correction in [fork PR3](https://github.com/krystophny/libneo/pull/3).
The Python EQDSK preparation reader needs
[fork PR4](https://github.com/krystophny/libneo/pull/4), f27ee06, for four-digit
fixed-width dimensions; the 1025² runs retain that exact source copy. The
Fortran converter/field reader is unchanged. Actual NEO-2 uses the retained
PR193 vector-reader build; source/build hashes are recorded with every job.

Use the commands in the TC24 README and fresh execution tags. For the fine
KIN6D export add `--grid 1025 --nlabel 1024 --ntheta 4096 --mpol 256
--eqdsk-reader <fixed-eqdsk_base.py>`. Actual vector readers use
`reference_exports --consumer gpec|neo2 --producer <run> --export <export-run>
--tag <unique-tag>`; `--reader-directory` selects the fixed GPEC build.

The old top-level package index and figures describe the superseded absolute-psi
JINTRAC experiment. They are preserved as history. The current archive and
figure URLs are in `reference/export_package.json` and `reference/artifacts.json`.

Chris&AI
