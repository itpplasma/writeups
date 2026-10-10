# KIN6D prescribed-q results

KIN6D `ccabcc5` ports the reviewed inverse branch and adds curved P2/P3
prescribed-q equilibria to `gs_phase1`. The native contract is constant physical
pprime, signed q(s_pol), signed total Phi and the supplied boundary. The solver
recovers a cubic FFprime law and signed F_edge. The nominal case F_edge is not
a constraint. The adapter retains the solved law for native field readback.
The subsequent integration pins FortNum `bfea03a`, which accepts convergence
on Brent's final permitted update; it repairs a retained Debug inverse check.
The archived convergence runs above precede that status-only dependency fix.

Twelve one-thread CPU runs use the unchanged Phase 3 cases and physical query
points. Every solve completed within 300 s; the slowest producer took 102.84 s.
[kin6d_comparison.csv](kin6d_comparison.csv),
[kin6d_self_convergence.csv](kin6d_self_convergence.csv) and
[kin6d_finest.csv](kin6d_finest.csv) retain resolution, cost, fields, q, axis,
volume, flux, curl current and integrated source current. Raw artifacts and
pre-execution hashes are in the run registry under tag
`kin6d-inverse-20261009-ccabcc5`. No timing repeats or leadership claim are made.

## Convergence

Solovev uses 24/48/96/192 boundary nodes and E1/E2 use 25/37/55/81. All meshes
are curved P3 with maximum area `(2*pi*a/n)^2/2`, `2*n+1` radial points and one
cubic FFprime interval. These budgets are refined together. Norms use the
same 600 R-weighted interior samples as the other-code study; they are not
whole-plasma bounds. The circular reference is the finest inverse state;
its zero errors in the CSV do not establish exactness.

| Case / resolution | psi rel. L2 | Bpol rel. L2 | F rel. L2 | q rel. max | Producer s |
|---|---:|---:|---:|---:|---:|
| E1 n37 vs n81 | 1.53e-7 | 3.09e-6 | 2.45e-7 | 3.16e-6 | 6.04 |
| E2 n55 vs n81 | 5.03e-8 | 1.77e-6 | 4.15e-8 | 1.82e-6 | 33.56 |
| Solovev n48 vs exact | 2.67e-7 | 8.30e-6 | 2.47e-7 | 2.94e-6 | 2.42 |
| Solovev n192 vs exact | 1.02e-9 | 7.82e-8 | 9.68e-10 | 3.16e-8 | 102.84 |

Those E1/E2/n48 Solovev rows also meet the sampled field maxima, axis, volume
and Phi targets. Signed Phi relative errors are below 3.8e-12 throughout.
Solovev's final refinement gives orders 3.94 in psi, 3.32 in Bpol and 4.00
in F. The independent cell-quadrature CTest also checks recovered FFprime
against exact zero and requires order >=3.5; it passes. Constant-q CTests
have last-triplet psi/BR/BZ/Btor orders 4.19/4.59/4.11/3.85 (E1) and
4.45/3.41/3.74/3.85 (E2). The CSV's log2 reduction is a reduction factor,
not an h-order for the non-doubling circular ladder.

Integrated source currents at the finest grids are -1.101493992 MA (E1),
-1.111790442 MA (E2) and -12.785832262 MA (Solovev). Solovev's relative
current error is 7.36e-10. These integrals use the actual curved P3 mesh and
executed law, with an 8/10-point quadrature comparison; the sampled jphi
column separately uses the common finite-difference curl. The latter has
lower regularity across FE faces and is not the recovered FFprime law.

The [main Phase 3 results](README.md) own the corrected final-stage public
CHEASE comparisons. Zero-pressure E1 is unaffected by the delivered-pressure
contract correction. Historical E2 public rows have finite pressure drift and
cannot qualify absolute agreement on the declared contract; the adapter now
enforces delivered pressure and Phi, but a corrected fine E2 ladder is pending.
The KIN6D convergence and exact Solovev checks above remain valid.

## Export and scope

[kin6d_exports.csv](kin6d_exports.csv) reports native, rectangular EQDSK and
actual libneo field readback at levels 1 and 3, using 129/257-square exports.
Finest libneo Bpol errors are 4.88e-8 (E1 versus native n81), 2.73e-7 (E2
versus native n81), and 5.33e-8 (Solovev versus exact). The field readers
preserve the executed F profile. Behavioral producer tests reverse q and Phi,
recover the reversed toroidal field, reload the native law, and round-trip
signed EQDSK q, Phi and fields. The nominal-F header defect is fixed with a
failing-before/passing-after regression; see EQ-KINV-1 in ERRATA.

[kin6d_consumers_gpec.csv](kin6d_consumers_gpec.csv) is the end-to-end consumer
cell: the retained GPEC/DCON reader (`read_eq_mod`, `grid_type='ldp'`,
`jac_type='hamada'`, SHA-256 `05278e4d…`) reads the same 129/257 canonical exports.
Six preregistered one-thread executions on CPU 12 took 0.27-0.38 s each and returned
5120 `(s_pol, theta)` samples in
`/home/ert/data/iter_tc24/phase3/runs/gpec-kin6d-readback-20261010-01`; GPEC's own
flux label, straight angle and signs are used as stored, with no rescaling or fit.

| Case / level | psi L2 | B_pol L2 / max | B_tor L2 | q rel. max | Phi_edge rel. | Hamada \|B\| / Jacobian |
|---|---:|---:|---:|---:|---:|---:|
| E1 1 | 2.80e-08 | 3.21e-06 / 2.47e-05 | 1.13e-10 | 2.25e-06 | 1.78e-07 | 8.71e-08 / 2.33e-06 |
| E1 3 | 7.98e-09 | 1.68e-06 / 8.21e-06 | 7.11e-11 | 1.39e-07 | 6.71e-09 | 6.20e-09 / 1.36e-07 |
| E2 1 | 4.16e-08 | 4.60e-06 / 2.82e-05 | 8.40e-11 | 1.95e-06 | 1.81e-07 | 1.79e-07 / 2.06e-06 |
| E2 3 | 9.04e-09 | 2.14e-06 / 1.19e-05 | 7.75e-11 | 1.55e-07 | 6.62e-09 | 1.01e-08 / 1.66e-07 |
| Solovev 1 | 2.81e-07 | 7.20e-06 / 4.87e-05 | 2.47e-07 | 4.22e-06 | 2.26e-07 | 8.33e-07 / 3.18e-06 |
| Solovev 3 | 9.12e-09 | 2.36e-06 / 1.17e-05 | 9.13e-10 | 2.91e-08 | 5.21e-09 | 1.20e-08 / 3.54e-08 |

The sampled field, q and total-flux errors meet the PLAN targets (psi L2 1e-6,
B_pol and B_tor L2 1e-5 with max 1e-4, q 1e-5, Phi_edge 1e-6). For Solovev the
oracle is the exact analytic state; the table also measures flux labels, the
Hamada |B| spectrum and its Jacobian against that independent oracle. For E1 and E2 the
oracle is the same-level KIN6D native field readback (a staged copy of `mesh.dat` and
the executed `profile-law.dat`, read through `gs_phase1 --evaluate-stream`), which is
independent of the exported EQDSK interpolation but not of KIN6D; those rows qualify
the export and GPEC readback of psi, BR, BZ, Bphi, q, s_pol, s_tor and Phi_edge, while
[Hamada contour measurements](kin6d_consumers_hamada.csv) trace the retained native
FE flux contours and integrate the volume angle independently of EQDSK/GPEC.
Their finest spectrum/Jacobian errors are below 1.7e-7; these are transfer errors
relative to each native state, not independent absolute equilibrium errors. Absolute E1/E2 accuracy must be assessed separately from these transfer errors:
KIN6D self-convergence remains measured, while the corrected public cross-check
and E2 pressure-contract limitation are recorded in the [main results](README.md). The pinned ccabcc5 executable is
no longer on disk; the native readback used the `kin6d` build at af84393 (`gs_phase1`
SHA-256 `b3042f67…`), whose `read_gs_mesh`, `sample_gs`, `sample_gs_many`,
`gs_profile_f` and `read_gs_profile_law` are byte-identical to ccabcc5 and which
reproduces the retained native samples bit-identically at every query point (the
`oracle_vs_retained_*` CSV columns are 0 for E1/E2). For the Solovev rows these columns
carry the exact-versus-native difference, that is the solver error (BR max 4.49e-05 at
level 1 and 1.79e-07 at level 3).

The supported branch has an isolated interior minimum of psi and constant
nonpositive pprime. The inverse-input/curved contour sensitivity product is
unavailable; retained affine-P2 derivative oracles remain supported. The
nonlinear majorant has status 4 (frozen-source diagnostic), not an error bound
for the complete inverse problem. The whole-domain ladder in
[kin6d_effectivity_native_solovev.csv](kin6d_effectivity_native_solovev.csv)
covers four retained native curved-P3 resolutions of Solovev_inverse_A3
(658 to 46,558 DOFs). Reader-computed energy error against the exact oracle
decreases at approximately h³ (DOF slopes −1.55 to −1.65), with order-8 to
order-12 quadrature drift below 1.6e-11. Diagnostic effectivity stays between
1.161 and 1.178. This establishes measured effectivity for Solovev. E1/E2
full-domain comparisons use corrected final-stage public CHEASE fields
([results](README.md)); their finite-reference uncertainty precludes a nonlinear reliability claim. The GPEC/DCON EQDSK
consumer readback of a KIN6D inverse export is measured and on target (above);
[NEO-2 vector readback](kin6d_consumers_neo2.csv) now uses the existing libneo
EQDSK-to-Boozer converter on the same six canonical exports. [Scalar and spectral
checks](kin6d_boozer.csv) include actual NEO-RT/NEO-2 readers. The finest Solovev
chart uses m48; other charts use m24. Finest Bpol L2 is 3.99e-7, 6.80e-7 and
1.90e-7 for E1/E2/Solovev, with q errors <=4.03e-7 and signed edge-flux errors
<=1.96e-8. Physical Jacobian errors against native contour currents and fields
(or the exact Solovev oracle) are <=1.90e-7. [Converter precision and grid controls](kin6d_consumers_neo2_controls.csv) expose
a separate radial-geometry serialization defect: eight-digit Fourier coefficients
produce an internal geometric-determinant residual of 5.58e-4 on frozen E1; the
full-precision writer (libneo `08ace36`, independent analytic-circle regression)
reduces it to 1.14e-5 without changing physics, mapping resolution or consumer.
This diagnostic is distinct from the physical Jacobian error, which falls from
5.48e-8 to 1.81e-8. Increasing only EQDSK grid257→513 gives 1.65e-5; increasing
only precise radial map512→1024 gives 4.36e-5. Thus the residual geometry metric
is not yet qualified by expected-rate convergence. Source inspection identifies
fixed adaptive tracing tolerance `relerr=1e-9` (the input `nstep` is ignored) as
a remaining floor candidate; these measurements do not establish that cause.
The actual physical field/q/flux/Jacobian reader columns above pass independently
of this internal derivative diagnostic. No additional E1 refinements are claimed.

Raw charts, reader outputs and native contour measurements are under
`/mnt/storage/codex-equilibrium-20261010/remaining_exports/scratch/runs/kin6d-consumers-20261010`.
Registered final-source remeasurement checks all six vector and four Hamada
rows without changing any retained producer state.

## Reproduction

From the controller checkout with a built KIN6D `gs_phase1`, use a unique new tag.
Before launching consumer readback, register and commit each case/level work root
with the exact reader, native-state and export hashes in the run registry:

```sh
export TMPDIR=/home/ert/code/worktrees/_lanes/kin6d-inverse/tmp
export KIN6D_BINARY=/home/ert/code/kin6d/build/gs_phase1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
mkdir -p "$TMPDIR"
python -m equilibrium.phase3.compare --tag NEW_UNIQUE_TAG --codes kin6d --cpu 12 --kin6d-binary "$KIN6D_BINARY" --lane /home/ert/code/worktrees/_lanes/kin6d-inverse
python -m equilibrium.phase3.exports --codes kin6d --levels 1 3 --cpu 13 --result-file kin6d_exports.csv
taskset -c 12 python -m equilibrium.phase3.consumers --codes kin6d --levels 1 3 --cpu 12 \
  --work-root /home/ert/data/iter_tc24/phase3/runs/NEW_UNIQUE_ROOT \
  --result-file kin6d_consumers_gpec.csv
python -m equilibrium.phase3.analyze
uv run python ops/run_registry.py
```

For source-current integration on a retained run, call
`python -m equilibrium.phase3.worker /RAW_RUN/request.json --current-only`.
`analyze` adopts the finest inverse KIN6D reference for circular cases. The
KIN6D-only CSVs here use that same analysis restricted to the twelve KIN6D
JSON rows and the original point files; historical other-code CSVs are left
for the controller's combined regeneration.

Chris&AI
