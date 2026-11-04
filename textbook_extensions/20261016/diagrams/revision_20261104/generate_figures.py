"""본문 코드와 대조한 구조 명세로 흑백 도식을 재생성합니다. 학습 결과를 생성하는 프로그램은 아닙니다."""
from pathlib import Path
import io, json, math, xml.etree.ElementTree as ET
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
OUT=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'svg.fonttype':'none','svg.hashsalt':'ai-course-20261104'})
S=[]
def add(name,old,title,nodes,edges,notes,explanation,size=(9,3.8),groups=None):
 S.append(dict(name=name,old=old,title=title,nodes=nodes,edges=edges,notes=notes,explanation=explanation,size=size,groups=groups or []))
def node(x,y,label,w=2.6,h=.9):return [x,y,w,h,label]
# 각 장 개요는 본문 sec_07_main.py의 실제 구현만 나타냅니다.
add('ch01_overview',1,'Chapter 1 Environment and event intervals',{
 'A':node(.2,2.2,'Versions and device\nrandom seed 42'), 'B':node(3.7,2.2,'9 selected events\nYear column'), 'C':node(7.2,2.2,'Year tensor\nshape (9,)'), 'D':node(7.2,.6,'Consecutive gaps\nshape (8,)'), 'E':node(3.7,.6,'Mean and gap plot\n8 intervals')}, [('A','B',''),('B','C',''),('C','D',''),('D','E','')],['Event selection changes the intervals. No prediction model is trained.'], '버전·장치·시드를 기록한 뒤 사건 연도 9개를 텐서로 변환합니다. 이웃한 연도를 빼므로 간격은 8개입니다. 평균 간격과 막대그래프는 선택한 사건 목록의 특성이며 인공지능 발전 속도를 추정한 값이 아닙니다.')
add('ch02_overview',13,'Chapter 2 Full-batch gradient descent',{
 'A':node(.2,2.2,'X and y\n120 training rows'), 'B':node(3.7,2.2,'Prediction\nX * W + b'), 'C':node(7.2,2.2,'Mean squared error\nbackward()'), 'D':node(7.2,.6,'Update W and b\nclear gradients'), 'E':node(3.7,.6,'301 recorded losses\ntraining loss plot')}, [('A','B',''),('B','C',''),('C','D',''),('D','B','next step'),('D','E','record')],['The recorded loss is measured before the corresponding parameter update.'], '120행 전체를 사용하는 전체배치 경사하강법(Full Batch Gradient Descent)입니다. 예측·손실·역전파·갱신·기울기 초기화를 반복하며 갱신 전 손실을 301번 기록합니다. 검증 손실이나 테스트 성능을 그린 그림이 아닙니다.')
add('ch03_overview',16,'Chapter 3 A-star search and termination',{
 'A':node(.2,2.2,'Start A\npriority queue'), 'B':node(3.7,2.2,'Pop lowest f\nf = g + h'), 'C':node(7.2,2.2,'Goal reached?'), 'D':node(3.7,.6,'Expand neighbors\nupdate best cost'), 'E':node(7.2,.6,'Return path and cost\nor report no path')}, [('A','B',''),('B','C',''),('C','D','no'),('D','B','queue not empty'),('C','E','yes'),('D','E','queue empty')],['This supplied graph returns A to C to D with total cost 4.'], '후보 우선순위는 누적 비용 g와 휴리스틱 h의 합으로 정합니다. 목표를 꺼내면 경로와 비용을 반환하며 후보가 소진되어도 종료합니다. 제공 그래프의 결과는 A→C→D, 비용 4입니다. 이 결과 하나로 모든 휴리스틱의 최적성을 보장하지 않습니다.')
add('ch04_overview',19,'Chapter 4 Housing data exploration',{
 'A':node(.2,2.2,'Housing table\n900 rows'), 'B':node(3.7,2.2,'Shape and head\ndescriptive statistics'), 'C':node(7.2,2.2,'Numeric correlation\nmatrix'), 'D':node(3.7,.6,'Area and Price\nscatter and fitted line'), 'E':node(7.2,.6,'Two plots\nsummary metrics')}, [('A','B',''),('B','C',''),('A','D',''),('C','E',''),('D','E','')],['The fitted line describes the same observed rows; it is not a held-out evaluation.'], '900행 주택 자료의 형태·일부 행·기술통계와 수치형 열 간 상관을 확인합니다. 면적과 가격의 산점도에 같은 자료로 계산한 직선을 겹칩니다. 관측 단위와 실측 출처가 확인되지 않은 열에 임의의 단위를 붙이지 않습니다.')
add('ch05_overview',22,'Chapter 5 Fit on training data only',{
 'A':node(.2,2.2,'100 synthetic rows\nX without target'), 'B':node(3.7,2.2,'Training rows\nfit_transform'), 'C':node(7.2,2.2,'Learned medians\nscales and categories'), 'D':node(3.7,.6,'Test rows\ntransform only'), 'E':node(7.2,.6,'Same output columns\nmissing-value check')}, [('A','B','80 percent'),('A','D','20 percent'),('B','C',''),('C','E',''),('C','D','reuse state'),('D','E','')],['Target is excluded from X. This example does not fit a classifier.'], '목표 열을 입력에서 제외하고 층화 분할(Stratified Split)을 수행합니다. 수치형 결측 대치·표준화와 범주형 결측 대치·원 핫 인코딩의 기준은 훈련 행에서만 적합합니다. 테스트 행은 같은 기준으로 변환하며 이 주 실습에는 분류기 학습이 없습니다.')
add('ch06_overview',24,'Chapter 6 Regression on the same split',{
 'A':node(.2,2.2,'Housing X and Price\n80:20 split'), 'B':node(3.7,2.2,'Fit linear regression\nRidge and Lasso'), 'C':node(7.2,2.2,'Predict test rows\nno refit on test'), 'D':node(3.7,.6,'Ridge prediction\nand residual plots'), 'E':node(7.2,.6,'MAE RMSE and R2\ncompare same rows')}, [('A','B','train'),('B','C',''),('A','C','test'),('C','D',''),('C','E','')],['All model scores use the same held-out rows. Residual = actual minus predicted.'], '세 회귀 모델은 같은 훈련·테스트 행을 사용합니다. 평균절대오차(Mean Absolute Error, MAE), 평균제곱근오차(Root Mean Squared Error, RMSE), 결정계수(Coefficient of Determination, R2)를 같은 평가 행에서 비교합니다. 잔차는 실제값에서 예측값을 뺀 값입니다.')
add('ch07_overview',27,'Chapter 7 Classification and score meaning',{
 'A':node(.2,2.2,'Breast-cancer data\nstratified split'), 'B':node(3.7,2.2,'Training pipeline\nscale and logistic fit'), 'C':node(7.2,2.2,'Test predictions\nand P(class 1)'), 'D':node(3.7,.6,'Confusion matrix\ntrue rows, pred columns'), 'E':node(7.2,.6,'Classification report\nROC AUC')}, [('A','B','train'),('B','C',''),('A','C','test'),('C','D',''),('C','E','')],['In this supplied dataset: class 0 = malignant; class 1 = benign.'], '로지스틱 회귀(Logistic Regression)와 표준화를 파이프라인(Pipeline)으로 묶습니다. 혼동행렬의 행은 실제값, 열은 예측값입니다. 이 자료의 클래스 1은 양성 종양(Benign)이므로 양성 클래스(Positive Class)를 악성 종양으로 오해하면 지표의 의미가 뒤바뀝니다.')
add('ch08_overview',29,'Chapter 8 Compare two ensemble pipelines',{
 'A':node(.2,2.2,'Churn table\n75:25 split'), 'B':node(3.7,2.2,'Median imputer\nRandom Forest'), 'C':node(3.7,.6,'Median imputer\nGradient Boosting'), 'D':node(7.2,2.2,'Same test rows\nAccuracy and F1'), 'E':node(7.2,.6,'Forest feature\nimportance plot')}, [('A','B','train'),('A','C','train'),('B','D',''),('C','D',''),('B','E','')],['Each pipeline learns imputation on training rows. XGBoost is not run here.'], '랜덤 포레스트(Random Forest)와 기울기 부스팅(Gradient Boosting)은 각각 훈련 자료의 중앙값으로 결측을 처리합니다. 같은 테스트 행에서 정확도(Accuracy)와 F1 점수를 비교하며 중요도 그림은 랜덤 포레스트 모델의 값입니다. 이 주 실습에서 실행하지 않는 XGBoost의 성능을 포함하지 않습니다.')
add('ch09_overview',31,'Chapter 9 Two independent input paths',{
 'A':node(.2,2.2,'Cancer table\ntrain and test split'), 'B':node(3.7,2.2,'Scale and RBF SVC\nfit training rows'), 'C':node(7.2,2.2,'Held-out\nclassification accuracy'), 'D':node(.2,.6,'Customer features\nno class target'), 'E':node(3.7,.6,'Scale then PCA\n2 components'), 'F':node(7.2,.6,'K-Means on PCA\nclusters and silhouette')}, [('A','B',''),('B','C',''),('D','E',''),('E','F','')],['These are separate datasets. The customer path is exploratory, without a held-out test.'], '위 경로는 유방암 자료의 분류이고 아래 경로는 고객 자료의 탐색입니다. 고객 경로에서는 표준화 후 주성분 분석(Principal Component Analysis, PCA) 2차원에 케이평균 군집화(K-Means Clustering)를 적합합니다. 서로 다른 입력과 평가 목적을 가진 두 경로를 하나의 연속 학습으로 해석하지 않습니다.')
add('ch10_overview',33,'Chapter 10 XOR training only',{
 'A':node(.2,2.2,'Four XOR rows\nX shape (4,2)'), 'B':node(3.7,2.2,'Linear 2 to 8\nTanh, Linear 8 to 2'), 'C':node(7.2,2.2,'Cross-entropy loss\nbackward and Adam'), 'D':node(7.2,.6,'1001 updates\ntraining loss history'), 'E':node(3.7,.6,'Predict same four rows\ntraining accuracy')}, [('A','B',''),('B','C',''),('C','B','next step'),('C','D','record'),('D','E','')],['No separate validation or test set exists in this four-row demonstration.'], '배타적 논리합(Exclusive OR, XOR) 네 행으로 다층 퍼셉트론(Multilayer Perceptron, MLP)을 학습합니다. 입력 2개·은닉 8개·출력 2개이며 교차엔트로피(Cross Entropy)를 줄입니다. 같은 네 행의 정확도는 학습 정확도이고 일반화 성능이 아닙니다.')
add('ch11_overview',35,'Chapter 11 Independent forward passes',{
 'A':node(.2,2.2,'Random image batch\n(4,1,28,28)'), 'B':node(3.7,2.2,'Convolution and pool\nflatten, linear'), 'C':node(7.2,2.2,'Image scores\n(4,10)'), 'D':node(.2,.6,'Random sequence batch\n(4,20,5)'), 'E':node(3.7,.6,'LSTM last time step\nlinear projection'), 'F':node(7.2,.6,'Sequence scores\n(4,3)')}, [('A','B',''),('B','C',''),('D','E',''),('E','F','')],['Random-input forward passes only. No optimizer, model training or accuracy evaluation.'], '합성곱 신경망(Convolutional Neural Network, CNN)과 장단기 메모리(Long Short Term Memory, LSTM)는 별도의 입력을 받습니다. 숫자 4는 배치 크기이고 10과 3은 출력 점수의 수입니다. 두 모델을 연결한 구조가 아니며 무작위 입력의 순전파 형태를 확인하는 실습입니다.')
add('ch12_overview',37,'Chapter 12 Retrieval and prompt construction',{
 'A':node(.2,2.2,'Query tokens\nfixed user question'), 'B':node(.2,.6,'60 course documents\ncontent tokens'), 'C':node(3.7,2.2,'Shared-token scores\nrank and top documents'), 'D':node(7.2,2.2,'Retrieved context\ndocument identifiers'), 'E':node(7.2,.6,'Question plus context\nsave prompt text')}, [('A','C',''),('B','C',''),('C','D',''),('D','E','')],['No language model is called. The saved prompt is not a generated answer.'], '질문과 문서의 공통 토큰(Token) 수로 문서를 정렬한 뒤 근거 문맥과 프롬프트(Prompt)를 만듭니다. 대규모 언어 모델(Large Language Model, LLM)을 호출하지 않으므로 저장한 문장은 생성 답변이 아닙니다. 어텐션(Attention)의 실제 계산은 별도의 12.11절 실습에서 확인합니다.')
add('ch13_overview',39,'Chapter 13 Synthetic distribution monitoring',{
 'A':node(.2,2.2,'Reference samples\n3000 synthetic rows'), 'B':node(.2,.6,'Current samples\n3000 synthetic rows'), 'C':node(3.7,2.2,'Shared bin boundaries\nreference and current ratios'), 'D':node(7.2,2.2,'Population stability\nindex calculation'), 'E':node(7.2,.6,'Rule-based status\ncompare density plots')}, [('A','C',''),('B','C',''),('C','D',''),('D','E','')],['PSI thresholds are teaching rules. The separate linear calculation is not a fitted predictor.'], '기준·현재 합성 자료를 공통 구간으로 나누어 비율을 비교하고 모집단 안정성 지수(Population Stability Index, PSI)를 계산합니다. 주의·재학습 검토는 교재의 예시 규칙이며 자동 재학습을 실행하는 명령이 아닙니다. 별도의 선형 계산값도 학습 모델의 예측과 구분합니다.')
# 개념 도식의 화살표는 명세에 정한 관계만 의미합니다.
add('ai_relationships',2,'Artificial intelligence and generative tasks',{
 'A':node(.3,3.8,'Artificial Intelligence',4.2,.9), 'B':node(.7,2.5,'Machine Learning',3.4,.9), 'C':node(1.1,1.2,'Deep Learning',2.6,.9), 'D':node(6,3.8,'Rule-based reasoning\nand search',3.7,.9), 'E':node(6,2.2,'Generative tasks\ntext, image, audio',3.7,.9), 'F':node(6,.6,'Deep and non-deep\ngenerative models',3.7,.9)}, [('A','B','includes'),('B','C','includes'),('A','D','includes'),('C','E','can support'),('F','E','can support')], ['Hierarchy and task purpose are different axes of description.','Generative AI is not defined as every model inside Deep Learning.'], '실선의 includes는 포함 관계입니다. 인공지능은 기계학습뿐 아니라 규칙 기반 추론과 탐색을 포함하고, 딥러닝은 기계학습의 한 방법입니다. can support는 수행 가능한 과제를 연결합니다. 생성은 과제의 목적이므로 딥러닝 내부의 가장 작은 범주로 일괄 정의하지 않습니다.',size=(9,5.4))
add('learning_modes',3,'Supervised, unsupervised and reinforcement learning',{
 'A':node(.2,3.8,'Training X and y',2.8), 'B':node(3.7,3.8,'Fit predictor',2.6), 'C':node(7,3.8,'New X to prediction',2.9), 'D':node(.2,2.2,'Training X only',2.8), 'E':node(3.7,2.2,'Fit representation\nor clustering',2.6), 'F':node(7,2.2,'Coordinates or\ncluster assignments',2.9), 'G':node(.2,.6,'Agent and policy',2.8), 'H':node(3.7,.6,'Environment',2.6), 'I':node(7,.6,'State and reward',2.9)}, [('A','B',''),('B','C',''),('D','E',''),('E','F',''),('G','H','action'),('H','I',''),('I','G','feedback')],['Training y is not provided to the unsupervised fit.','Reinforcement learning is an interaction loop, not static labeled pairs.'], '지도학습은 훈련 입력 X와 목표 y로 예측기를 적합한 뒤 새 입력을 예측합니다. 비지도학습은 y를 적합에 전달하지 않고 구조를 찾습니다. 강화학습은 에이전트(Agent)가 행동을 선택하고 환경(Environment)에서 상태와 보상 피드백을 받는 반복입니다. 세 경로의 화살표는 학습 방식의 차이를 설명하며 실제 측정 점수를 나타내지 않습니다.',size=(9,5.4))
add('generation_paths',4,'Three conceptual generation paths',{
 'A':node(.2,3.8,'Previous tokens',2.8), 'B':node(3.7,3.8,'Next-token distribution',2.7), 'C':node(7,3.8,'Select and append\nstop at end or limit',2.9), 'D':node(.2,2.2,'Noise and conditions',2.8), 'E':node(3.7,2.2,'Iterative denoising',2.7), 'F':node(7,2.2,'Image or latent\nthen decode',2.9), 'G':node(.2,.6,'Latent sample',2.8), 'H':node(3.7,.6,'Decoder or generator',2.7), 'I':node(7,.6,'Generated sample',2.9)}, [('A','B',''),('B','C',''),('C','A','continue'),('D','E',''),('E','F',''),('G','H',''),('H','I','')],['Conceptual model families; no trained generator or sample image is produced here.','The chapter 12 main program only constructs a retrieval-based prompt.'], '첫 행은 이전 토큰을 조건으로 다음 토큰을 선택·추가하는 자기회귀 생성(Autoregressive Generation)입니다. 종료 토큰이나 길이 제한을 만나면 멈춥니다. 둘째 행은 여러 단계의 잡음 제거를 사용하는 확산 모델(Diffusion Model)의 개념이고 셋째 행은 잠재 표본을 디코더(Decoder) 또는 생성기(Generator)로 변환하는 관점입니다. 서로 다른 생성 계열을 하나의 필수 순서로 연결하지 않습니다.',size=(9,5.4))
add('responsible_lifecycle',5,'Evidence across the model lifecycle',{
 'A':node(.2,3.8,'Data collection\nsource and permission',2.8), 'B':node(3.7,3.8,'Preparation\nquality and leakage',2.8), 'C':node(7,3.8,'Model fitting\nsplit and settings',2.8), 'D':node(7,2.1,'Evaluation\nerrors and group effects',2.8), 'E':node(3.7,2.1,'Deployment and review\nmonitor and respond',2.8), 'F':node(.2,2.1,'Change decision\nretain or revise',2.8), 'G':node(.2,.4,'Versioned evidence: data hashes, code, environment, logs and reviewer decisions',9.6,.8)}, [('A','B',''),('B','C',''),('C','D',''),('D','E',''),('E','F',''),('F','B','revise')],['Arrows show a review cycle. Check labels do not certify safety or fairness.'], '자료 수집에서는 출처·사용 권한, 준비 단계에서는 품질·누수, 학습에서는 분할·설정값을 관리합니다. 평가는 오류와 집단별 영향을 확인하고 운영 중 변화가 관찰되면 원인을 검토해 유지·수정 여부를 결정합니다. 아래의 증거 기록은 모든 단계에 공통으로 적용되며 확인 항목만 나열했다고 검증이 끝난 것은 아닙니다.',size=(9,5.6))
add('reproducibility',6,'Reproduction requires comparable conditions',{
 'A':node(.2,3.8,'Data bytes\nand file hashes',2.8), 'B':node(3.7,3.8,'Code and settings\nrandom generators',2.8), 'C':node(7,3.8,'Versions and hardware\nexecution conditions',2.8), 'D':node(3.7,2,'Run and save\noutputs and logs',2.8), 'E':node(7,2,'Compare with baseline\nexact or tolerance',2.8), 'F':node(7,.4,'Mismatch?\ninspect changed inputs',2.8)}, [('A','D',''),('B','D',''),('C','D',''),('D','E',''),('E','F','not equal')],['The same seed alone does not guarantee identical values across platforms.','Record the comparison tolerance before interpreting differences.'], '파일 해시는 입력 바이트의 동일성을, 코드 버전은 처리 절차를, 난수 발생기와 설정은 무작위 처리 조건을 식별합니다. 소프트웨어 버전과 장치 정보도 함께 기록한 뒤 기준 실행과 비교합니다. 정수는 정확 비교가 가능할 수 있지만 부동소수점은 계산 목적에 맞는 허용 오차를 먼저 정해야 합니다.',size=(9,5.6))
add('array_shapes',14,'Array rank and axis lengths are different',{
 'A':node(.2,2.2,'Scalar\nvalue 7, shape ()',4.5,.9), 'B':node(5.3,2.2,'Vector\n[2,5,1], shape (3,)',4.5,.9), 'C':node(.2,.6,'Matrix\n[[1,2,3],[4,5,6]], shape (2,3)',4.5,.9), 'D':node(5.3,.6,'3-axis array\n2 blocks of 2 by 3, shape (2,2,3)',4.5,.9)}, [],['These are separate examples, not shape-conversion instructions.','In array programming, scalar and matrix arrays are also tensors.'], '네 상자는 별도의 배열 예입니다. 스칼라는 축이 0개, 벡터는 축이 1개, 행렬은 축이 2개입니다. 형태(Shape)의 괄호 안 숫자는 각 축의 길이이고 축 개수와 원소 개수는 다릅니다. 배열 프로그래밍 문맥의 텐서(Tensor)는 3차원 이상만 뜻하지 않고 스칼라·벡터·행렬도 포함합니다.',size=(9,3.8))
# 겹침을 만드는 중복 경로를 정리하고 설명에 테스트 입력을 명시합니다.
for spec in S:
 if spec['name'] in ['ch06_overview','ch07_overview']:
  spec['edges']=[e for e in spec['edges'] if not(e[0]=='A' and e[1]=='C')]
 if spec['name']=='ch08_overview':
  del spec['nodes']['E'];spec['edges']=[e for e in spec['edges'] if e[1]!='E']
  spec['notes'].append('Feature importance is read from the fitted Random Forest, not the boosting model.')

def export(s):
 name=s['name'];fig,ax=plt.subplots(figsize=(s['size'][0],s['size'][1]+(.3 if len(s['notes'])>2 else 0)));fig.subplots_adjust(left=.015,right=.985,bottom=.02,top=.98)
 Y=5.6 if s['size'][1]>5 else 4.;ax.set(xlim=(0,10.1),ylim=(-.95 if len(s['notes'])>2 else -.65,Y));ax.axis('off');texts=[]
 texts.append(ax.text(5.05,Y-.13,s['title'],ha='center',va='top',fontsize=13,weight='bold'))
 mx=ET.Element('mxfile',host='app.diagrams.net');dia=ET.SubElement(mx,'diagram',name=name);gm=ET.SubElement(dia,'mxGraphModel');root=ET.SubElement(gm,'root');ET.SubElement(root,'mxCell',id='0');ET.SubElement(root,'mxCell',id='1',parent='0')
 mmd=['flowchart TD']
 for k,(x,y,w,h,label) in s['nodes'].items():
  ax.add_patch(Rectangle((x,y),w,h,lw=1,facecolor='white',edgecolor='black'));texts.append(ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=11.5))
  cell=ET.SubElement(root,'mxCell',id=k,value=label,style='whiteSpace=wrap;html=0;fillColor=#ffffff;strokeColor=#000000;fontColor=#000000;fontSize=16;',vertex='1',parent='1');ET.SubElement(cell,'mxGeometry',x=str(x*100),y=str((Y-y-h)*100),width=str(w*100),height=str(h*100),attrib={'as':'geometry'});mmd.append(' '+k+'["'+label.replace('\n',' ')+'"]')
 for i,(a,b,label) in enumerate(s['edges']):
  assert a in s['nodes'] and b in s['nodes'];x,y,w,h,_=s['nodes'][a];u,v,ww,hh,_=s['nodes'][b];dx=(u+ww/2)-(x+w/2);dy=(v+hh/2)-(y+h/2)
  if abs(dx)>abs(dy)*1.3:p=(x+w if dx>0 else x,y+h/2);q=(u if dx>0 else u+ww,v+hh/2)
  else:p=(x+w/2,y+h if dy>0 else y);q=(u+ww/2,v if dy>0 else v+hh)
  # 반복·피드백 화살표는 곡선으로 구분합니다.
  rad=.16 if label in ['revise','reuse state'] else 0
  if label in ['next step','continue'] and abs(dy)<.2:
   p=(x+w/2,y+h);q=(u+ww/2,v+hh);rad=.13
  if label=='feedback':
   p=(x+w/2,y);q=(u+ww/2,v);rad=-.13
  ax.add_patch(FancyArrowPatch(p,q,arrowstyle='->',mutation_scale=11,color='black',lw=1.1,connectionstyle=f'arc3,rad={rad}',shrinkA=3,shrinkB=3))
  if label:texts.append(ax.text((p[0]+q[0])/2,(p[1]+q[1])/2+(.42 if label in ['next step','continue'] and abs(dy)<.2 else -.36 if label=='feedback' else .12),label,ha='center',va='center',fontsize=8,bbox={'facecolor':'white','edgecolor':'none','pad':1}))
  cell=ET.SubElement(root,'mxCell',id='edge'+str(i),value=label,edge='1',parent='1',source=a,target=b,style='endArrow=classic;html=0;strokeColor=#000000;');ET.SubElement(cell,'mxGeometry',relative='1',attrib={'as':'geometry'});mmd.append(' '+a+(' -->|"'+label+'"| ' if label else ' --> ')+b)
 for j,line in enumerate(s['notes']):texts.append(ax.text(.1,-.01-j*.23,line,fontsize=9,va='top'))
 # 글자가 이미지 경계를 벗어나지 않는지 검사합니다.
 fig.canvas.draw();rr=fig.canvas.get_renderer()
 for t in texts:
  bb=t.get_window_extent(rr);assert bb.x0>=-1 and bb.x1<=fig.bbox.width+1 and bb.y0>=-1 and bb.y1<=fig.bbox.height+1,(name,t.get_text())
 buffer=io.BytesIO();fig.savefig(buffer,format='png',dpi=400,facecolor='white');(OUT/(name+'.png')).write_bytes(buffer.getvalue());fig.savefig(OUT/(name+'.svg'),metadata={'Date':None});plt.close(fig)
 ET.ElementTree(mx).write(OUT/(name+'.drawio'),encoding='utf-8',xml_declaration=True);(OUT/(name+'.mmd')).write_text('\n'.join(mmd)+'\n');(OUT/(name+'.json')).write_text(json.dumps(s,ensure_ascii=False,indent=2))
if __name__=='__main__':
 for s in S:export(s)
 (OUT/'manifest.json').write_text(json.dumps(S,ensure_ascii=False,indent=2));print('Generated',len(S),'editable diagrams')
