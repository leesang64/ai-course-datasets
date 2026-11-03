# 파이썬 기반 인공지능 교재 셀별 실습

2026년 11월 3일 개정에서는 본문 주 예제 13개, 추가 실습 26개, 확인 문제 8번 참고 코드 13개, 실습 과제 참고 코드 13개, 추가 실습 확인 과제 26개를 구분했습니다. 독립 프로그램은 91개이며 같은 내용의 전체 Python 코드와 셀별 Jupyter Notebook을 각각 제공합니다. 장별 안내 노트북 13개는 프로그램을 선택하는 목차입니다.

모든 독립 프로그램은 각 셀의 코드를 IPython에서 위에서 아래로 실행하여 결과를 저장했습니다. Jupyter 메시징 커널은 실행 환경의 소켓 제한 때문에 시작하지 못했으므로 별도 커널·브라우저 실행 완료로 표시하지 않습니다. 새 입력을 연결한 본문 예제의 결과는 과거 원고의 누락 입력 결과를 복구한 값이 아닙니다.

## 처음 실행하는 순서

1. 저장소 화면의 Code 메뉴에서 Download ZIP을 선택하고 압축을 풉니다. ZIP 안에서 파일을 직접 열지 않습니다.
2. 아래 폴더로 이동합니다. 이 폴더의 data_manifest.json과 ch01~ch13을 확인합니다.

```bash
cd ai-course-datasets-main/textbook_extensions/20261016
python -m venv .venv
```

Windows에서는 `.venv\Scripts\activate`, macOS·Linux에서는 `source .venv/bin/activate`를 실행합니다.

```bash
python -m pip install -r requirements.txt
python -m pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu
python -m ipykernel install --user --name ai-textbook --display-name "Python AI textbook"
python validate_course.py
python -m jupyterlab
```

위 PyTorch 명령은 CPU 실습용입니다. 운영체제와 Python에 맞는 배포 파일을 선택해야 하며 GPU 설치 완료를 뜻하지 않습니다. 노트북에서 Python AI textbook 커널을 선택한 뒤 `sys.executable`이 새 가상환경을 가리키는지 확인합니다. 장별 파일은 해당 파일이 있는 폴더에서 열고 커널을 다시 시작한 뒤 Run All을 선택합니다. 경로 검사에서 중단되면 현재 폴더와 장별 data 폴더를 확인합니다.

각 `.py` 파일도 해당 실습의 전체 코드입니다. 단독으로 복사하면 데이터까지 복사되는 것은 아니므로 data 폴더를 함께 준비합니다. 예를 들어 이 폴더에서 `python ch01/body/sec_07_main.py`로 실행할 수 있습니다. `body`는 본문, `extensions`는 추가 실습, `exercises`는 확인 문제와 추가 확인 과제, `assignments`는 실습 과제 참고 구현입니다.

## 실제 결과와 검증 범위

- 실행 로그와 수치는 각 프로그램 폴더의 `results/프로그램이름/`에 있습니다. SVG는 GitHub에 제공하며 300dpi PNG는 노트북과 프로그램을 실행하면 생성됩니다. 노트북에도 실제 계산한 그림이 저장되어 있습니다.
- [104개 노트북 셀 실행 기록](execution_20261103.json), [장·절별 대응과 결과](coverage_20261103.json), [모든 CSV 해시](data_manifest.json), [자료형·결측 사전](all_data_dictionary.json)를 제공합니다.
- Wine은 같은 13개 특성으로 지도·비지도 학습을 비교하기 위해 사용합니다. 군집 번호는 품종 정답 번호와 같지 않습니다. 그림에는 첫 두 특성을 표시하지만 모델 입력은 13개입니다.
- 본문 5장 입력은 새로 작성한 교육용 합성 자료입니다. 원래 누락 입력을 찾은 것처럼 표시하지 않습니다. 본문 7·9장 분류 자료는 사이킷런의 유방암 진단 자료이며 1은 양성 종양입니다.
- 본문 11장은 난수 텐서의 순전파 검사이며 CNN·LSTM을 실제 데이터로 학습한 실험이 아닙니다. 12장은 문서 검색과 프롬프트이며 생성 모델 호출 결과가 아닙니다. 13장의 선형 계산은 학습 모델 예측이 아닙니다.
- 문서 관련성 0·1·2점과 원인 가설 등 사람이 판단해야 하는 과제는 독자가 작성합니다. 코드는 빈 채점 양식을 제공하며 임의 점수를 생성하지 않습니다.

## 장별 전체 코드와 해설

- [제1장 본문·추가 실습·확인 문제·과제](ch01/README.md)
- [제2장 본문·추가 실습·확인 문제·과제](ch02/README.md)
- [제3장 본문·추가 실습·확인 문제·과제](ch03/README.md)
- [제4장 본문·추가 실습·확인 문제·과제](ch04/README.md)
- [제5장 본문·추가 실습·확인 문제·과제](ch05/README.md)
- [제6장 본문·추가 실습·확인 문제·과제](ch06/README.md)
- [제7장 본문·추가 실습·확인 문제·과제](ch07/README.md)
- [제8장 본문·추가 실습·확인 문제·과제](ch08/README.md)
- [제9장 본문·추가 실습·확인 문제·과제](ch09/README.md)
- [제10장 본문·추가 실습·확인 문제·과제](ch10/README.md)
- [제11장 본문·추가 실습·확인 문제·과제](ch11/README.md)
- [제12장 본문·추가 실습·확인 문제·과제](ch12/README.md)
- [제13장 본문·추가 실습·확인 문제·과제](ch13/README.md)

## 입력 출처

기존 저장소 자료는 파일과 행을 보존하고 필요한 열 이름·라벨 변환을 명시했습니다. 실측 여부나 단위를 확인할 수 없는 자료는 교육용 자료로 설명합니다. [Wine 공식 설명](https://scikit-learn.org/stable/datasets/toy_dataset.html#wine-recognition-dataset), [유방암 진단 자료 공식 설명](https://scikit-learn.org/stable/datasets/toy_dataset.html#breast-cancer-wisconsin-diagnostic-dataset)을 확인할 수 있습니다. 숫자 라벨의 의미는 프로그램별로 정의하며 다른 장과 자동으로 같다고 해석하지 않습니다.

