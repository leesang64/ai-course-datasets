from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
f=pd.read_csv(DATA/"wine.csv");X=f.drop(columns="target")
tr,te=train_test_split(np.arange(len(f)),test_size=.3,random_state=42)
scale=StandardScaler().fit(X.iloc[tr]);a=scale.transform(X.iloc[tr]);b=scale.transform(X.iloc[te])
full=PCA().fit(a);cumulative=np.cumsum(full.explained_variance_ratio_)
rows=[]
for components in [1,2,3,5,8,13]:
    m=PCA(n_components=components).fit(a)
    reconstructed=m.inverse_transform(m.transform(b))
    rows.append({"components":components,"scaled_test_mse":float(np.mean((b-reconstructed)**2))})
r=pd.DataFrame(rows);r.to_csv(OUT/"pca_reconstruction.csv",index=False)
fig,axes=plt.subplots(1,2,figsize=(7.2,3.5))
axes[0].plot(range(1,14),cumulative,"ko-")
axes[0].set(xlabel="Components",ylabel="Training cumulative variance",ylim=(0,1.03))
axes[1].plot(r.components,r.scaled_test_mse,"ks-")
axes[1].set(xlabel="Components",ylabel="Test reconstruction MSE")
figure(OUT,"pca_reconstruction")
report(OUT,"pca_reconstruction",{"train_n":len(tr),"test_n":len(te),
    "variance_first2":cumulative[1],"reconstruction":rows})
