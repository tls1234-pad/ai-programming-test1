from analysis import 불러오기, 정제, 반별평균

# PDF의 검증용 데이터 두 개를 같은 폴더에서 읽는다.
본 = 정제(불러오기("scores_2026.csv"))
미니 = 정제(불러오기("mini.csv"))


def test_정제하면_100행이_남는다():
    assert len(본) == 100


def test_반은_두_종류만_남는다():
    assert sorted(본["반"].unique()) == ["1반", "2반"]


def test_그룹합이_전체합과_같다():
    assert 본.groupby("반")["점수"].sum().sum() == 본["점수"].sum()


def test_손계산과_일치한다():
    assert len(미니) == 7
    assert 반별평균(미니)["1반"] == 80.0
    assert 반별평균(미니)["2반"] == 70.0
