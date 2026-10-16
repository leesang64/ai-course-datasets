"""고정 입력 재생성 검사. 기존 CSV 대신 generated_preview에 쓴 뒤 해시를 비교한다."""
from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
from sklearn.datasets import load_wine,make_moons
REPO=Path(__file__).resolve().parents[2]
ROOT=Path(__file__).resolve().parent/'generated_preview'
ROOT.mkdir(exist_ok=True)
def csv(ch,name,df,origin,meaning):
 folder=ROOT/f'ch{ch:02d}'/'data';folder.mkdir(parents=True,exist_ok=True)
 f=folder/name;df.to_csv(f,index=False,float_format='%.10g')
 return {'file':name,'rows':len(df),'columns':list(df.columns),'origin':origin,'meaning':meaning,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
DATA={i:[] for i in range(1,14)}
def data(ch,name,df,origin,meaning):DATA[ch].append(csv(ch,name,df,origin,meaning))
# Frozen inputs: originals are left untouched.
rng=np.random.default_rng(42)
wine=load_wine(as_frame=True);wd=wine.frame.copy();wd.columns=[c.replace('/','_').replace(' ','_') for c in wd.columns]
for ch in [1,7,8,9,10]:data(ch,'wine.csv',wd,'scikit-learn 내장 Wine 데이터(load_wine), UCI Wine에서 유래한 178개 관측. 생성 자료 아님.','13개 연속형 화학 분석 특성과 target(0,1,2). 7장은 target==0을 양성으로 재정의한다. 물리 단위는 원 출처 설명을 확인한다.')
x=np.linspace(-3,3,90);toy=pd.DataFrame({'x':x,'y':1.8*x+.7+rng.normal(0,.65,len(x))})
data(2,'linear.csv',toy,'난수 시드 42로 만든 교육용 합성 데이터. 실제 측정값 아님.','x 입력과 y 정답. y=1.8x+0.7+정규 잡음. 단위 없음.')
maze=np.array([[0,0,0,1,0,0],[1,1,0,1,0,1],[0,0,0,0,0,0],[0,1,1,1,1,0],[0,0,0,0,0,0],[1,1,0,1,1,0]])
data(3,'maze.csv',pd.DataFrame(maze,columns=[f'c{i}' for i in range(6)]),'저자가 정의한 6×6 교육용 격자. 실제 지도 아님.','0 이동 가능, 1 장애물. 시작 (0,0), 목표 (5,5), 상하좌우 비용 1.')
data(3,'items.csv',pd.DataFrame({'item':list('ABCDEFGH'),'weight':[2,3,4,5,6,7,3,2],'value':[6,8,9,12,14,16,7,5]}),'교육용 8개 배낭 물품을 명시적으로 정의. 실제 상품 가격 아님.','weight 중량과 value 효용은 무차원. 허용 중량 15. 선택 비트 0/1.')
# Fully synthetic customer example; no real customer records or identifiers.
synthetic_rng=np.random.default_rng(20261016)
n=1200
age=synthetic_rng.integers(18,81,n)
tenure=synthetic_rng.integers(1,73,n)
monthly=np.clip(synthetic_rng.normal(70,25,n),15,150)
contract=synthetic_rng.choice(['monthly','one_year','two_year'],n,p=[.55,.25,.2])
support=synthetic_rng.choice(['yes','no'],n,p=[.6,.4])
logit=-2.2+.012*(monthly-70)-.018*(tenure-30)+.9*(contract=='monthly')+.5*(support=='no')
probability=1/(1+np.exp(-logit))
churn=pd.DataFrame({'customer_id':[f'SYN{i:05d}' for i in range(n)],
    'age':age,'tenure':tenure,'monthly_charge':monthly,
    'total_charge':monthly*tenure+synthetic_rng.normal(0,40,n),
    'contract':contract,'internet':synthetic_rng.choice(['fiber','dsl','none'],n),
    'support':support,'ebilling':synthetic_rng.choice(['yes','no'],n),
    'churn':synthetic_rng.binomial(1,probability)})
for column in ['monthly_charge','total_charge','support']:
    churn.loc[synthetic_rng.choice(n,20,replace=False),column]=np.nan
for ch in [4,5]:data(ch,'churn.csv',churn,
    '난수 시드 20261016의 완전한 교육용 합성 고객 데이터. 실제 고객 자료를 복사·익명화한 것이 아니며 개인과 연결되지 않음.',
    'SYN 식별자는 생성 행 번호. 요금은 가상 단위. churn=1은 생성 확률에 따라 표집한 가상 이탈. 실제 고객 행동이나 기업 성능을 뜻하지 않는다.')
housing=pd.read_csv(REPO/'06_Regression/housing_regression.csv');housing.columns=['area','rooms','age','distance','school_score','price']
data(6,'housing.csv',housing,'기존 GitHub 06_Regression/housing_regression.csv를 열 이름만 바꾼 자료. 실측·합성 여부와 원 단위는 미확인.','price를 목표로 사용. area, rooms, age, distance, school_score는 입력. 가격 단위를 임의로 원으로 부르지 않는다.')
x=np.sort(rng.uniform(-3,3,100));data(6,'nonlinear.csv',pd.DataFrame({'x':x,'y':np.sin(1.5*x)+rng.normal(0,.25,len(x))}),'난수 시드 42의 교육용 합성 비선형 회귀. 실제 측정값 아님.','x 입력, y=sin(1.5x)+잡음. 다항식 차수와 과적합 비교. 단위 없음.')
moons,labels=make_moons(n_samples=300,noise=.16,random_state=42)
for ch in [9,10]:data(ch,'moons.csv',pd.DataFrame({'x1':moons[:,0],'x2':moons[:,1],'target':labels}),'scikit-learn make_moons로 생성한 교육용 합성 데이터, random_state=42.','x1/x2는 무차원 평면 좌표. 군집화에는 정답 target을 입력하지 않는다.')
img=np.zeros((12,12));img[:,6:]=1;img[4:8,3:9]=.5
data(11,'image.csv',pd.DataFrame(img,columns=[f'c{i}' for i in range(12)]),'교육용 12×12 합성 회색조 영상. 실제 사진 아님.','한 셀은 픽셀, 0~1 밝기. 수직 경계와 사각형을 정의했다.')
t=np.arange(360);signal=np.sin(2*np.pi*t/24)+.003*t+rng.normal(0,.12,len(t))
data(11,'series.csv',pd.DataFrame({'t':t,'signal':signal}),'시드 42로 만든 주기 24, 선형 추세 0.003t, 잡음의 교육용 합성 시계열.','t는 순서 번호이며 실제 시간 단위 아님. 미래 t의 값을 훈련 입력에 넣지 않는다.')
q=np.array([[1,0],[0,1],[1,1]],float);k=np.array([[1,0],[0,1],[1,1],[0,-1]],float)
data(12,'queries.csv',pd.DataFrame(q,columns=['d0','d1']),'직접 정의한 교육용 Q 행렬. 학습된 언어 임베딩 아님.','질의 3개×차원 2.')
data(12,'keys.csv',pd.DataFrame(k,columns=['d0','d1']),'직접 정의한 교육용 K 행렬. 학습된 언어 임베딩 아님.','키 4개×차원 2. V는 코드에 고정된 4×2 행렬.')
docs=pd.read_csv(REPO/'12_Sequence_Transformer_GenerativeAI/course_documents.csv').rename(columns={'document_id':'id'})
data(12,'documents.csv',docs,'기존 GitHub 12_Sequence_Transformer_GenerativeAI/course_documents.csv.','id/title/content는 교육용 검색 문서. TF-IDF 문자 n-gram으로 점수 계산. 외부 LLM 호출 없음.')
data(13,'drift.csv',pd.DataFrame({'reference':rng.normal(0,1,500),'current':rng.normal(.65,1.15,500)}),'시드 42의 교육용 합성 분포 이동. 실서비스 데이터 아님.','두 열은 각각 500개 기준·현재 관측. 짝지은 관측이 아니다. 평균과 척도를 다르게 설정했다.')
x=rng.normal(size=(360,3));y=2*x[:,0]-x[:,1]+.5*x[:,2]+rng.normal(0,.2,360)
data(13,'serving.csv',pd.DataFrame({'x0':x[:,0],'x1':x[:,1],'x2':x[:,2],'target':y}),'시드 42의 교육용 합성 회귀. 실제 운영 성능을 의미하지 않음.','3개 무차원 입력과 연속형 목표. 모델 저장·복원·입력 검증용.')

manifest=json.loads((Path(__file__).resolve().parent/'data_manifest.json').read_text())
for item in manifest:
    actual=hashlib.sha256((ROOT/item['file']).read_bytes()).hexdigest()
    if actual!=item['sha256']:raise RuntimeError('Regeneration differs: '+item['file'])
print('All regenerated CSV files match the committed SHA-256 values.')
