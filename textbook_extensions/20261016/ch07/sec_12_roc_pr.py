from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve,precision_recall_curve,roc_auc_score,average_precision_score,brier_score_loss
from sklearn.calibration import calibration_curve
f=pd.read_csv(DATA/"wine.csv");X=f.drop(columns="target");y=(f.target==0).astype(int)
tr,te=train_test_split(np.arange(len(f)),test_size=.3,stratify=y,random_state=24)
m=make_pipeline(StandardScaler(),LogisticRegression(C=.1,max_iter=1000))
m.fit(X.iloc[tr],y.iloc[tr]);p=m.predict_proba(X.iloc[te])[:,1];truth=y.iloc[te]
fpr,tpr,_=roc_curve(truth,p);precision,recall,_=precision_recall_curve(truth,p)
obs,prob=calibration_curve(truth,p,n_bins=5,strategy="uniform")
fig,axes=plt.subplots(1,3,figsize=(7.5,3.1))
axes[0].plot(fpr,tpr,"k-");axes[0].plot([0,1],[0,1],"k:")
axes[0].set(xlabel="False positive rate",ylabel="True positive rate",title="ROC")
axes[1].step(recall,precision,where="post",color="black")
axes[1].axhline(truth.mean(),color=".5",ls=":")
axes[1].set(xlabel="Recall",ylabel="Precision",title="PR")
axes[2].plot(prob,obs,"ko-");axes[2].plot([0,1],[0,1],"k:")
axes[2].set(xlabel="Mean probability",ylabel="Positive fraction",title="Calibration")
figure(OUT,"roc_pr")
pd.DataFrame({"true":truth.to_numpy(),"probability":p}).to_csv(OUT/"roc_pr.csv",index=False)
report(OUT,"roc_pr",{"test_n":len(te),"prevalence":truth.mean(),
    "ROC_AUC":roc_auc_score(truth,p),"AP":average_precision_score(truth,p),
    "Brier":brier_score_loss(truth,p)})
