import streamlit as st
from datetime import date

# -----------------------------
# PAGE CONFIG (BRAND FEEL)
# -----------------------------
st.set_page_config(
    page_title="FocusFlow - Goals System",
    page_icon="🎯",
    layout="wide"
)

# -----------------------------
# CUSTOM UI STYLE (CLEAN SaaS LOOK)
# -----------------------------
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-text {
        color: #666;
        margin-bottom: 20px;
    }
    .card {
        padding: 15px;
        border-radius: 12px;
        background-color: #f8f9fb;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# APP HEADER
# -----------------------------
st.markdown("<div class='main-title'>🎯 FocusFlow</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Your daily execution system for discipline, focus, and growth</div>", unsafe_allow_html=True)

st.write(f"📅 {date.today().strftime('%A, %B %d, %Y')}")

st.divider()

# -----------------------------
# SMART GOALS (EXPANDED)
# -----------------------------
SMART_GOALS = {
    "Reading": [
        "Read 10 pages",
        "Read 20 pages",
        "Read 30 minutes",
        "Summarize 1 chapter",
        "Highlight 5 key ideas",
        "Read non-fiction article"
    ],
    "Walking": [
        "2,000 steps",
        "5,000 steps",
        "10,000 steps",
        "30 min walk",
        "Outdoor walk",
        "Stretch after walk"
    ],
    "Gym": [
        "Full body workout",
        "Upper body day",
        "Lower body day",
        "20 min cardio",
        "Hydrate 1L water",
        "Protein intake tracked"
    ],
    "Work": [
        "Top 3 priorities completed",
        "1 hour deep work",
        "Email cleanup",
        "Plan tomorrow",
        "Finish pending task",
        "No distraction work block (45 min)"
    ]
}

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "completed" not in st.session_state:
    st.session_state.completed = {}

if "custom_goals" not in st.session_state:
    st.session_state.custom_goals = {}

if "points" not in st.session_state:
    st.session_state.points = 0

# -----------------------------
# CONFETTI EFFECT (REPLACEMENT FOR BALLOONS)
# -----------------------------
def celebrate():
    st.success("🔥 Goal completed! Keep building momentum.")
    st.snow()  # visual confetti-style effect

# -----------------------------
# SIDEBAR DASHBOARD
# -----------------------------
st.sidebar.header("📊 Daily Dashboard")

total_goals = 0
completed_goals = 0

for cat in SMART_GOALS:
    total_goals += len(SMART_GOALS[cat])
    completed_goals += sum(st.session_state.completed.get(cat, {}).values()) if cat in st.session_state.completed else 0

# include custom goals
for cat in st.session_state.custom_goals:
    total_goals += len(st.session_state.custom_goals[cat])
    completed_goals += sum(st.session_state.completed.get(cat, {}).values())

rate = completed_goals / total_goals if total_goals else 0

st.sidebar.metric("Completed", completed_goals)
st.sidebar.metric("Total", total_goals)
st.sidebar.progress(rate)

st.sidebar.metric("Points", st.session_state.points)

if st.session_state.points >= 100:
    st.sidebar.success("Level: Gold 🥇")
elif st.session_state.points >= 50:
    st.sidebar.info("Level: Silver 🥈")
else:
    st.sidebar.warning("Level: Bronze 🥉")

# -----------------------------
# ADD CUSTOM GOALS (PRO FEATURE)
# -----------------------------
st.sidebar.header("➕ Add Personal Goal")

with st.sidebar.form("add_goal_form"):
    category = st.selectbox("Category", list(SMART_GOALS.keys()) + ["Custom"])
    new_goal = st.text_input("Enter your goal")

    submitted = st.form_submit_button("Add Goal")

    if submitted and new_goal:
        if category == "Custom":
            category = "Personal"

        if category not in st.session_state.custom_goals:
            st.session_state.custom_goals[category] = []

        st.session_state.custom_goals[category].append(new_goal)
        st.success("Goal added successfully!")

# -----------------------------
# MAIN TABS
# -----------------------------
tabs = st.tabs(list(SMART_GOALS.keys()) + list(st.session_state.custom_goals.keys()))

all_categories = list(SMART_GOALS.keys()) + list(st.session_state.custom_goals.keys())

for i, category in enumerate(all_categories):

    with tabs[i]:
        st.markdown(f"### 📌 {category}")

        goals = SMART_GOALS.get(category, []) + st.session_state.custom_goals.get(category, [])

        if category not in st.session_state.completed:
            st.session_state.completed[category] = {}

        col1, col2 = st.columns([2, 1])

        with col1:
            for goal in goals:
                done = st.checkbox(goal, key=f"{category}_{goal}")

                prev = st.session_state.completed[category].get(goal, False)

                if done and not prev:
                    st.session_state.points += 10
                    celebrate()

                st.session_state.completed[category][goal] = done

        with col2:
            st.markdown("### 📊 Progress")

            total = len(goals)
            done_count = sum(st.session_state.completed[category].get(g, False) for g in goals)

            progress = done_count / total if total else 0

            st.progress(progress)
            st.write(f"{done_count} / {total}")

            st.markdown("### 🏆 Completed")
            for g in goals:
                if st.session_state.completed[category].get(g):
                    st.success(g)

        st.divider()

# -----------------------------
# FOOTER MOTIVATION PANEL
# -----------------------------
st.markdown("## 💬 Focus Message")

if completed_goals == 0:
    st.info("Start small. One goal creates momentum.")
elif completed_goals < 5:
    st.success("You're building rhythm. Keep going.")
elif completed_goals < 10:
    st.success("Momentum is building. Stay locked in.")
else:
    st.success("Elite execution today. You’re ahead of most people.")
