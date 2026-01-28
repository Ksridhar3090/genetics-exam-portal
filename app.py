import streamlit as st
import google.generativeai as genai
import json

# ================= CONFIGURATION =================
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# ================= DEFAULT NOTES =================
DEFAULT_NOTES = """
CELL BIOLOGY – MEMBRANE STRUCTURE & FUNCTION

1. Membrane Structure & Models
• Fluid Mosaic Model (1972): Proposed by Singer & Nicolson.
• Membrane is a two-dimensional fluid with lateral movement of lipids and proteins.
• Mature RBCs are model systems (RBC ghosts) due to absence of organelles.

2. Lipid Chemistry
• Glycerophospholipids – glycerol backbone, ester bonds
• Sphingolipids – sphingosine backbone, amide bond
• Cardiolipin – inner mitochondrial membrane
• Plasmalogens – ether bond, heart & brain
• Hopanoids – bacterial membrane stabilizers

3. Membrane Fluidity
• Depends on chain length & unsaturation
• Cis double bonds ↓ Tm (increase fluidity)
• Homeoviscous adaptation in cold organisms

4. Membrane Asymmetry
• Outer leaflet: PC, SM, glycolipids
• Inner leaflet: PE, PS, PI (negative charge)
• Flippase, Floppase, Scramblase maintain asymmetry

5. Signaling
• PI pathway → DAG + IP3
• PS exposure = apoptosis (“eat me” signal)
• GM1 ganglioside = cholera toxin receptor
"""

# ================= DEFAULT PYQs =================
DEFAULT_PYQS = """
1. Fluid mosaic model is applicable to which membranes? (DEC 2007)
2. Which cell is used as a model system for plasma membrane studies? (JUNE 2010)
3. Most common phospholipid in myelin sheath? (DEC 2011)
4. Phosphatidylserine is located where in the plasma membrane? (JUNE 2012)
5. Glycophorin spans membrane how many times? (DEC 2015)
6. Single-chain phospholipids form what structure? (DEC 2018)
7. Unsaturated fatty acids affect melting point how? (JUNE 2001)
8. Change in membrane fluidity is mainly due to what? (DEC 2003)
"""

# ================= AI FUNCTION =================
def get_quiz_data(notes, pyqs):
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    prompt = f"""
You are a university-level exam paper setter (MSc / NET standard).

TASK:
1. Analyze the PYQs to understand difficulty & pattern.
2. Generate exactly 3 NEW MCQs from the NOTES matching the SAME pattern.

RULES:
- Application-based, exam-oriented
- One correct option only
- Do NOT repeat PYQs
- Output ONLY valid JSON (no markdown)

PYQs:
{pyqs}

NOTES:
{notes}

OUTPUT FORMAT:
[
  {{
    "question": "Question text",
    "options": {{
      "A": "Option A",
      "B": "Option B",
      "C": "Option C",
      "D": "Option D"
    }},
    "correct": "A",
    "explanation": "Short explanation"
  }}
]
"""

    response = model.generate_content(prompt)
    clean = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)

# ================= APP UI =================
st.title("🧬 AI Exam Pattern MCQ Generator")

# ---------- Session State ----------
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# ---------- USER INPUT ----------
st.subheader("📘 Paste / Edit Your Notes")
user_notes = st.text_area(
    "Edit notes below (recommended 800–1500 words):",
    value=DEFAULT_NOTES,
    height=280
)

st.subheader("📑 Paste / Edit PYQs (Pattern Source)")
user_pyqs = st.text_area(
    "Edit PYQs below (3–8 ideal):",
    value=DEFAULT_PYQS,
    height=220
)

# ---------- GENERATE QUIZ ----------
if st.button("🔮 Generate Exam-Pattern Quiz"):
    with st.spinner("Professor AI is setting the exam..."):
        st.session_state.quiz_data = get_quiz_data(user_notes, user_pyqs)
        st.session_state.user_answers = {}
        st.session_state.submitted = False

# ---------- DISPLAY QUIZ ----------
if st.session_state.quiz_data:
    st.write("---")

    for i, q in enumerate(st.session_state.quiz_data):
        st.subheader(f"Q{i+1}. {q['question']}")

        choice = st.radio(
            "Choose one:",
            list(q["options"].keys()),
            format_func=lambda x: f"{x}. {q['options'][x]}",
            key=f"q{i}"
        )

        if choice:
            st.session_state.user_answers[i] = choice

        if st.session_state.submitted:
            if choice == q["correct"]:
                st.success("✅ Correct")
                st.info(q["explanation"])
            else:
                st.error("❌ Wrong")
                st.info(f"Correct answer: {q['correct']}")
                st.info(q["explanation"])

        st.write("---")

    if not st.session_state.submitted:
        if st.button("📝 Submit Exam"):
            st.session_state.submitted = True
            st.rerun()


