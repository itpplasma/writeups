"""Strict native FortSym proof gate and explicit bounded-capacity receipt."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--runner', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
folder = Path(__file__).resolve().parent
source = folder / 'hybrid_jets.wl'
result = subprocess.run([str(args.runner), str(source)], text=True,
                        capture_output=True, check=True)
assert not result.stderr, result.stderr
rows = dict(line.split('\t')[1:] for line in result.stdout.splitlines()
            if line.startswith('R\tr0'))
expected = {f'r{i:03}': ('-5/8' if i == 9 else '0') for i in range(1, 13)}
assert rows == expected, rows
probe = folder / 'hybrid_jets_full_capacity_probe.wl'
capacity = subprocess.run([str(args.runner), str(probe)], text=True,
                          capture_output=True, check=True)
assert 'more indeterminates' in capacity.stderr, capacity.stderr
data = dict(scope='Eleven exact single-sector/composition/field/axis identities; '
                 'known wrong coefficient rejected. Combined high-dimensional '
                 'probe is UNKNOWN, not a proved identity.',
            runner=str(args.runner), runner_sha256=sha(args.runner),
            producer_sha256=sha(__file__), source_sha256=sha(source),
            identities=rows, capacity_source_sha256=sha(probe),
            capacity_verdict='UNKNOWN: polynomial engine maximum12 indeterminates',
            capacity_diagnostics=capacity.stderr.splitlines())
with args.output.open('x') as stream:
    stream.write(json.dumps(data, indent=2) + '\n')
print('PASS eleven native exact identities and wrong-coefficient rejection; capacity gap explicit')
