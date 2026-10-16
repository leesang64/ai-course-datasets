from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
f=pd.read_csv(DATA/"serving.csv");features=["x0","x1","x2"]
tr,te=train_test_split(np.arange(len(f)),test_size=.3,random_state=42)
m=make_pipeline(StandardScaler(),Ridge(alpha=.1))
m.fit(f.iloc[tr][features],f.target.iloc[tr])
path=OUT/"model_roundtrip.joblib";joblib.dump({"features":features,"model":m},path)
loaded=joblib.load(path)  # Load only this trusted, locally created artifact.
def predict(frame):
    missing=set(loaded["features"])-set(frame.columns)
    if missing:raise ValueError(f"Missing fields: {sorted(missing)}")
    values=frame[loaded["features"]]
    if not np.isfinite(values.to_numpy(dtype=float)).all():
        raise ValueError("Input contains non-finite values")
    return loaded["model"].predict(values)
a=m.predict(f.iloc[te][features]);b=predict(f.iloc[te])
try:
    predict(f.iloc[te].drop(columns="x1"))
except ValueError as error:
    rejected=str(error)
else:raise AssertionError("Missing input was not rejected")
pd.DataFrame({"row":te,"true":f.target.iloc[te].to_numpy(),"before":a,"after":b}).to_csv(
    OUT/"model_roundtrip.csv",index=False)
plt.scatter(a,b,s=12,facecolors="none",edgecolors="black")
lo,hi=min(a),max(a);plt.plot([lo,hi],[lo,hi],"k--")
plt.xlabel("Before save");plt.ylabel("After reload");plt.title("Prediction round trip")
figure(OUT,"model_roundtrip")
report(OUT,"model_roundtrip",{"test_n":len(te),"max_abs_diff":float(np.max(np.abs(a-b))),
    "test_RMSE":float(np.sqrt(mean_squared_error(f.target.iloc[te],b))),"missing_field_rejected":rejected})
assert np.allclose(a,b)
