"""기본은 구문·자료·노트북 검사이고 --execute는 실제 Jupyter 커널 검사입니다."""
from pathlib import Path
import ast,json,argparse,hashlib
import nbformat
BASE=Path(__file__).resolve().parent;p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true');args=p.parse_args();coverage=json.loads((BASE/'coverage_20261103.json').read_text());manifest=json.loads((BASE/'data_manifest.json').read_text())
for x in manifest:assert hashlib.sha256((BASE/x['file']).read_bytes()).hexdigest()==x['sha256']
for x in coverage['programs']:
 path=BASE/(x['path']+'.ipynb');n=nbformat.read(path,as_version=4);nbformat.validate(n);source='\n'.join(c.source for c in n.cells if c.cell_type=='code');assert ast.dump(ast.parse(source))==ast.dump(ast.parse(path.with_suffix('.py').read_text()));assert '%run' not in source and 'from common import' not in source
 for c in n.cells:
  if c.cell_type=='code':assert not any(o.output_type=='error' for o in c.outputs)
 if args.execute:
  from nbclient import NotebookClient
  NotebookClient(n,timeout=180,kernel_name='ai-textbook',resources={'metadata':{'path':str(path.parent)}}).execute();nbformat.write(n,path)
print(json.dumps({'independent_programs':len(coverage['programs']),'csv_hashes':len(manifest),'jupyter_kernel_executed_in_this_check':args.execute},ensure_ascii=False,indent=2))
