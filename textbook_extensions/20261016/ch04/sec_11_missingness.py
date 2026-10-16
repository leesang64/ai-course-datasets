from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
f=pd.read_csv(DATA/"churn.csv")
f["total_charge"]=pd.to_numeric(f.total_charge,errors="coerce")
missing=f.isna().mean().sort_values(ascending=False)
missing.to_csv(OUT/"missingness.csv",header=["missing_fraction"])
fig,axes=plt.subplots(1,2,figsize=(7.2,4))
missing.plot.bar(ax=axes[0],color=".65",edgecolor="black")
axes[0].set(ylabel="Missing fraction",title="Missing values")
counts=f.contract.fillna("MISSING").value_counts()
axes[1].bar(np.arange(len(counts)),counts.values,color=".7",edgecolor="black")
axes[1].set_xticks(np.arange(len(counts)),[f"C{i}" for i in range(len(counts))])
axes[1].set(ylabel="Rows",title="Contract frequency")
figure(OUT,"missingness")
report(OUT,"missingness",{"rows":len(f),"duplicate_rows":int(f.duplicated().sum()),
    "missing_fraction":missing.to_dict(),"contract_codes":{
    f"C{i}":str(c) for i,c in enumerate(counts.index)}})
