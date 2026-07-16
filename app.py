import streamlit as st
import google.generativeai as genai
from PIL import Image
import random
import requests

# 1. Page Configuration
st.set_page_config(
    page_title="The Archimedean | Premium", 
    page_icon="🏛️", 
    layout="wide"
)

# Initialize Session State
if "authenticated" not in st.session_state: st.session_state.authenticated = False
if "history" not in st.session_state: st.session_state.history = []
if "problems_solved" not in st.session_state: st.session_state.problems_solved = 0
if "chat_history" not in st.session_state: st.session_state.chat_history = []

# --- QUOTE REPOSITORY ---
quotes = [
    '"Mathematics is the queen of the sciences." - Carl Friedrich Gauss',
    '"The book of nature is written in the language of mathematics." - Galileo Galilei',
    '"Pure mathematics is, in its way, the poetry of logical ideas." - Albert Einstein',
    '"There is no royal road to geometry." - Euclid',
    '"What we know is a drop, what we don\'t know is an ocean." - Isaac Newton',
    '"Nature is an infinite sphere of which the center is everywhere and the circumference nowhere." - Blaise Pascal',
    '"Number rules the universe." - Pythagoras'
]
q_sidebar, q_above, q_below = random.sample(quotes, 3)

# --- AUTHENTICATION GATE (The Landing Page) ---
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center; font-family: sans-serif; font-size: 3rem;'>ARCHIMEDEAN</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; font-size: 1.2rem;'>The Professional Mathematical Workspace</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.subheader("Welcome Back")
            user_key = st.text_input("Enter your License Key", type="password")
            if st.button("Unlock Engine", use_container_width=True, type="primary"):
                # Gumroad Verification Logic
                payload = {"product_permalink": st.secrets["gumroad_product_permalink"], "license_key": user_key}
                response = requests.post("https://api.gumroad.com/v2/licenses/verify", data=payload)
                if response.json().get("success"):
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid license key.")
            
            st.markdown("---")
            st.caption("New to Archimedean? [Get your License Here](https://your-gumroad-link.com)")
            st.info("💡 **Special Offer:** Use code **FREEMONTH** at checkout for 1 month free!")

    st.markdown("<br><br><p style='text-align: center; color: #888; font-size: 0.8rem;'>Need to cancel or manage your subscription? Check your original purchase email from Gumroad for the 'Manage Subscription' link.</p>", unsafe_allow_html=True)
    st.stop()

# --- MAIN APP (Only runs if authenticated) ---

# 2. Sidebar
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-family: serif; letter-spacing: 2px;'>ARCHIMEDEAN</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.success("🟢 System Online")
    st.metric("Solutions", st.session_state.problems_solved)
    st.markdown("---")
    st.caption(f"*{q_sidebar}*")

# 3. Header
st.markdown(f"<p style='text-align: center; font-style: italic; color: #777;'>{q_above}</p>", unsafe_allow_html=True)
st.title("🏛️ The Archimedean Interface")
st.markdown(f"<p style='text-align: center; font-style: italic; color: #555;'>{q_below}</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Visual Solver", "💬 Formula Assistant", "📚 Reference Library", "🕒 Solution Archive"])

with tab1:
    col_input, col_output = st.columns([1, 1.2])
    with col_input:
        uploaded_file = st.file_uploader("Upload Diagram", type=["png", "jpg"])
        user_problem = st.text_area("Constraints:", height=150)
        if st.button("⚡ Execute Solution", type="primary"):
            with col_output:
                with st.spinner("Synthesizing truth..."):
                    try:
                        model = genai.GenerativeModel('gemini-3.5-flash')
                        response = model.generate_content(["Solve:", user_problem])
                        st.markdown(response.text)
                        st.session_state.problems_solved += 1
                    except Exception as e:
                        st.warning("⚠️ System busy. Please wait 20s.")
    
with tab2:
    if prompt := st.chat_input("Ask about A-Level/IGCSE Physics..."):
        st.chat_message("user").markdown(prompt)
        try:
            model = genai.GenerativeModel('gemini-3.5-flash')
            res = model.generate_content(f"Explain for A-level: {prompt}")
            st.chat_message("assistant").markdown(res.text)
        except: st.error("Busy.")

with tab3:
    st.subheader("📚 Syllabus Formulas")
    syllabus = {
        "📐 Pure Math": [("Quadratic", "$x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$"), ("Sine Rule", "$\\frac{a}{\\sin A} = \\frac{b}{\\sin B}$")],
        "🚀 Kinematics": [("Displacement", "$s = ut + 0.5at^2$"), ("Velocity Squared", "$v^2 = u^2 + 2as$")],
        "⚙️ Dynamics": [("Newton's 2nd Law", "$\\Sigma F = ma$"), ("Momentum", "$p = mv$")]
    }
    for cat, items in syllabus.items():
        with st.expander(cat, expanded=True):
            for name, eq in items: st.markdown(f"- **{name}:** {eq}")

with tab4:
    for log in reversed(st.session_state.history): st.write(log)
