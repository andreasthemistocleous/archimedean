import streamlit as st
import google.generativeai as genai
from PIL import Image
import random 

# 1. Page Configuration (MUST BE FIRST)
st.set_page_config(
    page_title="The Archimedean", 
    page_icon="🏛️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Initialize session states
if "history" not in st.session_state:
    st.session_state.history = []
if "problems_solved" not in st.session_state:
    st.session_state.problems_solved = 0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- DYNAMIC QUOTE REPOSITORY ---
quotes = [
    '"Give me a place to stand, and a lever long enough, and I will move the world." - Archimedes',
    '"Mathematics is the queen of the sciences." - Carl Friedrich Gauss',
    '"The book of nature is written in the language of mathematics." - Galileo Galilei',
    '"Pure mathematics is, in its way, the poetry of logical ideas." - Albert Einstein',
    '"There is no royal road to geometry." - Euclid',
    '"What we know is a drop, what we don\'t know is an ocean." - Isaac Newton',
    '"Nature is an infinite sphere of which the center is everywhere and the circumference nowhere." - Blaise Pascal'
]
current_quote = random.choice(quotes)

# 2. Left Sidebar - The Archimedean Identity
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-family: serif; letter-spacing: 2px;'>ARCHIMEDEAN</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray; font-style: italic; font-size: 0.95rem;'>Absolute Mathematical Truth</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("⚙️ System Status")
    try:
        genai.configure(api_key=st.secrets["api_key"])
        st.success("🟢 Neural Core: ONLINE")
        st.caption("Engine: gemini-3.5-flash")
    except Exception:
        st.error("🔴 Neural Core: OFFLINE")
        st.caption("Missing API Key in Secrets")
    
    st.markdown("---")
    st.subheader("📊 Session Telemetry")
    st.metric(label="Solutions Executed", value=st.session_state.problems_solved)
    st.metric(label="System Integrity", value="100%")
    
    st.markdown("---")
    st.caption(f"*{current_quote}*")

# 3. Main Workspace Header
st.title("🏛️ The Archimedean Interface")
st.markdown("---")

# 4. Interface Tabs 
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Visual Solver", "💬 Formula Assistant", "📚 Reference Library", "🕒 Solution Archive"])

# --- TAB 1: THE CORE SOLVER ---
with tab1:
    col_input, col_output = st.columns([1, 1.2]) 
    
    with col_input:
        st.subheader("Define Parameters")
        uploaded_file = st.file_uploader("Upload System Diagram or Equation", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Visual Data Registered", use_column_width=True)

        user_problem = st.text_area("Set System Constraints & Variables:", height=120, placeholder="e.g., Define boundaries for integration, or detail physical forces...")
        solve_button = st.button("⚡ Execute Solution", use_container_width=True, type="primary")

    with col_output:
        st.subheader("Terminal Output")
        output_container = st.container(border=True, height=600) 
        
        if solve_button:
            if not uploaded_file and not user_problem:
                output_container.warning("⚠️ Parameters required to execute solution.")
            else:
                output_placeholder = output_container.empty()
                with st.spinner("Synthesizing mathematical truth..."):
                    try:
                        model = genai.GenerativeModel('gemini-3.5-flash')
                        # Simplified string format to prevent syntax errors
                        sys_instruction = "You are the Archimedean computational engine. Solve the STEM problem: 1. Define states. 2. State equations. 3. Show derivations in LaTeX. 4. State the final truth."
                        
                        contents = [sys_instruction]
                        if user_problem: contents.append(f"Constraints: {user_problem}")
                        if uploaded_file is not None: contents.append(image)
                        
                        response = model.generate_content(contents, stream=True)
                        full_text = ""
                        for chunk in response:
                            full_text += chunk.text
                            output_placeholder.markdown(full_text)
                        
                        st.session_state.problems_solved += 1
                        st.session_state.history.append({
                            "title": user_problem[:40] + "..." if user_problem else "Visual Diagram Solution",
                            "solution": full_text
                        })
                    except Exception as e:
                        output_container.error(f"Critical Fault: {e}")
        else:
            output_container.info("Awaiting parameters...")

# --- TAB 2: FORMULA ASSISTANT ---
with tab2:
    st.subheader("Query the Oracle")
    st.markdown("Ask for specific formulas, conceptual explanations, or general mathematical theory.")
    chat_container = st.container(border=True, height=500)
    
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
    if prompt := st.chat_input("e.g., What is the steady-flow energy equation?"):
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with chat_container:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                try:
                    model = genai.GenerativeModel('gemini-3.5-flash')
                    chat_prompt = f"You are an engineering assistant. Answer clearly, use LaTeX for formulas, and provide practical context. User Query: {prompt}"
                    
                    response = model.generate_content(chat_prompt, stream=True)
                    for chunk in response:
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                except Exception as e:
                    message_placeholder.error(f"Connection Error: {e}")
                    full_response = "Error retrieving data."
                    
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

# --- TAB 3: REFERENCE LIBRARY ---
with tab3:
    st.subheader("Standard Formulations Archive")
    search_query = st.text_input("🔍 Search by keyword (e.g., 'Velocity', 'Ohm', 'Integration')").lower()
    st.markdown("---")

    formulas = {
        "📐 Pure Mathematics": [
            ("Quadratic Formula", "$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$"),
            ("Sine Rule", "$\\frac{a}{\\sin A} = \\frac{b}{\\sin B} = \\frac{c}{\\sin C}$"),
            ("Cosine Rule", "$a^2 = b^2 + c^2 - 2bc \\cos A$"),
            ("Differentiation (Power Rule)", "$\\frac{d}{dx}(ax^n) = anx^{n-1}$")
        ],
        "🚀 Kinematics": [
            ("Velocity", "$v = u + at$"),
            ("Displacement", "$s = ut + \\frac{1}{2}at^2$"),
            ("Velocity Squared", "$v^2 = u^2 + 2as$")
        ],
        "⚙️ Dynamics": [
            ("Newton's Second Law", "$\\Sigma F = ma$"),
            ("Weight", "$W = mg$"),
            ("Momentum", "$p = mv$")
        ]
    }

    for category, items in formulas.items():
        matching = [item for item in items if search_query in item[0].lower() or search_query in category.lower()]
        if matching:
            with st.expander(category, expanded=bool(search_query)):
                for name, equation in matching:
                    st.markdown(f"- **{name}:** {equation}")

# --- TAB 4: SOLUTION ARCHIVE ---
with tab4:
    st.subheader("Session History log")
    if not st.session_state.history:
        st.caption("No solutions executed yet.")
    else:
        for idx, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Solution #{len(st.session_state.history) - idx}"):
                st.markdown(item['solution'])
