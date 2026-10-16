from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
f = pd.read_csv(DATA/"linear.csv")
x,y = f.x.to_numpy(),f.y.to_numpy()
theta = np.array([.4,-.2])
def loss(t):
    return np.mean((t[0]*x+t[1]-y)**2)
e = theta[0]*x+theta[1]-y
analytic = np.array([2*np.mean(e*x),2*np.mean(e)])
rows=[]
for h in np.logspace(-1,-9,9):
    numeric=[]
    for j in range(2):
        delta=np.zeros(2); delta[j]=h
        numeric.append((loss(theta+delta)-loss(theta-delta))/(2*h))
    rows.append({"h":h,"max_abs_error":float(np.max(
        np.abs(np.array(numeric)-analytic)))})
r=pd.DataFrame(rows);r.to_csv(OUT/"gradient_check.csv",index=False)
plt.loglog(r.h,np.maximum(r.max_abs_error,1e-16),"ko-")
plt.xlabel("Finite difference step h");plt.ylabel("Maximum absolute error")
plt.title("Analytic gradient versus central difference")
figure(OUT,"gradient_check")
report(OUT,"gradient_check",{"analytic_dw":analytic[0],
    "analytic_db":analytic[1],"min_abs_error":r.max_abs_error.min()})
assert r.max_abs_error.min() < 1e-6
