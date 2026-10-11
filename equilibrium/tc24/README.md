# TC24 equilibrium report

Consolidated Phase 6 report for Chris and the TC24 collaborators: exact,
circular, shaped, prescribed-q, received TC24 and cylinder studies, with
native and actual-consumer accuracy and the current defect dispositions.
The report source now includes the completed 11 October accuracy, native-stopping,
consumer and current-cost controls. Scientific slice closure remains open.
The native build regenerates its figures and numerical source-row indexes.

[artifacts.json](artifacts.json) owns the most recently published PDF and figure URLs,
hashes, source revision and reproduction commands. Slopbox links expire after
three days. Generated files stay under ignored `build/`; the committed inputs
and scripts are the durable reproduction path.

## Data and interpretation

- Snapshot: iter_tc24 `d8745dd06`.
  [sources.json](sources.json) pins every imported source, Git blob, SHA256 and
  CSV row count. No solver was rerun for this report.
- KIN6D current main is `648e544`, including curved P2/P3, cubic profiles,
  normalized current, prescribed q, performance and FortNum repairs.
  All 96 CPU and 96 Debug native preset checks pass.
  Every executed study retains its own source/binary pin and timing scope.
- The modx03 normalized-current study is separate from exact supplied-deck
  replay and the historical absolute-psi JINTRAC performance control. Neither
  historical use nor agreement with the finite public comparator proves accuracy.
- Inverse circular KIN6D rows use its own finest reference; historical other-code
  rows use public CHEASE. The figure uses adjacent differences to avoid mixing
  those references. The corrected four-row passing-state selection uses common
  circular references and exact Solovev, with its original timing caveats.
  Comparator zeros are not error measurements.
- [figure_points.csv](data/figure_points.csv) records each plotted point and its
  source row; [table_cells.csv](data/table_cells.csv) records numerical table
  cells and derived rates. Row numbers count CSV data records, excluding headers.
  Input constants are in [parameters.csv](data/parameters.csv).
- The [defect table](data/defects.csv) follows the reconciled ERRATA owner;
  [limitations.csv](data/limitations.csv) separates correct-limit numerical
  effects, model restrictions and unresolved candidates. Remote PR state was
  checked during consolidation; publication does not qualify a solver state.
- Historical circular cost curves retain their original pins. The matched
  five-code table repeats eight selected states three times on CPU7 with one
  numerical thread: 120 native passes and 114 sampled physical passes. The
  six VMEC++ A3.1 misses supply no qualified cost. KIN6D has the lowest
  observed qualified range in every case; this compares selected states under
  background load. Exact-case fresh cold DESC replays appear separately.
- Corrected public CHEASE E2 NS192 passes its physical and declared transfer
  targets. Strict inverse Solovev pressure transfer also passes; MARS coupled
  convergence remains open. Measured consumer projection defects are repaired and their
  geometric approximation limits are qualified separately from equilibrium
  accuracy. Seeded TC24 fields approach a finite NS384 reference whose own
  uncertainty remains material; nonlinear reliability remains open.

## Build and publish

Requirements: Python with NumPy and Matplotlib, plus `latexmk` and pdfLaTeX
with the usual AMS, Latin Modern, geometry, caption, booktabs, longtable and
hyperref packages. Use disk scratch:

```sh
export TMPDIR=/home/ert/code/worktrees/_lanes/consolidate/tmp
bash equilibrium/tc24/build.sh
```

The build regenerates figures, numerical tables and their row indexes before
running `latexmk`. It reads only the retained snapshot. No solver, network
connection or agent/model invocation is part of the build.

To re-create the fixed input snapshot from the owning local clones:

```sh
python equilibrium/tc24/snapshot.py \
  --tc24 /home/ert/code/worktrees/tc24-consolidate --kin6d /home/ert/code/kin6d
```

Changing the data revision is a report revision: update the pin, regenerate,
and reassess statements and scope. Do not relabel historical results as new
measurements. Publish the completed build with the repository's slopbox flow:

```sh
python equilibrium/tc24/publish.py \
  --uploader /home/ert/code/prompts/skills/slopbox/scripts/upload.sh
```

The publisher uploads each PDF separately and writes the artifact manifest.
It leaves the report source and scientific data unchanged. Publication does
not merge a solver fix or promote an equilibrium for perturbation use.

Chris&AI
