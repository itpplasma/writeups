#!/usr/bin/env python3
"""Render all rows of the pinned live defect ledger, with recorded supersessions."""
import csv
import re
from tables import BASE, DATA, OUT, tex

ERRATA = BASE + 'equilibrium/ERRATA.md'


def link(url, label):
    return r'\href{' + url.replace('%', r'\%') + '}{' + tex(label) + '}'


def render_links(text):
    parts = []
    last = 0
    for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', text):
        parts.append(tex(text[last:m.start()].replace('`', '')))
        url = m[2]
        if url.startswith('#'):
            url = ERRATA + url
        elif not url.startswith('http'):
            url = BASE + 'equilibrium/' + url
        parts.append(link(url, m[1]))
        last = m.end()
    parts.append(tex(text[last:].replace('`', '')))
    return ''.join(parts)


def main():
    source = (DATA / 'context/equilibrium__ERRATA.md').read_text()
    rows = []
    for line in source.split('## Live entries')[0].splitlines():
        if not line.startswith('| ') or line.startswith('| Code'):
            continue
        fields = [f.strip() for f in line.strip('|').split('|')]
        if len(fields) != 5:
            continue
        code, entry, issue, status, refs = fields
        ids = re.findall(r'\[(EQ-[^\]]+|DESC-D01)\]', entry)
        if ids == ['EQ-CYL-1']:
            refs = '[25d20db2d](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/commit/25d20db2d); continuation regression'
        row = dict(code=code, ids='/'.join(ids), issue=issue, source_status=status,
                   report_status=status, links=refs, note='', source='equilibrium/ERRATA.md')
        # The current owner ledger already resolves integration and PR supersessions.
        # Turn unlinked own-code revision identifiers into explicit commit links.
        if 'iter_tc24 `' in row['links']:
            row['links'] = re.sub(r'iter_tc24 `([0-9a-f]+)`',
                                 r'[\1](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/commit/\1)', row['links'])
        if 'EQ-D22' in ids:
            row['links'] += '; [35583217c](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/commit/35583217c)'
        if 'EQ-D35' in ids:
            row['links'] = '[3115ca5e9](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/commit/3115ca5e9); coverage correction'
        if 'EQ-D105' in ids:
            row['links'] = '[eaaf2f7f9](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/commit/eaaf2f7f9); native NaN rejection'
        if 'EQ-D20' in ids and 'boundary truncation' in status:
            row['report_status'] = 'explained'
        rows.append(row)

    with (DATA / 'defects.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)

    abbreviations = {'Public CHEASE': 'CHEASE-P', 'MARS CHEASE': 'CHEASE-M', 'INTERPOS / readers': 'Readers',
                     'iter_tc24 / DESC producer': 'Producer', 'iter_tc24 / CHEASE reader': 'Reader',
                     'iter_tc24 / Phase 3 analysis': 'Analysis', 'KIN6D / TC24': 'KIN6D', 'VMEC++ / readers': 'VMEC reader',
                     'DESC / readers': 'DESC reader', 'External evaluator': 'VMECerror'}
    status_names = {'fixed on main': 'fixed', 'PR open': 'PR open', 'PR on hold': 'held PR',
                    'open candidate': 'candidate', 'open': 'open', 'explained': 'limit',
                    'limitation: converging boundary truncation': 'limit',
                    'limitation: targets reached at M32': 'limit',
                    'PR open; closure recommended': 'held PR',
                    'PR open (TC24 path); other producers open': 'partial PR'}
    lines = [r'\begingroup\fontsize{8}{9}\selectfont', r'\setlength{\tabcolsep}{3pt}', r'\renewcommand{\arraystretch}{1.02}',
             r'\begin{longtable}{>{\raggedright\arraybackslash}p{1.55cm}>{\raggedright\arraybackslash}p{1.6cm}>{\raggedright\arraybackslash}p{6.05cm}>{\raggedright\arraybackslash}p{1.25cm}>{\raggedright\arraybackslash}p{4.65cm}}',
             r'\toprule Code & ID & Defect, candidate or scope & Status & Fix / evidence \\ \midrule',
             r'\endfirsthead', r'\toprule Code & ID & Defect, candidate or scope & Status & Fix / evidence \\ \midrule',
             r'\endhead', r'\bottomrule\endfoot']
    for r in rows:
        issue = r['issue']
        refs = render_links(r['links'])
        if r['note']:
            refs += r'\newline ' + tex(r['note'])
        ids = tex(r['ids']).replace('/', r'/\allowbreak ')
        lines.append(' & '.join([tex(abbreviations.get(r['code'], r['code'])), ids, tex(issue),
                                 tex(status_names.get(r['report_status'], r['report_status'])), refs]) + r' \\')
    lines += [r'\end{longtable}', r'\endgroup']
    (OUT / 'defects.tex').write_text('\n'.join(lines) + '\n')
    limitations = [
        ('EQ-D04 / D13', 'Input mismatch; open', 'JINTRAC derivative columns are inconsistent and retained as received. modx03 is the selected reference; native profile transfer remains measured separately.'),
        ('EQ-D08', 'Open candidate', 'Historical CHEASE export sensitivity is not fully attributed. The measured final exact-case paths do not qualify every export option.'),
        ('EQ-D09', 'Iteration error; controlled', 'RELAX=0 removes retained coarse derivative error in the linear exact case. Nonlinear stopping needs its own check.'),
        ('EQ-D12 / D31', 'Open candidates', 'Historical TC24 VMEC++ and CHEASE force/boundary discrepancies lack expected-rate closure; no native repair is inferred.'),
        ('EQ-D15', 'Discretization', 'P1 field and polygon-boundary errors improve under refinement. Curved P2/P3 evidence replaces that representation for current comparisons.'),
        ('EQ-D20 / exact DESC', 'Boundary representation', 'The shaped exact contour is truncated at the solution degree. M32 native continuation and calibrated stopping meet sampled targets; matched cold cost remains unmeasured.'),
        ('EQ-D20 / VMEC++', 'Method limitation', 'Bulk radial convergence is first order; maxima in the first radial cells converge more slowly under the native axis treatment.'),
        ('EQ-D20 / TC24 DESC', 'Open qualification', 'Native iteration caps and unresolved physical accuracy prevent admission of the retained TC24 states.'),
        ('EQ-D24 / Phase 3', 'Input path blocked', 'Mixed P1 geometry and smooth gradients are rejected. Curved P3 inverse fields, diagnostic stability and actual consumers are measured; coupled nonlinear reliability and geometric consistency remain open.'),
        ('EQ-D25', 'Model domain', 'The separatrix X-point is outside the nested-surface problem. The common interior TC24 boundary needs per-code representation checks.'),
        ('EQ-D88 / Phase 3', 'Open inverse candidate', 'The first constrained linear solve passes; near-axis prescribed-q/coarea source reconstruction and the coupled solve remain unqualified. PR43 is closed with reproducers retained.'),
        ('EQ-P2-1', 'Radial / stopping limits', 'Two circular VMEC++ cases miss combined targets. E2 A10 passes after a strict same-resolution restart. Tighter tolerance removes high-aspect-ratio plateaus; capped attempts remain failures.'),
        ('E4 / VMEC++', 'Radial discretization', 'Refinement decreases field and axis differences, but the delivered states remain above the combined targets.'),
        ('E4 / DESC', 'Stopping limit', 'Both laws have sampled passing states. A finite-beta warm restart meets targets and calibrated native stopping; historical capped states and costs remain unchanged.'),
        ('EQ-P4A-1', 'Estimator sharpness', 'Finite recovery at the cap supplies the functional estimate. Ordinary quadrature and represented-domain error remain separate from geometry error.'),
        ('EQ-EXPORT-2', 'Export limits; improved', 'Regular-boundary scan refinement and header precision remove the measured flux/q gap; other boundary exits retain their margin.'),
        ('Export studies', 'Sampling / conversion', 'Pooled and per-surface norms differ. No outer-shell or vacuum accuracy is established. Some below-target conversion errors level off.'),
        ('Spectral producers', 'Input transfer', 'Prescribed q and toroidal flux are transfer checks, not independent predictions. Their downstream converters remain unused.'),
        ('Phase 4b / Phase 5', 'Open candidates', 'Curved-P3 source laws and coarse Lundquist readback repairs are delivered. Held-quadrature TC24 poloidal-field convergence has the expected rate; target accuracy and geometric consistency remain unresolved.'),
        ('Phase 5 / finite A', 'Physical difference', 'Raw cylinder differences include toroidicity. Fixed-period first-order corrections and fixed-aspect resolution differences separate the effects.'),
        ('Phase 5 / DESC', 'Stopping qualification', 'All four aspect ratios pass sampled targets and calibrated stopping after native continuation; A10 requires M20. Historical capped states and cost curves are retained.'),
        ('MARS Hamada', 'Metric discretization', 'Jacobian refinement follows the expected second-order behavior on both exact cases. Perturbations and exterior vacuum fields were not measured.'),
    ]
    with (DATA / 'limitations.csv').open('w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['owner', 'classification', 'scope'])
        writer.writerows(limitations)
    lines = [r'\begingroup\small\setlength{\tabcolsep}{4pt}',
             r'\begin{longtable}{p{32mm}p{33mm}p{93mm}}',
             r'\toprule Owner & Class & Disposition \\ \midrule\endhead', r'\bottomrule\endfoot']
    lines += [' & '.join(map(tex, r)) + r' \\' for r in limitations]
    lines += [r'\end{longtable}\endgroup']
    (OUT / 'limitations.tex').write_text('\n'.join(lines) + '\n')
    print(f'{len(rows)} defect, candidate, and repair rows; no live PR-state claim.')


if __name__ == '__main__':
    main()
