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


def evidence(obj, field, value, rows, operation='identity', digits=3):
    TRACE.append({'object': obj, 'field': field, 'value': value, 'operation': operation,
                  'sources': ';'.join(f"{r['_file']}:{r['_row']}" for r in rows)})
    return number(value, digits)


def cell(obj, r, field, digits=3):
    evidence(obj, field, r[field], [r])
    return number(r[field], digits)


def macro(name, value, refs, field, operation='identity', digits=3):
    evidence(name, field, value, refs, operation)
    formatted = number(value, digits)
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


def inverse_tables():
    rows = read('phase3/results/comparison.csv') + read('phase3/results/kin6d_comparison.csv')
    cases = [('E1_constant_q_A10', 'E1'), ('E2_constant_q_A10', 'E2'), ('Solovev_inverse_A3', 'Solovev')]
    values = []
    for case, label in cases:
        for code in ['kin6d', 'chease_public', 'vmecpp', 'desc']:
            selected = [r for r in rows if r['case'] == case and r['code'] == code]
            if code == 'kin6d':
                level = '2' if label == 'E2' else '1'
                r = next(r for r in selected if r['level'] == level)
            else:
                r = max(selected, key=lambda r: float(r['dof']))
            obj = f'inverse:{case}:{code}'
            current = evidence(obj, 'I_phi_MA', float(r['I_phi_A']) / 1e6, [r], 'I_phi_A / 1e6')
            fields = [('ref.' if float(r[f]) == 0 and code == 'chease_public' and label != 'Solovev'
                       else cell(obj, r, f)) for f in ['bpol_l2', 'F_l2', 'q_max']]
            values.append([label, tex(LABELS[code])] + fields + [current, cell(obj, r, 'wall_s')])
    table('inverse_values', ['Case', 'Code', r'$B_p$ $L^2$', '$F$ $L^2$', '$q$ max', '$I$ (MA)', 'Time (s)'], values, 'llrrrrr')
    exact = [r for r in rows if r['case'] == 'Solovev_inverse_A3' and r['code'] == 'kin6d']
    coarse, fine = sorted(exact, key=lambda r: int(r['level']))[-2:]
    for field, name in [('psi_l2', 'InversePsiRate'), ('bpol_l2', 'InverseBRate'), ('F_l2', 'InverseFRate')]:
        macro(name, math.log2(float(coarse[field])/float(fine[field])), [coarse, fine], field,
              'log2(error_n96/error_n192), exact Solovev; boundary resolution doubled')
    macro('InverseFineB', fine['bpol_l2'], [fine], 'bpol_l2')
    ex = read('phase3/results/kin6d_exports.csv')
    vals = []
    for case, label in cases:
        r = next(r for r in ex if r['case'] == case and r['level'] == '3' and r['path'] == 'EQDSK_libneo')
        vals.append([label, cell('inverse_export:'+case, r, 'psi_l2'), cell('inverse_export:'+case, r, 'bpol_l2')])
    table('inverse_exports', ['Case', r'libneo $\psi$ $L^2$', r'libneo $B_p$ $L^2$'], vals)


    gpec = read('phase3/results/kin6d_consumers_gpec.csv')
    hamada = read('phase3/results/kin6d_consumers_hamada.csv')
    neo = read('phase3/results/kin6d_consumers_neo2.csv')
    vals = []
    for case, label in cases:
        for path, source in [('GPEC', gpec), ('NEO-2', neo)]:
            r = next(r for r in source if r['case'] == case and r['level'] == '3')
            jr = next((h for h in hamada if h['case'] == case and h['level'] == '3'), r) if path == 'GPEC' else r
            vals.append([label, path, cell('inverse_consumer:'+case+path, r, 'bpol_l2'),
                         cell('inverse_consumer:'+case+path, r, 'q_max_rel'),
                         cell('inverse_consumer:'+case+path, r, 'phi_edge_rel'),
                         cell('inverse_consumer:'+case+path, jr, 'jacobian_max_rel')])
    table('inverse_consumers', ['Case', 'Reader', r'$B_p$ $L^2$', '$q$ max', r'$\Phi_e$', '$J$ max'], vals, 'llrrrr')


def tc24_tables():
    base = 'phase4/tc24/reference/'
    variants = read(base+'variants.csv')
    names = {'reference': 'modx03 (reference)', 'gfile_chease': r'gfile\_chease',
             'jintrac': 'JINTRAC', 'leonardo': 'Leonardo CHEASE'}
    table('tc24_sources', ['Received equilibrium', '$R_0$ (m)', '$I_p$ (MA)', '$F_e$ (T m)', '$q_0$'],
          [[names[r['name']]]+[cell('tc24_source:'+r['name'],r,k,6) for k in ['R0','native_Ip_MA','native_F_edge','native_q0']] for r in variants])
    replay = read(base+'replay.csv')
    table('tc24_replay', ['Exact-deck replay', 'Time (s)', '$I_p$ (MA)', r'Source $B_p$ difference'],
          [[tex(LABELS[r['code']]),cell('replay',r,'wall_s'),
            evidence('replay','current_MA',float(r['current_A'])/1e6,[r],'current_A / 1e6',digits=9),
            cell('replay',r,'source_bpol_l2')] for r in replay])
    ref = next(r for r in variants if r['name']=='reference')
    macro('SourceHeaderCurrent', ref['native_Ip_MA'], [ref], 'native_Ip_MA', digits=9)
    macro('ReplayLogCurrent', float(replay[0]['received_log_current_A'])/1e6, [replay[0]], 'received_log_current_A', 'divide by 1e6', digits=9)
    rows = read(base+'comparison.csv'); vals=[]
    for code in CODES:
        r = max([r for r in rows if r['name']=='reference' and r['code']==code
                 and yes(r['native_converged']) and yes(r['readback_complete'])],key=lambda r: float(r['dof']))
        vals.append([tex(LABELS[code]),cell('tc24:'+code,r,'dof',6)] +
                    [('ref.' if code=='chease_public' else cell('tc24:'+code,r,f)) for f in ['psi_l2','bpol_l2','q_max']] +
                    [cell('tc24:'+code,r,'wall_s')])
    table('tc24_values', ['Code','DOF',r'$\psi$ $L^2$',r'$B_p$ $L^2$','$q$ max','Time (s)'], vals)
    convergence = read(base+'convergence.csv')
    for code,name in [('kin6d','Kin'),('chease_public','Public')]:
        r=max([r for r in convergence if r['code']==code],key=lambda r:float(r['fine_dof']))
        macro('Tc'+name+'BRate',r['apparent_bpol_l2_order'],[r],'apparent_bpol_l2_order')
        macro('Tc'+name+'PsiRate',r['apparent_psi_l2_order'],[r],'apparent_psi_l2_order')
    exports = read(base+'exports.csv'); consumers=read(base+'consumers.csv'); vals=[]
    for code in CODES[:3]:
        # The committed package selects the highest-resolution export of the finest producer.
        selected=[r for r in exports if r['name']=='reference' and r['code']==code]
        if code=='kin6d': selected=[r for r in selected if 'n96_' in r['producer'] and r['mpol']=='256']
        else: selected=[r for r in selected if 'n128_' in r['producer']]
        eq=next(r for r in selected if r['path']=='EQDSK_libneo'); boo=next(r for r in selected if r['path']=='Boozer')
        neo=next(r for r in consumers if r['kind']=='neo2' and r['export']==eq['export_root'])
        gpec=[r for r in consumers if r['kind']=='gpec' and r['producer']==eq['producer'] and r['bpol_l2']]
        vals.append([tex(LABELS[code]),cell('tc_export',eq,'bpol_l2'),cell('tc_export',boo,'bpol_l2'),
                     cell('tc_export',neo,'bpol_l2'),cell('tc_export',neo,'jacobian_geometry_max_rel'),
                     cell('tc_export',gpec[-1],'bpol_l2') if gpec else 'failed'])
    table('tc24_exports',['Producer','EQDSK $B_p$','Boozer $B_p$','NEO-2 $B_p$','NEO-2 $J$ max','GPEC $B_p$'], vals)
    timings=read('phase4/tc24/kin6d_performance/timings.csv')
    table('tc24_performance', ['$n$','DOF','Prior solve (s)','New solve (s)','Estimator (s)','Full run (s)'],
          [[cell('tc_perf',r,k,6 if k=='dof' else 3) for k in ['n','dof','baseline_s','solve_s','estimator_s','total_s']] for r in timings])


def main():
    OUT.mkdir(exist_ok=True)
    exact_tables(); toroidal_tables(); consumer_tables(); other_tables(); inverse_tables(); tc24_tables()
    (OUT / 'numbers.tex').write_text('\n'.join(MACROS) + '\n')
    with (DATA / 'table_cells.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(TRACE[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(TRACE)
    print(f'{len(TRACE)} numerical table cells and macros indexed by source rows.')


if __name__ == '__main__':
    main()
