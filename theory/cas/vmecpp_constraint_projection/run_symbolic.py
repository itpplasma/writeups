"""Exact native FortSym amplitude/chain sectors, with wrong-term rejection."""
import hashlib,json,subprocess
from pathlib import Path
folder=Path(__file__).resolve().parent
runner=Path('/home/ert/code/fortsym/build/bin/fortsym_wl_run')
source=folder/'constraint_sector.wl'
r=subprocess.run([str(runner),str(source)],text=True,capture_output=True,check=True)
assert not r.stderr,r.stderr
rows=dict(line.split('\t')[1:] for line in r.stdout.splitlines() if line.startswith('R\tr0'))
assert rows=={f'r{i:03}':('-4' if i==6 else '0') for i in range(1,9)},rows
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
receipt=dict(schema='vmecpp-native-constraint-sector-identity-v1',runner_sha256=sha(runner),source_sha256=sha(source),producer_sha256=sha(__file__),identities=rows,scope='Exact bounded amplitude/chain/fixed-filter identities; trigonometric orthogonality explicit; no live multiplier derivative claim')
(folder/'symbolic_results.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS seven exact native identities and missing-chain-term negative control')
