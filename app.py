import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Set up the Web Page
st.set_page_config(page_title="Engineering Math Solver", page_icon="⚙️")
st.title("⚙️ Engineering Math Solver")
st.write("Upload a picture of your problem or type it out to get an instant step-by-step solution.")

# 2. Configure the AI using Streamlit Secrets
try:
    genai.configure(api_key=st.secrets["api_key"])
except Exception:
    st.error("API Key missing. Please set 'api_key' in your Streamlit Secrets.")

# 3. User Input Area (Image + Text)
uploaded_file = st.file_uploader("Upload or paste an image of the problem here:", type=["png", "jpg", "jpeg"])
user_problem = st.text_area("Or type additional instructions/context here (optional):", height=100)

# 4. The Solving Logic
if st.button("Solve Problem"):
    if not uploaded_file and not user_problem:
        st.warning("Please upload an image or type a problem.")
    else:
        # Display the uploaded image immediately if it exists
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Your Problem", use_column_width=True)
        
        # Create an empty placeholder to stream the text into
        output_placeholder = st.empty()
        
        with st.spinner("Analyzing and solving..."):
            try:
                model = genai.GenerativeModel('gemini-3.5-flash')
                
                # Build the prompt package
                contents = [
                    """You are an expert mechanical engineering and advanced mathematics tutor. 
                    Solve the provided problem step-by-step. 
                    1. Define all variables. 
                    2. Show the exact equations used. 
                    3. Provide the final numerical answer. 
                    Format all mathematics using strict LaTeX so it renders perfectly."""
                ]
                
                if user_problem:
                    contents.append(f"User text: {user_problem}")
                if uploaded_file is not None:
                    contents.append(image)
                
                # Call the AI with stream=True
                response = model.generate_content(contents, stream=True)
                
                # Stream the chunks to the screen in real-time
                full_text = ""
                for chunk in response:
                    full_text += chunk.text
                    output_placeholder.markdown(full_text)
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
