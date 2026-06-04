# 🎓 MAKAUTSathi — AI Study Companion for MAKAUT BTech Students

Your all-in-one AI-powered study app built for Maulana Abul Kalam Azad University of Technology (MAKAUT) students. Powered by **Claude AI (Anthropic)**.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📝 Notes Generator | Syllabus-aligned detailed notes for any topic |
| 💡 Important Concepts | Key concepts & definitions prioritised for MAKAUT exams |
| ❓ PYQs with Answers | Previous year-style questions with model answers & examiner checklist |
| 🎯 Tips & Tricks | Mnemonics, shortcuts, paper-pattern insights |
| ✅ MCQs Practice | Auto-generated MCQ sets with auto-scoring |
| 📋 Notes Summary | Paste your notes → get crisp exam-ready summaries |
| 🧩 Quiz Mode | Interactive timed quiz with live score |
| 🃏 Flashcards | Flip-card revision with difficulty rating |
| 📐 Formula Sheet | All formulas, units & gotchas in one place |
| 📅 Study Planner | Day-by-day personalised MAKAUT exam study plan |

---

## 🚀 Setup Instructions

### 1. Clone / download this folder

```bash
cd MAKAUTSathi
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Anthropic API key

Edit `.streamlit/secrets.toml`:

```toml
ANTHROPIC_API_KEY = "sk-ant-api03-YOUR_KEY_HERE"
```

Get a **free** API key at: https://console.anthropic.com

### 4. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501` in your browser.

---

## 🌐 Deploy to Streamlit Cloud (Free)

1. Push this folder to a **GitHub repository**
2. Go to https://streamlit.io/cloud → **New app**
3. Connect your repo and set `app.py` as the main file
4. In **Advanced settings → Secrets**, add:
   ```
   ANTHROPIC_API_KEY = "sk-ant-api03-YOUR_KEY_HERE"
   ```
5. Click **Deploy** — your app is live!

---

## 📚 Supported Branches

- 💻 Computer Science & Engineering
- 📡 Electronics & Communication Engineering
- ⚙️ Mechanical Engineering
- 🏗️ Civil Engineering
- ⚡ Electrical Engineering
- 📚 Common / Core Subjects (Maths, Physics, Chemistry…)

---

## 🛠 Tech Stack

- **Frontend:** Streamlit (Python)
- **AI Backend:** Claude Sonnet 4 via Anthropic API
- **Language:** Python 3.9+

---

## 📄 Note on API

This app uses the **Anthropic API** (Claude AI), not OpenAI.  
Both offer free tiers — Anthropic's free tier is generous for student use.  
To switch to OpenAI, replace the `anthropic` client calls with `openai` calls targeting `gpt-4o-mini`.

---

Made with ❤️ for MAKAUT Students