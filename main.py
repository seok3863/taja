
import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# -------------------------------
# 기본 설정
# -------------------------------
st.set_page_config(
    page_title="한컴 스타일 타자연습",
    page_icon="⌨️",
    layout="wide"
)

# -------------------------------
# 디자인 CSS
# -------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #eef5fc;
}
.main-title {
    background: linear-gradient(120deg, #1769aa, #3298dc);
    color: white;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 20px;
}
.main-title h1 {
    color: white;
    font-size: 35px;
}
.main-title p {
    color: white;
    font-size: 16px;
}
.menu-box {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #cbdced;
    text-align: center;
}
.target-text {
    background: white;
    border: 2px solid #3695d5;
    border-radius: 12px;
    padding: 25px;
    font-size: 23px;
    line-height: 1.8;
    text-align: center;
    color: #174b78;
}
.stat-box {
    background: white;
    border-radius: 12px;
    padding: 18px;
    border: 1px solid #cbdced;
    text-align: center;
}
.stat-number {
    font-size: 30px;
    font-weight: bold;
    color: #1678bd;
}
div.stButton > button {
    background-color: #2185c5;
    color: white;
    border-radius: 9px;
    border: none;
    font-weight: bold;
    min-height: 42px;
}
div.stButton > button:hover {
    background-color: #12649c;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 데이터
# -------------------------------
WORDS = [
    "학교", "컴퓨터", "대한민국", "친구", "행복",
    "노력", "도전", "미래", "과학", "우주",
    "반도체", "인공지능", "정보기술", "창의력",
    "스마트폰", "알고리즘", "프로그래밍"
]

SENTENCES = [
    "꾸준한 노력은 결국 좋은 결과를 만들어 낸다.",
    "오늘의 작은 도전이 내일의 큰 변화를 만든다.",
    "새로운 것을 배우는 일은 언제나 즐거운 경험이다.",
    "자신의 꿈을 향해 한 걸음씩 나아가자.",
    "과학과 기술은 우리의 미래를 변화시키고 있다.",
    "포기하지 않고 계속 도전하는 자세가 중요하다.",
    "반도체 기술은 현대 사회의 다양한 분야에서 활용된다.",
    "좋은 습관은 작은 실천에서부터 시작된다."
]

# -------------------------------
# 세션 데이터 초기화
# -------------------------------
defaults = {
    "records": [],
    "best_speed": 0,
    "test_active": False,
    "test_start": 0.0,
    "test_text": "",
    "game_active": False,
    "game_start": 0.0,
    "game_score": 0,
    "game_round": 0,
    "game_word": random.choice(WORDS),
    "game_history": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -------------------------------
# 공통 함수
# -------------------------------
def get_accuracy(target, typed):
    if not typed:
        return 0

    correct = sum(
        1 for i, char in enumerate(typed)
        if i < len(target) and char == target[i]
    )

    return round(correct / max(len(typed), len(target)) * 100, 1)


def save_record(speed, accuracy, category):
    record = {
        "종류": category,
        "타수": speed,
        "정확도": accuracy,
        "시간": time.strftime("%H:%M:%S")
    }

    st.session_state.records.append(record)
    st.session_state.best_speed = max(
        st.session_state.best_speed, speed
    )


def show_header():
    st.markdown("""
    <div class="main-title">
        <h1>⌨️ 한컴 스타일 타자연습</h1>
        <p>즐겁게 연습하고 나의 타자 실력을 높여 보세요!</p>
    </div>
    """, unsafe_allow_html=True)


def show_stats():
    a, b, c = st.columns(3)

    with a:
        st.metric("🏆 최고 타수", f"{st.session_state.best_speed} 타/분")

    with b:
        st.metric("📝 총 연습 횟수", f"{len(st.session_state.records)}회")

    with c:
        if st.session_state.records:
            avg = sum(
                r["정확도"] for r in st.session_state.records
            ) / len(st.session_state.records)
        else:
            avg = 0

        st.metric("🎯 평균 정확도", f"{avg:.1f}%")


# -------------------------------
# 상단 화면
# -------------------------------
show_header()
show_stats()

st.sidebar.title("📚 연습 메뉴")

menu = st.sidebar.radio(
    "원하는 연습을 선택하세요.",
    [
        "🏠 홈",
        "⌨️ 자리 연습",
        "📝 낱말 연습",
        "📖 문장 연습",
        "🎮 타자 게임",
        "⏱️ 타자 속도 측정",
        "🏆 기록실"
    ]
)

difficulty = st.sidebar.selectbox(
    "난이도",
    ["쉬움", "보통", "어려움"]
)

st.sidebar.markdown("---")
st.sidebar.caption("꾸준한 연습이 실력을 만듭니다!")

# -------------------------------
# 홈
# -------------------------------
if menu == "🏠 홈":

    st.subheader("안녕하세요! 타자연습에 오신 것을 환영합니다.")

    st.info("왼쪽 메뉴에서 원하는 연습을 선택해 보세요.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="menu-box">
            <h2>⌨️ 자리 연습</h2>
            <p>키보드 자판의 위치를 익혀 보세요.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="menu-box">
            <h2>📖 문장 연습</h2>
            <p>다양한 문장을 입력하며 실력을 키워 보세요.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="menu-box">
            <h2>🎮 타자 게임</h2>
            <p>제한 시간 안에 단어를 입력해 보세요.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="menu-box">
            <h2>⏱️ 속도 측정</h2>
            <p>1분 동안 나의 타자 속도를 측정해 보세요.</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("💡 타자 실력 향상 팁")
    st.write("""
    - 키보드를 보지 않고 입력하는 연습을 해 보세요.
    - 처음에는 속도보다 정확도를 중요하게 생각하세요.
    - 매일 조금씩 꾸준히 연습하는 것이 좋습니다.
    """)

# -------------------------------
# 자리 연습
# -------------------------------
elif menu == "⌨️ 자리 연습":

    st.subheader("⌨️ 키보드 자리 연습")

    st.write("각 손가락이 담당하는 자판 위치를 익혀 보세요.")

    st.markdown("""
    <div class="target-text">
    <h3>기본 자리</h3>
    <h2>ㅁ ㄴ ㅇ ㄹ / ㅓ ㅏ ㅣ</h2>
    <hr>
    <h3>윗자리</h3>
    <h2>ㅂ ㅈ ㄷ ㄱ ㅅ ㅛ ㅕ ㅑ ㅐ ㅔ</h2>
    <hr>
    <h3>아랫자리</h3>
    <h2>ㅋ ㅌ ㅊ ㅍ ㅠ ㅜ ㅡ</h2>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("다음 글자를 그대로 입력해 보세요.")

    target = "asdf jkl; qwer uiop zxcv nm"

    st.code(target)

    answer = st.text_input(
        "입력창",
        key="keyboard_answer"
    )

    if st.button("자리 연습 확인"):
        if answer == target:
            st.success("정확합니다! 자판 위치를 잘 익혔어요!")
        else:
            st.warning("아직 다릅니다. 천천히 다시 연습해 보세요.")

# -------------------------------
# 낱말 연습
# -------------------------------
elif menu == "📝 낱말 연습":

    st.subheader("📝 낱말 연습")

    if difficulty == "쉬움":
        word = random.choice(WORDS[:9])
    elif difficulty == "보통":
        word = random.choice(WORDS[:14])
    else:
        word = random.choice(WORDS[9:])

    if "practice_word" not in st.session_state:
        st.session_state.practice_word = word

    st.markdown(
        f'<div class="target-text">{st.session_state.practice_word}</div>',
        unsafe_allow_html=True
    )

    answer = st.text_input(
        "위 낱말을 입력하세요.",
        key="word_answer"
    )

    if st.button("정답 확인", key="word_check"):
        target = st.session_state.practice_word

        if answer == target:
            st.success("정답입니다! 🎉")
            st.session_state.practice_word = random.choice(WORDS)
            st.session_state.pop("word_answer", None)
        else:
            st.error("다시 입력해 보세요.")

    if st.button("다음 낱말"):
        st.session_state.practice_word = random.choice(WORDS)
        st.session_state.pop("word_answer", None)
        st.rerun()

# -------------------------------
# 문장 연습
# -------------------------------
elif menu == "📖 문장 연습":

    st.subheader("📖 문장 연습")

    if "practice_sentence" not in st.session_state:
        st.session_state.practice_sentence = random.choice(SENTENCES)

    if difficulty == "어려움":
        st.session_state.practice_sentence = (
            "반도체 기술의 발전은 인공지능과 정보통신 산업의 혁신을 이끌고 있다."
        )

    target = st.session_state.practice_sentence

    st.markdown(
        f'<div class="target-text">{target}</div>',
        unsafe_allow_html=True
    )

    answer = st.text_area(
        "문장을 그대로 입력하세요.",
        height=120,
        key="sentence_answer"
    )

    if st.button("문장 채점하기"):
        accuracy = get_accuracy(target, answer)

        if answer == target:
            st.success("완벽합니다! 모든 글자를 정확하게 입력했어요!")
        else:
            st.warning(f"정확도: {accuracy}%")

            st.write("**정답 문장:**")
            st.write(target)

    if st.button("다른 문장 연습"):
        st.session_state.practice_sentence = random.choice(SENTENCES)
        st.session_state.pop("sentence_answer", None)
        st.rerun()

# -------------------------------
# 타자 게임
# -------------------------------
elif menu == "🎮 타자 게임":

    st.subheader("🎮 1분 타자 게임")

    st.write("화면에 나타나는 단어를 제한 시간 안에 입력하세요!")

    if not st.session_state.game_active:

        if st.button("게임 시작!", type="primary"):
            st.session_state.game_active = True
            st.session_state.game_start = time.time()
            st.session_state.game_score = 0
            st.session_state.game_round = 0
            st.session_state.game_history = []
            st.session_state.game_word = random.choice(WORDS)
            st.rerun()

    else:
        st_autorefresh(
            interval=1000,
            limit=None,
            key="game_refresh"
        )

        elapsed = time.time() - st.session_state.game_start
        remaining = max(0, 60 - int(elapsed))

        if remaining <= 0:
            st.session_state.game_active = False
            st.success(
                f"게임 종료! 최종 점수는 {st.session_state.game_score}점입니다."
            )
            st.rerun()

        st.metric("남은 시간", f"{remaining}초")
        st.metric("현재 점수", f"{st.session_state.game_score}점")

        st.markdown(
            f'<div class="target-text">{st.session_state.game_word}</div>',
            unsafe_allow_html=True
        )

        with st.form(
            key=f"game_form_{st.session_state.game_round}"
        ):
            answer = st.text_input("단어 입력")
            submitted = st.form_submit_button("입력!")

        if submitted:
            if answer.strip() == st.session_state.game_word:
                st.session_state.game_score += 10
                st.session_state.game_history.append("정답")
                st.success("정답! +10점")
            else:
                st.session_state.game_history.append("오답")
                st.error("오답입니다!")

            st.session_state.game_round += 1
            st.session_state.game_word = random.choice(WORDS)
            st.rerun()

# -------------------------------
# 타자 속도 측정
# -------------------------------
elif menu == "⏱️ 타자 속도 측정":

    st.subheader("⏱️ 1분 타자 속도 측정")

    st.write("60초 동안 문장을 입력하고 타자 실력을 확인하세요.")

    if not st.session_state.test_active:

        if st.button("측정 시작!", type="primary"):
            st.session_state.test_active = True
            st.session_state.test_start = time.time()
            st.session_state.test_text = ""
            st.rerun()

    else:
        st_autorefresh(
            interval=1000,
            limit=None,
            key="test_refresh"
        )

        elapsed = time.time() - st.session_state.test_start
        remaining = max(0, 60 - int(elapsed))

        target = random.choice(SENTENCES)

        st.metric("남은 시간", f"{remaining}초")

        typed = st.text_area(
            "아래 문장을 보고 계속 입력하세요.",
            value=st.session_state.test_text,
            height=130,
            key="test_input"
        )

        st.session_state.test_text = typed

        st.markdown(
            f'<div class="target-text">{target}</div>',
            unsafe_allow_html=True
        )

        if remaining <= 0:
            st.session_state.test_active = False

            speed = round(len(typed) / 60 * 60)
            accuracy = 100

            save_record(speed, accuracy, "1분 타자 측정")

            st.success("측정이 끝났습니다!")
            st.metric("입력 글자 수", f"{len(typed)}자")
            st.metric("평균 타수", f"{speed} 타/분")

            st.rerun()

# -------------------------------
# 기록실
# -------------------------------
elif menu == "🏆 기록실":

    st.subheader("🏆 나의 타자 기록실")

    if st.session_state.records:

        st.write("지금까지의 연습 기록입니다.")

        st.dataframe(
            st.session_state.records,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("📊 타자 기록 그래프")

        speeds = [
            r["타수"] for r in st.session_state.records
        ]

        st.line_chart(speeds)

        st.subheader("🎯 정확도 그래프")

        accuracies = [
            r["정확도"] for r in st.session_state.records
        ]

        st.bar_chart(accuracies)

        if st.button("기록 초기화"):
            st.session_state.records = []
            st.session_state.best_speed = 0
            st.rerun()

    else:
        st.info("아직 기록이 없습니다. 타자 연습을 시작해 보세요!")

# -------------------------------
# 하단
# -------------------------------
st.markdown("---")

st.markdown(
    "<center>⌨️ 나만의 타자연습 프로그램 | Made with Streamlit</center>",
    unsafe_allow_html=True
)
