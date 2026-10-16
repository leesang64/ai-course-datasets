from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
image=pd.read_csv(DATA/"image.csv").to_numpy()
kernel=np.array([[-1,0,1],[-2,0,2],[-1,0,1]],float)
# CNN libraries usually implement cross-correlation without kernel reversal.
windows=np.lib.stride_tricks.sliding_window_view(image,(3,3))
feature=np.einsum("ijab,ab->ij",windows,kernel)
activated=np.maximum(feature,0)
pooled=activated.reshape(5,2,5,2).max(axis=(1,3))
fig,axes=plt.subplots(1,3,figsize=(7.2,3.1))
for ax,a,title in zip(axes,[image,feature,pooled],
    ["Input 12 x 12","Correlation 10 x 10","ReLU + pool 5 x 5"]):
    im=ax.imshow(a,cmap="gray");ax.set_title(title,fontsize=9)
    ax.set(xlabel="Column",ylabel="Row");fig.colorbar(im,ax=ax,shrink=.65)
figure(OUT,"convolution")
pd.DataFrame(feature).to_csv(OUT/"convolution_feature.csv",index=False)
pd.DataFrame(pooled).to_csv(OUT/"convolution_pooled.csv",index=False)
report(OUT,"convolution",{"input_shape":list(image.shape),
    "feature_shape":list(feature.shape),"pooled_shape":list(pooled.shape),
    "kernel":kernel.tolist(),"stride":1,"padding":0})
assert feature.shape==(10,10) and pooled.shape==(5,5)
