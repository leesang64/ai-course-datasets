from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
f=pd.read_csv(DATA/"housing.csv");X=f.drop(columns="price");y=f.price
tr,te=train_test_split(np.arange(len(f)),test_size=.25,random_state=42)
model=make_pipeline(SimpleImputer(strategy="median"),StandardScaler(),Ridge(alpha=1))
model.fit(X.iloc[tr],y.iloc[tr]);pred=model.predict(X.iloc[te]);true=y.iloc[te].to_numpy()
residual=true-pred
pd.DataFrame({"row":te,"true":true,"pred":pred,"residual":residual}).to_csv(
    OUT/"regression_residual.csv",index=False)
fig,axes=plt.subplots(1,2,figsize=(7.2,3.6))
axes[0].scatter(true,pred,s=10,facecolors="none",edgecolors="black")
lims=[min(true.min(),pred.min()),max(true.max(),pred.max())]
axes[0].plot(lims,lims,"k--");axes[0].set(xlabel="Observed",ylabel="Predicted")
axes[1].scatter(pred,residual,s=10,facecolors="none",edgecolors="black")
axes[1].axhline(0,color="black",ls="--")
axes[1].set(xlabel="Predicted",ylabel="Observed - predicted")
for ax in axes:
    ax.ticklabel_format(style="sci",axis="both",scilimits=(0,0))
figure(OUT,"regression_residual")
report(OUT,"regression_residual",{"test_n":len(te),"MAE":mean_absolute_error(true,pred),
    "RMSE":float(np.sqrt(mean_squared_error(true,pred))),"R2":r2_score(true,pred)})
