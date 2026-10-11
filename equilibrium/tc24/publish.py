#!/usr/bin/env python3
"""Publish the rendered report and figures with the installed slopbox flow."""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from zipfile import ZIP_DEFLATED, ZipFile

import matplotlib
import numpy
import pypdf
from matplotlib.figure import Figure
from pypdf import PdfReader, PdfWriter

HERE = Path(__file__).resolve().parent
FIGURES = [
    ('exact_a3', 'exact_a3.pdf', 'Exact A3 convergence and cost'),
    ('exact_cerfon', 'exact_cerfon.pdf', 'Exact Cerfon convergence and cost'),
    ('circular_e1', 'circular_e1.pdf', 'Zero-pressure circular ladder'),
    ('circular_e2', 'circular_e2.pdf', 'Finite-pressure circular ladder'),
    ('circular_consumers', 'circular_consumers.pdf', 'Circular native and libneo readback'),
    ('large_aspect', 'large_aspect.pdf', 'Large-aspect-ratio remainder check'),
    ('shaped', 'shaped.pdf', 'E4 shaped convergence and cost'),
    ('e4_consumers', 'e4_consumers.pdf', 'E4 native and libneo readback'),
    ('consumer_exact', 'consumer_exact.pdf', 'Exact native-to-consumer accuracy'),
    ('cylinder', 'cylinder.pdf', 'Periodic-cylinder aspect and resolution study'),
    ('cylinder_time', 'cylinder_time.pdf', 'Periodic-cylinder change versus producer time'),
    ('inverse', 'inverse.pdf', 'Prescribed-q adjacent-resolution convergence and cost'),
    ('tc24', 'tc24.pdf', 'modx03 five-code convergence and cost'),
]
FIGURE_GROUPS = [
    ('Exact solutions', [('exact_a3', 'A3 exact LCFS'), ('exact_cerfon', 'Cerfon exact LCFS')]),
    ('Circular ladder', [('circular_e1', "E1 constant-FF'"), ('circular_e2', "E2 constant-p'"),
                         ('circular_consumers', 'Eight-case circular native and libneo readback'),
                         ('large_aspect', 'Absolute remainders from the leading shift')]),
    ('Shaped equilibrium (E4)', [('shaped', 'E4 zero- and finite-pressure laws'),
                                 ('e4_consumers', 'Two-law E4 native and libneo readback')]),
    ('Consumer readback', [('consumer_exact', 'Poloidal-field accuracy at successive readback paths')]),
    ('Prescribed-q inverse', [('inverse', 'Prescribed-q refinement')]),
    ('TC24 modx03', [('tc24', 'TC24 modx03 differences')]),
    ('Periodic cylinder', [('cylinder', 'Cylinder continuation and resolution differences'),
                           ('cylinder_time', 'Cylinder adjacent-resolution field change versus producer time')]),
]
PUBLICATION_ARTIFACTS = [
    ('report', 'report.pdf', 'TC24 axisymmetric equilibrium benchmark, consolidated report'),
    ('figure_booklet', 'figure_booklet.pdf', 'Case-indexed assessment figures with report captions'),
    ('individual_figures', 'individual_figures.zip', 'Standalone figure PDFs and plotted-point source index'),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_bundles(output_dir):
    """Build local figure deliverables from the rendered report and plots."""
    report_path = HERE / 'build' / 'report.pdf'
    for _, filename, _ in FIGURES:
        if not (HERE / 'build' / filename).is_file():
            raise SystemExit(f'Missing rendered figure: {filename}')
    if not report_path.is_file():
        raise SystemExit('Missing rendered report: report.pdf')
    output_dir.mkdir(parents=True, exist_ok=True)

    report = PdfReader(str(report_path))
    normalized_pages = [re.sub(r'[^a-z0-9]', '', (page.extract_text() or '').lower())
                        for page in report.pages]
    figure_pages = {}
    for group, entries in FIGURE_GROUPS:
        for key, caption in entries:
            needle = re.sub(r'[^a-z0-9]', '', caption.lower())
            matches = [i for i, text in enumerate(normalized_pages) if needle in text]
            if len(matches) != 1:
                raise SystemExit(f'Expected one report caption for {key}, found {len(matches)}')
            figure_pages[key] = matches[0]

    ordered_sources = []
    for _, entries in FIGURE_GROUPS:
        for key, _ in entries:
            source_page = figure_pages[key]
            if source_page not in ordered_sources:
                ordered_sources.append(source_page)
    booklet_page = {source_page: i + 1 for i, source_page in enumerate(ordered_sources)}

    index_path = output_dir / 'figure_index.pdf'
    figure = Figure(figsize=(8.27, 11.69), facecolor='white')
    figure.text(0.09, 0.94, 'Equilibrium assessment figures', fontsize=20, weight='bold')
    figure.text(0.09, 0.905, 'Case-indexed selection from the consolidated TC24 report', fontsize=11)
    figure.text(0.09, 0.875,
                'Right-hand numbers are booklet PDF pages (including this index); report footers stay unchanged.',
                fontsize=9)
    y = 0.82
    for group, entries in FIGURE_GROUPS:
        figure.text(0.09, y, group, fontsize=11, weight='bold')
        y -= 0.031
        for key, _ in entries:
            _, _, description = next(item for item in FIGURES if item[0] == key)
            page = booklet_page[figure_pages[key]] + 1
            figure.text(0.115, y, description, fontsize=9)
            figure.text(0.90, y, str(page), fontsize=9, ha='right')
            y -= 0.026
        y -= 0.012
    figure.text(0.09, 0.075,
                'Times retain their study-specific environments and definitions; this booklet makes no cross-study speed ranking.',
                fontsize=8, wrap=True)
    figure.savefig(index_path, format='pdf')

    booklet_path = output_dir / 'figure_booklet.pdf'
    writer = PdfWriter()
    index = PdfReader(str(index_path))
    writer.add_page(index.pages[0])
    for source_page in ordered_sources:
        writer.add_page(report.pages[source_page])
    for group, entries in FIGURE_GROUPS:
        first_page = booklet_page[figure_pages[entries[0][0]]]
        group_outline = writer.add_outline_item(group, first_page)
        for key, _ in entries:
            source_page = figure_pages[key]
            target_page = booklet_page[source_page]
            description = next(item[2] for item in FIGURES if item[0] == key)
            writer.add_outline_item(description, target_page, parent=group_outline)
    with booklet_path.open('wb') as stream:
        writer.write(stream)
    index_path.unlink()

    archive_path = output_dir / 'individual_figures.zip'
    descriptions = {key: description for key, _, description in FIGURES}
    with ZipFile(archive_path, 'w', ZIP_DEFLATED) as archive:
        for key, filename, _ in FIGURES:
            archive.write(HERE / 'build' / filename, f'figures/{filename}')
        archive.write(HERE / 'data' / 'figure_points.csv', 'data/figure_points.csv')
        listing = ['Standalone vector figure PDFs from the consolidated report.',
                   'data/figure_points.csv maps each plotted point to its source CSV row.',
                   'Use the accompanying case-indexed PDF for captions and scope.', '']
        for group, entries in FIGURE_GROUPS:
            listing.append(group + ':')
            listing.extend(f'  {key}.pdf — {descriptions[key]}' for key, _ in entries)
            listing.append('')
        archive.writestr('INDEX.txt', '\n'.join(listing))
    return booklet_path, archive_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--uploader', type=Path)
    parser.add_argument('--bundle-dir', type=Path, default=HERE / 'build' / 'publication')
    parser.add_argument('--prepare-bundles-only', action='store_true')
    args = parser.parse_args()
    if args.prepare_bundles_only:
        paths = build_bundles(args.bundle_dir)
        for path in paths:
            print(path)
        return
    if args.uploader is None:
        parser.error('--uploader is required unless --prepare-bundles-only is used')
    repo = HERE.parents[1]
    revision = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
    dirty = subprocess.check_output(['git', '-C', str(repo), 'status', '--porcelain', '--', str(HERE)], text=True)
    if dirty.strip():
        raise SystemExit('Commit the reviewed report source before publication.')
    booklet, archive = build_bundles(args.bundle_dir)
    artifact_paths = {
        'report.pdf': HERE / 'build' / 'report.pdf',
        'figure_booklet.pdf': booklet,
        'individual_figures.zip': archive,
    }
    tracked = subprocess.check_output(['git', '-C', str(repo), 'ls-files', '--', str(HERE)], text=True).splitlines()
    manifest = {
        'title': 'TC24 Phase 6 consolidated report', 'source_commit': revision,
        'source_base': 'fabe9256db7d1fa965ad7055faaa22d7f35c9e56',
        'source_branch': subprocess.check_output(
            ['git', '-C', str(repo), 'branch', '--show-current'], text=True).strip(),
        'input_manifest_sha256': sha(HERE / 'sources.json'),
        'data_pin': json.loads((HERE / 'sources.json').read_text())['tc24_commit'],
        'commands': ['TMPDIR=<disk-directory> bash equilibrium/tc24/build.sh',
                     'python equilibrium/tc24/publish.py --prepare-bundles-only'],
        'versions': {'python': sys.version.split()[0], 'numpy': numpy.__version__,
                     'matplotlib': matplotlib.__version__,
                     'pypdf': pypdf.__version__,
                     'pdf_engine': subprocess.check_output(['pdflatex', '--version'], text=True).splitlines()[0]},
        'source_sha256': {p: sha(repo / p) for p in tracked if not p.endswith('artifacts.json')},
        'artifacts': [],
    }
    target = HERE / 'artifacts.json'
    for key, filename, description in PUBLICATION_ARTIFACTS:
        path = artifact_paths[filename]
        now = datetime.now(timezone.utc)
        result = subprocess.run(['bash', str(args.uploader), str(path)], text=True, capture_output=True)
        if result.returncode:
            # No retries: in particular an HTTP 403 remains a publication block.
            raise SystemExit(f'Upload failed for {filename}: {result.stderr.strip()}')
        url = result.stdout.strip()
        extension = re.escape(path.suffix)
        if not re.fullmatch(rf'https://box\.sloppy\.at/[0-9a-f]{{5}}{extension}', url):
            raise SystemExit(f'Unexpected uploader result for {filename}: {url}')
        manifest['artifacts'].append({
            'id': key, 'file': filename, 'description': description, 'url': url,
            'bytes': path.stat().st_size, 'sha256': sha(path),
            'uploaded_at': now.isoformat(), 'expires_at': (now + timedelta(days=3)).isoformat(),
        })
        target.write_text(json.dumps(manifest, indent=2) + '\n')
        print(f'{key}: {url}', flush=True)


if __name__ == '__main__':
    main()
