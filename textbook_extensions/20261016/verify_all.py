from pathlib import Path
import hashlib,json,subprocess,sys,os
root=Path(__file__).resolve().parent
env=dict(os.environ,OPENBLAS_NUM_THREADS="1",OMP_NUM_THREADS="1",MPLBACKEND="Agg")
for item in json.loads((root/"data_manifest.json").read_text()):
    actual=hashlib.sha256((root/item["file"]).read_bytes()).hexdigest()
    if actual!=item["sha256"]:raise RuntimeError("CSV hash mismatch: "+item["file"])
for script in sorted(root.glob("ch*/sec_*.py")):
    print("RUN",script.relative_to(root),flush=True)
    subprocess.run([sys.executable,str(script)],env=env,check=True)
print("All program runs and CSV hashes passed.")
