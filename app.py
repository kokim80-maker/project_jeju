import pandas as pd
import plotly.express as px
import streamlit as st
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium

st.set_page_config(page_title="제주 카페 상권 분석", page_icon="☕", layout="wide")

CSV_PATH = "제주상권.csv"


@st.cache_data
def load_cafe_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="cp949")
    cafe = df[df["상권업종소분류명"] == "카페"].copy()
    cols = [
        "상호명", "시도명", "시군구명", "행정동명", "법정동명",
        "도로명주소", "지번주소", "경도", "위도",
    ]
    cafe = cafe[cols].dropna(subset=["경도", "위도"])
    cafe = cafe.rename(columns={"경도": "lon", "위도": "lat"})
    return cafe


cafe_df = load_cafe_data(CSV_PATH)

st.title("☕ 제주도 카페 상권 분석")
st.caption("데이터 출처: 제주상권.csv (상권업종소분류명 = '카페')")

# ---------------- 사이드바 필터 ----------------
st.sidebar.header("필터")

sigungu_list = sorted(cafe_df["시군구명"].unique())
selected_sigungu = st.sidebar.multiselect(
    "시군구 선택", sigungu_list, default=sigungu_list
)

filtered = cafe_df[cafe_df["시군구명"].isin(selected_sigungu)]

dong_list = sorted(filtered["행정동명"].unique())
selected_dong = st.sidebar.multiselect(
    "행정동 선택 (선택 안 하면 전체)", dong_list, default=[]
)
if selected_dong:
    filtered = filtered[filtered["행정동명"].isin(selected_dong)]

keyword = st.sidebar.text_input("상호명 검색")
if keyword:
    filtered = filtered[filtered["상호명"].str.contains(keyword, case=False, na=False)]

st.sidebar.markdown(f"**검색 결과: {len(filtered):,}개 카페**")

# ---------------- 개요 지표 ----------------
col1, col2, col3 = st.columns(3)
col1.metric("전체 카페 수", f"{len(cafe_df):,}개")
col2.metric("필터링된 카페 수", f"{len(filtered):,}개")
top_dong = (
    filtered["행정동명"].value_counts().idxmax() if not filtered.empty else "-"
)
col3.metric("카페가 가장 많은 행정동", top_dong)

st.divider()

# ---------------- 지역별 분포 ----------------
st.subheader("📊 지역별 카페 분포")

tab1, tab2 = st.tabs(["시군구별", "행정동별 TOP 15"])

with tab1:
    sigungu_count = (
        filtered["시군구명"].value_counts().reset_index()
    )
    sigungu_count.columns = ["시군구명", "카페 수"]
    fig1 = px.bar(
        sigungu_count, x="시군구명", y="카페 수", color="시군구명", text="카페 수"
    )
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, width="stretch")

with tab2:
    dong_count = (
        filtered["행정동명"].value_counts().head(15).reset_index()
    )
    dong_count.columns = ["행정동명", "카페 수"]
    fig2 = px.bar(
        dong_count.sort_values("카페 수"),
        x="카페 수", y="행정동명", orientation="h", text="카페 수"
    )
    st.plotly_chart(fig2, width="stretch")

st.divider()

# ---------------- 지도 시각화 ----------------
st.subheader("🗺️ 카페 위치 지도")

map_type = st.radio("지도 유형", ["마커 클러스터", "히트맵"], horizontal=True)

if not filtered.empty:
    center_lat = filtered["lat"].mean()
    center_lon = filtered["lon"].mean()
else:
    center_lat, center_lon = 33.38, 126.55

m = folium.Map(location=[center_lat, center_lon], zoom_start=10, tiles="CartoDB positron")

if map_type == "마커 클러스터":
    cluster = MarkerCluster().add_to(m)
    for _, row in filtered.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"{row['상호명']}<br>{row['도로명주소']}",
            tooltip=row["상호명"],
            icon=folium.Icon(color="orange", icon="coffee", prefix="fa"),
        ).add_to(cluster)
else:
    heat_data = filtered[["lat", "lon"]].values.tolist()
    HeatMap(heat_data, radius=12).add_to(m)

st_folium(m, use_container_width=True, height=600)

st.divider()

# ---------------- 원본 데이터 ----------------
with st.expander("📋 필터링된 원본 데이터 보기"):
    st.dataframe(filtered.reset_index(drop=True), width="stretch")
