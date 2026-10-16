from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import np, pd, plt, setup, figure, report
DATA, OUT = setup(__file__)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
f=pd.read_csv(DATA/"documents.csv").fillna("")
vectorizer=TfidfVectorizer(analyzer="char",ngram_range=(2,4))
matrix=vectorizer.fit_transform(f.content)
question="데이터 전처리와 결측값 처리 방법은?"
scores=cosine_similarity(vectorizer.transform([question]),matrix).ravel()
order=np.argsort(-scores,kind="stable")[:5]
result=f.iloc[order].copy();result["score"]=scores[order]
result.to_csv(OUT/"retrieval.csv",index=False)
context="\n\n".join(f"[{row.id}] {row.content}" for row in result.itertuples() if row.score>0)
prompt=f"질문: {question}\n\n근거:\n{context}\n\n근거에 있는 내용만 답하고 문서 ID를 표시하세요."
(OUT/"retrieval_prompt.txt").write_text(prompt,encoding="utf-8")
plt.bar(range(len(result)),result.score,color=".7",edgecolor="black")
plt.xticks(range(len(result)),result.id.astype(str),rotation=30)
plt.xlabel("Retrieved document ID");plt.ylabel("Cosine similarity")
plt.title("Character TF-IDF retrieval: top 5")
figure(OUT,"retrieval")
report(OUT,"retrieval",{"documents":len(f),"question":question,
    "top_ids":result.id.astype(str).tolist(),"top_scores":result.score.tolist(),
    "LLM_called":False})
