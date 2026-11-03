# %% 셀 1 라이브러리 가져오기
# 가져오기(Import) 문장으로 경로 객체(Path)를 연결합니다. 이 셀에서는 자료를 학습하지 않습니다.
from pathlib import Path

# 가져오기(Import) 문장으로 자바스크립트 객체 표기법(JavaScript Object Notation, JSON) 도구를 연결합니다. 이 셀에서는 자료를 학습하지 않습니다.
import json

# 가져오기(Import) 문장으로 수치 배열 도구 넘파이(Numerical Python, NumPy)의 별칭 np를 연결합니다. 이 셀에서는 자료를 학습하지 않습니다.
import numpy as np

# 가져오기(Import) 문장으로 자료 표 도구 판다스(pandas)의 별칭 pd를 연결합니다. 이 셀에서는 자료를 학습하지 않습니다.
import pandas as pd

# 가져오기(Import) 문장으로 맷플롯립 파이플롯(Matplotlib Pyplot)의 별칭 plt를 연결합니다. 이 셀에서는 자료를 학습하지 않습니다.
import matplotlib.pyplot as plt

# 가져오기(Import) 문장으로 셀 출력 표시 함수(display), 이미지 표시 객체(IPython Image)를 연결합니다. 이 셀에서는 자료를 학습하지 않습니다.
from IPython.display import display, Image as NotebookImage

# %% 셀 2 입력·계산·출력 확인
# 계산 결과의 축·제목·기호·범례를 설정합니다. 표시 방식이 바뀌어도 원본 수치가 바뀌는 것은 아닙니다.
plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":11,
    "axes.prop_cycle":plt.cycler(color=["black","0.45","0.7"]),
    "svg.fonttype":"none", "figure.figsize":(7.0,4.2)})

# 현재 노트북 또는 프로그램 폴더(Current Directory, HERE)를 오른쪽 식으로 계산하여 다음 단계에서 재사용합니다. 값과 형태(Shape)를 구분합니다.
HERE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()

# 장 폴더(Chapter Directory, CHAPTER)를 오른쪽 식으로 계산하여 다음 단계에서 재사용합니다. 값과 형태(Shape)를 구분합니다.
CHAPTER = HERE if (HERE / "data").exists() else HERE.parent

# 입력 자료 폴더(Data Directory, DATA)를 오른쪽 식으로 계산하여 다음 단계에서 재사용합니다. 값과 형태(Shape)를 구분합니다.
DATA = CHAPTER / "data"

# 결과 저장 폴더(Output Directory, OUT)를 오른쪽 식으로 계산하여 다음 단계에서 재사용합니다. 값과 형태(Shape)를 구분합니다.
OUT = HERE / "results" / "check_11_gradient_descent"

# 앞 셀의 값을 사용하여 OUT.mkdir(parents=True, exist_ok=True) 동작을 수행합니다. 셀 순서를 바꾸거나 중간 셀을 생략하지 않습니다.
OUT.mkdir(parents=True, exist_ok=True)

# 검증 조건(Assertion)이 참인지 확인합니다. 거짓이면 셀을 중단하며 성공한 결과로 기록하지 않습니다.
assert DATA.exists(), f"장별 data 폴더가 없습니다: {DATA}. 저장소 전체를 내려받으세요."

# %% 셀 3 함수와 모듈 정의
# 현재 계산으로 만든 그림을 SVG와 300dpi PNG로 저장하고 노트북 셀에 표시합니다.
def figure(out, name):
    # 실제 현재 그림을 벡터와 300dpi 흑백 삽입본으로 저장합니다.
    plt.tight_layout()
    plt.savefig(out / (name + ".svg"), facecolor="white")
    plt.savefig(out / (name + ".png"), dpi=300, facecolor="white")
    if "get_ipython" in globals():
        display(NotebookImage(filename=str(out / (name + ".png"))))
    plt.close()

# %% 셀 4 함수와 모듈 정의
# 계산한 지표를 JSON 파일과 셀의 문자 출력으로 기록합니다.
def report(out, name, metrics):
    # 계산된 값만 기록하며 비유한 수치를 성공값으로 바꾸지 않습니다.
    text = json.dumps(metrics, ensure_ascii=False, indent=2, allow_nan=False)
    (out / (name + ".json")).write_text(text, encoding="utf-8")
    print(text)

# %% 셀 5 입력·계산·출력 확인
# 자료 표(Data Frame, frame)에 CSV 파일을 표로 읽습니다. 열 이름과 목표 열을 다음 출력에서 확인합니다.
frame = pd.read_csv(DATA / "linear.csv")

# 변수 x·목표 벡터(Target Vector, y)를 오른쪽 식으로 계산하여 다음 단계에서 재사용합니다. 값과 형태(Shape)를 구분합니다.
x,y = frame.x.to_numpy(),frame.y.to_numpy()

# 변수 w·절편(Bias, b)를 오른쪽 식으로 계산하여 다음 단계에서 재사용합니다. 값과 형태(Shape)를 구분합니다.
w,b = 0.,0.

# 변수 rows를 오른쪽 식으로 계산하여 다음 단계에서 재사용합니다. 값과 형태(Shape)를 구분합니다.
rows = []

# 반복 조건 for epoch in range(80):에 따라 같은 처리를 수행합니다. 루프 내부의 들여쓰기는 반복마다 실행되며 반복 종료 뒤 변수에는 마지막 계산 상태가 남습니다.
for epoch in range(80):
    error = w*x+b-y
    loss = np.mean(error**2)
    rows.append({"epoch":epoch,"w":w,"b":b,"mse":loss})
    dw,db = 2*np.mean(error*x),2*np.mean(error)
    w -= .06*dw
    b -= .06*db

# 반복 기록(Iteration History, history)를 오른쪽 식으로 계산하여 다음 단계에서 재사용합니다. 값과 형태(Shape)를 구분합니다.
history = pd.DataFrame(rows)

# 앞 셀의 값을 사용하여 history.to_csv(OUT/"gradient_descent.csv",index=False) 동작을 수행합니다. 셀 순서를 바꾸거나 중간 셀을 생략하지 않습니다.
history.to_csv(OUT/"gradient_descent.csv",index=False)

# 변수 fig·변수 axes를 오른쪽 식으로 계산하여 다음 단계에서 재사용합니다. 값과 형태(Shape)를 구분합니다.
fig,axes=plt.subplots(1,2,figsize=(7.2,3.4))

# 앞 셀의 값을 사용하여 axes[0].scatter(x,y,s=12,facecolors="none",edgecolors="black") 동작을 수행합니다. 셀 순서를 바꾸거나 중간 셀을 생략하지 않습니다.
axes[0].scatter(x,y,s=12,facecolors="none",edgecolors="black")

# 앞 셀의 값을 사용하여 axes[0].plot(x,w*x+b,"k-") 동작을 수행합니다. 셀 순서를 바꾸거나 중간 셀을 생략하지 않습니다.
axes[0].plot(x,w*x+b,"k-")

# 앞 셀의 값을 사용하여 axes[0].set(xlabel="x",ylabel="y",title="Fitted line") 동작을 수행합니다. 셀 순서를 바꾸거나 중간 셀을 생략하지 않습니다.
axes[0].set(xlabel="x",ylabel="y",title="Fitted line")

# %% 셀 6 입력·계산·출력 확인
# 앞 셀의 값을 사용하여 axes[1].plot(history.epoch,history.mse,"k-") 동작을 수행합니다. 셀 순서를 바꾸거나 중간 셀을 생략하지 않습니다.
axes[1].plot(history.epoch,history.mse,"k-")

# 앞 셀의 값을 사용하여 axes[1].set(xlabel="Update step",ylabel="Training MSE",title="Loss history") 동작을 수행합니다. 셀 순서를 바꾸거나 중간 셀을 생략하지 않습니다.
axes[1].set(xlabel="Update step",ylabel="Training MSE",title="Loss history")

# 실제 계산한 그림을 저장하고 출력합니다. 가로축·세로축·범례의 의미는 이 실습의 결과 해설에서 확인합니다.
figure(OUT,"gradient_descent")

# 계산된 값만 결과 파일과 셀 출력에 기록합니다. 이후 비교에는 출력 파일과 데이터 버전을 함께 사용합니다.
report(OUT,"gradient_descent",{"w":w,"b":b,
    "initial_mse":float(history.mse.iloc[0]),
    "final_mse":float(np.mean((w*x+b-y)**2))})

# 변수 comparison를 오른쪽 식으로 계산하여 다음 단계에서 재사용합니다. 값과 형태(Shape)를 구분합니다.
comparison=[]

# 반복 조건 for lr in [.006,.6]:에 따라 같은 처리를 수행합니다. 루프 내부의 들여쓰기는 반복마다 실행되며 반복 종료 뒤 변수에는 마지막 계산 상태가 남습니다.
for lr in [.006,.6]:
    ww,bb=0.,0.
    with np.errstate(over="ignore",invalid="ignore"):
        for step in range(80):
            e=ww*x+bb-y
            ww-=lr*2*np.mean(e*x);bb-=lr*2*np.mean(e)
        mse=float(np.mean((ww*x+bb-y)**2))
    comparison.append({"learning_rate":lr,"final_mse":mse if np.isfinite(mse) else None,"finite":bool(np.isfinite(mse))})

# 계산된 값만 결과 파일과 셀 출력에 기록합니다. 이후 비교에는 출력 파일과 데이터 버전을 함께 사용합니다.
report(OUT,"exercise_check",{"comparison":comparison})
