import pandas as pd
import plotly.express as px
import streamlit as st


# --------------------------------------------------
# 기본 설정
# --------------------------------------------------

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide",
)

st.title("영화 데이터 그래프 도감 1 - 시간")

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
)


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜: YYYYMMDD 형태의 숫자를 실제 날짜형으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
    )

    # 숫자형 열 정리
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df.sort_values(["날짜", "순위"]).reset_index(drop=True)


df = load_data()


# --------------------------------------------------
# 그래프 1. 영화별 날짜별 일관객
# --------------------------------------------------

st.header("그래프 1. 영화별 일관객 변화")

movie_list = (
    df[["영화코드", "영화명"]]
    .drop_duplicates()
    .sort_values("영화명")
)

movie_options = dict(
    zip(movie_list["영화명"], movie_list["영화코드"])
)

selected_movie = st.selectbox(
    "영화를 선택하세요",
    options=list(movie_options.keys()),
)

selected_code = movie_options[selected_movie]

movie_df = (
    df[df["영화코드"] == selected_code]
    .sort_values("날짜")
    .copy()
)

fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"{selected_movie} - 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
    },
)

fig.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.subheader("이 그래프로 알 수 있는 것")

st.markdown(
    "선택한 영화의 날짜별 일관객 수 변화를 확인하여 시간에 따른 관객 수의 증가와 감소를 알 수 있다."
)


# --------------------------------------------------
# 그래프 2. 일관객 합계가 가장 큰 5편
# --------------------------------------------------

st.divider()
st.header("그래프 2. 일관객 합계 상위 5편의 날짜별 변화")

# 영화별 일관객 합계 계산
top5_movies = (
    df.groupby(["영화코드", "영화명"], as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
    .head(5)
)

# 상위 5편의 영화코드만 선택
top5_codes = top5_movies["영화코드"].tolist()

# 상위 5편의 날짜별 데이터 추출
top5_df = (
    df[df["영화코드"].isin(top5_codes)]
    .sort_values("날짜")
    .copy()
)

# 선 그래프 만들기
fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="이 기간 일관객 합계 상위 5편의 날짜별 일관객",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화",
    },
)

fig2.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수",
    legend_title="영화",
)

st.plotly_chart(
    fig2,
    use_container_width=True,
)

st.subheader("이 그래프로 알 수 있는 것")

st.markdown(
    "이 기간 동안 일관객 합계가 가장 큰 5편의 날짜별 관객 수 변화를 비교할 수 있다."
)


# --------------------------------------------------
# 그래프 3. 날짜별 10위권 일관객 합계
# --------------------------------------------------

st.divider()
st.header("그래프 3. 날짜별 10위권 일관객 합계")

# 날짜별 10위권 영화의 일관객 합계 계산
top10_daily = (
    df[df["순위"] <= 10]
    .groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

# 일관객 합계가 가장 큰 3일 찾기
top3_days = (
    top10_daily
    .nlargest(3, "일관객")
    .sort_values("날짜")
)

# 영역 그래프 만들기
fig3 = px.area(
    top10_daily,
    x="날짜",
    y="일관객",
    title="날짜별 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계",
    },
)

# 가장 큰 3일을 그래프 위에 표시
for _, row in top3_days.iterrows():
    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=row["날짜"].strftime("%Y-%m-%d"),
        showarrow=True,
        arrowhead=2,
        yshift=10,
    )

fig3.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>10위권 일관객 합계: %{y:,}명"
        "<extra></extra>"
    )
)

fig3.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계",
)

st.plotly_chart(
    fig3,
    use_container_width=True,
)

st.subheader("이 그래프로 알 수 있는 것")

st.markdown(
    "날짜별 10위권 영화의 일관객 합계를 비교하여 관객이 많이 몰린 날과 적게 몰린 날을 알 수 있다."
)


# --------------------------------------------------
# 그래프 4. 영화별 일관객 합계 TOP 10
# --------------------------------------------------

st.divider()
st.header("그래프 4. 영화별 일관객 합계 TOP 10")

# 영화별 일관객 합계와 10위권에 든 날수 계산
movie_summary = (
    df.groupby(["영화코드", "영화명"])
    .agg(
        일관객합계=("일관객", "sum"),
        십위권_일수=("순위", lambda x: (x <= 10).sum()),
    )
    .reset_index()
)

# 일관객 합계가 큰 TOP 10
top10_movies = (
    movie_summary
    .sort_values("일관객합계", ascending=False)
    .head(10)
    .sort_values("일관객합계", ascending=True)
)

# 가로 막대그래프
fig4 = px.bar(
    top10_movies,
    x="일관객합계",
    y="영화명",
    orientation="h",
    title="영화별 이 기간 일관객 합계 TOP 10",
    labels={
        "영화명": "영화",
        "일관객합계": "일관객 합계",
        "십위권_일수": "10위권에 든 날수",
    },
)

# 관객이 많은 영화가 위에 오도록 설정
fig4.update_layout(
    yaxis=dict(
        categoryorder="total ascending"
    ),
    xaxis_title="일관객 합계",
    yaxis_title="영화",
)

fig4.update_traces(
    hovertemplate=(
        "영화: %{y}"
        "<br>일관객 합계: %{x:,}명"
        "<br>10위권에 든 날수: %{customdata[0]}일"
        "<extra></extra>"
    ),
    customdata=top10_movies[["십위권_일수"]].values,
)

st.plotly_chart(
    fig4,
    use_container_width=True,
)

st.subheader("이 그래프로 알 수 있는 것")

st.markdown(
    "영화별 이 기간 일관객 합계를 비교하여 관객이 많이 본 영화와 10위권에 오래 머문 영화를 확인할 수 있다."
)


# --------------------------------------------------
# 그래프 5. 월 × 요일별 일관객 합계
# --------------------------------------------------

st.divider()
st.header("그래프 5. 월 × 요일별 일관객 합계")

# 날짜에서 월과 요일 추출
heatmap_df = df.copy()

heatmap_df["월"] = heatmap_df["날짜"].dt.month
heatmap_df["요일"] = heatmap_df["날짜"].dt.dayofweek

# 요일 이름 지정
weekday_names = {
    0: "월요일",
    1: "화요일",
    2: "수요일",
    3: "목요일",
    4: "금요일",
    5: "토요일",
    6: "일요일",
}

heatmap_df["요일명"] = heatmap_df["요일"].map(weekday_names)

# 월 × 요일별 일관객 합계
monthly_weekday = (
    heatmap_df
    .groupby(["월", "요일", "요일명"], as_index=False)["일관객"]
    .sum()
    .sort_values(["월", "요일"])
)

# 히트맵용 형태로 변환
pivot_df = monthly_weekday.pivot(
    index="월",
    columns="요일명",
    values="일관객",
)

# 요일 순서를 월요일 → 일요일로 지정
weekday_order = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일",
]

pivot_df = pivot_df.reindex(columns=weekday_order)

# 히트맵 만들기
fig5 = px.imshow(
    pivot_df,
    text_auto=".0f",
    aspect="auto",
    title="월 × 요일별 일관객 합계",
    labels={
        "x": "요일",
        "y": "월",
        "color": "일관객 합계",
    },
)

fig5.update_layout(
    xaxis_title="요일",
    yaxis_title="월",
)

st.plotly_chart(
    fig5,
    use_container_width=True,
)

st.subheader("이 그래프로 알 수 있는 것")

st.markdown(
    "월별과 요일별 일관객 합계를 비교하여 관객이 많이 몰린 월과 요일을 한눈에 확인할 수 있다."
)
