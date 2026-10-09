#!/usr/bin/env python3
"""Render report figures from the frozen CSVs, with a row index for every point."""
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
OUT = HERE / "build"
CODES = ["kin6d", "chease_public", "chease_mars", "vmecpp", "desc"]
LABELS = dict(zip(CODES, ["KIN6D", "CHEASE public", "CHEASE MARS", "VMEC++", "DESC"]))
COLORS = dict(zip(CODES, ["#176b43", "#2166ac", "#b36a12", "#9b3d89", "#bc3939"]))
POINTS = []


def read(path):
    with (DATA / path).open() as f:
        return [dict(r, _file=path, _row=i) for i, r in enumerate(csv.DictReader(f), 1)]


def yes(value):
    return str(value).lower() in {"true", "1", "1.0"}


def draw(ax, rows, xkey, ykey, figure, panel, label, color, **kwargs):
    points = []
    for r in rows:
        x, y = float(r[xkey]), float(r[ykey])
        if np.isfinite(x) and np.isfinite(y) and x > 0 and y > 0:
            points.append((x, y, r))
            POINTS.append(dict(figure=figure, panel=panel, series=label, x=x, y=y,
                               source=r['_file'], data_row=r['_row'], x_column=xkey,
                               y_column=ykey, transform=r.get('_transform', 'identity')))
    if points:
        points.sort(key=lambda p: p[0])
        ax.loglog([p[0] for p in points], [p[1] for p in points],
                  label=label, color=color, marker="o", markersize=3, linewidth=1.2, **kwargs)


def finish(fig, name, handles=None, labels=None):
    if handles is None:
        handles, labels = fig.axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=3, frameon=False,
               bbox_to_anchor=(.5, 1), fontsize=8)
    fig.tight_layout(rect=(0, 0, 1, .90 if len(fig.axes) <= 4 else .94))
    fig.savefig(OUT / f"{name}.pdf", metadata={"CreationDate": None, "ModDate": None})
    plt.close(fig)


def style(ax, xlabel, ylabel, target=None):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, which="major", color=".88", linewidth=.5)
    if target:
        ax.axhline(target, color=".45", linestyle=":", linewidth=.8)


def exact():
    for case, title in [("solovev_lcfs_A3", "A3 exact LCFS"),
                        ("solovev_cerfon_iter", "Cerfon exact LCFS")]:
        name = "exact_" + ("a3" if "A3" in case else "cerfon")
        rows = read(f"phase1/results/{case}.csv")
        fig, axes = plt.subplots(2, 2, figsize=(7, 4.6))
        for i, (metric, title_y, target) in enumerate(
                [("psi_l2", r"Relative $\psi$ $L^2$ error", 1e-6),
                 ("bpol_l2", r"Relative $B_{pol}$ $L^2$ error", 1e-5)]):
            for j, (x, title_x) in enumerate([("dof", "Producer DOF"), ("wall_s", "Recorded producer time [s]")]):
                ax = axes[i, j]
                for code, degree in [('kin6d', 2), ('kin6d', 3)] + [(c, None) for c in CODES[1:]]:
                    selected = [r for r in rows if r['code'] == code and yes(r['native_converged'])
                                and (degree is None or json.loads(r['resolution']).get('degree', 2) == degree)]
                    draw(ax, selected, x, metric, name, f"{i},{j}",
                         LABELS[code] + (f" P{degree}" if degree else ''),
                         '#559e88' if degree == 2 else COLORS[code], linestyle='--' if degree == 2 else '-')
                style(ax, title_x, title_y, target)
        finish(fig, name)


def toroidal(phase, cases, name):
    references = {r['case']: r for r in read(f"{phase}/results/reference_errors.csv")}
    fig, axes = plt.subplots(len(cases), 2, figsize=(7, 8.4 if len(cases) == 4 else 4.7))
    for i, case in enumerate(cases):
        rows = read(f"{phase}/results/{case}.csv")
        for j, (x, xlabel) in enumerate([("dof", "Producer DOF"), ("wall_s", "Producer time [s]")]):
            ax = axes[i, j]
            for code in CODES:
                chosen = [dict(r) for r in rows if r['code'] == code]
                for r in chosen:
                    if code == 'kin6d' and float(r['bpol_l2']) == 0:
                        ref = references[case]
                        r['bpol_l2'] = ref['bpol_richardson']
                        r['_transform'] = f"reference Richardson: {ref['_file']} row {ref['_row']}"
                good = [r for r in chosen if yes(r['native_converged'])]
                bad = [r for r in chosen if not yes(r['native_converged'])]
                draw(ax, good, x, 'bpol_l2', name, case + ':' + x, LABELS[code], COLORS[code])
                # A cross denotes a finite result that failed native stopping.
                for r in bad:
                    draw(ax, [r], x, 'bpol_l2', name, case + ':' + x, '_nolegend_', COLORS[code], linestyle='None')
                    ax.plot(float(r[x]), float(r['bpol_l2']), 'x', color=COLORS[code], ms=7)
            ax.set_title(case.replace('_', ' / ').replace('3p1', '3.1'), fontsize=9)
            style(ax, xlabel, r"$B_{pol}$ relative $L^2$ difference", 1e-5)
    finish(fig, name)


def physics():
    rows = read('phase2/results/physics.csv')
    fig, axes = plt.subplots(1, 2, figsize=(7, 3.2))
    for law, color in [('E1', COLORS['chease_public']), ('E2', COLORS['chease_mars'])]:
        selected = [dict(r) for r in rows if r['case'].startswith(law) and float(r['aspect_ratio']) >= 10]
        for r in selected:
            r['epsilon'] = 1 / float(r['aspect_ratio'])
            for key in ['shift_leading_difference', 'q_difference']:
                r[key] = abs(float(r[key]))
            r['_transform'] = 'x=1/aspect_ratio; y=absolute difference'
        for ax, key, title in zip(axes, ['shift_leading_difference', 'q_difference'],
                                   [r"$|\Delta/a-(\Delta/a)_{leading}|$", r"$|q(0)-q_{quadratic}|$"]):
            draw(ax, selected, 'epsilon', key, 'large_aspect', key, law, color)
            if key == 'q_difference':
                ax.errorbar([r['epsilon'] for r in selected], [r[key] for r in selected],
                            yerr=[abs(float(r['q_last_refinement'])) for r in selected],
                            fmt='none', color=color, capsize=3, linewidth=.8)
                for r in selected:
                    POINTS.append(dict(figure='large_aspect', panel=key, series=law + ' last-mesh change',
                                       x=r['epsilon'], y=abs(float(r['q_last_refinement'])),
                                       source=r['_file'], data_row=r['_row'], x_column='aspect_ratio',
                                       y_column='q_last_refinement', transform='x=1/A; y=absolute error-bar half-length'))
            style(ax, r"$1/A$", title)
    finish(fig, 'large_aspect')


def exports():
    allrows = read('phase1/results_export/summary.csv')
    # Final converter rows only: omit superseded scan/harmonic experiments.
    rows = [r for r in allrows if r['tag'].startswith('export_e2e2_final_') or r['tag'].startswith('readers_')]
    paths = [('native', 'Native'), ('fortran', 'EQDSK'), ('boozer_libneo_python', 'Boozer'),
             ('gpec_direct', 'GPEC'), ('neo2_full', 'NEO-2')]
    fig, axes = plt.subplots(2, 2, figsize=(7, 4.8))
    for i, case in enumerate(['solovev_lcfs_A3', 'solovev_cerfon_iter']):
        for j, higher in enumerate([False, True]):
            ax = axes[i, j]
            for variant, code in [('kin6d', 'kin6d'), ('public', 'chease_public'), ('mars', 'chease_mars')]:
                points = []
                for k, (path, _) in enumerate(paths):
                    subset = [r for r in rows if r['case'] == case and r['variant'] == variant and r['path'] == path]
                    if not subset:
                        raise ValueError((case, variant, path))
                    r = dict(sorted(subset, key=lambda r: int(r['n']))[-1 if higher else 0])
                    field = 'combined_bpol_l2' if path == 'boozer_libneo_python' else 'bpol_l2'
                    y = float(r[field]); points.append(y)
                    POINTS.append(dict(figure='consumer_exact', panel=f'{i},{j}', series=LABELS[code],
                                       x=k, y=y, source=r['_file'], data_row=r['_row'],
                                       x_column='path', y_column=field, transform='categorical path'))
                ax.semilogy(range(len(paths)), points, 'o-', color=COLORS[code], label=LABELS[code], markersize=4)
            ax.set_xticks(range(len(paths)), [p[1] for p in paths])
            ax.set_title(('A3' if i == 0 else 'Cerfon') + (' / finer producer' if higher else ' / coarser producer'), fontsize=9)
            style(ax, '', r"Relative $B_{pol}$ $L^2$ error", 1e-5)
    finish(fig, 'consumer_exact')


def cylinder():
    fine = read('phase5/results/finest.csv'); resolution = read('phase5/results/resolution.csv')
    fig, axes = plt.subplots(2, 2, figsize=(7, 4.9))
    for i, family in enumerate(['gold_hoyle', 'lundquist']):
        for code in CODES:
            sel = [r for r in fine if r['code'] == code and r['family'] == family and yes(r['native_converged']) and r['twist'] == '1' and r['reversal'] == '1']
            draw(axes[i, 0], sel, 'aspect', 'B_rel_L2', 'cylinder', family + ':aspect', LABELS[code], COLORS[code])
            sel = [r for r in resolution if r['code'] == code and r['family'] == family and r['aspect'] == '10' and r['twist'] == '1' and r['reversal'] == '1']
            draw(axes[i, 1], sel, 'dof', 'B_discretization_difference', 'cylinder', family + ':resolution', LABELS[code], COLORS[code])
        remainder = [r for r in fine if r['code'] == 'chease_public' and r['family'] == family and r['twist'] == '1' and r['reversal'] == '1']
        draw(axes[i, 0], remainder, 'aspect', 'B_first_order_remainder', 'cylinder', family + ':aspect', 'Public: first-order remainder', '.25', linestyle='--')
        axes[i, 0].set_title(family.replace('_', ' ').title(), fontsize=9)
        axes[i, 1].set_title('A = 10; adjacent resolutions', fontsize=9)
        style(axes[i, 0], 'Aspect ratio A', 'Field difference from cylinder')
        style(axes[i, 1], 'Coarser producer DOF', 'Adjacent field difference')
    finish(fig, 'cylinder')


def inverse():
    rows = read('phase3/results/comparison.csv') + read('phase3/results/kin6d_comparison.csv')
    pairs = read('phase3/results/self_convergence.csv') + read('phase3/results/kin6d_self_convergence.csv')
    cases = ['E1_constant_q_A10','E2_constant_q_A10','Solovev_inverse_A3']
    fig, axes = plt.subplots(3,2,figsize=(7,7.1))
    for i,case in enumerate(cases):
        for j,(x,label) in enumerate([('dof','Finer producer DOF'),('wall_s','Finer producer time [s]')]):
            for code in ['kin6d','chease_public','vmecpp','desc']:
                series=[]
                for r in pairs:
                    if (r['case'],r['code'])!=(case,code): continue
                    run=next(v for v in rows if (v['case'],v['code'],v['level'])==(case,code,r['level']))
                    series.append(dict(r,**{x:run[x]},_transform=f"adjacent-state difference; {x} from {run['_file']}:{run['_row']}"))
                draw(axes[i,j],series,x,'bpol_l2','inverse',case+':'+x,LABELS[code],COLORS[code])
            axes[i,j].set_title(case.replace('_',' / '),fontsize=9)
            style(axes[i,j],label,r'Adjacent $B_{pol}$ relative $L^2$ difference')
    finish(fig,'inverse')


def tc24():
    rows=read('phase4/tc24/reference/comparison.csv')
    rows=[r for r in rows if r['name']=='reference' and yes(r['native_converged']) and yes(r['readback_complete'])]
    fig,axes=plt.subplots(2,2,figsize=(7,4.8))
    for i,(metric,ylabel,target) in enumerate([('psi_l2',r'Relative $\psi$ difference',1e-6),('bpol_l2',r'Relative $B_{pol}$ difference',1e-5)]):
        for j,(x,label) in enumerate([('dof','Producer DOF'),('wall_s','Producer time [s]')]):
            for code in CODES:
                draw(axes[i,j],[r for r in rows if r['code']==code],x,metric,'tc24',f'{i},{j}',LABELS[code],COLORS[code])
            style(axes[i,j],label,ylabel,target)
    finish(fig,'tc24')


def main():
    OUT.mkdir(exist_ok=True)
    plt.rcParams.update({'font.size': 8, 'axes.spines.top': False, 'axes.spines.right': False,
                         'pdf.fonttype': 42, 'font.family': 'DejaVu Sans'})
    exact()
    for law in ['E1', 'E2']:
        toroidal('phase2', [f'{law}_A{a}' for a in ['40', '20', '10', '3p1']], 'circular_' + law.lower())
    toroidal('phase4', ['E4_E1', 'E4_E2'], 'shaped')
    physics(); exports(); cylinder(); inverse(); tc24()
    with (DATA / 'figure_points.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(POINTS[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(POINTS)
    print(f"Ten figures; {len(POINTS)} plotted points indexed by source CSV and data row.")


if __name__ == '__main__':
    main()
