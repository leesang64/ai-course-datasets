from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
frame = pd.read_csv(DATA / "linear.csv")
x,y = frame.x.to_numpy(),frame.y.to_numpy()
w,b = 0.,0.
rows = []
for epoch in range(80):
    error = w*x+b-y
    loss = np.mean(error**2)
    rows.append({"epoch":epoch,"w":w,"b":b,"mse":loss})
    dw,db = 2*np.mean(error*x),2*np.mean(error)
    w -= .06*dw
    b -= .06*db
history = pd.DataFrame(rows)
history.to_csv(OUT/"gradient_descent.csv",index=False)
fig,axes=plt.subplots(1,2,figsize=(7.2,3.4))
axes[0].scatter(x,y,s=12,facecolors="none",edgecolors="black")
axes[0].plot(x,w*x+b,"k-")
axes[0].set(xlabel="x",ylabel="y",title="Fitted line")
axes[1].plot(history.epoch,history.mse,"k-")
axes[1].set(xlabel="Update step",ylabel="Training MSE",title="Loss history")
figure(OUT,"gradient_descent")
report(OUT,"gradient_descent",{"w":w,"b":b,
    "initial_mse":float(history.mse.iloc[0]),
    "final_mse":float(np.mean((w*x+b-y)**2))})
