#!/usr/bin/env python3
"""Generate numerical report cells, recording their source rows and calculations."""
import csv
import json
import math
import re
from pathlib import Path

import numpy as np

from figures import CODES, DATA, HERE, LABELS, OUT, read, yes

TRACE = []
MACROS = []
TC24 = json.loads((HERE / 'sources.json').read_text())['tc24_commit']
BASE = f'https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/blob/{TC24}/'


def tex(text):
    text = str(text)
    for old, new in [('\\', r'\textbackslash{}'), ('&', r'\&'), ('%', r'\%'),
                     ('_', r'\_'), ('#', r'\#')]:
        text = text.replace(old, new)
    return text.replace('→', r'$\to$').replace('—', '---').replace('²', '$^2$')


def number(value, digits=3):
    v = float(value)
    if not math.isfinite(v):
        return '---'
    if v == 0:
        return '0'
    if abs(v) < .001 or abs(v) >= 1e5:
        mantissa, exponent = f'{v:.{digits-1}e}'.split('e')
        return rf'${mantissa}\times10^{{{int(exponent)}}}$'
    return f'{v:.{digits}g}'


def evidence(obj, field, value, rows, operation='identity'):
    TRACE.append({'object': obj, 'field': field, 'value': value, 'operation': operation,
                  'sources': ';'.join(f"{r['_file']}:{r['_row']}" for r in rows)})
    return number(value)


def cell(obj, r, field, digits=3):
    evidence(obj, field, r[field], [r])
    return number(r[field], digits)


def macro(name, value, refs, field, operation='identity'):
    formatted = evidence(name, field, value, refs, operation)
    MACROS.append('\\newcommand{\\' + name + '}{' + formatted + '}')


def table(name, headers, rows, spec=None):
    spec = spec or ('l' + 'r' * (len(headers)-1))
    lines = [r'\begin{tabular}{' + spec + '}', r'\toprule', ' & '.join(headers) + r' \\', r'\midrule']
    lines += [' & '.join(row) + r' \\' for row in rows]
    lines += [r'\bottomrule', r'\end{tabular}']
    (OUT / f'{name}.tex').write_text('\n'.join(lines) + '\n')


def rates(rows, code, field, obj):
    rs = sorted(rows, key=lambda r: float(r['dof']))[-3:]
    if code == 'kin6d':
        x = [math.log(float(r['dof'])) / 2 for r in rs]
    else:
        settings = [json.loads(r['resolution']) for r in rs]
        if code == 'desc':
            x = [s.get('M', s.get('m')) for s in settings]
        else:
            x = [math.log(s['ns'] - (1 if code == 'vmecpp' else 0)) for s in settings]
    value = -np.polyfit(x, [math.log(float(r[field])) for r in rs], 1)[0]
    evidence(obj, field + '_rate', value, rs, 'least-squares log(error) fit; see report rate definition')
    return f'{value:.2f}'


def exact_tables():
    rows = []; p3rows = []
    owner = read('kin6d/p2-p3.csv')
    for case, label in [('solovev_lcfs_A3', 'A3'), ('solovev_cerfon_iter', 'Cerfon')]:
        allrows = read(f'phase1/results/{case}.csv')
        for code, degree in [('kin6d', 2), ('kin6d', 3)] + [(c, None) for c in CODES[1:]]:
            rs = [r for r in allrows if r['code'] == code and yes(r['native_converged'])
                  and (degree is None or json.loads(r['resolution']).get('degree', 2) == degree)]
            passes = [r for r in rs if yes(r['accuracy_passed'])]
            chosen = min(passes, key=lambda r: float(r['wall_s'])) if passes else max(rs, key=lambda r: float(r['dof']))
            obj = f'exact:{case}:{code}:{degree}'
            rows.append([label, tex(LABELS[code] + (f' P{degree}' if degree else '')),
                         rates(rs, code, 'psi_l2', obj), rates(rs, code, 'bpol_l2', obj),
                         cell(obj, chosen, 'bpol_l2'), cell(obj, chosen, 'wall_s'), 'pass' if passes else 'gap'])
            if degree == 3:
                name = 'Athree' if label == 'A3' else 'Cerfon'
                macro('Pthree' + name + 'Time', chosen['wall_s'], [chosen], 'wall_s')
                macro('Pthree' + name + 'Error', chosen['bpol_l2'], [chosen], 'bpol_l2')
        for degree in ['2', '3']:
            rs = [r for r in owner if r['case'] == case and r['degree'] == degree]
            chosen = min([r for r in rs if yes(r['accuracy_passed'])], key=lambda r: float(r['wall_s']))
            obj = f'owner:{case}:P{degree}'
            p3rows.append([label, degree, cell(obj, chosen, 'n', 5), cell(obj, chosen, 'dof', 6),
                           cell(obj, chosen, 'psi_l2'), cell(obj, chosen, 'bpol_l2'), cell(obj, chosen, 'wall_s')])
    table('exact_rates', ['Case', 'Code', r'$p_\psi$ / $\alpha_\psi$', r'$p_B$ / $\alpha_B$', r'$B_{pol}$ $L^2$', 'Time (s)', 'Gate'], rows, 'llrrrrl')
    table('p3_cost', ['Case', 'Degree', '$n$', 'DOF', r'$\psi$ $L^2$', r'$B_{pol}$ $L^2$', 'Solve (s)'], p3rows, 'llrrrrr')


def toroidal_tables():
    for phase, cases in [('phase2', [f'{law}_A{a}' for law in ['E1', 'E2'] for a in ['40', '20', '10', '3p1']]),
                         ('phase4', ['E4_E1', 'E4_E2'])]:
        costs = read(f'{phase}/results/best_cost.csv'); refs = read(f'{phase}/results/reference_errors.csv')
        rows = []; refrows = []
        for case in cases:
            entries = {r['code']: r for r in costs if r['case'] == case}
            rows.append([tex(case.replace('_', '/').replace('3p1', '3.1'))] +
                        [cell(f'{phase}_cost:{case}', entries[c], 'wall_s') if c in entries else '---' for c in CODES])
            r = next(r for r in refs if r['case'] == case)
            refrows.append([tex(case.replace('_', '/').replace('3p1', '3.1'))] +
                           [cell(f'{phase}_reference:{case}', r, f) for f in
                            ['psi_richardson', 'bpol_richardson', 'majorant_relative', 'majorant_to_richardson']])
        headers = ['Case', 'KIN6D P3', 'Public', 'MARS', 'VMEC++', 'DESC']
        table(phase + '_cost', headers, rows)
        table(phase + '_reference', ['Case', r'$\psi$ Rich.', r'$B_{pol}$ Rich.', 'Rel. majorant', 'Ratio'], refrows)
        if phase == 'phase4':
            for r in refs:
                name = 'EfourZero' if r['case'] == 'E4_E1' else 'EfourFinite'
                macro(name + 'Reference', r['bpol_richardson'], [r], 'bpol_richardson')
                macro(name + 'Effectivity', r['majorant_to_richardson'], [r], 'majorant_to_richardson')
    costs = read('phase4/results/cost_by_bpol.csv')
    rows = []
    for case in ['E4_E1', 'E4_E2']:
        entries = {r['code']: r for r in costs if r['case'] == case and float(r['bpol_target']) == 1e-4}
        rows.append([tex(case)] + [cell('phase4_matched:' + case, entries[c], 'wall_s') for c in CODES])
    table('phase4_matched', headers, rows)
    physics = read('phase2/results/physics.csv')
    for law in ['E1', 'E2']:
        rs = [r for r in physics if r['case'].startswith(law) and float(r['aspect_ratio']) >= 10]
        for key, name in [('shift_leading_difference', 'Shift'), ('q_difference', 'Q')]:
            slope = np.polyfit([-math.log(float(r['aspect_ratio'])) for r in rs],
                               [math.log(abs(float(r[key]))) for r in rs], 1)[0]
            macro(('Eone' if law == 'E1' else 'Etwo') + name + 'Order', slope, rs, key, 'log-log fit over A=40,20,10')


def consumer_tables():
    rows = read('phase1/results_export/summary.csv')
    rows = [r for r in rows if r['tag'].startswith('export_e2e2_final_') or r['tag'].startswith('readers_')]
    fine = []
    for case, label in [('solovev_lcfs_A3', 'A3'), ('solovev_cerfon_iter', 'Cerfon')]:
        for variant in ['public', 'mars', 'kin6d']:
            vals = []
            for path, field in [('fortran', 'bpol_l2'), ('gpec_direct', 'bpol_l2'),
                                ('neo2_full', 'bpol_l2'), ('neo2_full', 'q_max_rel'),
                                ('neo2_full', 'jacobian_max_rel')]:
                r = max([r for r in rows if r['case'] == case and r['variant'] == variant and r['path'] == path], key=lambda r: int(r['n']))
                vals.append(cell(f'consumer:{case}:{variant}:{path}', r, field))
            fine.append([label, variant] + vals)
    table('consumer_fine', ['Case', 'Producer', 'EQDSK $B_p$', 'GPEC $B_p$', 'NEO-2 $B_p$', 'NEO-2 $q$', 'NEO-2 $J$'], fine, 'llrrrrr')
    mars = []
    for r in rows:
        if r['path'] == 'mars_hamada':
            native = next(n for n in rows if n['tag'] == r['tag'] and n['path'] == 'mars_native')
            mars.append(['A3' if 'A3' in r['case'] else 'Cerfon', cell('mars', r, 'n', 5),
                         cell('mars', native, 'bpol_l2'), cell('mars', r, 'bmn_rel'),
                         cell('mars', r, 'jacobian_max_rel')])
    table('mars', ['Case', '$n$', r'Native $B_{pol}$ $L^2$', 'Hamada spectrum', 'Hamada $J$ max'], mars, 'lrrrr')
    pooled = []
    for phase, cases in [('phase2', ['all']), ('phase4', ['E4_E1', 'E4_E2'])]:
        b = read(f'{phase}/results/boozer_volume.csv')
        for case in cases:
            selected = [r for r in b if case == 'all' or r['case'] == case]
            finest = [r for r in selected if float(r['dof']) == max(float(t['dof']) for t in selected if (t['case'], t['code']) == (r['case'], r['code']))]
            vals = []
            for field in ['psi_l2', 'bpol_l2']:
                r = max(finest, key=lambda r: float(r[field]))
                vals.append(cell(f'pooled:{phase}:{case}', r, field))
            pooled.append(['Circular' if case == 'all' else tex(case)] + vals)
    table('pooled', ['Finest producer paths', r'Boozer pooled $\psi$ $L^2$', r'Boozer pooled $B_{pol}$ $L^2$'], pooled)


def other_tables():
    rows = read('phase5/results/finest.csv')
    table('cylinder_values', ['Family at $A=300$', 'Cylinder difference', 'First-order remainder', 'Signed $q$ max'],
          [[r['family'].replace('_', ' ').title()] + [cell('cylinder_values', r, f) for f in
              ['B_rel_L2', 'B_first_order_remainder', 'q_rel_max']]
           for r in rows if r['code'] == 'chease_public' and r['aspect'] == '300' and r['twist'] == '1' and r['reversal'] == '1'])
    rows = read('phase4/tc24/source_consistency.csv')
    table('source_consistency', ['Received source', r'$\int p^\prime\,d\psi/\Delta p$', r'$\int FF^\prime\,d\psi/\Delta(F^2/2)$'],
          [[tex(source)] + [cell('source_consistency', next(r for r in rows if r['source'] == source and r['quantity'] == q), 'integral_over_change', 6)
                           for q in ['pressure', 'F_squared_over_2']] for source in dict.fromkeys(r['source'] for r in rows)])


def main():
    OUT.mkdir(exist_ok=True)
    exact_tables(); toroidal_tables(); consumer_tables(); other_tables()
    (OUT / 'numbers.tex').write_text('\n'.join(MACROS) + '\n')
    with (DATA / 'table_cells.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(TRACE[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(TRACE)
    print(f'{len(TRACE)} numerical table cells and macros indexed by source rows.')


if __name__ == '__main__':
    main()
