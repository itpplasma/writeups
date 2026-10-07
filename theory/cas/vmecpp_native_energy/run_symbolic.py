"""Bounded exact native energy/dual sectors; no solver dependency."""
from pathlib import Path
import hashlib,json,os,subprocess
folder=Path(__file__).resolve().parent
runner=Path(os.environ.get('FORTSYM_WL_RUN','/home/ert/code/fortsym/build/bin/fortsym_wl_run'))
source=folder/'half_energy_sector.wl'
result=subprocess.run([str(runner),str(source)],capture_output=True,text=True,check=True)
assert not result.stderr,result.stderr
rows=dict(line.split('\t')[1:] for line in result.stdout.splitlines() if line.startswith('R\tr0'))
assert rows=={f'r{i:03}':('-6' if i==7 else '0') for i in range(1,8)},rows
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
receipt=dict(schema='vmecpp-native-half-energy-sector-v1',runner_sha256=sha(runner),
 source_sha256=sha(source),producer_sha256=sha(__file__),identities=rows,
 scope='Signed axisymmetric half-cell algebra, gamma0, fixedp/fixedflux numerator constraints; chain/basis/quadrature assumptions separate. No full native projection/continuum proof.')
(folder/'symbolic_results.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS six exact half-cell/dual identities and missing-normalization negative control')
