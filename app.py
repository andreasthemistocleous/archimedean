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
                        contents = [
                            """You are the Archimedean computational engine. Solve the provided STEM problem step-by-step.
                            1. Define Initial States & Variables.
                            2.
