from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
f=pd.read_csv(DATA/"churn.csv")
cols=["age","tenure","monthly_charge","total_charge"]
f["total_charge"]=pd.to_numeric(f.total_charge,errors="coerce")
a=f[cols];corr=a.corr()
q1,q3=a.quantile(.25),a.quantile(.75)
flag=((a<q1-1.5*(q3-q1))|(a>q3+1.5*(q3-q1)))
flag.sum().to_csv(OUT/"outlier_counts.csv",header=["flagged"])
corr.to_csv(OUT/"correlation.csv")
fig,axes=plt.subplots(1,2,figsize=(7.2,3.7))
axes[0].scatter(a.tenure,a.total_charge,s=8,facecolors="none",edgecolors=".35")
axes[0].set(xlabel="Tenure",ylabel="Total charge",title="Observed pairs")
im=axes[1].imshow(corr,cmap="gray",vmin=-1,vmax=1)
axes[1].set_xticks(range(4),["Age","Tenure","Monthly","Total"],rotation=50)
axes[1].set_yticks(range(4),["Age","Tenure","Monthly","Total"])
fig.colorbar(im,ax=axes[1],shrink=.8,label="Pearson r")
figure(OUT,"correlation_outlier")
report(OUT,"correlation_outlier",{"iqr_flags":flag.sum().to_dict(),
    "pairwise_corr_tenure_total":float(corr.loc["tenure","total_charge"])})
