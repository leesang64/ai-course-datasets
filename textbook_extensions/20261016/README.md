# 13개 장 프로그램·데이터·결과 확장 (2026-10-16)

26개 추가 실습, 21개 고정 CSV 입력, 13개 Jupyter 노트북, 27개 실행 결과 그림을 포함한다.
노트북 65개 코드 셀은 IPython에서 순차 실행해 확인했다. 별도 Jupyter 서버 화면에서의 실행은 검증 범위에 포함하지 않는다.
현재 Word의 실제 목차에 맞춘 ch01~ch13이며, 기존 폴더 이름의 장 번호를 재해석해 덮어쓰지 않는다.

## 설치와 실행

Python 3.12 환경을 권장한다. 아래 명령은 이 폴더에서 실행한다.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python verify_all.py
jupyter lab
```

노트북은 각 chXX/chapter_practice.ipynb를 열어 전체 셀을 실행한다.
프로그램은 script 위치를 기준으로 입력을 읽으므로 `python ch07/sec_11_threshold_metrics.py`처럼 실행할 수 있다.
Jupyter의 커널과 패키지 설치 환경이 일치하는지 첫 셀에서 확인한다.

## 재현성과 자료 출처

- 기준 실행 환경은 environment.json, CSV 해시는 data_manifest.json, 장별 스키마·출처는 data_card.json에 있다.
- 원 저장소에서 복사한 자료의 실제 측정/합성 여부나 금액 단위가 확인되지 않은 경우 그 한계를 명시했다.
- 새 합성 자료는 관측 데이터로 부르지 않으며 생성 규칙과 난수 시드를 명시했다.
- Wine은 scikit-learn load_wine으로 배포되는 자료다. 원 출처와 이용 조건은 https://scikit-learn.org/stable/datasets/toy_dataset.html#wine-recognition-dataset 및 https://archive.ics.uci.edu/dataset/109/wine 를 확인한다.
- `results/*.svg`는 실제 실행한 계산에서 생성한 벡터 그림이다. 재실행 시 Word 삽입용 300dpi PNG도 생성된다.
- `results/*.joblib`은 사용자 실행 때 로컬에서 생성하며 GitHub에는 올리지 않는다. 신뢰할 수 없는 모델 파일은 역직렬화하지 않는다.
- 11.11은 고정 필터 연산, 11.12는 Ridge 시계열 기준선, 12.11은 수치 Attention, 12.12는 검색과 근거 프롬프트다. CNN/LSTM/LLM 전체 학습이나 운영 배포를 검증했다고 표시하지 않는다.

## 장·절 대응

- [제1장](ch01/README.md): 1.11 지도·비지도 학습의 입력과 출력 비교 / 1.12 난수 시드와 데이터 분할에 따른 평가 변동
- [제2장](ch02/README.md): 2.11 선형 회귀 손실과 경사하강법 궤적 / 2.12 중앙 차분으로 해석적 미분 검산
- [제3장](ch03/README.md): 3.11 BFS와 A*의 경로·확장 노드 비교 / 3.12 유전자 알고리즘과 완전 탐색의 배낭 해 비교
- [제4장](ch04/README.md): 4.11 결측 분포와 범주별 관측 수 탐색 / 4.12 산점도·상관행렬·이상값 플래그 비교
- [제5장](ch05/README.md): 5.11 혼합형 데이터 전처리 Pipeline과 계수 해석 / 5.12 훈련 통계 고정과 분포 이동 시 표준화
- [제6장](ch06/README.md): 6.11 다항 회귀 차수와 훈련·검증 오차 / 6.12 다변량 회귀의 예측·잔차 진단
- [제7장](ch07/README.md): 7.11 임계값 변화와 혼동행렬·정밀도·재현율 / 7.12 ROC·PR 곡선과 확률 보정 상태
- [제8장](ch08/README.md): 8.11 의사결정트리 깊이와 가지 분기 해석 / 8.12 앙상블 비교와 테스트 순열 중요도
- [제9장](ch09/README.md): 9.11 K-Means와 DBSCAN의 비선형 군집 비교 / 9.12 PCA 설명 분산과 재구성 오차
- [제10장](ch10/README.md): 10.11 MLP 은닉층과 비선형 결정 경계 / 10.12 훈련 크기에 따른 신경망 학습 곡선
- [제11장](ch11/README.md): 11.11 합성 영상의 필터·풀링과 크기 계산 / 11.12 시간순 분할의 한 단계 예측과 지속성 기준선
- [제12장](ch12/README.md): 12.11 Attention 점수·정규화·가중합의 수치 검증 / 12.12 한국어 문서 TF-IDF 검색과 근거 프롬프트
- [제13장](ch13/README.md): 13.11 PSI·KS와 분포 이동 모니터링 / 13.12 모델 저장·복원과 배치 추론 입력 검증
