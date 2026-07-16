import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# 1. Page Configuration
st.set_page_config(
    page_title="stemsolutions", 
    page_icon="🧬", 
    layout="centered"
)

# 2. Premium Custom Styling & Branding Header
st.markdown("<h1 style='text-align: center; font-size: 2.8rem;'>🧬 stemsolutions</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888; font-size: 1.1rem;'>The Ultimate Step-by-Step Engineering & Mathematical Workspace</p>", unsafe_allow_html=True)
st.markdown("---")

# Initialize session state for user history tracking (An excellent user retention feature)
if "history" not in st.session_state:
    st.session_state.history = []

# 3. Configure the AI using Streamlit Secrets
try:
    genai.configure(api_key=st.secrets["api_key"])
except Exception:
    st.error("🔒 Secure Configuration Profile Missing: Please add 'api_key' to your Streamlit Secrets.")

# 4. Two-Column Layout for Main Workspace and Sidebar Widgets
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📸 Submit Your Problem")
    uploaded_file = st.file_uploader(
        "Drag and drop a blueprint, problem sheet, or circuit diagram", 
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )

with col2:
    st.subheader("💡 Quick Actions")
    with st.popover("📐 View Formula References"):
        st.markdown("**Core Reference Relations:**")
        st.caption("Calculus: $\\int u \\, dv = uv - \\int v \\, du$")
        st.caption("Dynamics: $\\Sigma F = m \\cdot a$")
        st.caption("Thermodynamics: $\\Delta U = Q - W$")

# Expandable input for extra clarity
with st.expander("✏️ Add extra constraints or specific instructions (Optional)"):
    user_problem = st.text_area(
        "Clarify variables, state specific target units, or add text instructions:", 
        height=90,
        placeholder="e.g., Evaluate using Green's Theorem or use standard acceleration due to gravity..."
    )

st.markdown(" ") # Spacer

# 5. The Solver Engine Execution Loop
if st.button("🚀 Generate Verified Solution", use_container_width=True):
    if not uploaded_file and not user_problem:
        st.info("Please provide an image file or type out a problem context to begin.")
    else:
        st.markdown("---")
        
        # Immediate presentation of user assets
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Analyzed Asset Blueprint", use_column_width=True)
            
        st.subheader("✨ Active Solution Output")
        
        # Framed premium dynamic render box
        output_container = st.container(border=True)
        output_placeholder = output_container.empty()
        
        with st.spinner("Processing multi-modal inputs and drafting solution..."):
            try:
                model = genai.GenerativeModel('gemini-3.5-flash')
                
                contents = [
                    """You are an elite university professor specializing in advanced engineering math and physics. 
                    Solve the provided problem with absolute clarity and breakdown logic.
                    
                    Structure the markdown layout meticulously:
                    1. Use clear, clean subheadings (##) for logical steps (e.g., Parameters, Core Equations, Step-by-Step Derivation, Conclusion).
                    2. Explicitly write out variables and parameters.
                    3. Highlight final quantitative values clearly.
                    4. Format all math expressions, derivations, vectors, and matrices using strict LaTeX formatting.
                    """
                ]
                
                if user_problem:
                    contents.append(f"User parameters: {user_problem}")
                if uploaded_file is not None:
                    contents.append(image)
                
                response = model.generate_content(contents, stream=True)
                
                full_text = ""
                for chunk in response:
                    full_text += chunk.text
                    output_placeholder.markdown(full_text)
                
                # Append to history logging session state for the user
                st.session_state.history.append({
                    "title": user_problem[:30] + "..." if user_problem else "Image Analysis Request",
                    "solution": full_text
                })
                
            except Exception as e:
                st.error(f"Analysis Stopped: {e}")

# 6. User Retention & History Section
if st.session_state.history:
    st.markdown("---")
    st.subheader("🕒 Your Recent Workspace History")
    for idx, item in enumerate(reversed(st.session_state.history[-3:])):
        with st.expander(f"Review Solution {idx + 1}: {item['title']}"):
            st.markdown(item['solution'])
