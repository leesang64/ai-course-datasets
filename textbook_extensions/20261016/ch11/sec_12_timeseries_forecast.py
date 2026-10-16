from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error,mean_absolute_error
f=pd.read_csv(DATA/"series.csv");values=f.signal.to_numpy();lag=12
X=np.lib.stride_tricks.sliding_window_view(values,lag)[:-1].copy()
y=values[lag:];target_t=f.t.to_numpy()[lag:]
cut=int(len(X)*.75)
m=make_pipeline(StandardScaler(),Ridge(alpha=1))
m.fit(X[:cut],y[:cut]);pred=m.predict(X[cut:]);baseline=X[cut:,-1]
rows=pd.DataFrame({"t":target_t[cut:],"true":y[cut:],"ridge":pred,"persistence":baseline})
rows.to_csv(OUT/"timeseries_forecast.csv",index=False)
plt.plot(rows.t,rows.true,"k-",label="Observed")
plt.plot(rows.t,rows.ridge,"k--",label="Lag Ridge")
plt.plot(rows.t,rows.persistence,color=".6",ls=":",label="Persistence")
plt.xlabel("Target time index");plt.ylabel("Signal (unitless)");plt.legend(fontsize=9)
figure(OUT,"timeseries_forecast")
metrics={name:{"RMSE":float(np.sqrt(mean_squared_error(rows.true,rows[name]))),
    "MAE":mean_absolute_error(rows.true,rows[name])} for name in ["ridge","persistence"]}
report(OUT,"timeseries_forecast",{"train_windows":cut,"test_windows":len(rows),"metrics":metrics})
assert target_t[cut-1]<target_t[cut]
