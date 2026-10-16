from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
from collections import deque
import heapq
maze=pd.read_csv(DATA/"maze.csv").to_numpy()
start,goal=(0,0),(5,5)
def neighbors(u):
    for dr,dc in [(0,1),(1,0),(0,-1),(-1,0)]:
        v=(u[0]+dr,u[1]+dc)
        if 0<=v[0]<6 and 0<=v[1]<6 and maze[v]==0:
            yield v

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
# FIFO BFS is implemented explicitly, not as a priority-queue substitute.
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
fig,axes=plt.subplots(1,2,figsize=(7,3.6));metrics={}
for ax,label,fn in zip(axes,["BFS","A*"],[bfs,lambda:search(True)]):
    path,seen=fn();rr,cc=zip(*path)
    ax.imshow(maze,cmap="gray_r",vmin=0,vmax=1)
    ax.plot(cc,rr,"o-",color="0.5",markersize=5)
    ax.text(0,0,"S",ha="center");ax.text(5,5,"G",ha="center")
    ax.set(title=f"{label}: expanded {len(seen)}",xlabel="Column",ylabel="Row")
    metrics[label]={"steps":len(path)-1,"expanded":len(seen)}
    pd.DataFrame(path,columns=["row","column"]).to_csv(OUT/f"{label.replace('*','star')}_path.csv",index=False)
figure(OUT,"search_compare");report(OUT,"search_compare",metrics)
assert metrics["BFS"]["steps"]==metrics["A*"]["steps"]
