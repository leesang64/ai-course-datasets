"""현재 과정 검증기로 연결합니다."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("validate_course.py")),run_name="__main__")
