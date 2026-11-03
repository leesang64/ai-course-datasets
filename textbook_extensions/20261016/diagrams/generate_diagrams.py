from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,FancyArrowPatch
import xml.etree.ElementTree as ET
import json
OUT=Path(__file__).resolve().parent;OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none'})
def draw(name,title,nodes,edges,notes,mmd):
 fig,ax=plt.subplots(figsize=(9,4.8));ax.set(xlim=(0,10),ylim=(0,5));ax.axis('off')
 ax.text(5,4.8,title,ha='center',fontsize=13,weight='bold')
 mx=ET.Element('mxfile',host='app.diagrams.net');dg=ET.SubElement(mx,'diagram',name=name);gm=ET.SubElement(dg,'mxGraphModel');root=ET.SubElement(gm,'root');ET.SubElement(root,'mxCell',id='0');ET.SubElement(root,'mxCell',id='1',parent='0')
 for id,(x,y,w,h,label) in nodes.items():
  ax.add_patch(Rectangle((x,y),w,h,facecolor='white',edgecolor='black',lw=1.2));ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=12)
  c=ET.SubElement(root,'mxCell',id=id,value=label,style='rounded=0;whiteSpace=wrap;html=0;fillColor=#ffffff;strokeColor=#000000;fontColor=#000000;fontSize=16;',vertex='1',parent='1');ET.SubElement(c,'mxGeometry',x=str(x*120),y=str((5-y-h)*120),width=str(w*120),height=str(h*120),attrib={'as':'geometry'})
 for i,(a,b,style,label,side) in enumerate(edges):
  xa,ya,wa,ha,_=nodes[a];xb,yb,wb,hb,_=nodes[b]
  if side=='v':p=(xa+wa/2,ya);q=(xb+wb/2,yb+hb)
  else:p=(xa+wa,ya+ha/2);q=(xb,yb+hb/2)
  ax.add_patch(FancyArrowPatch(p,q,arrowstyle='->',mutation_scale=10,color='black',linestyle=style,connectionstyle='arc3,rad=0',lw=1.1))
  if label:ax.text((p[0]+q[0])/2,(p[1]+q[1])/2+.13,label,ha='center',va='bottom',fontsize=8.5,bbox=dict(facecolor="white",edgecolor="none",pad=1))
  c=ET.SubElement(root,'mxCell',id='e'+str(i),value=label,edge='1',parent='1',source=a,target=b,style='endArrow=classic;html=0;strokeColor=#000000;'+('dashed=1;' if style=='--' else ''));ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
 for y,text in notes:ax.text(.15,y,text,fontsize=11,ha='left',va='top')
 fig.subplots_adjust(left=.02,right=.98,bottom=.02,top=.98)
 fig.savefig(OUT/(name+'.png'),dpi=400,facecolor='white');fig.savefig(OUT/(name+'.svg'));plt.close(fig)
 ET.ElementTree(mx).write(OUT/(name+'.drawio'),encoding='utf-8',xml_declaration=True)
 (OUT/(name+'.mmd')).write_text(mmd)
 (OUT/(name+'.json')).write_text(json.dumps({'nodes':nodes,'edges':edges,'notes':notes},indent=2))
draw('ch11_tensor_flow','CNN and LSTM are independent paths',{
 'A':(.1,3.3,1.5,.85,'Image\n(4,1,28,28)'), 'B':(2.15,3.3,1.6,.85,'Conv2d + BN\nReLU\n(4,16,28,28)'), 'C':(4.35,3.3,1.45,.85,'MaxPool2d(2)\n(4,16,14,14)'), 'D':(6.4,3.3,1.35,.85,'flatten(1)\n(4,3136)'), 'E':(8.35,3.3,1.5,.85,'Linear\n3136 to 10\n(4,10) logits'),
 'F':(.1,1.7,1.5,.85,'Sequence\n(4,20,5)'), 'G':(2.15,1.7,2.1,.85,'LSTM(5,16)\nbatch_first=True\noutput: (4,20,16)'), 'H':(5.05,1.7,2.1,.85,'output[:, -1, :]\nlast time step\n(4,16)'), 'I':(8.05,1.7,1.8,.85,'Linear(16,3)\n(4,3) logits')},
 [('A','B','-','','h'),('B','C','-','','h'),('C','D','-','','h'),('D','E','-','','h'),('F','G','-','','h'),('G','H','-','','h'),('H','I','-','','h')],
 [(.95,'Conv2d: kernel=3, stride=1, padding=1. Pool: kernel=stride=2.'),(.6,'4 = batch size. Logits are unnormalized scores. No training or accuracy is shown.'),(.25,'CPU forward dimensions verified on 2026-11-03. No model training was performed.')],
 'flowchart TD\n subgraph CNN\n A["Image (4,1,28,28)"] --> B["Conv2d BN ReLU (4,16,28,28)"]\n B --> C["MaxPool (4,16,14,14)"] --> D["flatten(1) (4,3136)"] --> E["Linear (4,10) logits"]\n end\n subgraph LSTM\n F["Sequence (4,20,5)"] --> G["LSTM output (4,20,16)"]\n G --> H["Last time step (4,16)"] --> I["Linear (4,3) logits"]\n end\n')
draw('ch05_preprocessing_flow','Fit preprocessing on training data only',{
 'A':(.1,3.15,1.45,1.0,'X, y\n4 input fields\n80:20 split'), 'B':(2.35,3.15,1.55,1.,'X_train\nfit_transform'), 'C':(4.8,3.15,2.05,1.,'ColumnTransformer\nMedian + scale\nMode + OHE'), 'D':(8.05,3.15,1.8,1.,'Train array\n(n_train,p_out)\nfeature names'),
 'E':(2.35,1.35,1.55,1.,'X_test\ntransform only'), 'F':(4.8,1.35,2.05,1.,'Reuse fitted\nmedians, modes,\nscales, categories'), 'G':(8.05,1.35,1.8,1.,'Test array\n(n_test,p_out)\nsame feature\norder')},
 [('A','B','-','train','h'),('B','C','-','','h'),('C','D','-','','h'),('A','E','-','test','h'),('E','F','-','','h'),('F','G','-','','h'),('C','F','--','state','v')],
 [(.8,'Numeric fields: age, income. Categorical fields: gender, city. Target y is excluded.'),(.45,'OHE = OneHotEncoder(handle_unknown="ignore"). p_out depends on fitted categories.'),(.1,'No estimator fit or prediction exists in the main ch05 code. Input: 100 synthetic practice rows; no classifier is fitted here.')],
 'flowchart TD\n A["X y split 80:20"] --> B["X_train fit_transform"]\n A --> E["X_test transform only"]\n B --> C["Numeric median scale and category mode one hot"]\n C --> D["Train array feature names"]\n C -. "fitted state" .-> F["Reuse learned statistics and categories"]\n E --> F --> G["Test array same feature\norder"]\n')
assert 16*14*14==3136
assert ((28+2-1*(3-1)-1)//1+1)==28
assert ((28-2)//2+1)==14
print(OUT)
