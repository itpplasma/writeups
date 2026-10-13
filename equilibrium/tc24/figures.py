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
# Okabe--Ito palette; exact-case series also use distinct markers/line styles.
COLORS = dict(zip(CODES, ["#009E73", "#0072B2", "#E69F00", "#CC79A7", "#D55E00"]))
MARKERS = dict(zip(CODES, ["o", "s", "^", "v", "P"]))
POINTS = []


def read(path):
    with (DATA / path).open() as f:
        return [dict(r, _file=path, _row=i) for i, r in enumerate(csv.DictReader(f), 1)]


def yes(value):
    return str(value).lower() in {"true", "1", "1.0"}


def draw(ax, rows, xkey, ykey, figure, panel, label, color, point_label=None, **kwargs):
    points = []
    for r in rows:
        x, y = float(r[xkey]), float(r[ykey])
        if np.isfinite(x) and np.isfinite(y) and x > 0 and y > 0:
            points.append((x, y, r))
            POINTS.append(dict(figure=figure, panel=panel, series=point_label or label, x=x, y=y,
                               source=r['_file'], data_row=r['_row'], x_column=xkey,
                               y_column=ykey, transform=r.get('_transform', 'identity')))
    if points:
        points.sort(key=lambda p: p[0])
        ax.loglog([p[0] for p in points], [p[1] for p in points],
                  label=label, color=color, marker=kwargs.pop("marker", next((MARKERS[c] for c in CODES if label == LABELS[c]), "o")), markersize=3, linewidth=1.2, **kwargs)


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
        cold = [dict(r, wall_s=r["producer_s"]) for r in read("phase1/results/desc_cold_cost.csv")
                if r["case"] == case and yes(r["qualified"])]
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
                         COLORS[code], linestyle='--' if degree == 2 else '-',
                         marker='x' if degree == 2 else MARKERS[code])
                for r in cold:
                    r["_transform"] = "wall_s=producer_s; fresh cold target-passing replay"
                draw(ax, cold, x, metric, name, f"{i},{j}", "DESC cold target replay",
                     COLORS["desc"], linestyle="None", marker="D")
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
                ax.semilogy(range(len(paths)), points, marker=MARKERS[code], color=COLORS[code], label=LABELS[code], markersize=4)
            ax.set_xticks(range(len(paths)), [p[1] for p in paths])
            ax.set_title(('A3' if i == 0 else 'Cerfon') + (' / finer producer' if higher else ' / coarser producer'), fontsize=9)
            style(ax, '', r"Relative $B_{pol}$ $L^2$ error", 1e-5)
    finish(fig, 'consumer_exact')


def ladder_consumers(phase, cases, name, figsize):
    exports = read(f'{phase}/results/exports.csv')
    states = {}
    for case in cases:
        for state in read(f'{phase}/results/{case}.csv'):
            key = case, state['code'], int(float(state['dof']))
            if key in states:
                raise ValueError(f'duplicate producer state for native-stop join: {key}')
            states[key] = state

    nrows = (len(cases) + 1) // 2
    fig, axes = plt.subplots(nrows, 2, figsize=figsize, sharex=True, sharey=True,
                             squeeze=False)
    for i, case in enumerate(cases):
        ax = axes.flat[i]
        for code in CODES[:3]:
            native_path = 'FE' if code == 'kin6d' else 'NOUT'
            for path, path_label, linestyle in [
                    (native_path, 'native', '-'),
                    ('EQDSK_libneo', 'EQDSK/libneo', '--')]:
                selected = []
                failed = []
                for row in exports:
                    if (row['case'], row['code'], row['path']) != (case, code, path):
                        continue
                    state = states[(case, code, int(float(row['dof'])))]
                    item = dict(row)
                    status = 'passed native stopping' if yes(state['native_converged']) else 'failed native stopping'
                    item['_transform'] = (
                        f'{path}; {status} per {state["_file"]} row {state["_row"]}; '
                        'relative to the case KIN6D reference on its physical-point grid')
                    (selected if yes(state['native_converged']) else failed).append(item)
                label = f'{LABELS[code]} {path_label}'
                draw(ax, selected, 'dof', 'bpol_l2', name, case, label,
                     COLORS[code], marker=MARKERS[code], linestyle=linestyle)
                # Retain finite output from failed producer stops as crosses,
                # while keeping them out of the qualified refinement line.
                for item in failed:
                    draw(ax, [item], 'dof', 'bpol_l2', name, case, '_nolegend_',
                         COLORS[code], point_label=f'{LABELS[code]} {path_label} failed-stop',
                         marker='x', linestyle='None')
        if phase == 'phase2':
            law, aspect = case.split('_')
            aspect = '3.1' if aspect == 'A3p1' else aspect[1:]
            title = f'{law}, A={aspect}'
        else:
            title = "E4 E1 ($p'=0$)" if case == 'E4_E1' else "E4 E2 ($FF'=0$)"
        ax.set_title(title, fontsize=9)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.grid(True, which='major', color='.86', linewidth=.5)
        ax.grid(True, which='minor', color='.94', linewidth=.35)
        if i % 2:
            ax.tick_params(labelleft=False)
    for ax in axes.flat[len(cases):]:
        ax.set_visible(False)
    fig.supxlabel('Producer DOF')
    fig.supylabel(r'Relative $B_{pol}$ $L^2$ difference', x=.012)
    handles, labels = axes.flat[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=3, frameon=False,
               bbox_to_anchor=(.5, .995), fontsize=7.5)
    fig.tight_layout(rect=(.10, .06, .99, .90))
    fig.savefig(OUT / f'{name}.pdf', metadata={'CreationDate': None, 'ModDate': None})
    plt.close(fig)


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


def cylinder_time():
    runs = read('phase5/results/runs.csv')
    pairs = read('phase5/results/resolution.csv')
    families = [('gold_hoyle', 'Gold–Hoyle'), ('lundquist', 'Lundquist')]
    aspects = [10, 30, 100, 300]
    fig, axes = plt.subplots(len(aspects), 2, figsize=(7, 8.1),
                             sharex=True, sharey=True)
    for i, aspect in enumerate(aspects):
        for j, (family, family_label) in enumerate(families):
            ax = axes[i, j]
            for code in CODES:
                selected = []
                for pair in pairs:
                    if (pair['code'] != code or pair['family'] != family
                            or float(pair['aspect']) != aspect
                            or pair['twist'] != '1' or pair['reversal'] != '1'):
                        continue
                    fine_n = int(float(pair['next_n']))
                    candidates = [r for r in runs
                                  if r['code'] == code and r['family'] == family
                                  and float(r['aspect']) == aspect
                                  and r['twist'] == '1' and r['reversal'] == '1'
                                  and int(float(r['n'])) == fine_n
                                  and yes(r['native_converged'])]
                    if len(candidates) != 1:
                        raise ValueError(
                            f"expected one converged finer run for {family} A={aspect} "
                            f"{code} n={fine_n}, found {len(candidates)}")
                    # The fine-state producer time is paired with the existing
                    # adjacent-resolution field difference; no time is summed.
                    fine = candidates[-1]
                    selected.append(dict(
                        pair,
                        wall_s=fine['wall_s'],
                        _transform=(
                            f"adjacent n={pair['n']} to {pair['next_n']}; "
                            f"wall_s from {fine['_file']} row {fine['_row']}"),
                    ))
                draw(ax, selected, 'wall_s', 'B_discretization_difference',
                     'cylinder_time', f'{family}:A{aspect}', LABELS[code],
                     COLORS[code])
            ax.set_title(f'{family_label}, A={aspect}', fontsize=9)
            style(ax, '', '')
            if i == len(aspects) - 1:
                ax.set_xlabel('Finer-run producer wall time [s]')

    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=5, frameon=False,
               bbox_to_anchor=(.5, .99), fontsize=8)
    fig.supylabel(r'Adjacent relative field $L^2$ change', x=.012)
    fig.tight_layout(rect=(.08, .03, .99, .94))
    fig.savefig(OUT / 'cylinder_time.pdf',
                metadata={'CreationDate': None, 'ModDate': None})
    plt.close(fig)


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
    """Three panels: KIN6D self-convergence, comparator ladder, code differences with comparator floor."""
    ref = 'phase4/tc24/reference/'
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 3.1))
    # (a) KIN6D, current fixed-quadrature binary: successive differences and Richardson estimates.
    ax = axes[0]
    kin = read(ref + 'kin6d_refinement.csv')[:3]
    nn = [float(r['boundary_nodes']) for r in kin]
    for key, rate_key, name, col, mk in [('bpol_l2', 'generalized_bpol_rate', r'$B_{pol}$', '#0072B2', 'o'),
                                         ('psi_l2', 'generalized_psi_rate', r'$\psi$', '#D55E00', 's')]:
        adj = 'adjacent_' + key
        pts = [(float(r['boundary_nodes']), float(r[adj]), r) for r in kin if r[adj]]
        p = float(kin[2][rate_key])
        ratio = nn[2] / nn[1]
        e384 = pts[-1][1] / (ratio ** p - 1.0)
        rich = [(n, e384 * (nn[2] / n) ** p) for n in nn]
        for x, y, r in pts:
            record('tc24', '0', name + ' successive difference', x, y, r, 'boundary_nodes', adj)
        ax.loglog([x for x, _, _ in pts], [y for _, y, _ in pts], marker=mk, color=col, markersize=4,
                  linewidth=1.2, label=name + ' successive diff.')
        for (n, e), r in zip(rich, kin):
            POINTS.append(dict(figure='tc24', panel='0', series=name + ' Richardson error estimate', x=n, y=e,
                               source=r['_file'], data_row=r['_row'], x_column='boundary_nodes', y_column=adj,
                               transform=f'Richardson, p={p:.3f}, successive difference n320-n384'))
        ax.loglog([n for n, _ in rich], [e for _, e in rich], marker=mk, color=col, markerfacecolor='white',
                  markersize=4, linewidth=.8, linestyle='--', label=name + ' Richardson error')
        if key == 'bpol_l2':
            x0, y0 = pts[-1][0], pts[-1][1]
            xs = np.array([nn[0] * .97, nn[2] * 1.03])
            for q, ls in [(3, ':'), (4, '-.')]:
                ax.loglog(xs, y0 * (xs / x0) ** (-q) * 2.2, color='.4', linestyle=ls, linewidth=.8,
                          label=f'slope $p={q}$')
    style(ax, 'KIN6D boundary nodes $n$', r'Relative $L^2$ self-difference')
    ax.set_title('(a) KIN6D self-convergence', fontsize=8)
    ax.set_xticks([256, 320, 384]); ax.set_xticklabels(['256', '320', '384']); ax.minorticks_off()
    ax.set_ylim(3e-7, 3e-2)
    ax.legend(frameon=False, fontsize=5, loc='upper right')
    # (b) Public CHEASE ladder: differences to NS128 (NS16-64), successive differences above.
    ax = axes[1]
    hist = [r for r in read(ref + 'comparison_historical.csv') if r['name'] == 'reference'
            and r['code'] == 'chease_public' and float(r['bpol_l2']) > 0]
    unc = read(ref + 'reference_uncertainty.csv')[:1] + read(ref + 'reference_uncertainty_n320.csv')[2:3] + \
        read(ref + 'reference_uncertainty_n384.csv')[:1] + read(ref + 'reference_uncertainty_n512.csv')[:1]
    ns_fin = [256, 320, 384, 512]
    for key, col, mk, name in [('bpol_l2', '#0072B2', 'o', r'$B_{pol}$'), ('psi_l2', '#D55E00', 's', r'$\psi$')]:
        for r in hist:
            record('tc24', '1', name + ' vs NS128', float(r['ns']), float(r[key]), r, 'ns', key)
        for n, r in zip(ns_fin, unc):
            record('tc24', '1', name + ' successive', n, float(r[key]), r, 'comparison', key)
        ax.loglog([float(r['ns']) for r in hist], [float(r[key]) for r in hist], marker=mk, color=col,
                  markersize=4, linewidth=1.2, markerfacecolor='white', label=name + ' vs NS128')
        ax.loglog(ns_fin, [float(r[key]) for r in unc], marker=mk, color=col, markersize=4,
                  linewidth=1.2, label=name + ' successive NS')
    xs = np.array([16., 512.])
    ax.loglog(xs, 0.03 * (xs / 16) ** (-1.87), color='.4', linestyle=':', linewidth=.8, label='order 1.87')
    style(ax, 'Public CHEASE NS', 'Relative $L^2$ difference')
    ax.set_title('(b) public CHEASE ladder', fontsize=8)
    ax.set_xticks([16, 32, 64, 128, 256, 512]); ax.set_xticklabels(['16', '32', '64', '128', '256', '512'])
    ax.minorticks_off(); ax.set_ylim(3e-8, 3e-1)
    ax.legend(frameon=False, fontsize=5, loc='upper right')
    # (c) Code differences from the NS128 comparator; shading = comparator's own error.
    ax = axes[2]
    rows = [r for r in read(ref + 'comparison_historical.csv') if r['name'] == 'reference'
            and yes(r['native_converged']) and yes(r['readback_complete'])]
    for code in CODES:
        if code != 'chease_public':
            draw(ax, [r for r in rows if r['code'] == code], 'dof', 'bpol_l2', 'tc24', '2',
                 LABELS[code], COLORS[code])
    floor_row = unc[0]
    floor = float(floor_row['bpol_l2'])
    record('tc24', '2', 'NS128 error floor', 1e3, floor, floor_row, 'comparison', 'bpol_l2')
    ax.axhspan(1e-9, floor, color='.85', zorder=0)
    ax.axhline(floor, color='.4', linewidth=.8)
    ax.text(1.5e3, floor * .8, 'NS128 error\n(NS128 vs NS256)', fontsize=5.5, va='top')
    ax.set_ylim(1e-5, 5e-2)
    ax.legend(frameon=False, fontsize=5.5, loc='upper right')
    style(ax, 'Producer DOF', r'Relative $B_{pol}$ difference', 1e-5)
    ax.set_title('(c) differences vs NS128', fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / 'tc24.pdf', metadata={"CreationDate": None, "ModDate": None})
    plt.close(fig)


OCT13 = "tc24_20261013"
COLORS_13 = dict(COLORS, gvec="#56B4E9")
LABELS_13 = dict(LABELS, gvec="GVEC")
MARKERS_13 = dict(MARKERS, gvec="D")


def record(figure, panel, series, x, y, r, xkey, ykey):
    POINTS.append(dict(figure=figure, panel=panel, series=series, x=x, y=y, source=r['_file'],
                       data_row=r['_row'], x_column=xkey, y_column=ykey, transform='identity'))


def tc24_ns640():
    """TC24 cell against public CHEASE NS640; filled = native stop, open = no native stop."""
    rows = [r for r in read(f'{OCT13}/tc24_ns640.csv') if r['status'] != 'pending'
            and r['status'] != 'control' and r['wall_s']]
    fig, axes = plt.subplots(1, 2, figsize=(7, 3.1))
    for j, (metric, ylabel, target) in enumerate([('bpol_l2', r'Relative $B_{pol}$ $L^2$ vs NS640', 1e-5),
                                                   ('q_max', r'Max relative $q$ vs NS640', 1e-5)]):
        ax = axes[j]
        for code in ['kin6d', 'chease_public', 'chease_mars', 'vmecpp', 'desc', 'gvec']:
            sel = [r for r in rows if r['code'] == code and r[metric]]
            # q is a prescribed-iota readback for DESC (8.6e-8 by construction): not a solver error.
            if code == 'desc' and metric == 'q_max':
                continue
            for stop in [True, False]:
                pts = sorted([r for r in sel if yes(r['native_stop']) == stop], key=lambda r: float(r['wall_s']))
                if not pts:
                    continue
                for r in pts:
                    record('tc24_ns640', f'0,{j}', LABELS_13[code], float(r['wall_s']), float(r[metric]),
                           r, 'wall_s', metric)
                ax.loglog([float(r['wall_s']) for r in pts], [float(r[metric]) for r in pts],
                          # Only the single-thread CHEASE ladders are joined; other points differ in threads/settings.
                          linestyle='-' if stop and code.startswith('chease') else 'none',
                          marker=MARKERS_13[code], markersize=4, linewidth=1.0, color=COLORS_13[code],
                          markerfacecolor=COLORS_13[code] if stop else 'white',
                          label=LABELS_13[code] if stop else None)
        style(ax, 'Recorded wall time [s] (thread counts differ)', ylabel, target)
    axes[0].plot([], [], marker='o', color='.3', markerfacecolor='white', linestyle='none',
                 label='no native stop / folded')
    finish(fig, 'tc24_ns640')


def edge_scan():
    """GPEC n=3 resonant flux versus edge treatment."""
    rows = read(f'{OCT13}/gpec_edge_scan.csv')
    order = ['0.990', '0.995', '0.997', '0.999', 'full']
    fig, axes = plt.subplots(1, 2, figsize=(7, 2.9), sharey=True)
    qs = [('3.0', 'q=3', '#0072B2', 'o'), ('3.333', 'q=10/3', '#E69F00', 's'), ('3.667', 'q=11/3', '#D55E00', '^')]
    for j, (ph, title) in enumerate([('000', '(0,0,0)'), ('010', r'(0,$\pi$,0)')]):
        ax = axes[j]
        for q, lab, col, mk in qs:
            xs, ys, lo, hi = [], [], [], []
            for i, cut in enumerate(order):
                sel = [r for r in rows if r['phasing'] == ph and r['q'] == q and r['cut'].startswith(cut)]
                if not sel:
                    continue
                vals = [float(r['singflx_T']) for r in sel]
                for r in sel:
                    record('edge_scan', f'0,{j}', lab, i, float(r['singflx_T']), r, 'cut', 'singflx_T')
                xs.append(i); ys.append(np.median(vals)); lo.append(min(vals)); hi.append(max(vals))
            ax.errorbar(xs, ys, yerr=[np.array(ys) - lo, np.array(hi) - ys], color=col, marker=mk,
                        markersize=4, linewidth=1.0, capsize=2, label=lab)
        ax.set_yscale('log')
        ax.set_xticks(range(len(order)), ['0.990', '0.995', '0.997', '0.999', 'full\nLCFS'])
        ax.set_title(f'phasing {title}', fontsize=8)
        style(ax, r'Edge: hard cut $s_{pol}$ or full LCFS', r'GPEC $|$singflx$|$ [T]' if j == 0 else '')
    finish(fig, 'edge_scan')


def linear_response():
    """MARS-F ideal resonant b_Boozer against GPEC bno at identical cuts and bl2 coils."""
    rows = read(f'{OCT13}/marsf_gpec.csv')
    order = ['c0995', 'c0997', 'full']
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    style_q = {'3': ('#0072B2', 'o'), '10/3': ('#E69F00', 's'), '11/3': ('#D55E00', '^')}
    for q, (col, mk) in style_q.items():
        for ph, fill, dx in [('000', True, -0.08), ('010', False, 0.08)]:
            sel = [r for r in rows if r['q'] == q and r['phasing'] == ph]
            xs = [order.index(r['cut']) + dx for r in sel]
            ys = [float(r['ratio']) for r in sel]
            for r, x, y in zip(sel, xs, ys):
                record('linear_response', '0,0', f'q={q} {ph}', x, y, r, 'cut', 'ratio')
            ax.plot(xs, ys, linestyle='none', marker=mk, color=col, markersize=5,
                    markerfacecolor=col if fill else 'white',
                    label=f'q={q}, ' + ('(0,0,0)' if ph == '000' else r'(0,$\pi$,0)'))
    ax.axhline(1, color='.45', linestyle=':', linewidth=.8)
    ax.set_yscale('log')
    ax.set_xticks(range(3), ['cut 0.995', 'cut 0.997', 'full LCFS'])
    style(ax, 'Edge treatment (identical in both codes)', r'MARS-F $b_{\rm Boozer}$ / GPEC bno')
    ax.legend(fontsize=6.5, frameon=False, ncol=2, loc='lower left')
    fig.tight_layout()
    fig.savefig(OUT / 'linear_response.pdf', metadata={'CreationDate': None, 'ModDate': None})
    plt.close(fig)


def gvec3d_gpec():
    """GVEC nonlinear fixed-boundary 3D (1 % of 90 kAt) against fixed-boundary GPEC, 0.995 cut."""
    rows = read(f'{OCT13}/gvec3d_gpec.csv')
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    for qty, lab, col in [('bn_E', r'$\delta B\cdot n$', '#0072B2'), ('xi_n', r'$\xi\cdot n$', '#D55E00')]:
        for ph, ls, mk in [('000', '-', 'o'), ('010', '--', 's')]:
            sel = sorted([r for r in rows if r['quantity'] == qty and r['phasing'] == ph],
                         key=lambda r: float(r['psiN']))
            for r in sel:
                record('gvec3d_gpec', '0,0', f'{qty} {ph}', float(r['psiN']), float(r['rel_diff']), r,
                       'psiN', 'rel_diff')
            ax.plot([float(r['psiN']) for r in sel], [float(r['rel_diff']) for r in sel], color=col,
                    linestyle=ls, marker=mk, markersize=3.5, linewidth=1.0,
                    label=lab + (' (0,0,0)' if ph == '000' else r' (0,$\pi$,0)'))
    ax.axvline(0.935, color='.6', linewidth=.6)
    ax.text(0.936, 0.42, 'q=3', fontsize=6.5, color='.4')
    ax.set_ylim(0, 0.45)
    style(ax, r'$\psi_N$', 'Relative difference of $n=3$ harmonics')
    ax.legend(fontsize=6.5, frameon=False, loc='upper left')
    fig.tight_layout()
    fig.savefig(OUT / 'gvec3d_gpec.pdf', metadata={'CreationDate': None, 'ModDate': None})
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    plt.rcParams.update({'font.size': 8, 'axes.spines.top': False, 'axes.spines.right': False,
                         'pdf.fonttype': 42, 'font.family': 'DejaVu Sans'})
    exact()
    for law in ['E1', 'E2']:
        toroidal('phase2', [f'{law}_A{a}' for a in ['40', '20', '10', '3p1']], 'circular_' + law.lower())
    toroidal('phase4', ['E4_E1', 'E4_E2'], 'shaped')
    physics(); exports()
    ladder_consumers('phase2', [f'{law}_A{aspect}' for aspect in ['40', '20', '10', '3p1']
                                for law in ['E1', 'E2']],
                     'circular_consumers', (7.1, 8.2))
    ladder_consumers('phase4', ['E4_E1', 'E4_E2'], 'e4_consumers', (7.1, 3.8))
    cylinder(); cylinder_time(); inverse(); tc24()
    tc24_ns640(); edge_scan(); linear_response(); gvec3d_gpec()
    with (DATA / 'figure_points.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(POINTS[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(POINTS)
    print(f"Seventeen figures; {len(POINTS)} plotted points indexed by source CSV and data row.")


if __name__ == '__main__':
    main()
