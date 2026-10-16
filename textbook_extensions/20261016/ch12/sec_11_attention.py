from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
Q=pd.read_csv(DATA/"queries.csv").to_numpy()
K=pd.read_csv(DATA/"keys.csv").to_numpy()
V=np.array([[1,0],[0,1],[1,1],[-1,1]],float)
logits=Q@K.T/np.sqrt(K.shape[1])
stable=logits-logits.max(axis=1,keepdims=True)
weights=np.exp(stable);weights/=weights.sum(axis=1,keepdims=True)
output=weights@V
fig,axes=plt.subplots(1,2,figsize=(7.2,3.6))
for ax,a,title in zip(axes,[weights,output],["Attention weights (3 x 4)","Weighted values (3 x 2)"]):
    im=ax.imshow(a,cmap="gray",aspect="auto");ax.set_title(title,fontsize=10)
    ax.set(xlabel="Key / output dimension",ylabel="Query")
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            ax.text(j,i,f"{a[i,j]:.2f}",ha="center",va="center",
                color="white" if a[i,j]<a.mean() else "black",fontsize=9)
    fig.colorbar(im,ax=ax,shrink=.7)
figure(OUT,"attention")
pd.DataFrame(weights).to_csv(OUT/"attention_weights.csv",index=False)
pd.DataFrame(output).to_csv(OUT/"attention_output.csv",index=False)
report(OUT,"attention",{"Q_shape":list(Q.shape),"K_shape":list(K.shape),
    "V_shape":list(V.shape),"row_sums":weights.sum(axis=1).tolist(),
    "output_shape":list(output.shape)})
assert np.allclose(weights.sum(axis=1),1) and output.shape==(3,2)
