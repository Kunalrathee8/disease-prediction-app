import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="MediBot AI",
    layout="wide",
    page_icon="🩺",
    initial_sidebar_state="expanded",
)

# Keep sidebar open by default; allow user to reopen it via button
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:         #080c12;
    --surface:    #0e1521;
    --card:       #111827;
    --border:     #1e293b;
    --accent:     #06b6d4;
    --accent2:    #10b981;
    --danger:     #f43f5e;
    --muted:      #64748b;
    --text:       #e2e8f0;
    --sub:        #94a3b8;
    --bot-bubble: #0f2744;
    --user-bubble:#0d3328;
    --glow:       rgba(6,182,212,0.18);
}

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* Remove ALL default Streamlit spacing */
#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding-top: 0 !important;
    padding-bottom: 2rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    max-width: 820px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }

.sidebar-brand {
    padding: 1.6rem 1.4rem 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 0.5rem;
}
.sidebar-brand .logo { font-size: 1.5rem; font-weight: 700; color: var(--accent); }
.sidebar-brand .logo span { color: var(--text); }
.sidebar-brand .tagline { font-size: 0.72rem; color: var(--muted); margin-top: 2px; }

/* ── Chat header — sticks right at top ── */
.chat-header {
    padding: 1rem 0 0.9rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.2rem;
    position: sticky;
    top: 0;
    background: var(--bg);
    z-index: 100;
}
.chat-header .avatar {
    width: 40px; height: 40px; border-radius: 11px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; flex-shrink: 0;
    background: linear-gradient(135deg,#0e7490,#0891b2);
    box-shadow: 0 0 0 1px var(--border), 0 0 14px var(--glow);
}
.chat-header .hname { font-weight: 600; font-size: 0.92rem; color: var(--text); }
.chat-header .hstatus {
    font-size: 0.7rem; color: var(--accent2);
    display: flex; align-items: center; gap: 4px; margin-top: 2px;
}
.chat-header .hstatus::before {
    content: ''; width: 6px; height: 6px;
    background: var(--accent2); border-radius: 50%;
    display: inline-block; box-shadow: 0 0 5px var(--accent2);
}

/* ── Messages ── */
.msg-bot {
    display: flex; align-items: flex-start; gap: 0.55rem;
    margin-bottom: 0.9rem;
    animation: fadeIn 0.3s ease;
}
.bot-icon {
    width: 28px; height: 28px; border-radius: 8px; flex-shrink: 0; margin-top: 2px;
    background: linear-gradient(135deg,#0ea5e9,#06b6d4);
    display: flex; align-items: center; justify-content: center; font-size: 0.8rem;
    box-shadow: 0 0 8px rgba(6,182,212,0.3);
}
.bubble-bot {
    background: var(--bot-bubble);
    border: 1px solid rgba(6,182,212,0.18);
    border-radius: 4px 14px 14px 14px;
    padding: 0.8rem 1rem;
    font-size: 0.88rem; color: var(--text); line-height: 1.65;
    max-width: 82%;
    box-shadow: 0 2px 10px rgba(0,0,0,0.25);
}

.msg-user {
    display: flex; justify-content: flex-end;
    margin-bottom: 0.9rem;
    animation: fadeIn 0.25s ease;
}
.bubble-user {
    background: var(--user-bubble);
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 14px 4px 14px 14px;
    padding: 0.7rem 1rem;
    font-size: 0.88rem; color: var(--text); max-width: 60%;
    font-family: 'JetBrains Mono', monospace;
    box-shadow: 0 2px 10px rgba(0,0,0,0.25);
}

/* Progress */
.step-chip {
    display: inline-block;
    background: rgba(6,182,212,0.12); border: 1px solid rgba(6,182,212,0.25);
    border-radius: 99px; padding: 2px 9px;
    font-size: 0.67rem; color: var(--accent); font-weight: 600; margin-bottom: 5px;
}
.prog-wrap {
    background: var(--border); border-radius: 99px;
    height: 3px; margin: 3px 0 2px; overflow: hidden;
}
.prog-fill {
    height: 100%; border-radius: 99px;
    background: linear-gradient(90deg,var(--accent),var(--accent2));
}
.prog-lbl { font-size: 0.66rem; color: var(--muted); text-align: right; margin-bottom: 7px; }

.hint-text {
    margin-top: 5px; padding: 4px 9px;
    background: rgba(255,255,255,0.04); border-radius: 7px;
    font-size: 0.74rem; color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    border-left: 2px solid rgba(6,182,212,0.4);
}

/* Result */
.result-card {
    border-radius: 14px; padding: 1.1rem 1.3rem;
    margin-bottom: 0.9rem;
    animation: fadeIn 0.4s ease;
    border: 1px solid rgba(16,185,129,0.3);
    background: linear-gradient(135deg,rgba(16,185,129,0.08),rgba(6,182,212,0.04));
}
.result-card.bad {
    border-color: rgba(244,63,94,0.3);
    background: linear-gradient(135deg,rgba(244,63,94,0.08),rgba(244,63,94,0.03));
}
.result-tag { font-size: 0.67rem; font-weight: 700; letter-spacing: 1.1px; text-transform: uppercase; color: var(--muted); margin-bottom: 5px; }
.result-title { font-size: 1.05rem; font-weight: 700; color: var(--accent2); margin-bottom: 4px; }
.result-card.bad .result-title { color: var(--danger); }
.result-detail { font-size: 0.82rem; color: var(--sub); line-height: 1.6; }
.result-disclaimer {
    font-size: 0.69rem; color: #334155; margin-top: 9px;
    padding-top: 9px; border-top: 1px solid var(--border);
}

/* Input row */
.input-row {
    position: sticky;
    bottom: 0;
    background: var(--bg);
    padding: 0.9rem 0 1rem;
    border-top: 1px solid var(--border);
    margin-top: 0.5rem;
}

/* Streamlit input */
[data-testid="stTextInput"] > div > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    font-size: 0.88rem !important;
    color: var(--text) !important;
    transition: border-color .2s, box-shadow .2s !important;
}
[data-testid="stTextInput"] > div > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(6,182,212,.13) !important;
}
[data-testid="stTextInput"] label { display: none !important; }
[data-testid="stTextInput"] input { color: var(--text) !important; font-family: 'Sora', sans-serif !important; }
[data-testid="stTextInput"] input::placeholder { color: var(--muted) !important; font-size: 0.82rem !important; }

/* Button */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg,#0891b2,#06b6d4) !important;
    color: #fff !important; border: none !important; border-radius: 11px !important;
    font-family: 'Sora', sans-serif !important; font-weight: 600 !important;
    font-size: 0.88rem !important; padding: 0.58rem 1.3rem !important;
    transition: transform .15s, box-shadow .2s !important;
    box-shadow: 0 4px 12px rgba(6,182,212,0.3) !important;
    white-space: nowrap;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 7px 18px rgba(6,182,212,.45) !important;
}

.nav-link { border-radius: 10px !important; }
.nav-link.active { background: linear-gradient(135deg,#0e4f6b,#0c3d54) !important; }

/* Switch disease button in header */
.switch-btn-wrap {
    margin-left: auto;
}
.switch-btn-wrap button {
    background: rgba(6,182,212,0.12) !important;
    border: 1px solid rgba(6,182,212,0.3) !important;
    border-radius: 99px !important;
    padding: 4px 14px !important;
    font-size: 0.72rem !important;
    color: #06b6d4 !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    box-shadow: none !important;
    white-space: nowrap;
}

@keyframes fadeIn {
    from { opacity:0; transform:translateY(6px); }
    to   { opacity:1; transform:translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# ── Load models ───────────────────────────────────────────────────────────────
working_dir = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_models():
    dm = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))
    hm = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))
    pm = pickle.load(open(f'{working_dir}/saved_models/parkinsons_model.sav', 'rb'))
    return dm, hm, pm

diabetes_model, heart_disease_model, parkinsons_model = load_models()

# ── Questions ─────────────────────────────────────────────────────────────────
DIABETES_QUESTIONS = [
    {"key": "Pregnancies",              "question": "How many times has the patient been pregnant?",        "hint": "Enter 0 if not applicable  •  e.g. 2"},
    {"key": "Glucose",                  "question": "What is the plasma glucose level? (mg/dL)",            "hint": "2-hour oral glucose tolerance test  •  e.g. 120"},
    {"key": "BloodPressure",            "question": "What is the diastolic blood pressure? (mm Hg)",        "hint": "Resting diastolic  •  e.g. 80"},
    {"key": "SkinThickness",            "question": "What is the triceps skin fold thickness? (mm)",         "hint": "Measured at triceps  •  e.g. 20"},
    {"key": "Insulin",                  "question": "What is the 2-hour serum insulin level? (μU/mL)",      "hint": "Post-glucose test  •  e.g. 85"},
    {"key": "BMI",                      "question": "What is the patient's Body Mass Index (BMI)?",         "hint": "Weight (kg) ÷ Height (m)²  •  e.g. 28.5"},
    {"key": "DiabetesPedigreeFunction", "question": "What is the Diabetes Pedigree Function score?",        "hint": "Genetic likelihood  •  range 0–2.5  •  e.g. 0.627"},
    {"key": "Age",                      "question": "What is the patient's age? (years)",                   "hint": "e.g. 35"},
]

HEART_QUESTIONS = [
    {"key": "age",      "question": "What is the patient's age? (years)",                           "hint": "e.g. 55"},
    {"key": "sex",      "question": "What is the patient's biological sex?",                        "hint": "1 = Male   |   0 = Female"},
    {"key": "cp",       "question": "What type of chest pain does the patient experience?",         "hint": "0 = Typical   1 = Atypical   2 = Non-anginal   3 = Asymptomatic"},
    {"key": "trestbps", "question": "What is the resting blood pressure? (mm Hg)",                 "hint": "On hospital admission  •  e.g. 130"},
    {"key": "chol",     "question": "What is the serum cholesterol level? (mg/dL)",                "hint": "e.g. 250"},
    {"key": "fbs",      "question": "Is fasting blood sugar greater than 120 mg/dL?",              "hint": "1 = Yes   |   0 = No"},
    {"key": "restecg",  "question": "What are the resting ECG results?",                           "hint": "0 = Normal   1 = ST-T abnormality   2 = LV hypertrophy"},
    {"key": "thalach",  "question": "What is the maximum heart rate achieved? (bpm)",              "hint": "Peak exercise heart rate  •  e.g. 150"},
    {"key": "exang",    "question": "Did the patient have exercise-induced angina?",               "hint": "1 = Yes   |   0 = No"},
    {"key": "oldpeak",  "question": "What is the ST depression (exercise vs rest)?",               "hint": "Oldpeak value  •  e.g. 1.5"},
    {"key": "slope",    "question": "What is the slope of the peak exercise ST segment?",          "hint": "0 = Upsloping   1 = Flat   2 = Downsloping"},
    {"key": "ca",       "question": "How many major vessels are colored by fluoroscopy?",          "hint": "0 to 3 vessels"},
    {"key": "thal",     "question": "What is the thalassemia classification?",                     "hint": "0 = Normal   1 = Fixed defect   2 = Reversible defect"},
]

PARKINSONS_QUESTIONS = [
    {"key": "fo",             "question": "Average vocal fundamental frequency — MDVP:Fo (Hz)",    "hint": "e.g. 119.992"},
    {"key": "fhi",            "question": "Maximum vocal fundamental frequency — MDVP:Fhi (Hz)",   "hint": "e.g. 157.302"},
    {"key": "flo",            "question": "Minimum vocal fundamental frequency — MDVP:Flo (Hz)",   "hint": "e.g. 74.997"},
    {"key": "Jitter_percent", "question": "MDVP Jitter (%) — cycle-to-cycle frequency variation",  "hint": "e.g. 0.00784"},
    {"key": "Jitter_Abs",     "question": "Absolute jitter — MDVP:Jitter(Abs)",                    "hint": "e.g. 0.00007"},
    {"key": "RAP",            "question": "Relative Average Perturbation — MDVP:RAP",              "hint": "e.g. 0.0037"},
    {"key": "PPQ",            "question": "5-point Period Perturbation Quotient — MDVP:PPQ",       "hint": "e.g. 0.0043"},
    {"key": "DDP",            "question": "Average absolute difference of periods — Jitter:DDP",   "hint": "e.g. 0.0111"},
    {"key": "Shimmer",        "question": "Amplitude variation — MDVP:Shimmer",                    "hint": "e.g. 0.029"},
    {"key": "Shimmer_dB",     "question": "Shimmer in decibels — MDVP:Shimmer(dB)",               "hint": "e.g. 0.282"},
    {"key": "APQ3",           "question": "3-point Amplitude Perturbation Quotient — APQ3",        "hint": "e.g. 0.0143"},
    {"key": "APQ5",           "question": "5-point Amplitude Perturbation Quotient — APQ5",        "hint": "e.g. 0.0181"},
    {"key": "APQ",            "question": "11-point Amplitude Perturbation Quotient — MDVP:APQ",   "hint": "e.g. 0.0247"},
    {"key": "DDA",            "question": "Average of APQ3 differences — Shimmer:DDA",            "hint": "e.g. 0.0430"},
    {"key": "NHR",            "question": "Noise-to-Harmonics Ratio (NHR)",                        "hint": "e.g. 0.0148"},
    {"key": "HNR",            "question": "Harmonics-to-Noise Ratio (HNR) in dB",                 "hint": "e.g. 21.033"},
    {"key": "RPDE",           "question": "Recurrence Period Density Entropy (RPDE)",              "hint": "e.g. 0.4144"},
    {"key": "DFA",            "question": "Detrended Fluctuation Analysis (DFA)",                  "hint": "e.g. 0.8156"},
    {"key": "spread1",        "question": "Nonlinear F0 variation — spread1",                      "hint": "e.g. -4.813"},
    {"key": "spread2",        "question": "Nonlinear F0 variation — spread2",                      "hint": "e.g. 0.2664"},
    {"key": "D2",             "question": "Correlation dimension (D2)",                            "hint": "e.g. 2.301"},
    {"key": "PPE",            "question": "Pitch Period Entropy (PPE)",                            "hint": "e.g. 0.2842"},
]

DISEASE_CONFIG = {
    "Diabetes":      {"questions": DIABETES_QUESTIONS,   "emoji": "🩸"},
    "Heart Disease": {"questions": HEART_QUESTIONS,      "emoji": "❤️"},
    "Parkinsons":    {"questions": PARKINSONS_QUESTIONS, "emoji": "🧠"},
}

# ── Session state ─────────────────────────────────────────────────────────────
def init_state(disease):
    if st.session_state.get("disease") != disease:
        st.session_state.disease = disease
        st.session_state.step    = 0
        st.session_state.answers = {}
        st.session_state.history = []
        st.session_state.done    = False
        total = len(DISEASE_CONFIG[disease]["questions"])
        st.session_state.history.append({"role": "welcome", "disease": disease, "total": total})
        q = DISEASE_CONFIG[disease]["questions"][0]
        st.session_state.history.append({
            "role": "bot", "question": q["question"],
            "hint": q["hint"], "step": 1, "total": total
        })

def reset_chat():
    disease = st.session_state.get("disease", "Diabetes")
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    init_state(disease)

def run_prediction(disease, answers):
    cfg    = DISEASE_CONFIG[disease]
    keys   = [q["key"] for q in cfg["questions"]]
    values = [float(answers[k]) for k in keys]
    if disease == "Diabetes":
        pred = diabetes_model.predict([values])[0]
        return (True,  "Diabetic Indicators Found",
                "The model detects patterns consistent with diabetes. Please consult an endocrinologist for a full clinical evaluation.") \
               if pred == 1 else \
               (False, "No Diabetes Detected",
                "The model finds no significant diabetes indicators. Keep up with regular health check-ups and a balanced lifestyle.")
    elif disease == "Heart Disease":
        pred = heart_disease_model.predict([values])[0]
        return (True,  "Heart Disease Risk Detected",
                "The model identifies cardiovascular risk factors. Please seek evaluation from a cardiologist as soon as possible.") \
               if pred == 1 else \
               (False, "No Heart Disease Detected",
                "The model finds no significant cardiac risk indicators. Maintain a heart-healthy lifestyle with regular exercise.")
    else:
        pred = parkinsons_model.predict([values])[0]
        return (True,  "Parkinson's Indicators Found",
                "Voice biomarkers suggest Parkinson's disease patterns. Please consult a neurologist for a clinical assessment.") \
               if pred == 1 else \
               (False, "No Parkinson's Detected",
                "Voice biomarkers show no significant Parkinson's indicators. Continue with regular neurological check-ups.")

# ── Render helpers ────────────────────────────────────────────────────────────
def render_welcome(disease, total):
    emoji = DISEASE_CONFIG[disease]["emoji"]
    st.markdown(f"""
    <div class="msg-bot">
        <div class="bot-icon">🩺</div>
        <div class="bubble-bot">
            <div style="font-size:1rem;font-weight:600;color:#e2e8f0;margin-bottom:5px">Hello! I'm MediBot 👋</div>
            <div style="font-size:0.86rem;color:#94a3b8;line-height:1.7">
                I'll walk you through a
                <span style="color:#06b6d4;font-weight:600">{emoji} {disease} Screening</span>
                by asking <span style="color:#06b6d4;font-weight:600">{total} clinical questions</span> — one at a time.<br><br>
                Type your answer below and press <span style="color:#10b981;font-weight:600">Send ➤</span> to continue.
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

def render_bot_bubble(question, hint, step, total):
    pct = int((step - 1) / total * 100)
    st.markdown(f"""
    <div class="msg-bot">
        <div class="bot-icon">🩺</div>
        <div class="bubble-bot">
            <div style="margin-bottom:5px"><span class="step-chip">Question {step} of {total}</span></div>
            <div class="prog-wrap"><div class="prog-fill" style="width:{pct}%"></div></div>
            <div class="prog-lbl">{pct}% complete</div>
            <div style="font-size:0.9rem;font-weight:500;color:#e2e8f0;margin-bottom:5px">{question}</div>
            <div class="hint-text">💡 {hint}</div>
        </div>
    </div>""", unsafe_allow_html=True)

def render_user_bubble(text):
    st.markdown(f"""
    <div class="msg-user">
        <div class="bubble-user">{text}</div>
    </div>""", unsafe_allow_html=True)

def render_thinking():
    st.markdown("""
    <div class="msg-bot">
        <div class="bot-icon">🩺</div>
        <div class="bubble-bot" style="color:#94a3b8;font-style:italic;font-size:0.86rem">
            ⏳ All data collected — running the ML model now…
        </div>
    </div>""", unsafe_allow_html=True)

def render_result(danger, label, detail):
    cls  = "result-card bad" if danger else "result-card"
    icon = "⚠️" if danger else "✅"
    st.markdown(f"""
    <div class="{cls}">
        <div class="result-tag">🧪 Screening Result</div>
        <div class="result-title">{icon}&nbsp; {label}</div>
        <div class="result-detail">{detail}</div>
        <div class="result-disclaimer">
            ⚠️ AI screening — for <b>educational purposes only</b>.
            Always consult a qualified healthcare professional for a definitive diagnosis.
        </div>
    </div>""", unsafe_allow_html=True)

def render_error(text):
    st.markdown(f"""
    <div class="msg-bot">
        <div class="bot-icon">🩺</div>
        <div class="bubble-bot" style="border-color:rgba(244,63,94,0.35)">
            <span style="color:#f43f5e;font-weight:600">⚠️ {text}</span>
        </div>
    </div>""", unsafe_allow_html=True)

# ── Disease selection (single source of truth) ────────────────────────────────
disease_options = ["Diabetes", "Heart Disease", "Parkinsons"]
if "disease" not in st.session_state:
    st.session_state.disease = "Diabetes"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="logo">Medi<span>Bot</span> 🩺</div>
        <div class="tagline">AI-powered disease screening</div>
    </div>""", unsafe_allow_html=True)

    sidebar_choice = option_menu(
        menu_title=None,
        options=disease_options,
        icons=["droplet-half", "heart-pulse", "person-lines-fill"],
        default_index=disease_options.index(st.session_state.disease),
        styles={
            "container":         {"padding": "0.5rem 0.8rem", "background": "transparent"},
            "icon":              {"font-size": "0.9rem"},
            "nav-link":          {"font-size": "0.85rem", "font-weight": "500",
                                  "color": "#94a3b8", "padding": "0.6rem 1rem"},
            "nav-link-selected": {"font-weight": "600", "color": "#e2e8f0"},
        },
    )
    if sidebar_choice != st.session_state.disease:
        init_state(sidebar_choice)
        st.rerun()

    st.markdown("---")
    if st.button("🔄  Restart Chat"):
        reset_chat()
        st.rerun()
    st.markdown("""
    <div style='padding:0.4rem;font-size:0.73rem;color:#475569;line-height:1.7'>
    <b style='color:#64748b'>⚠️ Disclaimer</b><br>
    For educational screening only. Does <b>not</b> replace professional medical diagnosis.
    </div>""", unsafe_allow_html=True)

# ── Init ──────────────────────────────────────────────────────────────────────
selected = st.session_state.disease
init_state(selected)
cfg       = DISEASE_CONFIG[selected]
questions = cfg["questions"]
total     = len(questions)

# ── CHAT HEADER ───────────────────────────────────────────────────────────────
col_header, col_switcher = st.columns([3, 1])

with col_header:
    st.markdown(f"""
    <div class="chat-header">
        <div class="avatar">{cfg['emoji']}</div>
        <div>
            <div class="hname">MediBot — {selected} Screening</div>
            <div class="hstatus">Online &nbsp;·&nbsp; {total} questions</div>
        </div>
    </div>""", unsafe_allow_html=True)

with col_switcher:
    st.markdown("<div style='padding-top:0.6rem'></div>", unsafe_allow_html=True)
    new_disease = st.selectbox(
        "🔀 Switch",
        options=disease_options,
        index=disease_options.index(selected),
        key="disease_switcher",
    )
    if new_disease != selected:
        init_state(new_disease)
        st.rerun()

# ── MESSAGES (render directly, no wrapper div with fixed height) ──────────────
for msg in st.session_state.history:
    if   msg["role"] == "welcome":  render_welcome(msg["disease"], msg["total"])
    elif msg["role"] == "bot":      render_bot_bubble(msg["question"], msg["hint"], msg["step"], msg["total"])
    elif msg["role"] == "user":     render_user_bubble(msg["text"])
    elif msg["role"] == "thinking": render_thinking()
    elif msg["role"] == "result":   render_result(msg["danger"], msg["label"], msg["detail"])
    elif msg["role"] == "error":    render_error(msg["text"])

# ── INPUT ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="input-row">', unsafe_allow_html=True)

if not st.session_state.done:
    current_q = questions[st.session_state.step]
    col_inp, col_btn = st.columns([5, 1])

    with col_inp:
        user_val = st.text_input(
            "answer",
            placeholder=f"Type your answer…   •   {current_q['hint']}",
            key=f"inp_{st.session_state.step}_{selected}",
            label_visibility="collapsed",
        )
    with col_btn:
        send = st.button("Send ➤", key=f"send_{st.session_state.step}_{selected}")

    if send:
        val = user_val.strip()
        if not val:
            st.session_state.history.append({"role": "error", "text": "Please type a value before sending."})
            st.rerun()
        try:
            float(val)
        except ValueError:
            st.session_state.history.append({"role": "error", "text": "Please enter a valid number (e.g. 28.5)."})
            st.rerun()

        st.session_state.answers[current_q["key"]] = val
        st.session_state.history.append({"role": "user", "text": val})

        next_step = st.session_state.step + 1
        if next_step < total:
            nq = questions[next_step]
            st.session_state.history.append({
                "role": "bot", "question": nq["question"],
                "hint": nq["hint"], "step": next_step + 1, "total": total,
            })
            st.session_state.step = next_step
        else:
            st.session_state.history.append({"role": "thinking"})
            danger, label, detail = run_prediction(selected, st.session_state.answers)
            st.session_state.history.append({
                "role": "result", "danger": danger, "label": label, "detail": detail
            })
            st.session_state.done = True

        st.rerun()
else:
    st.markdown("""
    <div style='text-align:center;padding:0.5rem 0 0.2rem'>
        <span style='font-size:0.82rem;color:#475569'>Screening complete.</span>
    </div>""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2,2,2])
    with col2:
        if st.button("🔄  Start New Screening"):
            reset_chat()
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
