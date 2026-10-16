from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
import platform, sklearn
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
frame = pd.read_csv(DATA / "wine.csv")
X, y = frame.drop(columns="target"), frame["target"]
rows = []
for seed in range(10):
    a,b = train_test_split(np.arange(len(X)),test_size=.3,
        stratify=y,random_state=seed)
    model = make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000))
    model.fit(X.iloc[a],y.iloc[a])
    rows.append({"seed":seed,"accuracy":accuracy_score(y.iloc[b],
        model.predict(X.iloc[b]))})
result = pd.DataFrame(rows)
result.to_csv(OUT/"seed_sensitivity.csv",index=False)
plt.plot(result.seed,result.accuracy,"o-",color="black")
plt.xlabel("Split seed"); plt.ylabel("Test accuracy")
plt.ylim(0,1.03); plt.title("Same procedure, different splits")
figure(OUT,"seed_sensitivity")
report(OUT,"seed_sensitivity",{"python":platform.python_version(),
    "sklearn":sklearn.__version__,"accuracy_mean":result.accuracy.mean(),
    "accuracy_std_ddof1":result.accuracy.std(ddof=1)})
