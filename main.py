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

# 여기에 직접 문장을 작성하세요.
st.markdown(
    "_이곳에 이 그래프로 알 수 있는 것을 한 문장으로 작성하세요._"
)


# --------------------------------------------------
# 그래프 2. 앞으로 추가할 영역
# --------------------------------------------------

st.divider()
st.header("그래프 2")

# 앞으로 두 번째 그래프를 여기에 추가하세요.

st.subheader("이 그래프로 알 수 있는 것")

# 여기에 직접 문장을 작성하세요.
st.markdown(
    "_이곳에 이 그래프로 알 수 있는 것을 한 문장으로 작성하세요._"
)


# --------------------------------------------------
# 그래프 3. 앞으로 추가할 영역
# --------------------------------------------------

st.divider()
st.header("그래프 3")

# 앞으로 세 번째 그래프를 여기에 추가하세요.

st.subheader("이 그래프로 알 수 있는 것")

# 여기에 직접 문장을 작성하세요.
st.markdown(
    "_이곳에 이 그래프로 알 수 있는 것을 한 문장으로 작성하세요._"
)
