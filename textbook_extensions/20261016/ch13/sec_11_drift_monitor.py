from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
from scipy.stats import ks_2samp
f=pd.read_csv(DATA/"drift.csv")
ref,cur=f.reference.to_numpy(),f.current.to_numpy()
edges=np.quantile(ref,np.linspace(0,1,11));edges[0]=-np.inf;edges[-1]=np.inf
p=np.histogram(ref,edges)[0]/len(ref);q=np.histogram(cur,edges)[0]/len(cur)
# Small pseudo-count smoothing; renormalize to keep probabilities summing to 1.
eps=1e-6;p=(p+eps)/(p+eps).sum();q=(q+eps)/(q+eps).sum()
contribution=(q-p)*np.log(q/p);psi=float(contribution.sum())
ks=ks_2samp(ref,cur)
r=pd.DataFrame({"bin":range(10),"reference_fraction":p,"current_fraction":q,
    "psi_contribution":contribution});r.to_csv(OUT/"drift_monitor.csv",index=False)
fig,axes=plt.subplots(1,2,figsize=(7.2,3.6))
axes[0].hist([ref,cur],bins=25,histtype="step",density=True,label=["Reference","Current"])
axes[0].set(xlabel="Feature value",ylabel="Density");axes[0].legend(fontsize=8)
axes[1].bar(range(10),contribution,color=".7",edgecolor="black")
axes[1].set(xlabel="Reference quantile bin",ylabel="PSI contribution")
figure(OUT,"drift_monitor")
report(OUT,"drift_monitor",{"PSI":psi,"KS_statistic":float(ks.statistic),
    "KS_pvalue":float(ks.pvalue),"reference_n":len(ref),"current_n":len(cur)})
