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

import matplotlib
import numpy

HERE = Path(__file__).resolve().parent
ARTIFACTS = [
    ('report', 'report.pdf', 'TC24 axisymmetric equilibrium benchmark, consolidated report'),
    ('exact_a3', 'exact_a3.pdf', 'Exact A3 convergence and cost'),
    ('exact_cerfon', 'exact_cerfon.pdf', 'Exact Cerfon convergence and cost'),
    ('circular_e1', 'circular_e1.pdf', 'Zero-pressure circular ladder'),
    ('circular_e2', 'circular_e2.pdf', 'Finite-pressure circular ladder'),
    ('large_aspect', 'large_aspect.pdf', 'Large-aspect-ratio remainder check'),
    ('shaped', 'shaped.pdf', 'E4 shaped convergence and cost'),
    ('consumer_exact', 'consumer_exact.pdf', 'Exact native-to-consumer accuracy'),
    ('cylinder', 'cylinder.pdf', 'Periodic-cylinder aspect and resolution study'),
    ('inverse', 'inverse.pdf', 'Prescribed-q adjacent-resolution convergence and cost'),
    ('tc24', 'tc24.pdf', 'modx03 five-code convergence and cost'),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--uploader', type=Path, required=True)
    args = parser.parse_args()
    repo = HERE.parents[1]
    revision = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
    dirty = subprocess.check_output(['git', '-C', str(repo), 'status', '--porcelain', '--', str(HERE)], text=True)
    if dirty.strip():
        raise SystemExit('Commit the reviewed report source before publication.')
    for _, filename, _ in ARTIFACTS:
        if not (HERE / 'build' / filename).is_file():
            raise SystemExit(f'Missing rendered artifact: {filename}')
    tracked = subprocess.check_output(['git', '-C', str(repo), 'ls-files', '--', str(HERE)], text=True).splitlines()
    manifest = {
        'title': 'TC24 Phase 6 consolidated report', 'source_commit': revision,
        'source_base': 'fabe9256db7d1fa965ad7055faaa22d7f35c9e56',
        'source_branch': 'equilibrium/slice-report-20261009',
        'input_manifest_sha256': sha(HERE / 'sources.json'),
        'data_pin': json.loads((HERE / 'sources.json').read_text())['tc24_commit'],
        'commands': ['TMPDIR=<disk-directory> bash equilibrium/tc24/build.sh'],
        'versions': {'python': sys.version.split()[0], 'numpy': numpy.__version__,
                     'matplotlib': matplotlib.__version__,
                     'pdf_engine': subprocess.check_output(['pdflatex', '--version'], text=True).splitlines()[0]},
        'source_sha256': {p: sha(repo / p) for p in tracked if not p.endswith('artifacts.json')},
        'artifacts': [],
    }
    target = HERE / 'artifacts.json'
    for key, filename, description in ARTIFACTS:
        path = HERE / 'build' / filename
        now = datetime.now(timezone.utc)
        result = subprocess.run(['bash', str(args.uploader), str(path)], text=True, capture_output=True)
        if result.returncode:
            # No retries: in particular an HTTP 403 remains a publication block.
            raise SystemExit(f'Upload failed for {filename}: {result.stderr.strip()}')
        url = result.stdout.strip()
        if not re.fullmatch(r'https://box\.sloppy\.at/[0-9a-f]{5}\.pdf', url):
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
