import streamlit as st
import google.generativeai as genai
import json

# ================= CONFIGURATION =================
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# ================= EMBEDDED COURSE DATA =================
COURSE_DATA = {
    "Unit 1: Membrane Structure & Function": {
        "notes": """
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
• PS exposure = apoptosis ("eat me" signal)
• GM1 ganglioside = cholera toxin receptor
""",
        "pyqs": """
1. Fluid mosaic model is applicable to which membranes? (DEC 2007)
2. Which cell is used as a model system for plasma membrane studies? (JUNE 2010)
3. Most common phospholipid in myelin sheath? (DEC 2011)
4. Phosphatidylserine is located where in the plasma membrane? (JUNE 2012)
5. Glycophorin spans membrane how many times? (DEC 2015)
6. Single-chain phospholipids form what structure? (DEC 2018)
7. Unsaturated fatty acids affect melting point how? (JUNE 2001)
8. Change in membrane fluidity is mainly due to what? (DEC 2003)
"""
    },
    
    "Unit 2: Cell Transport Mechanisms": {
        "notes": """
CELL TRANSPORT MECHANISMS

1. Passive Transport
• Simple Diffusion: O2, CO2, steroid hormones
• Facilitated Diffusion: GLUT transporters, ion channels
• Aquaporins: Water transport (AQP1 in RBCs)

2. Active Transport
• Primary: Na+/K+ ATPase (3 Na+ out, 2 K+ in)
• Secondary: SGLT1 (Na+-glucose cotransporter)
• ABC Transporters: MDR1/P-glycoprotein (drug efflux)

3. Vesicular Transport
• Endocytosis: Clathrin-mediated, caveolin-mediated
• Exocytosis: Constitutive vs regulated
• Receptor-mediated: LDL receptor pathway

4. Membrane Potential
• Resting potential: -70 mV (neurons)
• Goldman equation: Multiple ion contributions
• Nernst equation: Single ion equilibrium
""",
        "pyqs": """
1. Na+/K+ ATPase transports how many ions? (DEC 2009)
2. GLUT4 is regulated by which hormone? (JUNE 2013)
3. Clathrin-coated pits are involved in? (DEC 2014)
4. Which protein is mutated in cystic fibrosis? (JUNE 2016)
5. Aquaporin-1 is primarily found in? (DEC 2017)
"""
    },
    
    "Unit 3: Cell Signaling & Communication": {
        "notes": """
CELL SIGNALING & COMMUNICATION

1. Signal Transduction Pathways
• GPCR Pathway: cAMP/PKA, IP3/Ca2+, DAG/PKC
• Receptor Tyrosine Kinases: MAPK cascade
• JAK-STAT: Cytokine signaling
• Notch & Wnt: Developmental signaling

2. Second Messengers
• cAMP: Activates PKA
• Ca2+: Calmodulin, PKC activation
• IP3: ER calcium release
• DAG: PKC activation
• cGMP: NO signaling, vision

3. Gap Junctions
• Connexins form connexons
• Allow passage of <1000 Da molecules
• Important in cardiac muscle, neurons

4. Adhesion Molecules
• Cadherins: Ca2+-dependent, adherens junctions
• Integrins: ECM binding, focal adhesions
• Selectins: Leukocyte rolling
• Ig superfamily: ICAM, VCAM
""",
        "pyqs": """
1. Which second messenger activates protein kinase A? (DEC 2008)
2. Gap junctions are made of which protein? (JUNE 2011)
3. E-cadherin requires which ion for function? (DEC 2012)
4. RTKs activate which signaling cascade? (JUNE 2015)
5. Nitric oxide produces which second messenger? (DEC 2019)
"""
    }
}

# ================= AI FUNCTION =================
def get_quiz_data(notes, pyqs):
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    prompt = f"""
You are a university-level exam paper setter (MSc / NET standard).

TASK:
1. Analyze the PYQs to understand difficulty & pattern.
2. Generate exactly 10 NEW MCQs from the NOTES matching the SAME pattern.

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

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    /* Main container */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Unit folder styling */
    .unit-folder {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .unit-folder:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Content sections */
    .content-box {
        background: white;
        padding: 20px;
        border-radius: 8px;
        margin: 15px 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Question card */
    .question-card {
        background: white;
        padding: 25px;
        border-radius: 10px;
        margin: 20px 0;
        box-shadow: 0 3px 8px rgba(0,0,0,0.1);
        border-top: 3px solid #667eea;
    }
    
    /* Stats badge */
    .stats-badge {
        background: #e3f2fd;
        padding: 10px 20px;
        border-radius: 20px;
        display: inline-block;
        margin: 5px;
        font-weight: 600;
        color: #1976d2;
    }
    
    /* Header styling */
    h1 {
        color: #2c3e50;
        font-weight: 700;
    }
    
    h2 {
        color: #34495e;
        font-weight: 600;
    }
    
    h3 {
        color: #667eea;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ================= SESSION STATE =================
if "selected_unit" not in st.session_state:
    st.session_state.selected_unit = None
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "show_content" not in st.session_state:
    st.session_state.show_content = False

# ================= HEADER =================
st.title("🧬 AI Exam Pattern MCQ Generator")
st.markdown("### 📚 Select a unit to begin your preparation")

# ================= UNIT SELECTION =================
col1, col2, col3 = st.columns(3)

units = list(COURSE_DATA.keys())

with col1:
    if st.button(f"📁 {units[0]}", use_container_width=True):
        st.session_state.selected_unit = units[0]
        st.session_state.quiz_data = None
        st.session_state.submitted = False
        st.session_state.user_answers = {}
        st.session_state.show_content = False

with col2:
    if st.button(f"📁 {units[1]}", use_container_width=True):
        st.session_state.selected_unit = units[1]
        st.session_state.quiz_data = None
        st.session_state.submitted = False
        st.session_state.user_answers = {}
        st.session_state.show_content = False

with col3:
    if st.button(f"📁 {units[2]}", use_container_width=True):
        st.session_state.selected_unit = units[2]
        st.session_state.quiz_data = None
        st.session_state.submitted = False
        st.session_state.user_answers = {}
        st.session_state.show_content = False

# ================= UNIT CONTENT DISPLAY =================
if st.session_state.selected_unit:
    st.markdown("---")
    
    # Unit header
    st.markdown(f"## 📖 {st.session_state.selected_unit}")
    
    unit_data = COURSE_DATA[st.session_state.selected_unit]
    
    # Expandable sections for Notes and PYQs
    col_a, col_b = st.columns(2)
    
    with col_a:
        with st.expander("📝 **View Study Notes**", expanded=st.session_state.show_content):
            st.markdown(f'<div class="content-box">', unsafe_allow_html=True)
            st.markdown(unit_data["notes"])
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col_b:
        with st.expander("📋 **View Previous Year Questions**", expanded=st.session_state.show_content):
            st.markdown(f'<div class="content-box">', unsafe_allow_html=True)
            st.markdown(unit_data["pyqs"])
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate Quiz Button
    st.markdown("###")
    col_generate = st.columns([1, 2, 1])[1]
    
    with col_generate:
        if st.button("🎯 **Generate MCQs**", use_container_width=True, type="primary"):
            with st.spinner("🤖 AI is preparing your exam questions..."):
                st.session_state.quiz_data = get_quiz_data(
                    unit_data["notes"], 
                    unit_data["pyqs"]
                )
                st.session_state.user_answers = {}
                st.session_state.submitted = False
                st.success("✅ Quiz generated successfully!")

# ================= QUIZ DISPLAY =================
if st.session_state.quiz_data:
    st.markdown("---")
    st.markdown("## 📝 Your Exam Questions")
    
    # Quiz instructions
    st.info("💡 **Instructions:** Answer all questions and click 'Submit Answers' to see your results.")
    
    for i, q in enumerate(st.session_state.quiz_data):
        st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
        
        # Question number and text
        st.markdown(f"### Question {i+1}")
        st.markdown(f"**{q['question']}**")
        st.markdown("###")
        
        # Options
        choice = st.radio(
            "Select your answer:",
            list(q["options"].keys()),
            format_func=lambda x: f"{x}. {q['options'][x]}",
            key=f"q{i}",
            label_visibility="collapsed"
        )

        if choice:
            st.session_state.user_answers[i] = choice

        # Show results after submission
        if st.session_state.submitted:
            st.markdown("###")
            if choice == q["correct"]:
                st.success("✅ **Correct Answer!**")
                st.markdown(f"**Explanation:** {q['explanation']}")
            else:
                st.error("❌ **Incorrect**")
                st.markdown(f"**Correct Answer:** {q['correct']}. {q['options'][q['correct']]}")
                st.markdown(f"**Explanation:** {q['explanation']}")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Submit button
    if not st.session_state.submitted:
        st.markdown("###")
        col_submit = st.columns([1, 2, 1])[1]
        
        with col_submit:
            if st.button("📤 **Submit Answers**", use_container_width=True, type="primary"):
                if len(st.session_state.user_answers) < len(st.session_state.quiz_data):
                    st.warning("⚠️ Please answer all questions before submitting!")
                else:
                    st.session_state.submitted = True
                    st.rerun()
    
    # Show score after submission
    if st.session_state.submitted:
        st.markdown("---")
        correct_count = sum(
            1 for i, q in enumerate(st.session_state.quiz_data)
            if st.session_state.user_answers.get(i) == q["correct"]
        )
        total = len(st.session_state.quiz_data)
        percentage = (correct_count / total) * 100
        
        # Score display
        st.markdown("## 🎯 Your Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'<div class="stats-badge">Score: {correct_count}/{total}</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div class="stats-badge">Percentage: {percentage:.1f}%</div>', unsafe_allow_html=True)
        
        with col3:
            if percentage >= 80:
                st.markdown(f'<div class="stats-badge" style="background: #c8e6c9; color: #2e7d32;">Grade: Excellent! 🌟</div>', unsafe_allow_html=True)
            elif percentage >= 60:
                st.markdown(f'<div class="stats-badge" style="background: #fff9c4; color: #f57f17;">Grade: Good 👍</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="stats-badge" style="background: #ffccbc; color: #d84315;">Grade: Needs Improvement 📚</div>', unsafe_allow_html=True)
        
        # Retry button
        st.markdown("###")
        col_retry = st.columns([1, 2, 1])[1]
        
        with col_retry:
            if st.button("🔄 **Try Another Quiz**", use_container_width=True):
                st.session_state.quiz_data = None
                st.session_state.user_answers = {}
                st.session_state.submitted = False
                st.rerun()

# ================= FOOTER =================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 20px;'>
    <p>🎓 Powered by Google Gemini AI | Made with ❤️ for serious exam preparation</p>
</div>
""", unsafe_allow_html=True)







