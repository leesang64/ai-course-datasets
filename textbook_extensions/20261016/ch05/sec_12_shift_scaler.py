from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
f=pd.read_csv(DATA/"churn.csv")
a,b=train_test_split(np.arange(len(f)),test_size=.3,random_state=42)
train=f.iloc[a][["monthly_charge"]]
current=f.iloc[b][["monthly_charge"]].copy()
# Intentionally shifted scenario; not an observed future distribution.
current["monthly_charge"]+=25
pre=make_pipeline(SimpleImputer(strategy="median"),StandardScaler())
z_train=pre.fit_transform(train).ravel()
z_current=pre.transform(current).ravel()
wrong=make_pipeline(SimpleImputer(strategy="median"),StandardScaler())
z_refit=wrong.fit_transform(current).ravel()
fig,axes=plt.subplots(1,2,figsize=(7.2,3.6))
axes[0].hist([train.to_numpy().ravel(),current.to_numpy().ravel()],
    bins=18,histtype="step",label=["Training","Shifted current"])
axes[0].set(xlabel="Monthly charge (source units)",ylabel="Rows")
axes[1].hist([z_train,z_current,z_refit],bins=18,histtype="step",
    label=["Training z","Fixed scaler","Refit on current"])
axes[1].set(xlabel="Standardized value",ylabel="Rows")
for ax in axes:ax.legend(fontsize=8)
figure(OUT,"shift_scaler")
pd.DataFrame({"fixed":z_current,"refit":z_refit}).to_csv(OUT/"shift_scaler.csv",index=False)
report(OUT,"shift_scaler",{"training_mean":float(z_train.mean()),
    "current_fixed_mean":float(z_current.mean()),"current_refit_mean":float(z_refit.mean())})
