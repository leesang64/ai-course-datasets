# %% 셀 1 도구 가져오기
# 넘파이(Numerical Python, NumPy)는 수치 배열과 행렬 연산을 제공합니다. np는 이 도구의 별칭이며, Path는 실행 결과를 저장할 경로 객체입니다. 이 셀에서는 입력을 계산하지 않습니다.
import numpy as np
from pathlib import Path

# %% 셀 2 값과 형태 확인
# 외부 자료를 내려받지 않고 모든 원소를 코드에 명시합니다. 손으로 내적을 확인하기에 작은 배열을 선택했습니다. shape는 각 축의 길이이고 ndim은 축의 개수입니다. reshape는 원소 수를 보존해야 합니다.
# 각 예제는 별도의 배열입니다. 자동으로 서로 변환되는 과정이 아닙니다.
scalar = np.array(7)
x = np.array([2, 3])
w = np.array([4, 5])
A = np.array([[1, 2, 3], [4, 5, 6]])
B = np.array([[1, 0], [0, 1], [1, 1]])
T = np.arange(12).reshape(2, 2, 3)
for name, value in [("scalar", scalar), ("x", x), ("A", A), ("T", T)]:
    print(name, "shape=", value.shape, "ndim=", value.ndim)

# %% 셀 3 원소별 곱과 내적
# 별표(*)는 원소별 곱이고 골뱅이(@)는 이 실습에서 내적 또는 행렬곱입니다. x와 w는 길이가 각각 2이므로 대응 원소의 곱을 합하면 23입니다. 검증문(Assertion)은 이 손계산과 코드가 일치하는지 확인합니다.
elementwise = x * w
dot_value = x @ w
prediction = dot_value + 1
print("elementwise:", elementwise.tolist())
print("dot:", int(dot_value))
print("prediction with b=1:", int(prediction))
assert elementwise.tolist() == [8, 15]
assert int(dot_value) == 23
assert int(prediction) == 24

# %% 셀 4 행렬곱과 실패 조건
# A는 (2,3), B는 (3,2)입니다. 가운데 길이 3이 같아야 곱할 수 있고 결과는 (2,2)입니다. A의 첫 행과 B의 첫 열을 곱해 더하면 1×1+2×0+3×1=4입니다. 길이가 맞지 않는 A@A는 의도한 실패 예이며, 예외 처리로 확인합니다.
C = A @ B
print("A @ B:", C.tolist(), "shape=", C.shape)
assert C.tolist() == [[4, 5], [10, 11]]
try:
    invalid = A @ A
except ValueError:
    print("Expected rejection: inner dimensions do not match.")
else:
    raise AssertionError("잘못된 행렬곱이 거부되지 않았습니다.")

# %% 셀 5 브로드캐스팅 확인
# 벡터 v의 (3,)과 열 배열의 (3,1)은 같은 형태가 아닙니다. 두 배열을 그대로 빼면 (3,3)으로 브로드캐스팅(Broadcasting)됩니다. 오류가 나지 않더라도 표본별 차이를 계산하려는 의도와 다를 수 있습니다.
v = np.array([1, 2, 3])
column = v.reshape(3, 1)
unintended = v - column
intended = column - column
print("(3,) minus (3,1):", unintended.shape)
print("(3,1) minus (3,1):", intended.shape)
assert unintended.shape == (3, 3)
assert intended.shape == (3, 1)
print("All numeric and shape assertions passed.")
