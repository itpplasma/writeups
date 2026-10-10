# Phase 5: periodic-cylinder limit

This is the C0 Gold–Hoyle/Lundquist field and signed-q comparison at
A=10,30,100,300, plus exact-cylinder KIM equilibrium ingress. All five codes now
have finite-A results, including native KIN6D P3 nonlinear solves. Its exact
Gold–Hoyle evaluator remains separate from the PDE convergence study.

Figure: [PNG](https://box.sloppy.at/272c9.png), [PDF](https://box.sloppy.at/baeda.pdf).
The original campaign contains 150 cylinder executions: 143 completed and seven retained
failures. The comparison CSV has 132 result rows; 130 report native convergence
and two are DESC iteration-cap outputs. This KIN6D increment adds 26 successful
runs and two coarse readback failures. Its 34 selected Python tests pass.

## Physical cases and source laws

[cases.json](../cases.json) fixes a=0.62 m, L=2π×6.2 m and |Baxis|=5.3 T.
The geometric torus radius is Rmajor=Aa; L stays fixed. This resolves the
incompatible wording “fixed L=2πR0 while R0 tends to infinity” using the C0
contract's independent reference length. Physical pitch stays fixed.

The primary has negative RH twist: GH q_RH=-1.5; Lundquist αa=-1.5.
The latter is the contract's positive-α reference with the explicit twist
control applied so both forward cases have an axis-minimum flux gauge.
Stored cylinder coordinates are RH; x=R-Rmajor, y=-Z and z aligned with +phi
give Btheta_c=-Btheta_RH and q_c=-L q_RH/(2πRmajor).

Set u=psi/Rmajor, psi_edge=0, F=Rmajor f(u), and p'=0. With b=Baxis:

| Family | Cylinder fields | Absolute-flux toroidal law |
|---|---|---|
| Gold–Hoyle | Bz=b/(1+τ²r²), Btheta=τr Bz | f(u)=Bz(a) exp(2τu/b), FF'=Rmajor (2τ/b) f² |
| Lundquist | Bz=b J0(αr), Btheta=b J1(αr) | f(u)=Bz(a)+αu, FF'=Rmajor αf |

Here u'=-Btheta_RH, τ=2π/(L q_RH), and u(a)=0. These laws fix Fedge
and the absolute flux dependence, without fitting amplitudes or signs.
Finite-A axis field and toroidal flux are outputs. This is a **forward-law
continuation**, distinct from the older contract proposal's inverse
continuation at fixed cylinder flux. Both have the same exact cylinder limit.
VMEC++/DESC receive q(s_tor) and Phi from the finest public-CHEASE forward
solution; they do not additionally prescribe Fedge or current.

Writing ε=1/Rmajor gives

```
Delta u - ε/(1+εx) u_x + g(u) = 0,     g=f df/du.
u=u0+εu1+O(ε²),  Delta u0+g(u0)=0,
(Delta+g'(u0))u1 = u0_x,              u1|r=a=0.
```

The m=1 correction is u1=h(r)cos(theta), where
`h=u0' [K(r)-K(a)]` and `K'=integral_0^r t u0'(t)^2 dt/[r u0'(r)^2]`.
[model.py](../model.py) evaluates this unfitted correction. Its symbolic
expansion replays the existing native FortSym leading-order map; the
behavioral test verifies an O(A^-2) force residual in the corrected field.
The angular first correction integrates to zero: field error is O(A^-1),
while integrated flux and scaled-q differences start at O(A^-2).
This is consistent with the zeroth/first-order screw-pinch expansion in
[Freidberg's MIT Lecture 5, p.7](https://ocw.mit.edu/courses/22-615-mhd-theory-of-fusion-systems-spring-2007/a5c962e43b645b825b13715a131166e2_lecture5.pdf).

## Solver routes and measurement

| Code | Checked route | Resolution / disposition |
|---|---|---|
| KIN6D | `gold_hoyle_demo`, native exact evaluator | Both q signs and field reversal; no discretization claim |
| KIN6D P3 | `gs_phase1` at `2d8142a`, absolute cubic p'/FF' profiles | Curved boundary nodes 16,32,64; Lundquist also 128. Two 16-node readback failures retained; native fields and measured q |
| Public CHEASE | Finite-R GS, forward EXPEQ profiles | NS=NT=16,32,64; no exact-cylinder switch demonstrated |
| MARS CHEASE | Same forward laws and boundary | NS=NT=16,32,64; no exact-cylinder switch demonstrated |
| VMEC++ | Native fixed-boundary toroidal equilibrium | ns=33,65,129; mpol=12; ntheta=48; no translational-cylinder route in the inspected producer/API |
| DESC | `Equilibrium` with `FourierRZToroidalSurface` | L=M=4,6,8, with 12/16 Lundquist refinements; N=0; no translational-cylinder route in the inspected producer/API |
| KIM | Actual native profile reader and `calculate_equil` | Exact cylinder, positive-radius B² seed; equilibrium only |

CHEASE resolves its normalized profile chart against the absolute-psi law by
a secant iteration, retaining every native iteration. Its profile-map tolerance
is 3e-9; exported source-law mismatch is recorded in `runs.csv`. No solver
source is modified. The common adapter now accepts validated tabulated p'/FF'
profiles in addition to constant sources; its SI normalization has a behavioral
unit test.

KIN6D uses the same absolute-psi laws: exact affine FF' for Lundquist and 128
cubic Hermite intervals for Gold–Hoyle, with exact endpoint values/slopes and
Fedge. The interval extends to 1.5 times the cylinder axis flux; the law is never
rescaled to a computed axis. Native source/primitive readback differs from the
analytic law by at most 8.8e-16 (FF') and 5.2e-16 (F). The regression also checks
both twist signs and field reversal against the exact cylinder fields.

There are 512 fixed off-grid points on 0.05≤r/a≤0.90, with radial area weights.
q uses 101 points on 0.05≤s_tor≤0.98 and includes the canonical sign. Native
KIN6D/VMEC++/DESC fields and CHEASE **exported-and-read-back** EQDSK fields are named
separately. CHEASE export grids are 257²; no native CHEASE field-error claim
is inferred from those exports. Resolution differences include export error.
q for VMEC++/DESC is prescribed; its agreement is an input-transfer check,
not independent force-balance evidence. No export-to-GPEC/MARS/NEO consumer
qualification is claimed by this cylinder lane.

`runs.csv` holds all study metrics, `finest.csv` the finest resolution,
`resolution.csv` adjacent-resolution field/q differences, and `aspect_rates.csv`
the observed powers between consecutive A values. Differences are reported
directly, without treating a two-level difference as a certified error bound.
Failed/unsupported requests remain in `failures.csv` and the registry.
All solves are local and single-threaded with a 300 s native solve limit;
wall time includes producer setup and source-map iterations, before common
sample evaluation. CPU affinity is recorded per run; this is not a matched
cost ranking across otherwise different environments.

Finest public-CHEASE values (the MARS variant agrees within its measured
export/discretization differences):

| Family / relative error | A=10 | A=30 | A=100 | A=300 |
|---|---:|---:|---:|---:|
| GH field L2 | 4.52955e-2 | 1.50172e-2 | 4.50239e-3 | 1.50071e-3 |
| GH first-order remainder | 2.88340e-3 | 3.18220e-4 | 2.86178e-5 | 3.17955e-6 |
| GH signed q max | 7.71489e-3 | 8.50052e-4 | 7.64320e-5 | 8.49144e-6 |
| Lundquist field L2 | 3.88586e-2 | 1.29088e-2 | 3.87115e-3 | 1.29033e-3 |
| Lundquist first-order remainder | 1.91989e-3 | 2.12042e-4 | 1.90709e-5 | 2.12047e-6 |
| Lundquist signed q max | 8.63907e-3 | 9.51682e-4 | 8.55662e-5 | 9.500e-6 |

These raw field differences are finite-toroidicity effects, not numerical
errors of that size. The three-resolution CHEASE A10 field differences give
orders 2.97/2.98 for GH and 3.24/3.08 for Lundquist (public/MARS). GH A300
differences reach a few 1e-9, already below the PLAN target; no further floor
investigation is justified. VMEC++ Lundquist differences fall approximately
quadratically over the measured ladder, faster than the conservative first-order
radial expectation. Its remaining q readback error at high A contains radial
interpolation error as well as the prescribed finite-A q correction.

## KIN6D P3 convergence

KIN6D boundary-node counts 16/32/64 match the nominal CHEASE NS/NT levels.
The mesh uses `max_area=(2*pi*a/n)^2/2`, curved P3 and nonlinear/quadrature
tolerances 1e-11.
Expected field order is three. Lundquist adds n=128 at all four A values to
separate its discretization contribution from the A300 first-order remainder.
The finest values are n=64 for Gold–Hoyle and n=128 for Lundquist:

| Family / relative error | A=10 | A=30 | A=100 | A=300 |
|---|---:|---:|---:|---:|
| GH field L2 | 4.52955e-02 | 1.50172e-02 | 4.50239e-03 | 1.50071e-03 |
| GH first-order remainder | 2.88340e-03 | 3.18220e-04 | 2.86179e-05 | 3.17964e-06 |
| GH signed q max | 7.71578e-03 | 8.50711e-04 | 7.72465e-05 | 9.14839e-06 |
| Lundquist field L2 | 3.88586e-02 | 1.29088e-02 | 3.87115e-03 | 1.29035e-03 |
| Lundquist first-order remainder | 1.91989e-03 | 2.12035e-04 | 1.90771e-05 | 2.15532e-06 |
| Lundquist signed q max | 8.63884e-03 | 9.51437e-04 | 8.53196e-05 | 9.35121e-06 |

Field differences from the exact cylinder scale as A^-1 (orders 1.000–1.005).
After subtracting the unfitted first-order correction, orders are 2.000–2.006
(GH) and 1.985–2.006 (Lundquist). Mesh differences decrease separately:
GH orders are 4.59–4.91 on this weak-twist ladder, already below the field target;
Lundquist's 32/64/128 orders are 2.76–3.17, consistent with the expected P3 rate.
The finest-to-public-CHEASE field differences are 4.9e-9–6.5e-9 L2 for GH and
4.0e-7–4.2e-7 for Lundquist, including the CHEASE export uncertainty.
Thus the much larger raw cylinder differences are finite-toroidicity effects.
Signed-q aspect orders are 1.94–2.01, with a sub-target mesh/readback contribution.

Finest producer wall times are 27.6–39.6 s (GH) and 5.18–8.36 s (Lundquist),
including native estimator and contour readback. The solves used separate fixed
cores (GH: 20; Lundquist: 21), one thread each; all native solves stayed below
300 s. Every executable embeds clean KIN6D commit `2d8142a`; copies, tables,
input hashes and outputs are retained beside the registered manifests.
For nonlinear laws the estimator returns status 4: a frozen-source error indicator,
not a qualified nonlinear error bound. No estimator effectivity claim is made.
The historical n=16 Lundquist failures at A=100,300 are fixed on current KIN6D
main. Both exact retained requests now solve and read back successfully; see
[EQ-CYL-2](../../ERRATA.md#eq-cyl-2-kin6d-coarse-p3-readback-failures) and
[coarse replay metrics](kin6d_coarse_readback.csv). Fine-ladder accuracy and
historical timings above keep their original executable pins.

DESC's optimizer success flag does not imply field accuracy. The original
Lundquist L=M=12 states remain above the field target. At A300, L=M=16
reduces total-B L2 to 6.39e-6 but still misses the separate psi and Bpol
targets and exhausts 200 iterations. Another 100 strict iterations barely
change the total-B error (6.36e-6), so relaxing stopping alone is insufficient.

Same-contract native warm refinement to L=M=18 closes the A100/A300 cells:
psi L2 is 3.83e-7/3.45e-7; Bpol L2 is 3.92e-6/3.42e-6 and max
1.43e-5/1.08e-5; Btor L2 is 8.53e-7/7.93e-7. Axis and volume meet 1e-6.
q (1.34e-10/1.36e-10) and Phi (zero discrepancy) check prescribed input
transfer. The strict M18 solves cap at 200/150 iterations, already meeting
all these physical norms. Case-specific gradient tolerances 1e-7/1e-8 then
stop natively in two iterations, with the physical norms rechecked afterward.
These tolerances apply to these cases; they do not change producer defaults.
[Native target controls](desc_target_controls.csv) retain settings and every
PLAN quantity against the same public-CHEASE samples, including its export
uncertainty. A100/A300 M18 warm costs are 168.88/140.71 s plus
57.03/37.98 s for calibrated stopping, on CPU6 with one thread. They include
load/JAX compilation, exclude readback, and supplement the unchanged original
campaign cost curves.

The additional A30 M18 state meets all physical norms. After another 200
iterations at gtol=1e-8 (still capped), psi L2 is 2.14e-7, Bpol L2/max
2.50e-6/6.91e-6, Btor L2 6.56e-7 and axis 1.63e-7. q/Phi transfer and
volume pass. Its measured gradient is 6.55e-8; case-specific gtol=1e-7 accepts
this existing state at iteration zero. This changes stopping qualification,
not physical accuracy; every norm is checked again on the saved native state.
The intermediate control costs 152.01 s and the final stopping check 32.86 s.
A10's M18 axis error remains 1.316e-6 after two 200-iteration controls;
further same-resolution iteration improves it by only 6.3%.
Its warm M18/continuation costs are 122.37/129.51 s; A30 warm M18 costs
166.72 s, on CPU6 with one thread and the same scope as the high-A controls.

A10 refinement to L=M=20 closes its remaining target cell:
axis error falls to 3.91e-7, psi L2 to 1.63e-7, Bpol L2/max to
1.45e-6/4.95e-6 and Btor L2/max to 3.82e-7/1.39e-6. Volume is within
4.44e-16; prescribed q/Phi transfer is within 1.96e-10/zero. The unchanged
pressure/q/Phi/boundary deck uses the retained M18 strict state as its seed.
Case-specific gtol=1e-9 stops natively after 121 iterations (gradient 3.96e-10),
with ftol=xtol=1e-12, maxiter=200. Every physical norm was checked afterward.
The native warm solve costs 156.77 s on CPU6, one thread, including load/JAX
and excluding readback. The original cost curves stay unchanged.
The original caps remain in `runs.csv`/`failures.csv`. The continuation-input
repair is recorded in [EQ-CYL-1](../../ERRATA.md#eq-cyl-1-desc-continuation-and-omitted-zero-modes).

## Signed controls and KIM input

`kim/` contains six native input sets (both families, primary/twist/reversal):
headerless radius/q tables in cm and RH signed q, matching n/Te/Ti/Er grids,
SI reference CSVs, hashes, btor in Gauss and the exact positive-radius B² seed.
R0_KIM=620 cm; the phase map is m_KIM=m, n_KIM=-n. KIM_PERIODIC is radial
periodicity and is not used. The placeholder density is constant, temperatures
are zero, and pressure is zero. These are equilibrium-reader inputs, **not**
a kinetic-response deck.

The existing actual-reader/ODE harness is built from KAMEL/FortNum/FortIO
sources in the lane's disk directory. It reads the delivered inputs without
stubs and compares 63 native points to the exact fields. All six controls pass:
maximum normalized component error 7.38e-15 (GH), 3.46e-10 (Lundquist).
The native KIN6D GH evaluator has error 1.05e-17 for both twist signs and
global reversal. See `native_checks.json`; executable copies, native logs,
source commits and hashes are retained in the registered raw run directories.
The build uses the retained `periodic_cylinder_native_kim_20261008_v2`
CMake project with `-DFORTIO_SOURCE_DIR=/home/ert/code/kin6d/build/_deps/fortio-src`,
`-DCMAKE_BUILD_TYPE=Release`, a disk `-B` directory, and target
`test_native_kim_equilibrium_only` with `-j1`.

VMEC++ and DESC GH A30 controls reverse q with poloidal field, and reverse all field
components with signed toroidal flux; the corresponding field/q readbacks
match their requested symmetry partners exactly at stored precision (`signs.csv`).

## Reproduction and remaining decision

Run from the repository root; set TMPDIR to a disk directory. Existing solver
environments and binary pins are resolved by the Phase 1 environment helper.

```
python -m pytest -q tests/test_phase5.py tests/test_phase1_kin6d_export.py tests/test_phase1_compare.py --basetemp="$TMPDIR/pytest"
python -m equilibrium.phase5.driver --tag UNIQUE --codes chease_public chease_mars
python -m equilibrium.phase5.analyze --tags UNIQUE
python -m equilibrium.phase5.driver --tag UNIQUE --codes vmecpp desc --references equilibrium/phase5/results/references.json
python -m equilibrium.phase5.driver --tag UNIQUE_KIN --codes kin6d --lane "$TMPDIR"
python -m equilibrium.phase5.driver --tag UNIQUE_KIN_FINE --codes kin6d --families lundquist --lane "$TMPDIR" --index 3 --res '{"boundary_nodes":128,"max_area":0.0004631196205784606,"curved":true,"degree":3,"nonlinear_tolerance":1e-11,"quadrature_tolerance":1e-11}'
python -m equilibrium.phase5.kim equilibrium/phase5/results/kim
python -m equilibrium.phase5.native_checks --tag UNIQUE
python -m equilibrium.phase5.analyze --tags cyl20261009_forward cyl20261009_forward2 cyl20261009_vmec cyl20261009_desc cyl20261009_descseed cyl20261009_descseed2 cyl20261009_twist cyl20261009_reversal cyl20261009_kinp3
python -m equilibrium.phase5.plot --output "$TMPDIR/cylinder_kin6d.png"
uv run python ops/run_registry.py
```

The forward-reference index points to the exact retained requests for this
study; a fresh campaign must regenerate it from its own finest forward runs.
Generated plots/PDFs stay outside Git; `artifacts.json` owns their hashes/URLs.
The collection tag `cyl20261009_kinp3` includes the retained historical failures
and the new `_profiles`/`_refine` runs. Fresh tags must be added to `--tags`.
The finite-A KIN6D profile/F/q route is qualified on the successful ladders.
The coarse readback failures are closed by the retained-input replays.
DESC's original capped L=M=16 outputs retain their failure flags; the
additional A30/A100/A300 M18 and A10 M20 controls qualify native stopping
and sampled accuracy. The consumer-path exclusions above still prevent
claiming closure of the entire equilibrium slice.

Chris&AI
