from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,f1_score
f=pd.read_csv(DATA/"churn.csv")
f["total_charge"]=pd.to_numeric(f.total_charge,errors="coerce")
num=["age","tenure","monthly_charge","total_charge"]
cat=["contract","internet","support","ebilling"]
X,y=f[num+cat],f.churn.astype(int)
train,test=train_test_split(np.arange(len(f)),test_size=.3,
    stratify=y,random_state=42)
pre=ColumnTransformer([
    ("num",Pipeline([("fill",SimpleImputer(strategy="median")),
        ("scale",StandardScaler())]),num),
    ("cat",Pipeline([("fill",SimpleImputer(strategy="most_frequent")),
        ("onehot",OneHotEncoder(handle_unknown="ignore"))]),cat)])
model=Pipeline([("pre",pre),("clf",LogisticRegression(max_iter=1000))])
model.fit(X.iloc[train],y.iloc[train]);pred=model.predict(X.iloc[test])
names=model["pre"].get_feature_names_out();coef=model["clf"].coef_[0]
order=np.argsort(np.abs(coef))[-10:]
pd.DataFrame({"feature":names,"coefficient":coef}).to_csv(
    OUT/"mixed_pipeline.csv",index=False)
plt.barh(range(len(order)),coef[order],color=".7",edgecolor="black")
plt.yticks(range(len(order)),[f"F{i}" for i in order],fontsize=10)
plt.xlabel("Logistic coefficient");plt.title("Largest absolute coefficients")
figure(OUT,"mixed_pipeline")
report(OUT,"mixed_pipeline",{"train_n":len(train),"test_n":len(test),
    "transformed_features":len(names),"figure_feature_codes":{f"F{i}":str(names[i]) for i in order},"accuracy":accuracy_score(y.iloc[test],pred),
    "f1":f1_score(y.iloc[test],pred,zero_division=0)})
