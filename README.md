# ⚡ NeetCode 150 — DSA Tracker

A dark-themed, Streamlit-based DSA progress tracker for all 150 NeetCode problems — with direct LeetCode links, per-problem notes, and persistent progress tracking.

> Built as part of my public **Learning Journey** on LinkedIn. Solving NeetCode 150 in Java, one problem at a time.

---

## 🚀 Live Demo

<!-- Replace with your Streamlit Cloud URL after deployment -->
**[→ Open Tracker](https://your-app.streamlit.app)**

---

## ✨ Features

- **All 150 problems** in NeetCode order, grouped by category
- **Direct LeetCode links** — opens the problem on your logged-in profile
- **Mark as solved** — checkbox with auto-save to `progress.json`
- **Per-problem notes** — save your approach, time complexity, edge cases
- **Stats dashboard** — Easy / Medium / Hard breakdown with progress bars
- **Filters** — by category, difficulty, status, or keyword search
- **Export / Import** — back up or restore progress as JSON

---

## 📁 Project Structure

```
.
├── app.py                  # Main Streamlit app
├── neetcode150_data.py     # All 150 problem definitions (title, slug, difficulty)
├── requirements.txt        # Python dependencies
├── progress.json           # Auto-generated progress file (gitignore this locally)
└── README.md
```

---

## 🛠️ Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/your-username/neetcode-tracker.git
cd neetcode-tracker

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

Progress is saved to `progress.json` in the same directory — fully persistent locally.

---

## ☁️ Deploy on Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Connect your GitHub repo, set `app.py` as the main file
4. Click **Deploy**

> **Note:** Streamlit Cloud has an ephemeral filesystem — `progress.json` resets on each restart. Use the **Export / Import JSON** buttons in the sidebar to back up your progress between sessions.

---

## 📊 Problems Covered

| Category              | Problems |
|-----------------------|----------|
| Arrays & Hashing      | 9        |
| Two Pointers          | 5        |
| Sliding Window        | 6        |
| Stack                 | 7        |
| Binary Search         | 7        |
| Linked List           | 11       |
| Trees                 | 15       |
| Tries                 | 3        |
| Heap / Priority Queue | 7        |
| Backtracking          | 9        |
| Graphs                | 13       |
| Advanced Graphs       | 6        |
| 1D DP                 | 12       |
| 2D DP                 | 11       |
| Greedy                | 8        |
| Intervals             | 6        |
| Math & Geometry       | 8        |
| Bit Manipulation      | 7        |
| **Total**             | **150**  |

---

## 🧰 Tech Stack

- **Python** — core language
- **Streamlit** — UI framework
- **JSON** — lightweight progress persistence
- **Google Fonts** — JetBrains Mono + Space Grotesk

---

## 👤 Author

**Adarsh Verma**
B.Tech IT (AI/ML) — AKTU, Kanpur
Documenting my learning journey daily on LinkedIn.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/your-profile)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github)](https://github.com/your-username)

---

## 📄 License

MIT — free to fork, adapt, and use for your own DSA grind.
