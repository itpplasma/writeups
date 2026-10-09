# TC24 equilibrium report

First complete Phase 6 draft for Chris and later the TC24 collaborators. The
[LaTeX source](report.tex) covers the exact, circular, E4 and cylinder studies,
actual export/consumer accuracy, the live defect ledger and classified limits.
Phase 3 inverse and Phase 4b actual TC24 have explicit placeholders. This draft
does not close the equilibrium slice.

The [artifact manifest](artifacts.json) owns the uploaded report and eight
figure URLs, hashes, expiry and build commands. PDFs and plots are generated
under ignored `build/` and are never committed. Slopbox links expire after
three days; regenerate from this source and the retained numerical data.

## Data and interpretation

- Primary snapshot: iter_tc24 `916dc6d9da0ca843d6b4a6d67b46e62ff37ef94e`.
  [sources.json](sources.json) pins every imported source with its Git blob,
  SHA256 and CSV row count. These are project-authored data and context; no
  third-party solver source or literature PDF is imported or relicensed.
- The refreshed Phase 1 CSVs contain KIN6D P2 **and P3**, at `fa5c388`.
  Their older README describes an earlier P2-only comparison. Figure series
  and rate fits use the executed degree, never a mixture of the two ladders.
- The older KIN6D owner study, committed at `3c851d7`, extends P2 to finer
  meshes. Its table is explicitly separate from the refreshed common study.
- Circular cost CSVs predate the later FortNum Brent repair. The report records
  the repair and retains those historical timings; it does not promote the
  later speed claim without a refreshed committed comparison CSV.
- [figure_points.csv](data/figure_points.csv) indexes every plotted point and
  error bar; [table_cells.csv](data/table_cells.csv) indexes numerical table
  cells and derived rates. `data_row` counts CSV records from one, excluding
  the header. Tables distinguish passing selections from finest failing states.
- [defects.csv](data/defects.csv) preserves every live ledger row, its recorded
  status and the report disposition. Dated PR-index supersessions are applied;
  this is not a live remote-state audit. The KIN6D integration history is pinned
  separately. [limitations.csv](data/limitations.csv) retains the cause classes.
- Native stopping, sampled physical accuracy, prescribed-profile transfer and
  actual consumer coverage are separate. Raw runs and their input/binary hashes
  remain at the registered TC24 owners; no solver was rerun for this report.

## Build and publish

Requirements: Python with NumPy and Matplotlib, plus `latexmk` and pdfLaTeX
with the usual AMS, Latin Modern, geometry, caption, booktabs, longtable and
hyperref packages. Use disk scratch:

```sh
export TMPDIR=/home/ert/code/worktrees/_lanes/report/tmp
bash equilibrium/tc24/build.sh
```

The build regenerates figures, numerical tables and their row indexes before
running `latexmk`. It reads only the retained snapshot. No solver, network
connection or agent/model invocation is part of the build.

To re-create the fixed input snapshot from the owning local clones:

```sh
python equilibrium/tc24/snapshot.py \
  --tc24 /home/ert/code/worktrees/tc24-report --kin6d /home/ert/code/kin6d
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
