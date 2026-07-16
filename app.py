import streamlit as st
import google.generativeai as genai

# 1. Set up the Web Page
st.set_page_config(page_title="Engineering Math Solver", page_icon="⚙️")
st.title("⚙️ Engineering Math Solver")
st.write("Input any complex mathematical or physics problem, and get a step-by-step solution.")

# 2. Secure API Key Input (So you don't expose your key)
api_key = st.sidebar.text_input("Enter your Google Gemini API Key:", type="password")

# 3. User Input Area
user_problem = st.text_area("Paste your problem here:", height=150)

# 4. The Solving Logic
if st.button("Solve Problem"):
    if not api_key:
        st.warning("Please enter your API key in the sidebar first.")
    elif not user_problem:
        st.warning("Please enter a problem to solve.")
    else:
        with st.spinner("Calculating step-by-step solution..."):
            try:
                # Configure the AI
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # The Secret Prompt Engineering
                system_prompt = f"""
                You are an expert mechanical engineering and advanced mathematics tutor. 
                Solve the following problem step-by-step. 
                1. Define all variables. 
                2. Show the exact equations used. 
                3. Provide the final numerical answer. 
                Format all mathematics using strict LaTeX so it renders perfectly.
                
                User problem: {user_problem}
                """
                
                # Call the AI and display the result
                response = model.generate_content(system_prompt)
                st.success("Solution Found!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
