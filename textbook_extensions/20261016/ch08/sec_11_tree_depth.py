from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier,plot_tree
from sklearn.metrics import accuracy_score
f=pd.read_csv(DATA/"wine.csv");X=f.drop(columns="target");y=f.target
tr,va=train_test_split(np.arange(len(f)),test_size=.3,stratify=y,random_state=42)
rows=[]
for depth in [1,2,3,4,6,None]:
    m=DecisionTreeClassifier(max_depth=depth,random_state=42)
    m.fit(X.iloc[tr],y.iloc[tr])
    rows.append({"depth_label":str(depth),"nodes":m.tree_.node_count,
        "train_accuracy":accuracy_score(y.iloc[tr],m.predict(X.iloc[tr])),
        "validation_accuracy":accuracy_score(y.iloc[va],m.predict(X.iloc[va]))})
r=pd.DataFrame(rows);r.to_csv(OUT/"tree_depth.csv",index=False)
plt.plot(range(len(r)),r.train_accuracy,"ko-",label="Train")
plt.plot(range(len(r)),r.validation_accuracy,"ks--",label="Validation")
plt.xticks(range(len(r)),r.depth_label);plt.ylim(0,1.03)
plt.xlabel("Maximum depth (None: unrestricted)");plt.ylabel("Accuracy");plt.legend()
figure(OUT,"tree_depth")
small=DecisionTreeClassifier(max_depth=2,random_state=42).fit(X.iloc[tr],y.iloc[tr])
plt.figure(figsize=(9,4.5))
plot_tree(small,feature_names=X.columns,class_names=["0","1","2"],
    filled=False,rounded=False,fontsize=11,impurity=True)
figure(OUT,"tree_structure")
report(OUT,"tree_depth",{"validation_n":len(va),"comparison":rows})
