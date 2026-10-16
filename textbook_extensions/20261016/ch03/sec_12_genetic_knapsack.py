from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
from itertools import product
items=pd.read_csv(DATA/"items.csv")
w,v=items.weight.to_numpy(),items.value.to_numpy()
capacity=15
rng=np.random.default_rng(42)
def score(pop):
    return np.where(pop@w<=capacity,pop@v,0)
all_bits=np.array(list(product([0,1],repeat=len(w))))
optimal=int(score(all_bits).max())
pop=rng.integers(0,2,size=(40,len(w)));history=[]
for generation in range(45):
    fitness=score(pop);elite=pop[np.argmax(fitness)].copy()
    history.append({"generation":generation,"best":int(fitness.max()),
        "mean":float(fitness.mean())})
    next_pop=[elite]
    while len(next_pop)<len(pop):
        parents=[]
        for _ in range(2):
            candidates=rng.integers(0,len(pop),3)
            parents.append(pop[candidates[np.argmax(fitness[candidates])]])
        cut=int(rng.integers(1,len(w)))
        child=np.r_[parents[0][:cut],parents[1][cut:]]
        child=np.logical_xor(child,rng.random(len(w))<.05).astype(int)
        next_pop.append(child)
    pop=np.array(next_pop)
fitness=score(pop);best=pop[np.argmax(fitness)]
h=pd.DataFrame(history);h.to_csv(OUT/"genetic_knapsack.csv",index=False)
plt.plot(h.generation,h.best,"k-",label="Best feasible value")
plt.plot(h.generation,h["mean"],"k--",label="Population mean fitness")
plt.axhline(optimal,color=".5",ls=":",label="Exact optimum")
plt.xlabel("Generation");plt.ylabel("Fitness / value");plt.legend(fontsize=9)
figure(OUT,"genetic_knapsack")
report(OUT,"genetic_knapsack",{"exact_optimum":optimal,
    "ga_value":int(best@v),"ga_weight":int(best@w),"bits":best.tolist()})
assert best@w<=capacity
