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
f=pd.read_csv(DATA/"wine.csv");X=f.drop(columns="target");y=f.target
pool,va=train_test_split(np.arange(len(f)),test_size=.3,stratify=y,random_state=42)
rng=np.random.default_rng(42);ordered=[]
# Stratified prefixes ensure every class is represented at small sizes.
by_class=[rng.permutation(pool[y.iloc[pool].to_numpy()==c]) for c in sorted(y.unique())]
for group in zip(*[list(a)+[None]*(max(map(len,by_class))-len(a)) for a in by_class]):
    ordered.extend([i for i in group if i is not None])
rows=[]
for size in [18,36,60,90,len(pool)]:
    tr=np.array(ordered[:size])
    m=make_pipeline(StandardScaler(),MLPClassifier(hidden_layer_sizes=(12,),
        solver="lbfgs",alpha=.2,max_iter=2000,random_state=42))
    m.fit(X.iloc[tr],y.iloc[tr])
    rows.append({"train_n":len(tr),"train_accuracy":accuracy_score(y.iloc[tr],m.predict(X.iloc[tr])),
        "validation_accuracy":accuracy_score(y.iloc[va],m.predict(X.iloc[va]))})
r=pd.DataFrame(rows);r.to_csv(OUT/"mlp_learning_curve.csv",index=False)
plt.plot(r.train_n,r.train_accuracy,"ko-",label="Train")
plt.plot(r.train_n,r.validation_accuracy,"ks--",label="Validation")
plt.xlabel("Training rows");plt.ylabel("Accuracy");plt.ylim(0,1.03);plt.legend()
figure(OUT,"mlp_learning_curve");report(OUT,"mlp_learning_curve",{"validation_n":len(va),"curve":rows})
