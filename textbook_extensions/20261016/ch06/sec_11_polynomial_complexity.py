from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures,StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
f=pd.read_csv(DATA/"nonlinear.csv");X=f[["x"]];y=f.y
tr,va=train_test_split(np.arange(len(f)),test_size=.35,random_state=42)
rows=[];grid=pd.DataFrame({"x":np.linspace(-3,3,200)})
fig,axes=plt.subplots(1,2,figsize=(7.2,3.7))
axes[0].scatter(X.iloc[tr,0],y.iloc[tr],s=12,facecolors="none",edgecolors="black")
for degree,style in zip([1,3,12],["-","--",":"]):
    model=make_pipeline(PolynomialFeatures(degree,include_bias=False),
        StandardScaler(),Ridge(alpha=.01))
    model.fit(X.iloc[tr],y.iloc[tr])
    rows.append({"degree":degree,"train_mse":mean_squared_error(y.iloc[tr],model.predict(X.iloc[tr])),
        "validation_mse":mean_squared_error(y.iloc[va],model.predict(X.iloc[va]))})
    axes[0].plot(grid.x,model.predict(grid),style,color="black",label=f"Degree {degree}")
r=pd.DataFrame(rows);r.to_csv(OUT/"polynomial_complexity.csv",index=False)
axes[0].set(xlabel="x",ylabel="y",ylim=(-2.5,2.5));axes[0].legend(fontsize=8)
axes[1].plot(r.degree,r.train_mse,"ko-",label="Train")
axes[1].plot(r.degree,r.validation_mse,"ks--",label="Validation")
axes[1].set(xlabel="Degree",ylabel="MSE");axes[1].legend(fontsize=8)
figure(OUT,"polynomial_complexity")
report(OUT,"polynomial_complexity",{"train_n":len(tr),"validation_n":len(va),
    "comparison":rows})
