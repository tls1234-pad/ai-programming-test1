"""11주차 pytest 예제: 정상 입력, 예외, 점수 경계값을 확인합니다.

이 파일을 load_scores.py, scores.csv, empty.csv, weird.csv와 같은 폴더에 두세요.
터미널 실행: python -m pytest test_load_scores.py -v
AI 도움으로 작성한 예제이므로 README의 AI 사용 내역에 기록하세요.
"""

from pathlib import Path

import pytest

from load_scores import load_scores


# 테스트 파일과 같은 폴더에서 CSV를 찾습니다.
DATA_DIR = Path(__file__).resolve().parent


def test_정상파일의_유효한_성적과_건너뛴_기록():
    kept, skipped = load_scores(DATA_DIR / "scores.csv")

    # 동명이인은 둘 다 남기고, 이름에 들어 있는 쉼표도 보존해야 합니다.
    assert kept == [
        ("김하나", 88),
        ("최,네번", 77),
        ("김하나", 91),
        ("윤보람", 64),
        ("서한별", 95),
    ]
    assert skipped == [
        (3, "이두리,105", "점수가 0~100 밖"),
        (4, "박세찬,", "점수가 비어 있음"),
        (7, "정오름,-5", "점수가 0~100 밖"),
        (8, "한겨울,결석", "점수가 정수가 아님"),
        (9, "장미르,72,비고없음", "열 개수가 2가 아님"),
    ]


def test_헤더만_있는_파일():
    kept, skipped = load_scores(DATA_DIR / "empty.csv")
    assert kept == []
    assert skipped == []


def test_없는_파일은_예외가_발생한다(tmp_path):
    # pytest가 만든 임시 폴더 안의, 실제로 존재하지 않는 파일을 사용합니다.
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "없는파일.csv")


def test_이상한_입력과_점수_앞뒤_공백():
    kept, skipped = load_scores(DATA_DIR / "weird.csv")
    assert kept == [("한겨울", 77), ("윤보람", 88)]
    assert skipped == [
        (2, ",90", "이름이 비어 있음"),
        (3, "서한별,", "점수가 비어 있음"),
        (4, "서한별,", "점수가 비어 있음"),
        (5, "김,쉼표,1000", "점수가 0~100 밖"),
        (6, "이두리,-100", "점수가 0~100 밖"),
        (7, "박세찬,88.5", "점수가 정수가 아님"),
        (9, "장미르,7 2", "점수가 정수가 아님"),
    ]


# 아래 6개 입력은 각각 별도 테스트로 실행됩니다.
@pytest.mark.parametrize(
    "score, valid",
    [(-1, False), (0, True), (1, True), (99, True), (100, True), (101, False)],
)
def test_점수_경계값(tmp_path, score, valid):
    path = tmp_path / "boundary.csv"
    path.write_text(f"name,score\n경계학생,{score}\n", encoding="utf-8")

    kept, skipped = load_scores(path)

    if valid:
        assert kept == [("경계학생", score)]
        assert skipped == []
    else:
        assert kept == []
        assert skipped == [(2, f"경계학생,{score}", "점수가 0~100 밖")]
