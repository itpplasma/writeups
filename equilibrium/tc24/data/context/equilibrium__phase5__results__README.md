# Phase 5: periodic-cylinder limit

This is the C0 Gold–Hoyle/Lundquist field and signed-q comparison at
A=10,30,100,300, plus exact-cylinder KIM equilibrium ingress. The KIN6D P3
finite-A cell is **blocked by unsupported profile laws**. Its exact Gold–Hoyle
evaluator is reported separately and is not a PDE convergence result.

Figure: [PNG](https://box.sloppy.at/79392.png), [PDF](https://box.sloppy.at/b5059.pdf).
The registry contains 122 lane executions: 117 completed and five retained
failures. The comparison CSV has 106 result rows, including two native
iteration-cap outputs; 104 report native convergence. The 27 selected Python
tests pass, including the failing-before/passing-after producer regression.

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
| KIN6D P3 | Requested `build/gs_phase1` and Phase 1 producer | Producer rejects nonconstant sources; `gs_profile_load` also explicitly rejects P3/mapped geometry. Both families have retained failed requests. No Lundquist/cylinder PDE route demonstrated |
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

There are 512 fixed off-grid points on 0.05≤r/a≤0.90, with radial area weights.
q uses 101 points on 0.05≤s_tor≤0.98 and includes the canonical sign. Native
VMEC++/DESC fields and CHEASE **exported-and-read-back** EQDSK fields are named
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

DESC's optimizer success flag does not imply field accuracy: Lundquist at
L=M=4 or 6 still has significant discretization error. The additional spectral
refinement is retained rather than treating that flag as an accuracy gate.
At L=M=12, the DESC-to-public-CHEASE field differences are 1.15e-4–1.97e-4
(L2). The A300 cold L=M=16 result reduces this to 6.39e-6 L2 and 1.68e-5 max,
but hits 200 iterations. A repeat initialized by a native L=M=12 solve also
hits 200 iterations (1.06e-5 L2). Both stay marked `native_converged=false`
and are excluded from the finest-converged curves, while remaining in
`runs.csv`/`failures.csv`. This demonstrates decreasing discretization error;
it does not close DESC's stopping-criterion qualification for this strong-twist
case. `B_to_public_L2/max` use the same physical points and include the
CHEASE reference/export uncertainty (adjacent-resolution L2 difference ~1e-7).
The continuation-input defect found during this check is fixed locally:
[EQ-CYL-1](../../ERRATA.md#eq-cyl-1-desc-continuation-and-omitted-zero-modes).

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
python -m pytest -q tests/test_phase5.py --basetemp="$TMPDIR/pytest"
python -m equilibrium.phase5.driver --tag UNIQUE --codes chease_public chease_mars
python -m equilibrium.phase5.analyze --tags UNIQUE
python -m equilibrium.phase5.driver --tag UNIQUE --codes vmecpp desc --references equilibrium/phase5/results/references.json
python -m equilibrium.phase5.kim equilibrium/phase5/results/kim
python -m equilibrium.phase5.native_checks --tag UNIQUE
python -m equilibrium.phase5.analyze --tags cyl20261009_forward cyl20261009_forward2 cyl20261009_vmec cyl20261009_desc cyl20261009_descseed cyl20261009_descseed2 cyl20261009_twist cyl20261009_reversal cyl20261009_kinp3
python -m equilibrium.phase5.plot --output "$TMPDIR/cylinder.png"
uv run python ops/run_registry.py
```

The forward-reference index points to the exact retained requests for this
study; a fresh campaign must regenerate it from its own finest forward runs.
Generated plots/PDFs stay outside Git; `artifacts.json` owns their hashes/URLs.
KIN6D P3 still needs generic curved-P3 nonlinear profile loading and matching
F/q readback before the requested five-code Phase 5 comparison is complete.
That is the controller's remaining implementation decision; analytic evaluator
success does not close it. DESC's two capped L=M=16 outputs also remain
unqualified as converged native solves. No solver-result defect is claimed from unsupported
geometry/profile combinations.

Chris&AI
