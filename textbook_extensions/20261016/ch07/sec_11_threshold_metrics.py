from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix,accuracy_score,precision_score,recall_score,f1_score
f=pd.read_csv(DATA/"wine.csv");X=f.drop(columns="target");y=(f.target==0).astype(int)
tr,va=train_test_split(np.arange(len(f)),test_size=.3,stratify=y,random_state=42)
m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000))
m.fit(X.iloc[tr],y.iloc[tr]);p=m.predict_proba(X.iloc[va])[:,1];truth=y.iloc[va]
rows=[]
for threshold in np.linspace(.05,.95,19):
    pred=(p>=threshold).astype(int);tn,fp,fn,tp=confusion_matrix(truth,pred,labels=[0,1]).ravel()
    rows.append({"threshold":threshold,"TN":int(tn),"FP":int(fp),"FN":int(fn),"TP":int(tp),
        "Accuracy":accuracy_score(truth,pred),"Precision":precision_score(truth,pred,zero_division=0),
        "Recall":recall_score(truth,pred,zero_division=0),"F1":f1_score(truth,pred,zero_division=0)})
r=pd.DataFrame(rows);r.to_csv(OUT/"threshold_metrics.csv",index=False)
for col,style in zip(["Precision","Recall","F1"],["-","--",":"]):
    plt.plot(r.threshold,r[col],style,color="black",label=col)
plt.ylim(0,1.03);plt.xlabel("Probability threshold");plt.ylabel("Metric");plt.legend()
figure(OUT,"threshold_metrics")
base=next(row for row in rows if np.isclose(row["threshold"],.5))
report(OUT,"threshold_metrics",{"validation_n":len(va),"positive_definition":"wine target == 0",
    "at_threshold_0.5":base})
assert base["TN"]+base["FP"]+base["FN"]+base["TP"]==len(va)
