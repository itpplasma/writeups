# Phase 2 circular toroidal ladder

Eight circular cases, five codes, at least four resolutions per code. E1/E2
use A=40,20,10; `E1_A3p1` and `E2_A3p1` are the two E3 source-law variants.
The study is delivered; three VMEC++ cases remain outside the sampled PLAN
targets. No exact toroidal interior solution is used.

[Cases](../cases.json) are generated from the authoritative contract by
[cases.py](../cases.py): R0=6.2 m, B0=5.3 T, Fedge=32.86 T m, q_source_scale=1.5,
psi_edge=pressure_edge=0, SI/COCOS 3. E1 has p'=0, FF'=-7.066666666666666 T;
E2 has FF'=0, p'=-146292.2647219988 Pa/(Wb/rad). The source scale does not
prescribe constant q. Boundaries contain 4096 exact circle samples plus closure;
public CHEASE receives every second sample to fit its NPBPS=2300 capacity.
Historical runs were not reused. The registry retains 193 completed solves and
18 aborted attempts (16 initial public-CHEASE boundary-capacity failures and
two VMEC++ timeouts). Raw outputs and every attempted solve are in
`/home/ert/data/iter_tc24/phase1/<code>/runs/phase2_20261009_*` and the registry.

The finest KIN6D P3 state at boundary_nodes=192 is the numerical reference.
Its ladder is 24,48,96,192; dense circular boundaries, source constants and
radial/angular readback counts 513/128 are held fixed. The Phase 1 metric and
seeded-point logic is reused: 4000 area-uniform points with s_pol<=0.98,
physical-volume weights R, and 40 s_tor levels in [0.05,0.98]. Relative maxima
use reference maxima, except q's pointwise relative maximum. No alignment,
scale, smoothing, phase or sign is fitted. Sampling excludes the outer shell;
these are sampled accuracy gates, not a whole-plasma enclosure.

VMEC++ and DESC receive pressure(s_tor), iota(s_tor), Phi_edge and the boundary
from the finest forward reference. Their q/Phi errors measure input transfer;
physical psi/B/axis comparisons remain independent outputs. CHEASE is run in
its constant-source forward mode. [rates.csv](rates.csv) gives self-convergence
and Richardson estimates; [finest.csv](finest.csv) retains the largest delivered
state even when native stopping failed. [qualified.csv](qualified.csv) selects
the finest state passing all sampled gates and native stopping.

The recovered-flux majorant is computed inside KIN6D on its represented domain.
It estimates the energy norm sqrt(integral R*|delta Bpol|^2 dR dZ), using ordinary
quadrature. Richardson uses the fixed interior samples; its energy conversion
uses pi*a^2 times their mean, so the excluded shell remains a sampling difference.
The estimates agree in magnitude; they are not claimed identical norms.

| Case | psi Richardson | Bpol Richardson | relative majorant | majorant / Richardson |
|---|---:|---:|---:|---:|
| E1_A10 | 6.01e-10 | 7.59e-09 | 1.82e-08 | 2.40 |
| E1_A20 | 6.00e-10 | 8.06e-09 | 1.69e-08 | 2.10 |
| E1_A3p1 | 6.04e-10 | 1.83e-08 | 5.49e-08 | 2.99 |
| E1_A40 | 6.01e-10 | 7.15e-09 | 1.65e-08 | 2.31 |
| E2_A10 | 6.11e-10 | 1.76e-08 | 2.37e-08 | 1.34 |
| E2_A20 | 6.03e-10 | 1.17e-08 | 1.84e-08 | 1.57 |
| E2_A3p1 | 7.59e-10 | 6.50e-08 | 8.17e-08 | 1.26 |
| E2_A40 | 6.01e-10 | 7.75e-09 | 1.70e-08 | 2.19 |

Volume error versus the analytic circular volume is 3.54e-10 at the reference
mesh. The largest last-mesh axis change is 3.6e-8 relative to R0; the largest
Phi_edge change is 5.6e-9. [reference_errors.csv](reference_errors.csv) retains
these checks and the full-domain majorant separately from sampled differences.
Expected field rates: P3 at least third order; CHEASE bicubic; VMEC++ at least
first order radially; DESC spectral. Below-target export/reference floors end
rate interpretation. Early and last interval rates are retained explicitly.

DOF axes retain each producer's definition: KIN6D unconstrained nodal coefficients; CHEASE
4*NS*(NT+1) Hermite coefficients; VMEC++ NS*(3*MPOL-2), including constrained
coefficients; DESC optimizer variables. They are useful resolution measures,
not equal operation counts.

Lowest measured producer wall time in seconds passing all sampled targets:

| Case | KIN6D P3 | CHEASE public | CHEASE MARS | VMEC++ | DESC |
|---|---:|---:|---:|---:|---:|
| E1_A10 | 1.99 | 1.28 | 1.52 | 7.31 | 35.96 |
| E1_A20 | 2.00 | 1.17 | 1.32 | 8.65 | 32.74 |
| E1_A3p1 | 5.16 | 2.47 | 3.83 | — | 60.49 |
| E1_A40 | 1.94 | 1.28 | 1.27 | 5.64 | 30.53 |
| E2_A10 | 2.10 | 1.22 | 1.27 | — | 30.34 |
| E2_A20 | 1.95 | 1.22 | 1.37 | 76.92 | 40.79 |
| E2_A3p1 | 1.92 | 2.47 | 5.78 | — | 58.19 |
| E2_A40 | 1.98 | 1.17 | 1.32 | 60.49 | 33.44 |

Current-main KIN6D producer costs at the same eight previously passing states
are retained separately in [kin6d_current_cost.csv](kin6d_current_cost.csv).
The historical table and `best_cost.csv` above remain unchanged. Each new run
uses identical native input and boundary bytes, mesh settings, fixed reference
and sample points; all eight retain the same DOF and pass native stopping and
all sampled physical targets. Only these selected states were repeated.

| Case | Historical producer s | Current producer s |
|---|---:|---:|
| E1_A10 | 1.993 | 0.423 |
| E1_A20 | 1.998 | 0.419 |
| E1_A3p1 | 5.163 | 1.695 |
| E1_A40 | 1.942 | 0.417 |
| E2_A10 | 2.102 | 0.428 |
| E2_A20 | 1.948 | 0.413 |
| E2_A3p1 | 1.920 | 0.418 |
| E2_A40 | 1.978 | 0.412 |

The current source is `f6a33c91610e49e7eba63c0b4f8dcc099e8a77e1`;
archived CPU binary SHA256 is
`66037bab430bd3696ca902b411f37a2ad9f9e75b5dedef5d92638e71ee43448c`.
Both costs measure the existing worker's producer call, including mesh,
assembly/solve, estimator, native outputs and contour/profile readback;
subsequent accuracy comparison and Python worker startup are excluded.
Historical source is `b2e8c97fc19f3bf62f0d3d6925713b5a494b4604`;
its binary SHA256 is
`3469d21d2fce232478440c1e2213676ed5b2483d13211f3dfd4dbb595911c88d`.
Both historical and new pins and raw roots are retained in the cost CSV.

The new calls ran sequentially on CPU3 with one numerical thread after the
other campaign native computations paused. Ambient host load averages were
5.98/6.36/7.30; desktop, synchronization and other
background processes remained active, so this is not a globally idle-host
measurement. Other-code costs above retain their historical execution
conditions. These single repeats demonstrate current cost at matched sampled
accuracy; they do not establish a controlled cross-code speed ranking.
Raw requests, manifests, outputs and ambient process snapshot are in
`/mnt/storage/codex-equilibrium-20261010/kin6d_tc24/scratch/phase2_currentcost_20261010`.

KIN6D producer time includes mesh/assembly/solve, its majorant, native export
and contour/profile readback. The original solve-only time is retained as
`producer_reported_s`; comparison-point and error-oracle evaluation is excluded
for every code. The common forward reference construction is excluded from
VMEC++/DESC timings. Runs use one pinned logical CPU on a Ryzen 9 5950X, with
one thread in numerical libraries; concurrent lanes make these single timings
indicative. KIN6D does not yet beat public CHEASE across this ladder when its
estimator/readback cost is included.

Remaining numerical limitations are owned by [ERRATA EQ-P2-1](../../ERRATA.md#eq-p2-1).
A targeted E2/A10 NS=1025, mpol=16, ftol=1e-18 repeat also exceeds
300 s (`vmecpp_phase2_E2_A10_ns1025_20261010_01`); its input, native log and
reference-evaluator pin are retained in the registry. It supplies no passing
accuracy row; the NS513 axis gap remains unqualified.
Public CHEASE E1/A3.1 NS=128 also reports a magnetic-axis minimizer warning;
its field differences are below target, but it is excluded from qualification.
NS=64 passes. Crosses in the cost figures mark native stopping failures.

For e=1/A, the symbolic disk expansion gives

- E1: Delta/a=e/8+11e^3/512+O(e^5), q(0)/q_s=1+(q_s^-2-1/8)e^2+O(e^4).
- E2: Delta/a=5e/8-209e^3/512+O(e^5), q(0)/q_s=1-15e^2/8+O(e^4).

[expansion.py](../expansion.py) also derives the q quartic coefficient. The
PDE and circular boundary residuals are tested symbolically. Over A=40,20,10,
unweighted fits of log absolute difference against log(1/A) give
leading-shift remainder orders 3.002 / 2.991 (E1/E2); q remainder
orders are 4.005 / 3.990. A=3.1 is displayed separately from the asymptotic claim.
[physics.csv](physics.csv) includes the signed differences and last q-axis mesh
change; the latter, without an assumed safety factor, supplies the plot bars.

End-to-end data: [exports.csv](exports.csv), [boozer.csv](boozer.csv), and
[boozer_volume.csv](boozer_volume.csv) compare
KIN6D FE/CHEASE NOUT, producer EQDSK, the actual libneo field_eq reader, Boozer
spectra/fields/flux labels, and actual NEO-RT/NEO-2 readers. Boozer references
trace the numerical psi contour and independently integrate its B^2/Bpol
angle; a circular-flux analytic spectrum tests this map. The volume table pools
12 surfaces over 0.05<=s_tor<=0.98 with the contour volume Jacobian and radial
trapezoidal weights. This differs from the native random-point quadrature.
Per-surface psi errors in boozer.csv use each surface's own psi norm: the
near-edge maximum reaches 2.12e-5 and is retained, not compared to a global L2
target. The combined volume norm and absolute flux-label errors are reported
separately. No outer-shell accuracy claim is made. At the finest states, maximum pooled
Boozer psi/Bpol L2 errors are 3.82e-7/2.65e-7; maximum surface B_mn and
consumer q errors are 3.25e-8 and 3.92e-8. These measured paths pass the
corresponding targets. KIN6D EQDSK reuses the
pending exporter from `ade9cb8ac`, saved and hashed beside each readback, without
merging its lane. The reader binaries reuse the export lane's archived libneo
fork fixes; their executed hashes are in each readback manifest. VMEC++/DESC
are measured through their native wout/HDF5 states; their downstream converters
are unused under the explicit [consumer inventory](../../phase1/results_export/README.md#consumer-inventory-and-bounded-gaps). Native MARS Fourier/Hamada and standalone GPEC reconstruction
remain outside this measured package, as recorded by the export lane.

Reproduction: generate cases with `python -m equilibrium.phase2.cases`; run
`python -m equilibrium.phase2.compare --tag UNIQUE --cases E1_A40 --cpu 12`
(and the other seven IDs). The retained request.json files own the executed
resolution/tolerance repeats. Run `phase2.analyze --tag phase2_20261009`, then
`phase2.exports`, `phase2.boozer`, and `phase2.plot --output DISK_DIRECTORY` as
modules under `equilibrium`. Reader steps use the system Python with libneo;
VMEC++/DESC producers use the existing lane environments. Numerical data and
fixed points are committed; native states remain at the registered raw roots.
The executed KIN6D binary and validation logs are archived under the E1_A40
reference run's `study_artifacts/`; set KIN6D_BINARY to its `tools/gs_phase1`
for numerical-reference evaluation. Its build cache pins the build settings.
Plots/PDFs are excluded from Git and uploaded by [publish.py](../publish.py).

Validation: 34 Python tests pass, 5 optional-environment tests skip. Behavioral
oracles cover symbolic PDE/boundary/asymptotic identities, nonlinear flux-map
transfer to both inverse solvers, Richardson recovery, analytic Boozer spectrum,
and the existing common metrics/readers/producers. KIN6D P3 majorant's exact
behavioral test failed before its extension and passes with effectivity 1.14;
P2/P3 native convergence CTests pass (2/2). Focused Ruff and diff checks pass. No new confirmed third-party solver defect
was found. Controller: integrate KIN6D `b2e8c97`, this lane, and exporter
`ade9cb8ac`; retain the three VMEC++ target gaps and the consumer exclusions.

Artifact URLs and SHA256 values: [artifacts.json](artifacts.json).

PDF figures (PNG companions and hashes are in artifacts.json):

| Case | Error / DOF | Error / wall time | Exports / consumers |
|---|---|---|---|
| E1_A40 | [DOF](https://box.sloppy.at/95bfb.pdf) | [Time](https://box.sloppy.at/8baeb.pdf) | [Readback](https://box.sloppy.at/999ad.pdf) |
| E1_A20 | [DOF](https://box.sloppy.at/c5dfa.pdf) | [Time](https://box.sloppy.at/f7741.pdf) | [Readback](https://box.sloppy.at/a2ee7.pdf) |
| E1_A10 | [DOF](https://box.sloppy.at/ceaa3.pdf) | [Time](https://box.sloppy.at/1f0fc.pdf) | [Readback](https://box.sloppy.at/12c1c.pdf) |
| E1_A3p1 | [DOF](https://box.sloppy.at/6c8d8.pdf) | [Time](https://box.sloppy.at/50943.pdf) | [Readback](https://box.sloppy.at/44fdb.pdf) |
| E2_A40 | [DOF](https://box.sloppy.at/8733b.pdf) | [Time](https://box.sloppy.at/a0fbd.pdf) | [Readback](https://box.sloppy.at/74e90.pdf) |
| E2_A20 | [DOF](https://box.sloppy.at/bdf0a.pdf) | [Time](https://box.sloppy.at/f9bca.pdf) | [Readback](https://box.sloppy.at/2e0bc.pdf) |
| E2_A10 | [DOF](https://box.sloppy.at/cdf8a.pdf) | [Time](https://box.sloppy.at/7376b.pdf) | [Readback](https://box.sloppy.at/bd8c5.pdf) |
| E2_A3p1 | [DOF](https://box.sloppy.at/727e8.pdf) | [Time](https://box.sloppy.at/7b22a.pdf) | [Readback](https://box.sloppy.at/069b0.pdf) |

[Shafranov shift and q scaling](https://box.sloppy.at/06f39.pdf)


Chris&AI
