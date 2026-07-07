# 제주도 카페 상권 분석 대시보드

`제주상권.csv`(소상공인 상가업소 데이터) 중 `상권업종소분류명`이 "카페"인 데이터를 필터링하여
지역별 분포와 지도 시각화를 제공하는 Streamlit 앱입니다.

## 로컬 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Community Cloud 배포

1. 이 저장소를 GitHub에 올립니다. (`app.py`, `제주상권.csv`, `requirements.txt` 포함)
2. https://share.streamlit.io 접속 후 GitHub 계정으로 로그인합니다.
3. "New app" → 저장소/브랜치 선택 → Main file path에 `app.py` 입력 후 배포합니다.
4. `requirements.txt`가 저장소 루트에 있으면 자동으로 의존성이 설치됩니다.

## 파일 구성

| 파일 | 설명 |
|---|---|
| `app.py` | Streamlit 앱 소스 코드 |
| `제주상권.csv` | 원본 상권 데이터 (앱이 런타임에 직접 로드) |
| `requirements.txt` | Python 의존성 목록 |
| `.gitignore` | Git 추적 제외 목록 |
