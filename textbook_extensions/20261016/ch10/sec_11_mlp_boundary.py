from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
f=pd.read_csv(DATA/"moons.csv");X=f[["x1","x2"]];y=f.target
tr,te=train_test_split(np.arange(len(f)),test_size=.3,stratify=y,random_state=42)
g0,g1=np.meshgrid(np.linspace(-1.5,2.5,130),np.linspace(-1,1.7,100))
grid=pd.DataFrame({"x1":g0.ravel(),"x2":g1.ravel()})
fig,axes=plt.subplots(1,2,figsize=(7.2,3.5));metrics={}
for ax,width in zip(axes,[2,20]):
    m=make_pipeline(StandardScaler(),MLPClassifier(hidden_layer_sizes=(width,),
        solver="lbfgs",max_iter=3000,alpha=.1,random_state=42))
    m.fit(X.iloc[tr],y.iloc[tr]);p=m.predict_proba(grid)[:,1].reshape(g0.shape)
    ax.contourf(g0,g1,p,levels=[0,.5,1],colors=[".92",".6"])
    ax.contour(g0,g1,p,levels=[.5],colors="black",linewidths=1)
    for c,marker in [(0,"o"),(1,"x")]:
        sel=y.iloc[te].to_numpy()==c
        ax.scatter(X.iloc[te,0][sel],X.iloc[te,1][sel],s=16,marker=marker,c="black")
    ax.set(title=f"Hidden units: {width}",xlabel="x1",ylabel="x2")
    metrics[str(width)]={"test_accuracy":accuracy_score(y.iloc[te],m.predict(X.iloc[te])),
        "iterations":int(m[-1].n_iter_)}
figure(OUT,"mlp_boundary");report(OUT,"mlp_boundary",metrics)
