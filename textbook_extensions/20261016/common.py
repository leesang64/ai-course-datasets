"""공통 입출력: CSV 고정 입력, 흑백 그래프, 실행 지표 저장."""
from pathlib import Path
import json
import io
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":11,
    "axes.prop_cycle":plt.cycler(color=["black","0.45","0.7"]),
    "svg.fonttype":"none", "figure.figsize":(7.0,4.2)})

def setup(script):
    folder=Path(script).resolve().parent
    out=folder/"results"
    out.mkdir(exist_ok=True)
    return folder/"data", out

def figure(out, name):
    plt.tight_layout()
    for suffix in ["png","svg"]:
        buffer=io.BytesIO()
        plt.savefig(buffer,format=suffix,dpi=300,facecolor="white")
        target=out/(name+"."+suffix)
        temp=target.with_suffix(target.suffix+".tmp")
        temp.write_bytes(buffer.getvalue())
        temp.replace(target)
    plt.close()

def report(out, name, metrics):
    text=json.dumps(metrics,ensure_ascii=False,indent=2,allow_nan=False)
    (out/(name+".json")).write_text(text,encoding="utf-8")
    print(text)
