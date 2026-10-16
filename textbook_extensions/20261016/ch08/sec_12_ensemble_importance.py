from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import accuracy_score
f=pd.read_csv(DATA/"wine.csv");X=f.drop(columns="target");y=f.target
tr,te=train_test_split(np.arange(len(f)),test_size=.3,stratify=y,random_state=42)
models={"RandomForest":RandomForestClassifier(n_estimators=100,random_state=42,n_jobs=1),
    "GradientBoosting":GradientBoostingClassifier(random_state=42)}
metrics={}
for name,m in models.items():
    m.fit(X.iloc[tr],y.iloc[tr])
    metrics[name]=accuracy_score(y.iloc[te],m.predict(X.iloc[te]))
rf=models["RandomForest"]
imp=permutation_importance(rf,X.iloc[te],y.iloc[te],scoring="accuracy",
    n_repeats=10,random_state=42,n_jobs=1)
r=pd.DataFrame({"feature":X.columns,"mean_drop":imp.importances_mean,
    "std_drop":imp.importances_std}).sort_values("mean_drop")
r.to_csv(OUT/"ensemble_importance.csv",index=False)
plt.barh(r.feature,r.mean_drop,xerr=r.std_drop,color=".7",edgecolor="black")
plt.xlabel("Accuracy decrease after permutation");plt.title("Held-out permutation importance")
figure(OUT,"ensemble_importance")
report(OUT,"ensemble_importance",{"test_n":len(te),"accuracy":metrics})
