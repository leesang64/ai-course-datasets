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

# 가져오기(Import) 문장으로 deque 기능를 연결합니다. 이 셀에서는 자료를 학습하지 않습니다.
from collections import deque

# 가져오기(Import) 문장으로 heapq 기능를 연결합니다. 이 셀에서는 자료를 학습하지 않습니다.
import heapq

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
OUT = HERE / "results" / "check_11_search_compare"

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
# 변수 maze에 CSV 파일을 표로 읽습니다. 열 이름과 목표 열을 다음 출력에서 확인합니다.
maze=pd.read_csv(DATA/"maze.csv").to_numpy()

# 변수 start·변수 goal를 오른쪽 식으로 계산하여 다음 단계에서 재사용합니다. 값과 형태(Shape)를 구분합니다.
start,goal=(0,0),(5,5)

# %% 셀 6 함수와 모듈 정의
# 함수 neighbors의 입력·계산·반환을 정의합니다. 이 셀은 함수를 준비하며 실제 호출은 뒤 셀에서 수행합니다.
def neighbors(u):
    for dr,dc in [(0,1),(1,0),(0,-1),(-1,0)]:
        v=(u[0]+dr,u[1]+dc)
        if 0<=v[0]<6 and 0<=v[1]<6 and maze[v]==0:
            yield v

# %% 셀 7 함수와 모듈 정의
# 함수 search의 입력·계산·반환을 정의합니다. 이 셀은 함수를 준비하며 실제 호출은 뒤 셀에서 수행합니다.
def search(astar):
    frontier=[(0,start)];parent={start:None};cost={start:0};seen=[]
    while frontier:
        _,u=heapq.heappop(frontier)
        if u in seen: continue
        seen.append(u)
        if u==goal: break
        for v in neighbors(u):
            new=cost[u]+1
            if v not in cost or new<cost[v]:
                cost[v]=new;parent[v]=u
                h=abs(v[0]-goal[0])+abs(v[1]-goal[1]) if astar else 0
                heapq.heappush(frontier,(new+h,v))
    path=[];u=goal
    while u is not None: path.append(u);u=parent[u]
    return path[::-1],seen

# %% 셀 8 함수와 모듈 정의
# 함수 bfs의 입력·계산·반환을 정의합니다. 이 셀은 함수를 준비하며 실제 호출은 뒤 셀에서 수행합니다.
def bfs():
    q=deque([start]);parent={start:None};seen=[]
    while q:
        u=q.popleft();seen.append(u)
        if u==goal:break
        for v in neighbors(u):
            if v not in parent:parent[v]=u;q.append(v)
    path=[];u=goal
    while u is not None:path.append(u);u=parent[u]
    return path[::-1],seen

# %% 셀 9 입력·계산·출력 확인
# 변수 fig·변수 axes를 오른쪽 식으로 계산하여 다음 단계에서 재사용합니다. 값과 형태(Shape)를 구분합니다.
fig,axes=plt.subplots(1,2,figsize=(7,3.6))

# 계산된 평가 지표(Evaluation Metrics, metrics)를 오른쪽 식으로 계산하여 다음 단계에서 재사용합니다. 값과 형태(Shape)를 구분합니다.
metrics={}

# 반복 조건 for ax,label,fn in zip(axes,["BFS","A*"],[bfs,lambda:search(True)]):에 따라 같은 처리를 수행합니다. 루프 내부의 들여쓰기는 반복마다 실행되며 반복 종료 뒤 변수에는 마지막 계산 상태가 남습니다.
for ax,label,fn in zip(axes,["BFS","A*"],[bfs,lambda:search(True)]):
    path,seen=fn();rr,cc=zip(*path)
    ax.imshow(maze,cmap="gray_r",vmin=0,vmax=1)
    ax.plot(cc,rr,"o-",color="0.5",markersize=5)
    ax.text(0,0,"S",ha="center");ax.text(5,5,"G",ha="center")
    ax.set(title=f"{label}: expanded {len(seen)}",xlabel="Column",ylabel="Row")
    metrics[label]={"steps":len(path)-1,"expanded":len(seen)}
    pd.DataFrame(path,columns=["row","column"]).to_csv(OUT/f"{label.replace('*','star')}_path.csv",index=False)

# 실제 계산한 그림을 저장하고 출력합니다. 가로축·세로축·범례의 의미는 이 실습의 결과 해설에서 확인합니다.
figure(OUT,"search_compare")

# 계산된 값만 결과 파일과 셀 출력에 기록합니다. 이후 비교에는 출력 파일과 데이터 버전을 함께 사용합니다.
report(OUT,"search_compare",metrics)

# 검증 조건(Assertion)이 참인지 확인합니다. 거짓이면 셀을 중단하며 성공한 결과로 기록하지 않습니다.
assert metrics["BFS"]["steps"]==metrics["A*"]["steps"]

# 반복 조건 for label,fn in [("BFS",bfs),("Astar",lambda:search(True))]:에 따라 같은 처리를 수행합니다. 루프 내부의 들여쓰기는 반복마다 실행되며 반복 종료 뒤 변수에는 마지막 계산 상태가 남습니다.
for label,fn in [("BFS",bfs),("Astar",lambda:search(True))]:
    route,_=fn()
    assert all(maze[u]==0 for u in route)
    assert all(abs(a[0]-b[0])+abs(a[1]-b[1])==1 for a,b in zip(route,route[1:]))

# %% 셀 10 입력·계산·출력 확인
# 계산된 값만 결과 파일과 셀 출력에 기록합니다. 이후 비교에는 출력 파일과 데이터 버전을 함께 사용합니다.
report(OUT,"exercise_check",{"both_paths_valid":True,"equal_steps":metrics["BFS"]["steps"]==metrics["A*"]["steps"]})
