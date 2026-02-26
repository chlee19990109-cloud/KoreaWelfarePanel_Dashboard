import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# 과제
# 1. 주제에서 사용하는 변수 전처리 추가
# 2. 사이드바에 주제에서 사용하는 변수 필터 추가
# 3. 컬럼 레이아웃으로 주제별 시각화와 집계표(테이블) 나타내기

# 웹 페이지 타이틀
img = Image.open("sample.png")
st.set_page_config(layout="wide", page_title="복지패널 데이터분석 시각화 대시보드", page_icon=img)

# 한글 폰트 지정
plt.rc("font", family="Malgun Gothic")
# 마이너스 기호 깨짐 방지
plt.rcParams["axes.unicode_minus"] = False


# 데이터 로드 함수
# 캐시
@st.cache_data
def load_welfare(sav_path: str):
    raw_welfare = pd.read_csv(sav_path)
    welfare = raw_welfare.copy()
    welfare = welfare.rename(
        columns={
            "h10_g3": "sex",  #  성별
            "h10_g4": "birth_year",  #  태어난 연도
            "h10_g10": "marital_status",  #  혼인 상태
            "h10_g11": "religion",  #  종교
            "h10_eco9": "job_code",  #  직업 코드
            "p1002_8aq1": "income",  #  월급
            "h10_reg7": "region_code"
        }
    )  #  지역 코드

    # 전처리
    if "sex" in welfare.columns:
        welfare["sex"] = welfare["sex"].replace(9, np.nan)
        welfare["sex"] = welfare["sex"].map({1: "male", 2: "female"})

    if "income" in welfare.columns:
        welfare["income"] = welfare["income"].replace(9999, np.nan)
        welfare["income"] = np.where(welfare["income"] == 0, np.nan, welfare["income"])

    if "birth_year" in welfare.columns:
        welfare["birth_year"] = welfare["birth_year"].replace(9999, np.nan)
        welfare["age"] = 2015 - welfare["birth_year"] + 1

        def age_group(age):
            if pd.isnull(age):
                return np.nan
            elif age >= 60:
                return "old"
            elif age >= 30:
                return "middle"
            else:
                return "young"

        welfare["age_group"] = welfare["age"].apply(age_group)

    if "job_code" in welfare.columns:
        welfare["job_code"] = np.where(
            welfare["job_code"] == 9999, np.nan, welfare["job_code"]
        )
        job_list = pd.read_excel(
            "data/welfare_2015_codebook.xlsx", sheet_name="직종코드"
        )
        welfare = welfare.merge(job_list, how="left", on="job_code")
    
    if "religion" in welfare.columns:
        welfare["religion"] = welfare["religion"].replace(9, np.nan)
        welfare["religion"] = welfare["religion"].map({1: "Yes", 2: "No"})
    
    if "marital_status" in welfare.columns:
        welfare["marital_status"] = welfare["marital_status"].replace(9, np.nan)
        # 이혼율 = 이혼 / (유배우+이혼) * 100
        # 이혼 여부 변수 만들기
        def divorce_yn(marital_status):
            if marital_status == 1:
                return 'marriage'
            elif marital_status == 3:
                return 'divorce'
            else:
                return np.nan
        welfare['marriage'] = welfare['marital_status'].apply(divorce_yn)
    
    if "region_code" in welfare.columns:
        welfare["region_code"] = welfare["region_code"].replace(9, np.nan)
        region_list = pd.DataFrame({'region_code' : [1, 2, 3, 4, 5, 6, 7],
                            'region'      : ['서울',
                                             '수도권(인천/경기)',
                                             '부산/경남/울산',
                                             '대구/경북',
                                             '대전/충남',
                                             '강원/충북',
                                             '광주/전남/전북/제주도']})
        welfare = welfare.merge(region_list, how = 'left', on = 'region_code')
    
    return welfare


# 사이드바
st.sidebar.title("데이터 로드")
data_path = st.sidebar.text_input("데이터 파일 경로", value="data/welfare_2015.csv")

if st.sidebar.button("데이터 로드"):
    st.rerun()

# 메인
st.title("한국복지패널 대시보드")
st.markdown("데이터 출처: 복지패널 데이터 (로컬에 csv 파일 필요)")

# 데이터 로드
try:
    welfare = load_welfare(data_path)
    st.success("데이터 로드 완료: {}행 {}열".format(welfare.shape[0], welfare.shape[1]))
except Exception as e:
    st.error(f"데이터를 불러오는 데 실패했습니다. 경로와 파일을 확인하세요.\n에러: {e}")
    st.stop()

# 대시보드 레이아웃
# 필터
st.sidebar.header("필터")


# 성별 필터
if "sex" in welfare.columns:
    value_list = ["All"] + sorted(welfare["sex"].dropna().unique().tolist())
    select_sex = st.sidebar.selectbox("성별", value_list, index=0)
else:
    select_sex = "All"


# 연령 범위 필터
if "age" in welfare.columns:
    min_age = int(welfare["age"].dropna().min())
    max_age = int(welfare["age"].dropna().max())
    slider_range = st.sidebar.slider(
        "연령 범위", min_value=min_age, max_value=max_age, value=(min_age, max_age)
    )
    filter_button = st.sidebar.button("필터 적용")
else:
    slider_range = None


# 연령대 필터
# 여러 개 선택할 수 있는 multiselect
value_list = ["All"] + sorted(welfare["age_group"].dropna().unique().tolist())
if "age_group" in welfare.columns:
    select_multi_age_group = st.sidebar.multiselect(
        "확인하고 싶은 연령대를 선택하세요(복수 선택 가능)",
        value_list
    )
else:
    select_multi_age_group = "All"


# 직업 필터
# 여러 개 선택할 수 있는 multiselect
value_list = ["All"] + sorted(welfare["job"].dropna().unique().tolist())
if "job" in welfare.columns:
    select_multi_job = st.sidebar.multiselect(
        "확인하고 싶은 직업을 선택하세요(복수 선택 가능)",
        value_list
    )
else:
    select_multi_job = "All"


# 종교 유무 필터
if "religion" in welfare.columns:
    value_list = ["All"] + sorted(welfare["religion"].dropna().unique().tolist())
    select_religion = st.sidebar.selectbox("종교 유무", value_list, index=0)
else:
    select_religion = "All"


# 이혼 여부 필터
if "marriage" in welfare.columns:
    value_list = ["All"] + sorted(welfare["marriage"].dropna().unique().tolist())
    select_marriage = st.sidebar.selectbox("이혼 여부", value_list, index=0)
else:
    select_marriage = "All"


# 지역 필터
# 여러 개 선택할 수 있는 multiselect
value_list = ["All"] + sorted(welfare["region"].dropna().unique().tolist())
if "region" in welfare.columns:
    select_multi_region = st.sidebar.multiselect(
        "확인하고 싶은 지역을 선택하세요(복수 선택 가능)",
        value_list
    )
else:
    select_multi_region = "All"



# 성별에 따른 월급 차이 - '성별에 따라 월급이 다를까?'
st.subheader("1. 성별에 따른 월급 차이 - '성별에 따라 월급이 다를까?'")

if select_sex != "All" and "sex" in welfare.columns:
    tmp_welfare = welfare[welfare["sex"] == select_sex]
    st.write("필터로 선택한 데이터 첫 5행")
    st.table(tmp_welfare.head())

col1, col2 = st.columns([2, 1])
with col1:
    if "sex" in welfare.columns and "income" in welfare.columns:
        sex_income = (
            welfare.dropna(subset=["sex", "income"])
            .groupby("sex", as_index=False)
            .agg(mean_income=("income", "mean"))
        )
        # 시각화
        fig1, ax1 = plt.subplots()
        sns.barplot(x="sex", y="mean_income", data=sex_income, ax=ax1)
        plt.title("성별에 따른 평균 월급 막대 그래프")
        plt.xlabel("성별")
        plt.ylabel("평균 월급")
        for i, j in enumerate(sex_income["mean_income"]):
            ax1.annotate(
                round(j),
                (i, j),
                xytext=(0, 2),
                textcoords="offset points",
                fontsize=8,
                ha="center",
                color="black"
            )
        st.pyplot(fig1)
    else:
        st.info("성별/월급 변수가 없어 해당 그래프를 표시할 수 없습니다.")

with col2:
    st.markdown("테이블")
    if "sex" in welfare.columns and "income" in welfare.columns:
        st.write(sex_income)
    else:
        st.write("변수 없음")



# 나이와 월급의 관계 - '몇 살 때 월급을 가장 많이 받을까?'
st.subheader("2. 나이와 월급의 관계 - '몇 살 때 월급을 가장 많이 받을까?'")

if filter_button:
    tmp_welfare = welfare[
        (welfare["age"] >= slider_range[0]) & (welfare["age"] <= slider_range[1])
    ]
    st.write("필터로 선택한 데이터 첫 5행")
    st.table(tmp_welfare.head())

col1, col2 = st.columns([2, 1])
with col1:
    if "age" in welfare.columns and "income" in welfare.columns:
        age_income = (
            welfare.dropna(subset=["age", "income"])
            .groupby("age", as_index=False)
            .agg(mean_income=("income", "mean"))
        )
        # 시각화
        fig2, ax2 = plt.subplots()
        sns.lineplot(x="age", y="mean_income", data=age_income, ax=ax2)
        plt.title("나이에 따른 평균 월급 선 그래프")
        plt.xlabel("나이")
        plt.ylabel("평균 월급")
        st.pyplot(fig2)
    else:
        st.info("나이/월급 변수가 없어 해당 그래프를 표시할 수 없습니다.")

with col2:
    st.markdown("테이블")
    if "age" in welfare.columns and "income" in welfare.columns:
        st.write(age_income)
    else:
        st.write("변수 없음")

# 나머지 주제는 여러분들이 직접 만들어 보아요!

# 연령대에 따른 월급 차이 - 어떤 연령대의 월급이 가장 많을까?
st.subheader("3. 연령대에 따른 월급 차이 - 어떤 연령대의 월급이 가장 많을까?")

if select_multi_age_group != "All" and "age_group" in welfare.columns:
    tmp_welfare = welfare[welfare["age_group"].isin(select_multi_age_group)]
    st.write("필터로 선택한 데이터 첫 5행")
    st.table(tmp_welfare.head())

col1, col2 = st.columns([2, 1])
with col1:
    if "age_group" in welfare.columns and "income" in welfare.columns:
        age_group_income = (
            welfare.dropna(subset=["age_group", "income"])
            .groupby("age_group", as_index=False)
            .agg(mean_income=("income", "mean"))
        )
        # 시각화
        fig3, ax3 = plt.subplots()
        sns.barplot(
            x="age_group",
            y="mean_income",
            data=age_group_income,
            ax=ax3,
            order=["young", "middle", "old"]
        )
        plt.title("연령대에 따른 평균 월급 막대 그래프")
        plt.xlabel("연령대")
        plt.ylabel("평균 월급")
        st.pyplot(fig3)
    else:
        st.info("연령대/월급 변수가 없어 해당 그래프를 표시할 수 없습니다.")

with col2:
    st.markdown("테이블")
    if "age_group" in welfare.columns and "income" in welfare.columns:
        st.write(age_group_income)
    else:
        st.write("변수 없음")



# 연령대 및 성별 월급 차이 - 성별 월급 차이는 연령대별로 다를까?
st.subheader("4. 연령대 및 성별 월급 차이 - 성별 월급 차이는 연령대별로 다를까?")

if (
    select_sex != "All"
    and select_multi_age_group != "All"
    and "sex" in welfare.columns
    and "age_group" in welfare.columns
):
    tmp_welfare = welfare[
        (welfare["sex"] == select_sex)
        & (welfare["age_group"].isin(select_multi_age_group))
    ]
    st.write("필터로 선택한 데이터 첫 5행")
    st.table(tmp_welfare.head())

col1, col2 = st.columns([2, 1])
with col1:
    if (
        "sex" in welfare.columns
        and "age_group" in welfare.columns
        and "income" in welfare.columns
    ):
        age_group_sex_income = (
            welfare.dropna(subset=["age_group", "sex", "income"])
            .groupby(["age_group", "sex"], as_index=False)
            .agg(mean_income=("income", "mean"))
        )
        # 시각화
        fig4, ax4 = plt.subplots()
        sns.barplot(
            x="age_group",
            y="mean_income",
            hue="sex",
            data=age_group_sex_income,
            order=["young", "middle", "old"],
            ax=ax4
        )
        plt.title("연령대 및 성별에 따른 평균 월급 막대 그래프")
        plt.xlabel("연령대 및 성별")
        plt.ylabel("평균 월급")
        st.pyplot(fig4)
    else:
        st.info("연령대/성별/월급 변수가 없어 해당 그래프를 표시할 수 없습니다.")

with col2:
    st.markdown("테이블")
    if (
        "sex" in welfare.columns
        and "age_group" in welfare.columns
        and "income" in welfare.columns
    ):
        st.write(age_group_sex_income)
    else:
        st.write("변수 없음")



# 직업별 월급 차이 - 어떤 직업이 월급을 가장 많이 받을까?
st.subheader("5. 직업별 월급 차이 - 어떤 직업이 월급을 가장 많이 받을까?")

if select_multi_job != "All" and "job" in welfare.columns:
    tmp_welfare = welfare[welfare["job"].isin(select_multi_job)]
    st.write("필터로 선택한 데이터 첫 5행")
    st.table(tmp_welfare.head())

col1, col2 = st.columns([2, 1])
with col1:
    if "job" in welfare.columns and "income" in welfare.columns:
        job_income = (
            welfare.dropna(subset=["job", "income"])
            .groupby("job", as_index=False)
            .agg(mean_income=("income", "mean"))
        )
        top10 = job_income.sort_values("mean_income", ascending=False).head(10)
        # 시각화
        fig5, ax5 = plt.subplots()
        sns.barplot(y="job", x="mean_income", data=top10)
        plt.title("직업에 따른 상위 10개 평균 월급 막대 그래프")
        plt.xlabel("직업")
        plt.ylabel("평균 월급")
        st.pyplot(fig5)
    else:
        st.info("직업/월급 변수가 없어 해당 그래프를 표시할 수 없습니다.")

with col2:
    st.markdown("테이블")
    if "job" in welfare.columns and "income" in welfare.columns:
        st.write(top10)
    else:
        st.write("변수 없음")



# 성별 직업 빈도 - 성별로 어떤 직업이 가장 많을까?
st.subheader("6. 성별 직업 빈도 - 성별로 어떤 직업이 가장 많을까?")

if select_sex != "All" and "sex" in welfare.columns:
    tmp_welfare = welfare[welfare["sex"] == select_sex]
    st.write("필터로 선택한 데이터 첫 5행")
    st.table(tmp_welfare.head())

col1, col2 = st.columns([2, 1])
with col1:
    if "sex" in welfare.columns and "job" in welfare.columns:
        job_male = welfare[welfare['sex'] == 'male'].dropna(subset = ['job']) \
                                            .groupby('job', as_index = False) \
                                            .agg(n = ('job', 'count')) \
                                            .sort_values('n', ascending = False) \
                                            .head(10)
        # 시각화
        fig6_1, ax6_1 = plt.subplots()
        sns.barplot(x = 'n', y = 'job', data = job_male, ax=ax6_1, errorbar = None)
        plt.title("남성 직업 빈도 막대 그래프")
        plt.xlabel("N")
        plt.ylabel("직업")
        st.pyplot(fig6_1)
    else:
        st.info("성별에 해당되는 직업이 없어 그래프를 표시할 수 없습니다.")

with col2:
    st.markdown("테이블")
    if "sex" in welfare.columns and "job" in welfare.columns:
        st.write(job_male)
    else:
        st.write("변수 없음")

col1, col2 = st.columns([2, 1])
with col1:
    if "sex" in welfare.columns and "job" in welfare.columns:
        job_female = welfare[welfare['sex'] == 'female'].dropna(subset = ['job']) \
                                                .groupby('job', as_index = False) \
                                                .agg(n = ('job', 'count')) \
                                                .sort_values('n', ascending = False) \
                                                .head(10)
       # 시각화
        fig6_2, ax6_2 = plt.subplots()
        sns.barplot(x = 'n', y = 'job', data = job_female, ax=ax6_2, errorbar = None)
        plt.title("여성 직업 빈도 막대 그래프")
        plt.xlabel("N")
        plt.ylabel("직업")
        st.pyplot(fig6_2)
    else:
        st.info("성별에 해당되는 직업이 없어 그래프를 표시할 수 없습니다.")

with col2:
    st.markdown("테이블")
    if "sex" in welfare.columns and "job" in welfare.columns:
        st.write(job_female)
    else:
        st.write("변수 없음")



# 종교 유무에 따른 이혼율 - 종교가 있으면 이혼을 덜 할까?
st.subheader("7. 종교 유무에 따른 이혼율 - 종교가 있으면 이혼을 덜 할까?")

if select_religion != "All" and "religion" in welfare.columns:
    tmp_welfare = welfare[welfare["religion"] == select_religion]
    st.write("필터로 선택한 데이터 첫 5행")
    st.table(tmp_welfare.head())

col1, col2 = st.columns([2, 1])
with col1:
    if "religion" in welfare.columns and "marriage" in welfare.columns:
        religion_div = welfare.dropna(subset = ['religion', 'marriage']) \
                      .groupby('religion', as_index = False) \
                      ['marriage'] \
                      .value_counts(normalize = True)
        religion_div[religion_div['marriage'] == 'divorce']
        religion_div = religion_div[religion_div['marriage'] == 'divorce'] \
               .assign(proportion = religion_div['proportion'] * 100) \
               .round(2)
        # 시각화
        fig7, ax7 = plt.subplots()
        sns.barplot(
            x="religion",
            y="proportion",
            data=religion_div,
            ax=ax7,
            order=["Yes", "No"]
        )
        plt.title("종교 유무에 따른 이혼율 막대 그래프")
        plt.xlabel("종교")
        plt.ylabel("이혼율")
        st.pyplot(fig7)
    else:
        st.info("종교/이혼율 변수가 없어 해당 그래프를 표시할 수 없습니다.")

with col2:
    st.markdown("테이블")
    if "religion" in welfare.columns and "marriage" in welfare.columns:
        st.write(religion_div)
    else:
        st.write("변수 없음")



# 지역별 연령대 비율 - 어느 지역에 노년층이 많을까?
st.subheader("8. 지역별 연령대 비율 - 어느 지역에 노년층이 많을까?")

if select_multi_region != "All" and "region" in welfare.columns:
    tmp_welfare = welfare[welfare["region"].isin(select_multi_region)]
    st.write("필터로 선택한 데이터 첫 5행")
    st.table(tmp_welfare.head())

col1, col2 = st.columns([2, 1])
with col1:
    if "region" in welfare.columns and "age_group" in welfare.columns:
        region_age_group = welfare.dropna(subset = ['age_group']) \
                     .groupby('region', as_index = False) \
                     ['age_group'] \
                     .value_counts(normalize = True)
        region_age_group = region_age_group.assign(proportion = region_age_group['proportion'] * 100).round(2)
        
        pivot_region_age_group = region_age_group[['region', 'age_group', 'proportion']] \
                          .pivot(index   = 'region',
                          columns = 'age_group',
                          values  = 'proportion'
                          )
        pivot_region_age_group.sort_values('old')
        reorder_pivot_region_age_group = pivot_region_age_group.sort_values('old')[['young', 'middle', 'old']]
        
        # 시각화: 막대 그래프
        fig8_1, ax8_1 = plt.subplots()
        sns.barplot(
            y="region",
            x="proportion",
            hue="age_group",
            data=region_age_group,
            ax=ax8_1,
            hue_order=["old", "middle", "young"]
        )
        ax8_1.set_xlim(0, 60)
        plt.legend(loc = 'best')
        plt.title("지역에 따른 연령대 막대 그래프")
        plt.xlabel("비율")
        plt.ylabel("지역")
        st.pyplot(fig8_1)
        
        # 시각화: 누적 막대 그래프
        fig8_2, ax8_2 = plt.subplots()
        reorder_pivot_region_age_group.plot.barh(stacked=True, ax=ax8_2) # 오름 차순의 반대 = 축 전환
        # reorder_pivot_region_age_group.plot.bar(stacked = True) # 오름 차순
        plt.legend(bbox_to_anchor=(1.0, 1.0)) # 우상
        plt.legend(loc = 'best')
        plt.title("지역에 따른 연령대 누적 가로 막대 그래프")
        plt.xlabel("비율")
        plt.ylabel("지역")
        st.pyplot(fig8_2)    
    else:
        st.info("지역/연령대 변수가 없어 해당 그래프를 표시할 수 없습니다.")

with col2:
    st.markdown("테이블")
    if "region" in welfare.columns and "age_group" in welfare.columns:
        st.write(region_age_group)
    else:
        st.write("변수 없음")


# 끝
