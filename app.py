import streamlit as st
from openai import OpenAI
import json
import random

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MAKAUTSathi 🎓",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS — Indigo/Deep-space theme with sharp accents
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Sora', sans-serif !important;
    box-sizing: border-box;
}

/* ── App background ── */
.stApp {
    background: #080c14;
    color: #dde3f0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0c111e !important;
    border-right: 1px solid #1e2a42;
}
section[data-testid="stSidebar"] * { color: #c8d4ef !important; }
section[data-testid="stSidebar"] .stRadio > label { font-weight: 600; }

/* ── Main header banner ── */
.mkst-hero {
    background: linear-gradient(135deg, #1a237e 0%, #283593 40%, #0d47a1 100%);
    border: 1px solid #3949ab55;
    border-radius: 16px;
    padding: 32px 28px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 40px rgba(26,35,126,0.5);
}
.mkst-hero::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at top right, rgba(100,130,255,0.18), transparent 60%);
    pointer-events: none;
}
.mkst-hero h1 {
    font-size: 2.4rem; font-weight: 800;
    color: #ffffff; margin: 0 0 6px;
    letter-spacing: -0.5px;
}
.mkst-hero p {
    font-size: 1rem; color: rgba(255,255,255,0.78);
    margin: 0; font-weight: 400;
}
.mkst-hero .badge-row {
    display: flex; gap: 10px; margin-top: 14px; flex-wrap: wrap;
}
.mkst-badge {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.22);
    border-radius: 20px; padding: 4px 14px;
    font-size: 0.78rem; color: #cdd5f0 !important;
    font-weight: 500;
}

/* ── Cards ── */
.mkst-card {
    background: #0f1525;
    border: 1px solid #1e2a42;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 16px;
    transition: border-color 0.25s;
}
.mkst-card:hover { border-color: #3949ab; }
.mkst-card h3 {
    color: #7986cb; margin: 0 0 8px; font-size: 1rem; font-weight: 600;
}
.mkst-card p {
    color: #8896b8; font-size: 0.86rem; margin: 0; line-height: 1.55;
}

/* ── AI Response box ── */
.mkst-result {
    background: #0b1120;
    border: 1px solid #1e2a42;
    border-left: 4px solid #3f51b5;
    border-radius: 10px;
    padding: 24px 26px;
    margin-top: 18px;
    color: #cdd5f0;
    line-height: 1.75;
    font-size: 0.95rem;
}
.mkst-result h1, .mkst-result h2, .mkst-result h3 { color: #7986cb; }
.mkst-result strong { color: #9fa8da; }
.mkst-result code {
    font-family: 'JetBrains Mono', monospace !important;
    background: #1a2035; padding: 2px 7px; border-radius: 5px;
    font-size: 0.85rem; color: #80cbc4;
}
.mkst-result ul, .mkst-result ol { padding-left: 22px; }

/* ── Flashcard ── */
.fc-card {
    background: linear-gradient(145deg, #0f1525, #141d32);
    border: 2px solid #283593;
    border-radius: 18px;
    padding: 48px 36px;
    text-align: center;
    min-height: 240px;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    box-shadow: 0 12px 40px rgba(26,35,126,0.35);
    margin: 20px 0;
}
.fc-card.answer { border-color: #1b5e20; }
.fc-label {
    font-size: 0.72rem; letter-spacing: 3px; text-transform: uppercase;
    color: #5c6bc0; font-weight: 600; margin-bottom: 18px;
}
.fc-front-text {
    font-size: 1.3rem; font-weight: 600; color: #9fa8da; line-height: 1.55;
}
.fc-back-text {
    font-size: 1.05rem; color: #a5d6a7; line-height: 1.7;
}

/* ── Score / Result box ── */
.mkst-score {
    background: linear-gradient(135deg, #1a237e, #283593);
    border-radius: 14px; padding: 28px 24px;
    text-align: center; color: #fff;
    margin: 18px 0;
    box-shadow: 0 8px 30px rgba(26,35,126,0.4);
}
.mkst-score h1 { font-size: 2.4rem; margin: 0; }
.mkst-score p { opacity: 0.85; margin: 6px 0 0; }

/* ── Correct / Wrong chips ── */
.chip-correct {
    background: rgba(27,94,32,0.25); border-left: 3px solid #2e7d32;
    border-radius: 8px; padding: 14px 16px; margin: 8px 0; color: #a5d6a7;
}
.chip-wrong {
    background: rgba(183,28,28,0.2); border-left: 3px solid #c62828;
    border-radius: 8px; padding: 14px 16px; margin: 8px 0; color: #ef9a9a;
}

/* ── Streamlit widget overrides ── */
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
    background: #0f1525 !important;
    border: 1px solid #1e2a42 !important;
    color: #cdd5f0 !important;
    border-radius: 8px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #3949ab !important;
    box-shadow: 0 0 0 2px rgba(57,73,171,0.3) !important;
}
.stButton > button {
    background: #1a237e !important;
    color: #fff !important;
    border: 1px solid #283593 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'Sora', sans-serif !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #283593 !important;
    border-color: #3949ab !important;
    box-shadow: 0 4px 18px rgba(26,35,126,0.45) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1565c0, #1a237e) !important;
    border: none !important;
    box-shadow: 0 4px 16px rgba(21,101,192,0.4) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 22px rgba(21,101,192,0.55) !important;
}
.stProgress > div > div { background: #1565c0 !important; }
.stDownloadButton > button {
    background: #0d2137 !important;
    border: 1px solid #1565c0 !important;
    color: #90caf9 !important;
}
div[data-testid="stTab"] button {
    color: #7986cb !important;
    font-weight: 600 !important;
}
div[data-testid="stTab"] button[aria-selected="true"] {
    color: #fff !important;
    border-bottom: 2px solid #3f51b5 !important;
}
.stSlider > div > div > div { background: #1565c0 !important; }
.stAlert { border-radius: 10px !important; }

/* ── Section headings ── */
.section-title {
    font-size: 1.6rem; font-weight: 700; color: #7986cb;
    margin-bottom: 6px; letter-spacing: -0.3px;
}
.section-sub {
    color: #576080; font-size: 0.88rem; margin-bottom: 22px;
}

/* ── Quiz progress bar text ── */
.quiz-meta {
    display: flex; justify-content: space-between;
    color: #576080; font-size: 0.85rem; margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SUBJECTS DATA
# ─────────────────────────────────────────────────────────────────────────────
SUBJECTS = {
    "💻 Computer Science & Engineering": [
        "Data Structures and Algorithms",
        "Operating Systems",
        "Database Management Systems",
        "Computer Networks",
        "Software Engineering",
        "Theory of Computation",
        "Compiler Design",
        "Computer Architecture & Organization",
        "Artificial Intelligence",
        "Machine Learning",
        "Web Technologies",
        "Object Oriented Programming (Java/C++)",
        "Discrete Mathematics",
        "Design and Analysis of Algorithms",
    ],
    "📡 Electronics & Communication Engg.": [
        "Analog Electronics",
        "Digital Electronics",
        "Signals and Systems",
        "Communication Systems",
        "Electromagnetic Field Theory",
        "VLSI Design",
        "Microprocessor & Microcontroller",
        "Control Systems",
        "Antenna & Wave Propagation",
        "Digital Signal Processing",
    ],
    "⚙️ Mechanical Engineering": [
        "Thermodynamics",
        "Fluid Mechanics",
        "Strength of Materials",
        "Machine Design",
        "Manufacturing Technology",
        "Theory of Machines",
        "Heat and Mass Transfer",
        "Engineering Mechanics",
        "Industrial Engineering",
        "Refrigeration & Air Conditioning",
    ],
    "🏗️ Civil Engineering": [
        "Structural Analysis",
        "Concrete Technology (RCC Design)",
        "Soil Mechanics & Foundation Engineering",
        "Fluid Mechanics & Hydraulics",
        "Transportation Engineering",
        "Environmental Engineering",
        "Surveying",
        "Steel Structure Design",
    ],
    "⚡ Electrical Engineering": [
        "Circuit Theory & Networks",
        "Electrical Machines",
        "Power Systems",
        "Control Systems",
        "Power Electronics",
        "Microprocessor & Microcontroller",
        "Electromagnetic Field Theory",
        "Digital Electronics",
        "Measurement & Instrumentation",
    ],
    "📚 Common / Core Subjects": [
        "Engineering Mathematics (M1, M2, M3)",
        "Engineering Physics",
        "Engineering Chemistry",
        "Basic Electronics & Electrical Engg.",
        "Environmental Science",
        "English & Communication Skills",
        "Engineering Drawing & Graphics",
        "Computer Programming (C / Python)",
        "Economics for Engineers",
    ],
}

SEMESTERS = [f"Semester {i}" for i in range(1, 9)]

# ─────────────────────────────────────────────────────────────────────────────
# AI CLIENT & HELPERS
# ─────────────────────────────────────────────────────────────────────────────
# ── Groq is 100% free and uses the standard OpenAI SDK ──────────────────────
GROQ_MODEL = "llama-3.3-70b-versatile"   # best free model on Groq


@st.cache_resource
def get_client() -> OpenAI:
    return OpenAI(
        api_key=st.secrets["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1",
    )


SYSTEM_DEFAULT = (
    "You are MAKAUTSathi, an expert educational AI assistant for MAKAUT "
    "(Maulana Abul Kalam Azad University of Technology) BTech students in West Bengal, India. "
    "Provide accurate, MAKAUT-syllabus-aligned, well-structured responses. "
    "Use markdown formatting. Be comprehensive yet exam-focused."
)


def call_ai(prompt: str, system: str = SYSTEM_DEFAULT, max_tokens: int = 2200) -> str:
    client = get_client()
    with st.spinner("🤖 MAKAUTSathi is generating your content…"):
        resp = client.chat.completions.create(
            model=GROQ_MODEL,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt},
            ],
        )
    return resp.choices[0].message.content


def call_ai_json(prompt: str, max_tokens: int = 3000) -> list | None:
    """Call AI and parse JSON array response."""
    client = get_client()
    with st.spinner("🤖 MAKAUTSathi is generating…"):
        resp = client.chat.completions.create(
            model=GROQ_MODEL,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": "Return ONLY a valid JSON array, no markdown fences, no preamble, no extra text."},
                {"role": "user",   "content": prompt},
            ],
        )
    raw = resp.choices[0].message.content.strip()
    # Strip markdown fences if present
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else raw
        if raw.startswith("json"):
            raw = raw[4:]
    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        return None


def download_btn(content: str, filename: str):
    st.download_button(
        "⬇️  Download as .txt",
        data=content,
        file_name=filename,
        mime="text/plain",
        use_container_width=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="mkst-hero">
    <h1>🎓 MAKAUTSathi</h1>
    <p>Your AI-powered study companion — built exclusively for MAKAUT BTech students</p>
    <div class="badge-row">
        <span class="mkst-badge">📝 Notes</span>
        <span class="mkst-badge">❓ PYQs</span>
        <span class="mkst-badge">🧩 Quizzes</span>
        <span class="mkst-badge">🃏 Flashcards</span>
        <span class="mkst-badge">📐 Formulas</span>
        <span class="mkst-badge">📅 Study Planner</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎓 MAKAUTSathi")
    st.caption("Navigate below ↓")
    st.divider()

    feature = st.radio(
        "Feature",
        [
            "🏠  Home",
            "📝  Notes Generator",
            "💡  Important Concepts",
            "❓  PYQs with Answers",
            "🎯  Tips & Tricks",
            "✅  MCQs Practice",
            "📋  Notes Summary",
            "🧩  Quiz Mode",
            "🃏  Flashcards",
            "📐  Formula Sheet",
            "📅  Study Planner",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("#### 📚 Context Selector")

    branch = st.selectbox("Branch", list(SUBJECTS.keys()), label_visibility="visible")
    subject = st.selectbox("Subject", SUBJECTS[branch], label_visibility="visible")
    semester = st.selectbox("Semester", SEMESTERS, index=3, label_visibility="visible")

    st.divider()
    st.markdown(
        "<div style='text-align:center;color:#3d4f6e;font-size:0.78rem;line-height:1.6'>"
        "Made with ❤️ for MAKAUT Students<br>"
        # "<span style='color:#3949ab'>Claude AI — Anthropic</span>"
        "</div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# PAGES
# ─────────────────────────────────────────────────────────────────────────────

# ═══════════════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════════════
if feature == "🏠  Home":
    st.markdown('<div class="section-title">Welcome to MAKAUTSathi 👋</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Select a feature from the sidebar to get started. Here\'s everything that\'s available:</div>', unsafe_allow_html=True)

    features_data = [
        ("📝", "Notes Generator", "Detailed syllabus-aligned notes for any topic — export as .txt"),
        ("💡", "Important Concepts", "Key concepts, definitions & exam-frequent topics at a glance"),
        ("❓", "PYQs with Answers", "Previous year question–style Q&A with examiner tips"),
        ("🎯", "Tips & Tricks", "Mnemonics, shortcuts & MAKAUT exam strategies"),
        ("✅", "MCQs Practice", "Instant MCQ sets with answer reveal & auto-scoring"),
        ("📋", "Notes Summary", "Paste your notes → get crisp revision-ready summaries"),
        ("🧩", "Quiz Mode", "Timed interactive quiz with live score tracking"),
        ("🃏", "Flashcards", "Flip-card revision with Easy / Moderate / Difficult rating"),
        ("📐", "Formula Sheet", "All important formulas, units & gotchas in one place"),
        ("📅", "Study Planner", "Personalised day-by-day exam study plan for MAKAUT"),
    ]

    cols = st.columns(3)
    for i, (icon, name, desc) in enumerate(features_data):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="mkst-card">
                <h3>{icon} {name}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="mkst-result" style="margin-top:8px">
        <h3 style="margin-top:0">🚀 Quick Start Guide</h3>
        <ol>
            <li>Pick your <strong>Branch → Subject → Semester</strong> in the left sidebar</li>
            <li>Choose a <strong>Feature</strong> from the navigation menu</li>
            <li>Enter a topic and click <strong>Generate</strong></li>
            <li>Download or copy your study material instantly</li>
        </ol>
        <p style="color:#576080;font-size:0.85rem;margin-bottom:0">
        💡 Tip: Bookmark this app and use it daily — consistent short sessions beat last-minute cramming!
        </p>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# NOTES GENERATOR
# ═══════════════════════════════════════════════════
elif feature == "📝  Notes Generator":
    st.markdown('<div class="section-title">📝 Notes Generator</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">{subject} · {semester}</div>', unsafe_allow_html=True)

    topic = st.text_input("Topic / Chapter", placeholder="e.g., Binary Search Trees, Linked Lists, Deadlocks…")

    col1, col2, col3 = st.columns(3)
    with col1:
        detail = st.select_slider("Detail Level", ["Brief", "Standard", "Detailed", "Comprehensive"], value="Standard")
    with col2:
        inc_examples = st.checkbox("✅ Include Examples", value=True)
    with col3:
        inc_diagrams = st.checkbox("✅ Describe Diagrams", value=True)

    if st.button("📝 Generate Notes", type="primary", use_container_width=True):
        if not topic.strip():
            st.warning("Please enter a topic first.")
        else:
            prompt = f"""Generate {detail.lower()} study notes for MAKAUT BTech {semester} students.

**Subject:** {subject}
**Topic:** {topic}

Structure:
## 1. Introduction & Definition
## 2. Core Concepts (bullet-point list)
## 3. Detailed Explanation
{"## 4. Worked Examples & Illustrations" if inc_examples else ""}
{"## 5. Diagrams & Visual Representations (describe clearly)" if inc_diagrams else ""}
## 6. Important Points to Remember
## 7. Exam Tips (MAKAUT-specific, 3–4 points)

Align strictly with MAKAUT syllabus. Use clear headings, bullet points, and code blocks where relevant."""

            result = call_ai(prompt, max_tokens=2800)
            st.markdown('<div class="mkst-result">', unsafe_allow_html=True)
            st.markdown(result)
            st.markdown('</div>', unsafe_allow_html=True)
            download_btn(result, f"MAKAUTSathi_{subject}_{topic}_Notes.txt")


# ═══════════════════════════════════════════════════
# IMPORTANT CONCEPTS
# ═══════════════════════════════════════════════════
elif feature == "💡  Important Concepts":
    st.markdown('<div class="section-title">💡 Important Concepts</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">{subject} · {semester}</div>', unsafe_allow_html=True)

    topic = st.text_input("Topic / Chapter", placeholder="e.g., Sorting Algorithms, Normalization, Thermodynamic Cycles…")
    exam_focus = st.checkbox("🎯 Prioritise MAKAUT exam-frequent concepts", value=True)

    if st.button("💡 Get Important Concepts", type="primary", use_container_width=True):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            prompt = f"""List the most important concepts for MAKAUT BTech {semester} — **{subject}**: *{topic}*.
{"Emphasise concepts that appear most frequently in MAKAUT university question papers." if exam_focus else ""}

Format exactly as:
## 🔑 Must-Know Core Concepts
(5–7 concepts with 2-line explanation each)

## ⭐ Important Concepts
(4–6 concepts)

## 💡 Advanced / Application Concepts
(3–4 concepts)

## 📌 Key Definitions
(7+ terms with crisp definitions)

## 🎯 Top MAKAUT Exam Topics (from this chapter)
(Numbered list of 5 topics most asked in MAKAUT papers, with expected marks)"""

            result = call_ai(prompt, max_tokens=2200)
            st.markdown('<div class="mkst-result">', unsafe_allow_html=True)
            st.markdown(result)
            st.markdown('</div>', unsafe_allow_html=True)
            download_btn(result, f"MAKAUTSathi_{subject}_{topic}_Concepts.txt")


# ═══════════════════════════════════════════════════
# PYQs WITH ANSWERS
# ═══════════════════════════════════════════════════
elif feature == "❓  PYQs with Answers":
    st.markdown('<div class="section-title">❓ PYQs with Answers</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">{subject} · {semester}</div>', unsafe_allow_html=True)

    topic = st.text_input("Topic / Chapter", placeholder="e.g., Trees, SQL Queries, 2nd Law of Thermodynamics…")

    col1, col2, col3 = st.columns(3)
    with col1:
        q_type = st.selectbox("Question Type", ["All Types", "Short Answer (2–5 marks)", "Long Answer (10–15 marks)", "Numerical / Derivation"])
    with col2:
        num_q = st.slider("Number of Questions", 3, 10, 5)
    with col3:
        marks_scheme = st.selectbox("Marks Scheme", ["MAKAUT Standard", "2 marks", "5 marks", "10 marks", "15 marks"])

    if st.button("❓ Generate PYQ-Style Q&A", type="primary", use_container_width=True):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            prompt = f"""Generate {num_q} MAKAUT-style previous year exam questions **with detailed answers** for:

**Subject:** {subject} | **Topic:** {topic} | **Semester:** {semester}
**Question Type:** {q_type} | **Marks:** {marks_scheme}

For each question use this format:

---
**Q[N]. [Question text]** *(Marks: X — MAKAUT 20XX pattern)*

**✏️ Model Answer:**
[Complete answer as expected in MAKAUT exam]

**📌 Examiner's Checklist (what to include for full marks):**
- [Point 1]
- [Point 2]
- [Point 3]

---

Make questions realistic, cover different sub-topics, and include at least one diagram-based or numerical question where applicable."""

            result = call_ai(prompt, max_tokens=3000)
            st.markdown('<div class="mkst-result">', unsafe_allow_html=True)
            st.markdown(result)
            st.markdown('</div>', unsafe_allow_html=True)
            download_btn(result, f"MAKAUTSathi_{subject}_{topic}_PYQs.txt")


# ═══════════════════════════════════════════════════
# TIPS & TRICKS
# ═══════════════════════════════════════════════════
elif feature == "🎯  Tips & Tricks":
    st.markdown('<div class="section-title">🎯 Tips & Tricks</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">{subject} · {semester}</div>', unsafe_allow_html=True)

    topic = st.text_input("Topic (optional — leave blank for general subject tips)", placeholder="e.g., Sorting, Normalization…")
    categories = st.multiselect(
        "Select categories:",
        ["🧠 Mnemonics & Memory Tricks", "⚡ Problem-Solving Shortcuts", "📝 Exam Writing Tips",
         "⚠️ Common Mistakes to Avoid", "⏱️ Time Management", "🔁 Quick Revision Strategies",
         "📌 MAKAUT Paper Pattern Insights"],
        default=["🧠 Mnemonics & Memory Tricks", "⚡ Problem-Solving Shortcuts", "📝 Exam Writing Tips"],
    )

    if st.button("🎯 Get Tips & Tricks", type="primary", use_container_width=True):
        cats = ", ".join(categories) if categories else "General"
        prompt = f"""Give practical tips and tricks for MAKAUT BTech {semester} students:

**Subject:** {subject}
**Topic:** {topic if topic.strip() else "General subject tips"}
**Categories needed:** {cats}

For each category requested, create a clearly labelled section with 4–6 specific, actionable tips.
Include MAKAUT-specific advice (paper pattern, answer-writing format, marking scheme awareness).
Use bullet points and bold key phrases. Add emojis for readability."""

        result = call_ai(prompt, max_tokens=2000)
        st.markdown('<div class="mkst-result">', unsafe_allow_html=True)
        st.markdown(result)
        st.markdown('</div>', unsafe_allow_html=True)
        download_btn(result, f"MAKAUTSathi_{subject}_Tips.txt")


# ═══════════════════════════════════════════════════
# MCQs PRACTICE
# ═══════════════════════════════════════════════════
elif feature == "✅  MCQs Practice":
    st.markdown('<div class="section-title">✅ MCQs Practice</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">{subject} · {semester}</div>', unsafe_allow_html=True)

    # Initialise session state
    if "mcqs" not in st.session_state:
        st.session_state.mcqs = []
        st.session_state.mcq_answers = {}
        st.session_state.mcq_submitted = False

    topic = st.text_input("Topic", placeholder="e.g., Linked Lists, ER Model, Newton's Laws…", key="mcq_topic")
    col1, col2 = st.columns(2)
    with col1:
        num_mcqs = st.slider("Number of MCQs", 5, 20, 10)
    with col2:
        difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard", "Mixed"], value="Mixed")

    if st.button("✅ Generate MCQs", type="primary", use_container_width=True):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            prompt = f"""Generate {num_mcqs} MCQs for MAKAUT BTech {semester} students.
Subject: {subject}, Topic: {topic}, Difficulty: {difficulty}.

Return ONLY a JSON array like:
[{{"q":"Question text?","options":["A) opt1","B) opt2","C) opt3","D) opt4"],"answer":"A","explanation":"Reason A is correct"}}]"""
            data = call_ai_json(prompt)
            if data:
                st.session_state.mcqs = data
                st.session_state.mcq_answers = {}
                st.session_state.mcq_submitted = False
            else:
                st.error("Could not parse MCQs. Please try again.")

    if st.session_state.mcqs:
        mcqs = st.session_state.mcqs

        if not st.session_state.mcq_submitted:
            for i, mcq in enumerate(mcqs):
                st.markdown(f"**Q{i+1}. {mcq['q']}**")
                choice = st.radio(
                    f"Answer for Q{i+1}",
                    mcq["options"],
                    key=f"mcq_radio_{i}",
                    label_visibility="collapsed",
                )
                if choice:
                    st.session_state.mcq_answers[i] = choice[0]  # A/B/C/D
                st.divider()

            if st.button("📊 Submit & See Results", type="primary", use_container_width=True):
                st.session_state.mcq_submitted = True
                st.rerun()

        else:
            score = 0
            for i, mcq in enumerate(mcqs):
                user = st.session_state.mcq_answers.get(i, "—")
                correct = mcq["answer"]
                ok = user == correct
                score += int(ok)
                icon = "✅" if ok else "❌"
                cls = "chip-correct" if ok else "chip-wrong"
                st.markdown(f"""
                <div class="{cls}">
                    <strong>{icon} Q{i+1}. {mcq['q']}</strong><br>
                    Your answer: <strong>{user}</strong> &nbsp;|&nbsp; Correct: <strong>{correct}</strong><br>
                    <em style="opacity:0.8">💡 {mcq.get('explanation','')}</em>
                </div>
                """, unsafe_allow_html=True)

            pct = int(score / len(mcqs) * 100)
            grade = "🏆 Outstanding!" if pct >= 85 else "⭐ Great job!" if pct >= 70 else "👍 Good effort!" if pct >= 50 else "📚 Keep practising!"
            st.markdown(f"""
            <div class="mkst-score">
                <h1>{score}/{len(mcqs)} &nbsp; ({pct}%)</h1>
                <p>{grade}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🔄 New MCQ Set", use_container_width=True):
                st.session_state.mcqs = []
                st.session_state.mcq_submitted = False
                st.rerun()


# ═══════════════════════════════════════════════════
# NOTES SUMMARY
# ═══════════════════════════════════════════════════
elif feature == "📋  Notes Summary":
    st.markdown('<div class="section-title">📋 Notes Summary</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">{subject} · {semester}</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📄 Summarise My Notes", "📚 Generate Topic Summary"])

    with tab1:
        user_text = st.text_area("Paste your notes / textbook content here:", height=260,
                                 placeholder="Paste any notes, paragraphs, or content you want summarised…")
        style = st.selectbox("Summary Style", ["Concise Key Points", "Detailed Explanation", "Bullet Points Only",
                                                "Mind Map Format", "Exam-Ready Revision Sheet"])
        if st.button("📋 Summarise", type="primary", use_container_width=True):
            if not user_text.strip():
                st.warning("Please paste your notes.")
            else:
                prompt = f"""Summarise the following notes for a MAKAUT BTech {semester} student studying {subject}.
Style: {style}

NOTES:
{user_text}

Create a structured, exam-focused summary. Highlight key terms in bold."""
                result = call_ai(prompt, max_tokens=1600)
                st.markdown('<div class="mkst-result">', unsafe_allow_html=True)
                st.markdown(result)
                st.markdown('</div>', unsafe_allow_html=True)
                download_btn(result, f"MAKAUTSathi_{subject}_Summary.txt")

    with tab2:
        topic = st.text_input("Topic / Full Chapter to Summarise",
                              placeholder="e.g., Full chapter on Trees, Complete Thermodynamics cycle…")
        if st.button("📚 Generate Summary", type="primary", use_container_width=True):
            if not topic.strip():
                st.warning("Please enter a topic.")
            else:
                prompt = f"""Generate a comprehensive exam-ready summary for MAKAUT BTech {semester} students:
Subject: {subject} | Topic: {topic}

## 📌 Chapter Overview (3–4 sentences)
## 🔑 Key Formulas / Algorithms / Rules (table format where possible)
## 📊 10 Quick Revision Bullet Points
## ❓ 5 Likely Exam Questions (with expected marks)
## ⚠️ Common Errors Students Make
## 💡 Last-Minute Exam Tip"""
                result = call_ai(prompt, max_tokens=2200)
                st.markdown('<div class="mkst-result">', unsafe_allow_html=True)
                st.markdown(result)
                st.markdown('</div>', unsafe_allow_html=True)
                download_btn(result, f"MAKAUTSathi_{subject}_{topic}_Summary.txt")


# ═══════════════════════════════════════════════════
# QUIZ MODE
# ═══════════════════════════════════════════════════
elif feature == "🧩  Quiz Mode":
    st.markdown('<div class="section-title">🧩 Quiz Mode</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">{subject} · {semester} — beat your score!</div>', unsafe_allow_html=True)

    # Session state
    for key, default in [("quiz_active", False), ("quiz_qs", []), ("quiz_idx", 0),
                          ("quiz_score", 0), ("quiz_answered", False), ("quiz_user_ans", "")]:
        if key not in st.session_state:
            st.session_state[key] = default

    if not st.session_state.quiz_active:
        topic = st.text_input("Quiz Topic", placeholder="e.g., Sorting Algorithms, SQL, Fluid Statics…")
        col1, col2 = st.columns(2)
        with col1:
            num_q = st.slider("Number of Questions", 5, 15, 8)
        with col2:
            qtype = st.selectbox("Question Type", ["Multiple Choice (4 options)", "True / False", "Mixed"])

        if st.button("🚀 Start Quiz", type="primary", use_container_width=True):
            if not topic.strip():
                st.warning("Please enter a topic.")
            else:
                prompt = f"""Generate exactly {num_q} {qtype} quiz questions for MAKAUT BTech {semester} students.
Subject: {subject}, Topic: {topic}.

Return ONLY a JSON array:
[{{"q":"Question?","options":["A) opt1","B) opt2","C) opt3","D) opt4"],"answer":"A","explanation":"Reason A is correct"}}]

For True/False use options ["A) True","B) False"] with answer "A" or "B"."""
                data = call_ai_json(prompt, max_tokens=2800)
                if data:
                    st.session_state.quiz_qs = data
                    st.session_state.quiz_active = True
                    st.session_state.quiz_idx = 0
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_answered = False
                    st.session_state.quiz_user_ans = ""
                    st.rerun()
                else:
                    st.error("Failed to generate quiz. Please try again.")

    else:
        qs = st.session_state.quiz_qs
        idx = st.session_state.quiz_idx

        if idx < len(qs):
            q = qs[idx]
            progress_val = idx / len(qs)
            st.markdown(f"""
            <div class="quiz-meta">
                <span>Question {idx+1} of {len(qs)}</span>
                <span>Score: {st.session_state.quiz_score} / {idx}</span>
            </div>
            """, unsafe_allow_html=True)
            st.progress(progress_val)

            st.markdown(f"""
            <div class="fc-card">
                <div class="fc-label">Question {idx+1}</div>
                <div class="fc-front-text">{q['q']}</div>
            </div>
            """, unsafe_allow_html=True)

            if not st.session_state.quiz_answered:
                for opt in q["options"]:
                    if st.button(opt, key=f"qopt_{idx}_{opt}", use_container_width=True):
                        st.session_state.quiz_user_ans = opt[0]
                        st.session_state.quiz_answered = True
                        if opt[0] == q["answer"]:
                            st.session_state.quiz_score += 1
                        st.rerun()
            else:
                user_a = st.session_state.quiz_user_ans
                correct_a = q["answer"]
                if user_a == correct_a:
                    st.markdown('<div class="chip-correct">✅ Correct! Well done.</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chip-wrong">❌ Wrong! Correct answer was: <strong>{correct_a}</strong></div>', unsafe_allow_html=True)
                st.info(f"💡 **Explanation:** {q.get('explanation', 'N/A')}")

                if st.button("Next ▶️", type="primary", use_container_width=True):
                    st.session_state.quiz_idx += 1
                    st.session_state.quiz_answered = False
                    st.session_state.quiz_user_ans = ""
                    st.rerun()

        else:
            total = len(qs)
            score = st.session_state.quiz_score
            pct = int(score / total * 100)
            grade = "🏆 Outstanding!" if pct >= 90 else "⭐ Great job!" if pct >= 70 else "👍 Good effort!" if pct >= 50 else "📚 Keep studying!"
            st.markdown(f"""
            <div class="mkst-score">
                <h1>🏁 Quiz Complete!</h1>
                <h1>{score} / {total} &nbsp; ({pct}%)</h1>
                <p>{grade}</p>
            </div>
            """, unsafe_allow_html=True)
            if score == total:
                st.balloons()

            if st.button("🔄 New Quiz", type="primary", use_container_width=True):
                st.session_state.quiz_active = False
                st.rerun()


# ═══════════════════════════════════════════════════
# FLASHCARDS
# ═══════════════════════════════════════════════════
elif feature == "🃏  Flashcards":
    st.markdown('<div class="section-title">🃏 Flashcards</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">{subject} · {semester} — flip & revise</div>', unsafe_allow_html=True)

    for key, default in [("fc_cards", []), ("fc_idx", 0), ("fc_show", False)]:
        if key not in st.session_state:
            st.session_state[key] = default

    topic = st.text_input("Topic for Flashcards", placeholder="e.g., Binary Trees, SQL Commands, Newton's Laws…")
    col1, col2 = st.columns(2)
    with col1:
        num_cards = st.slider("Number of Flashcards", 5, 20, 10)
    with col2:
        card_type = st.selectbox("Card Type",
                                 ["Definition Cards", "Formula Cards", "Concept → Application",
                                  "Algorithm Steps", "Q&A Style", "Mixed"])

    if st.button("🃏 Generate Flashcards", type="primary", use_container_width=True):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            prompt = f"""Generate {num_cards} {card_type} flashcards for MAKAUT BTech {semester} — {subject}: {topic}.

Return ONLY a JSON array:
[{{"front":"Term or question on the front","back":"Definition, answer, or explanation on the back"}}]

Keep fronts concise (1 line). Backs should be informative but not overly long (2–4 lines max)."""
            data = call_ai_json(prompt, max_tokens=2200)
            if data:
                st.session_state.fc_cards = data
                st.session_state.fc_idx = 0
                st.session_state.fc_show = False
                st.rerun()
            else:
                st.error("Failed to generate flashcards. Please try again.")

    if st.session_state.fc_cards:
        cards = st.session_state.fc_cards
        idx = st.session_state.fc_idx
        total = len(cards)

        st.markdown(f"**Card {idx+1} of {total}**")
        st.progress((idx + 1) / total)

        card = cards[idx]

        if not st.session_state.fc_show:
            st.markdown(f"""
            <div class="fc-card">
                <div class="fc-label">📌 Front</div>
                <div class="fc-front-text">{card['front']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("👁️  Reveal Answer", type="primary", use_container_width=True):
                st.session_state.fc_show = True
                st.rerun()
        else:
            st.markdown(f"""
            <div class="fc-card answer">
                <div class="fc-label" style="color:#388e3c">✅ Back (Answer)</div>
                <div class="fc-back-text">{card['back']}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**How well did you know this?**")
            c1, c2, c3 = st.columns(3)

            def next_card():
                st.session_state.fc_show = False
                if st.session_state.fc_idx + 1 < total:
                    st.session_state.fc_idx += 1
                else:
                    st.balloons()

            with c1:
                if st.button("😕 Difficult", use_container_width=True):
                    next_card(); st.rerun()
            with c2:
                if st.button("🤔 Moderate", use_container_width=True):
                    next_card(); st.rerun()
            with c3:
                if st.button("😊 Easy", use_container_width=True):
                    next_card(); st.rerun()

        # Prev / Next nav
        nav1, nav2 = st.columns(2)
        with nav1:
            if st.button("⬅️ Previous") and idx > 0:
                st.session_state.fc_idx -= 1
                st.session_state.fc_show = False
                st.rerun()
        with nav2:
            if st.button("Next ➡️") and idx < total - 1:
                st.session_state.fc_idx += 1
                st.session_state.fc_show = False
                st.rerun()

        if idx == total - 1:
            st.success("🎉 You've completed all flashcards!")
            if st.button("🔄 Restart from Card 1"):
                st.session_state.fc_idx = 0
                st.session_state.fc_show = False
                st.rerun()


# ═══════════════════════════════════════════════════
# FORMULA SHEET
# ═══════════════════════════════════════════════════
elif feature == "📐  Formula Sheet":
    st.markdown('<div class="section-title">📐 Formula Sheet</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">{subject} · {semester}</div>', unsafe_allow_html=True)

    topic = st.text_input("Topic / Chapter", placeholder="e.g., Calculus, Thermodynamics, Circuit Analysis…")
    col1, col2 = st.columns(2)
    with col1:
        inc_deriv = st.checkbox("Include Brief Derivations", value=False)
    with col2:
        inc_units = st.checkbox("Include Units & Dimensions", value=True)

    if st.button("📐 Generate Formula Sheet", type="primary", use_container_width=True):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            prompt = f"""Create a comprehensive formula sheet for MAKAUT BTech {semester} students.
Subject: {subject} | Topic: {topic}

## 📐 Core Formulas
| Formula | Symbol Meanings | Use Case |

## 🔢 Derived / Secondary Formulas

{"## 📏 Units & Dimensions" if inc_units else ""}
(Table: Quantity | Symbol | SI Unit | Dimension)

{"## 📊 Key Derivations (2–3 steps each)" if inc_deriv else ""}

## ⚠️ Common Formula Mistakes (Top 5)

## 🎯 MAKAUT Exam Formula Priority
(Which formulas are most asked — mark as ⭐⭐⭐ / ⭐⭐ / ⭐)"""

            result = call_ai(prompt, max_tokens=2600)
            st.markdown('<div class="mkst-result">', unsafe_allow_html=True)
            st.markdown(result)
            st.markdown('</div>', unsafe_allow_html=True)
            download_btn(result, f"MAKAUTSathi_{subject}_Formula_Sheet.txt")


# ═══════════════════════════════════════════════════
# STUDY PLANNER
# ═══════════════════════════════════════════════════
elif feature == "📅  Study Planner":
    st.markdown('<div class="section-title">📅 Personalised Study Planner</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Get a day-by-day MAKAUT exam study plan tailored to you</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        exam_days = st.number_input("Days until exam", min_value=3, max_value=180, value=30)
        hours_pd = st.number_input("Study hours per day", min_value=1, max_value=14, value=6)
        weak_subs = st.multiselect("Weak Subjects (need more time)",
                                   [s for v in SUBJECTS.values() for s in v])
    with col2:
        strong_subs = st.multiselect("Strong Subjects (less time needed)",
                                     [s for v in SUBJECTS.values() for s in v])
        style = st.selectbox("Study Style", ["Exam Focused (Intensive)", "Balanced", "Topic Deep Dive", "Revision Heavy"])
        pomodoro = st.checkbox("Include Pomodoro break schedule", value=True)

    if st.button("📅 Generate My Study Plan", type="primary", use_container_width=True):
        branch_name = branch.split(" ", 1)[1] if " " in branch else branch
        prompt = f"""Create a personalised MAKAUT BTech exam study plan:

- Branch: {branch_name}
- Semester: {semester}
- Days until exam: {exam_days}
- Hours per day: {hours_pd}
- Weak subjects (more time): {weak_subs if weak_subs else "Not specified"}
- Strong subjects (less time): {strong_subs if strong_subs else "Not specified"}
- Study style: {style}
- Pomodoro breaks: {pomodoro}

Include:
## 🗓️ Phase-wise Study Plan
(Divide {exam_days} days into phases: Foundation → Practice → Revision → Mock Test)

## ⏰ Daily Schedule Template ({hours_pd} hours)
{"(25 min study / 5 min break Pomodoro blocks)" if pomodoro else ""}

## 📊 Subject-wise Time Allocation Table
(Subject | Days Allocated | Priority | Target Chapters)

## 🔁 Weekly Checkpoints (what to complete each week)

## 🔥 Final 7-Day Exam Sprint Strategy

## 📋 MAKAUT Exam Day Checklist"""

        result = call_ai(prompt, max_tokens=2800)
        st.markdown('<div class="mkst-result">', unsafe_allow_html=True)
        st.markdown(result)
        st.markdown('</div>', unsafe_allow_html=True)
        download_btn(result, "MAKAUTSathi_Study_Plan.txt")