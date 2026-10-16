from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
from sklearn.cluster import KMeans,DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import adjusted_rand_score,silhouette_score
f=pd.read_csv(DATA/"moons.csv");X=StandardScaler().fit_transform(f[["x1","x2"]])
models={"KMeans":KMeans(n_clusters=2,random_state=42,n_init=10),
    "DBSCAN":DBSCAN(eps=.28,min_samples=5)}
fig,axes=plt.subplots(1,2,figsize=(7.2,3.5));metrics={}
for ax,(name,m) in zip(axes,models.items()):
    labels=m.fit_predict(X)
    for i,c in enumerate(np.unique(labels)):
        mask=labels==c
        ax.scatter(X[mask,0],X[mask,1],marker=["x","o","s","^"][i%4],
            c="black",s=12,label=f"Group {c}")
    keep=labels!=-1;valid=np.unique(labels[keep])
    sil=float(silhouette_score(X[keep],labels[keep])) if 1<len(valid)<keep.sum() else None
    metrics[name]={"ARI":adjusted_rand_score(f.target,labels),
        "noise_n":int((labels==-1).sum()),"silhouette_without_noise":sil}
    ax.set(title=name,xlabel="Scaled x1",ylabel="Scaled x2");ax.legend(fontsize=7)
    pd.DataFrame({"label":labels}).to_csv(OUT/f"{name}_labels.csv",index=False)
figure(OUT,"clustering_compare");report(OUT,"clustering_compare",metrics)
