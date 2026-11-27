import pandas as pd
from pathlib import Path

# 실행 위치가 달라도 이 파일과 같은 폴더의 CSV를 읽는다.
BASE_DIR = Path(__file__).resolve().parent


def 불러오기(파일명="scores_2026.csv", encoding="utf-8"):
    return pd.read_csv(BASE_DIR / 파일명, encoding=encoding)


def 정제(df):
    """빈 점수, 완전 중복, 공백, 범위 밖 점수를 순서대로 처리한다."""
    print("시작         ", len(df))
    df = df.dropna(subset=["점수"])
    print("빈 칸 제거   ", len(df))
    df = df.drop_duplicates().copy()
    print("중복 제거    ", len(df))
    #df["반"] = df["반"].str.strip()
    #df["과목"] = df["과목"].str.strip()
    print("공백 제거    ", len(df))
    df = df[(df["점수"] >= 0) & (df["점수"] <= 100)]
    print("범위 밖 제거 ", len(df))
    return df


def 반별평균(df):
    return df.groupby("반")["점수"].mean()


def 과목반별평균(df):
    return df.groupby(["과목", "반"])["점수"].mean()


def 반별통계(df):
    return df.groupby("반")["점수"].agg(
        개수="count", 평균="mean", 중앙값="median", 최댓값="max"
    ).round(2)


def main():
    # STEP 1. 원본 진단
    원본 = 불러오기()
    print("[STEP 1] 원본 진단")
    print("행과 열:", 원본.shape)
    print(원본.head(2))
    print("빈 점수:", 원본["점수"].isna().sum())
    print("완전 중복:", 원본.duplicated().sum())
    print("반 종류:", 원본["반"].unique())
    print("과목 종류:", 원본["과목"].unique())
    print(원본["점수"].describe())

    # STEP 2. 정제
    print("\n[STEP 2] 정제")
    df = 정제(원본)
    print("반 종류:", sorted(df["반"].unique()))
    print("과목 종류:", sorted(df["과목"].unique()))

    # STEP 3. 필터링, 그룹화, 통계
    print("\n[STEP 3] 분석")
    수학 = df[df["과목"] == "수학"]
    print("수학 행 수:", len(수학))
    print("\n반별 평균")
    print(반별평균(df).round(2))
    print("\n과목 × 반 평균")
    print(과목반별평균(df).round(2))
    print("\n과목 × 반 개수")
    print(df.groupby(["과목", "반"])["점수"].count())
    print("\n반별 통계")
    print(반별통계(df))

    # STEP 4. 합계, 개수, 스팟 체크 및 mini.csv 손계산 대조
    print("\n[STEP 4] 검증")
    그룹합 = df.groupby("반")["점수"].sum().sum()
    전체합 = df["점수"].sum()
    print("합계 일치:", 그룹합, 전체합, 그룹합 == 전체합)
    그룹개수 = df.groupby("반")["점수"].count().sum()
    print("개수 일치:", 그룹개수, len(df), 그룹개수 == len(df))
    점수들 = df[(df["반"] == "1반") & (df["과목"] == "수학")]["점수"]
    print("1반 수학 점수:", 점수들.tolist())
    if len(점수들) > 0:
        print("1반 수학 평균:", 점수들.sum() / len(점수들))
        print("그룹화 결과:", 과목반별평균(df).loc[("수학", "1반")])

    print("\nmini.csv 손계산 대조")
    미니 = 정제(불러오기("mini.csv"))
    print("정제 후 행 수:", len(미니))
    print(반별평균(미니).round(2))


if __name__ == "__main__":
    main()
