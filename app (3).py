import streamlit as st
import json
import os
from datetime import datetime, date
from neetcode150_data import PROBLEMS

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NeetCode 150 Tracker",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Persistence helpers (JSON file-based) ────────────────────────────────────
DATA_FILE = "progress.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"solved": {}, "notes": {}, "dates": {}, "difficulty_override": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

# ── Categories & helpers ─────────────────────────────────────────────────────
CATEGORIES = list(dict.fromkeys(p["category"] for p in PROBLEMS))
DIFF_COLOR = {"Easy": "#00b894", "Medium": "#fdcb6e", "Hard": "#d63031"}
DIFF_BG    = {"Easy": "#00b89422", "Medium": "#fdcb6e22", "Hard": "#d6303122"}

def get_stats():
    total   = len(PROBLEMS)
    solved  = sum(1 for p in PROBLEMS if str(p["id"]) in data["solved"] and data["solved"][str(p["id"])])
    easy    = sum(1 for p in PROBLEMS if p["difficulty"] == "Easy")
    medium  = sum(1 for p in PROBLEMS if p["difficulty"] == "Medium")
    hard    = sum(1 for p in PROBLEMS if p["difficulty"] == "Hard")
    s_easy  = sum(1 for p in PROBLEMS if p["difficulty"] == "Easy"   and data["solved"].get(str(p["id"])))
    s_med   = sum(1 for p in PROBLEMS if p["difficulty"] == "Medium" and data["solved"].get(str(p["id"])))
    s_hard  = sum(1 for p in PROBLEMS if p["difficulty"] == "Hard"   and data["solved"].get(str(p["id"])))
    return total, solved, easy, medium, hard, s_easy, s_med, s_hard

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* Dark background */
.stApp { background: #0d1117; color: #e6edf3; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #161b22 !important;
    border-right: 1px solid #30363d;
}
[data-testid="stSidebar"] * { color: #e6edf3 !important; }

/* Metric cards */
.metric-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
}
.metric-num  { font-size: 2rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
.metric-label { font-size: 0.78rem; color: #8b949e; margin-top: 2px; text-transform: uppercase; letter-spacing: 1px; }

/* Progress bar */
.prog-wrap { background: #21262d; border-radius: 999px; height: 10px; overflow: hidden; margin: 6px 0; }
.prog-fill  { height: 10px; border-radius: 999px; transition: width 0.4s; }

/* Problem row */
.prob-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 14px;
    border-radius: 8px;
    border: 1px solid #21262d;
    background: #161b22;
    margin-bottom: 6px;
    transition: border-color 0.2s;
}
.prob-row:hover { border-color: #58a6ff; }
.prob-row.solved { border-color: #238636; background: #0d1f0d; }

.prob-num  { font-family: 'JetBrains Mono', monospace; color: #8b949e; font-size: 0.8rem; min-width: 28px; }
.prob-title { flex: 1; font-weight: 500; font-size: 0.92rem; }
.diff-badge {
    font-size: 0.72rem; font-weight: 600; padding: 2px 10px;
    border-radius: 999px; font-family: 'JetBrains Mono', monospace;
}
.lc-btn {
    background: #1f6feb; color: #fff; border: none;
    border-radius: 6px; padding: 4px 12px; font-size: 0.78rem;
    cursor: pointer; text-decoration: none; font-weight: 600;
}
.lc-btn:hover { background: #388bfd; }

/* Category header */
.cat-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: #58a6ff;
    border-bottom: 1px solid #21262d;
    padding-bottom: 6px; margin: 22px 0 10px;
}

/* Selectbox / inputs dark */
.stSelectbox > div, .stTextInput > div > div, .stTextArea > div > div {
    background: #21262d !important; border-color: #30363d !important; color: #e6edf3 !important;
}

/* Checkbox */
.stCheckbox > label { color: #e6edf3 !important; }

/* Buttons */
.stButton > button {
    background: #21262d; border: 1px solid #30363d; color: #e6edf3;
    border-radius: 6px; font-family: 'Space Grotesk', sans-serif;
}
.stButton > button:hover { border-color: #58a6ff; color: #58a6ff; }

/* Expander */
.streamlit-expanderHeader { background: #161b22 !important; color: #e6edf3 !important; }
.streamlit-expanderContent { background: #0d1117 !important; }

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ NC-150 Tracker")
    st.markdown("---")

    # Filter controls
    st.markdown("### Filters")
    sel_cat  = st.selectbox("Category", ["All"] + CATEGORIES)
    sel_diff = st.selectbox("Difficulty", ["All", "Easy", "Medium", "Hard"])
    sel_stat = st.selectbox("Status", ["All", "Solved", "Unsolved"])
    search   = st.text_input("🔍 Search problems", placeholder="e.g. Two Sum")

    st.markdown("---")
    st.markdown("### Actions")
    if st.button("🔄 Reset All Progress", use_container_width=True):
        st.session_state.data = {"solved": {}, "notes": {}, "dates": {}, "difficulty_override": {}}
        save_data(st.session_state.data)
        st.rerun()

    # Export
    export_json = json.dumps(data, indent=2)
    st.download_button("💾 Export Progress (JSON)", export_json, "neetcode_progress.json", use_container_width=True)

    # Import
    uploaded = st.file_uploader("📂 Import Progress", type="json")
    if uploaded:
        imported = json.load(uploaded)
        st.session_state.data = imported
        save_data(imported)
        st.success("Imported!")
        st.rerun()

# ── Main ──────────────────────────────────────────────────────────────────────
total, solved, easy, medium, hard, s_easy, s_med, s_hard = get_stats()
pct = round(solved / total * 100, 1)

st.markdown("# ⚡ NeetCode 150 — DSA Tracker")
st.caption("Track your grind. Every solved problem brings you closer to the offer.")

# ── Stats row ────────────────────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-num" style="color:#58a6ff">{solved}/{total}</div>
        <div class="metric-label">Total Solved</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-num" style="color:#00b894">{s_easy}/{easy}</div>
        <div class="metric-label">Easy</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-num" style="color:#fdcb6e">{s_med}/{medium}</div>
        <div class="metric-label">Medium</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-num" style="color:#d63031">{s_hard}/{hard}</div>
        <div class="metric-label">Hard</div>
    </div>""", unsafe_allow_html=True)

with col5:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-num" style="color:#a371f7">{pct}%</div>
        <div class="metric-label">Complete</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Overall progress bar
st.markdown(f"""
<div style="margin-bottom:4px;font-size:0.82rem;color:#8b949e;">Overall Progress</div>
<div class="prog-wrap">
  <div class="prog-fill" style="width:{pct}%;background:linear-gradient(90deg,#1f6feb,#a371f7)"></div>
</div>
<div style="font-size:0.78rem;color:#8b949e;margin-bottom:18px;">{pct}% — {total-solved} remaining</div>
""", unsafe_allow_html=True)

# Per-difficulty mini bars
dc1, dc2, dc3 = st.columns(3)
for col, label, s, t, color in [
    (dc1, "Easy",   s_easy, easy,   "#00b894"),
    (dc2, "Medium", s_med,  medium, "#fdcb6e"),
    (dc3, "Hard",   s_hard, hard,   "#d63031"),
]:
    p = round(s/t*100,1) if t else 0
    with col:
        st.markdown(f"""
        <div style="font-size:0.75rem;color:{color};font-weight:600;margin-bottom:3px;">{label} {s}/{t}</div>
        <div class="prog-wrap"><div class="prog-fill" style="width:{p}%;background:{color}"></div></div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ── Filter problems ───────────────────────────────────────────────────────────
filtered = PROBLEMS
if sel_cat  != "All":   filtered = [p for p in filtered if p["category"] == sel_cat]
if sel_diff != "All":   filtered = [p for p in filtered if p["difficulty"] == sel_diff]
if sel_stat == "Solved":   filtered = [p for p in filtered if data["solved"].get(str(p["id"]))]
if sel_stat == "Unsolved": filtered = [p for p in filtered if not data["solved"].get(str(p["id"]))]
if search:
    q = search.lower()
    filtered = [p for p in filtered if q in p["title"].lower() or q in p["category"].lower()]

# ── Render problems by category ──────────────────────────────────────────────
current_cat = None
for prob in filtered:
    pid = str(prob["id"])
    lc_url = f"https://leetcode.com/problems/{prob['leetcode_slug']}/"

    if prob["category"] != current_cat:
        current_cat = prob["category"]
        cat_probs   = [p for p in filtered if p["category"] == current_cat]
        cat_solved  = sum(1 for p in cat_probs if data["solved"].get(str(p["id"])))
        st.markdown(f"""
        <div class="cat-header">{current_cat}
          <span style="color:#8b949e;font-size:0.75rem;font-weight:400;margin-left:10px;">
            {cat_solved}/{len(cat_probs)}
          </span>
        </div>""", unsafe_allow_html=True)

    is_solved = bool(data["solved"].get(pid))
    diff  = prob["difficulty"]
    dc    = DIFF_COLOR[diff]
    db    = DIFF_BG[diff]
    solved_class = "solved" if is_solved else ""
    check_icon   = "✅" if is_solved else "⬜"

    # Problem row (HTML display)
    st.markdown(f"""
    <div class="prob-row {solved_class}">
      <span class="prob-num">#{prob['id']}</span>
      <span class="prob-title">{check_icon} {prob['title']}</span>
      <span class="diff-badge" style="color:{dc};background:{db};">{diff}</span>
      <a href="{lc_url}" target="_blank" class="lc-btn">LeetCode ↗</a>
    </div>
    """, unsafe_allow_html=True)

    # Controls (checkbox + notes in expander)
    c1, c2 = st.columns([1, 6])
    with c1:
        checked = st.checkbox("Solved", value=is_solved, key=f"chk_{pid}", label_visibility="collapsed")
        if checked != is_solved:
            data["solved"][pid] = checked
            if checked:
                data["dates"][pid] = str(date.today())
            else:
                data["dates"].pop(pid, None)
            save_data(data)
            st.rerun()
    with c2:
        with st.expander("📝 Notes", expanded=False):
            note = st.text_area(
                "Notes",
                value=data["notes"].get(pid, ""),
                key=f"note_{pid}",
                placeholder="Approach, time complexity, edge cases...",
                label_visibility="collapsed",
                height=80,
            )
            if st.button("Save", key=f"save_{pid}"):
                data["notes"][pid] = note
                save_data(data)
                st.success("Saved!", icon="✅")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
solved_dates = sorted([(v, k) for k, v in data["dates"].items() if v], reverse=True)
if solved_dates:
    last_date, last_pid = solved_dates[0]
    last_prob = next((p["title"] for p in PROBLEMS if str(p["id"]) == last_pid), "?")
    st.caption(f"🕒 Last solved: **{last_prob}** on {last_date}")
st.caption("Built for Adarsh's Learning Journey • NeetCode 150")
