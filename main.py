import streamlit as st
import pandas as pd
from app_utils import CurriculumManagement

# 웹페이지 부분
# 직접 시연해보고 싶다면, app_utils.py, main.py를 받고 requirements.txt의 라이브러리를 다운받은 후,
# pycharm 터미널에 들어가 [> streamlit run main.py] 로 치면 된다.

# 페이지 전체 설정
st.set_page_config(
    page_title="Yoon's Portfolio",
    page_icon=":computer:",
    layout="wide"
)

# 본문
st.title("나만의 커리큘럼 생성기")
st.write("역할: 자신이 원하는 공부를 하면서 어떤 순서로 할지 모르는 경우가 많았을 것인데, 그 가이드라인을 제시해줌")

with st.form("Plan"):

    # 과목 목록과 선이수 관계를 엑셀 파일로 입력받음
    subject_file = st.file_uploader("List of Subjects", type=["csv", "xlsx"])
    relation_file = st.file_uploader("Relation of Subjects", type=["csv", "xlsx"])

    submit = st.form_submit_button("Submit")

    if submit:

        # 엑셀 파일 정보를 dataframe으로 변환
        subject_df = pd.read_csv(subject_file)
        subject_df = subject_df.set_index('id')
        relation_df = pd.read_csv(relation_file)

        # 커리큘럼을 짜주는 클래스
        c = CurriculumManagement(subject_df, relation_df)

        # 만약 자료에 사이클이 존재한다면: 그건 잘못된 자료이므로 판단 거부
        if c.is_acyclic():
            st.error("Acyclic problem")

        # 더 쉬운 내용을 빠르게 배우도록 구성
        result = c.easier_order()

        # 데이터프레임 출력
        st.dataframe(subject_df.loc[result])




