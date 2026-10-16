from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, adjusted_rand_score
frame = pd.read_csv(DATA / "wine.csv")
X = frame.drop(columns="target")
y = frame["target"]
train, test = train_test_split(np.arange(len(X)), test_size=.3,
    stratify=y, random_state=42)
clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
clf.fit(X.iloc[train], y.iloc[train])
pred = clf.predict(X.iloc[test])
cluster = make_pipeline(StandardScaler(), KMeans(n_clusters=3,
    random_state=42, n_init=10))
cluster.fit(X.iloc[train])
groups = cluster.predict(X.iloc[test])
metrics = {"test_n":len(test), "accuracy":accuracy_score(y.iloc[test],pred),
    "cluster_ARI":adjusted_rand_score(y.iloc[test],groups)}
fig, axes = plt.subplots(1,2,figsize=(7.2,3.5))
for ax, labels, title in zip(axes,[pred,groups],["Supervised", "Unsupervised"]):
    for c, marker in enumerate(["o","s","^"]):
        mask = labels == c
        ax.scatter(X.iloc[test,0][mask],X.iloc[test,1][mask],
            marker=marker,facecolors="none",edgecolors="black",label=str(c))
    ax.set(xlabel="Alcohol",ylabel="Malic acid",title=title)
    ax.legend(fontsize=8)
figure(OUT,"learning_modes")
pd.DataFrame({"row":test,"true":y.iloc[test].to_numpy(),
    "pred":pred,"cluster":groups}).to_csv(OUT/"learning_modes.csv",index=False)
report(OUT,"learning_modes",metrics)
