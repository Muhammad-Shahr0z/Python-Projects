import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from streamlit_lottie import st_lottie
import json
import requests
import time

# Set page config FIRST
st.set_page_config(
    page_title="English Grammar Tutor",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load Lottie animations
def load_lottie_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

lottie_animation_header = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_jcikwtux.json")
lottie_animation_footer = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_vybwn7df.json")




# Custom CSS for premium look, animations and styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    :root {
        --primary: #2A3950;
        --secondary: #3E54AC;
        --accent: #FF7F50;
        --background: #F5F7FA;
        --card-bg: #FFFFFF;
    }

    * {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background-color: var(--background);
    }

    /* Header Styling */
    .title-text {
        color: var(--primary);
        font-weight: 700;
        font-size: 3rem;
        text-align: center;
        margin-bottom: 10px;
        animation: fadeInDown 1s ease-out;
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Text Area Styling */
    .stTextArea textarea {
        border: 2px solid var(--primary) !important;
        border-radius: 10px !important;
        transition: all 0.3s ease;
        padding: 10px;
        font-size: 1rem;
    }

    .stTextArea textarea:focus {
        border-color: var(--secondary) !important;
        box-shadow: 0 0 8px rgba(62, 84, 172, 0.3) !important;
    }

    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, var(--secondary), var(--accent)) !important;
        color: #fff !important;
        border-radius: 25px !important;
        padding: 12px 24px !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: none;
        width: 100%;
        font-weight: 600;
        font-size: 1rem;
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(62, 84, 172, 0.4);
    }

    /* Success and Error Boxes */
    .success-box, .error-box {
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        animation: slideIn 0.5s ease;
    }

    .success-box {
        background: #e8f5e9;
        border-left: 5px solid #4CAF50;
    }

    .error-box {
        background: #ffebee;
        border-left: 5px solid #f44336;
    }

    @keyframes slideIn {
        from { transform: translateX(20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    /* Loader Animation */
    .loader {
        animation: spin 1s linear infinite;
        border: 4px solid #f3f3f3;
        border-top: 4px solid var(--secondary);
        border-radius: 50%;
        width: 30px;
        height: 30px;
        margin: 20px auto;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Expander and Card styling */
    .expander .streamlit-expanderHeader {
        font-weight: 600;
        color: var(--primary);
    }
    .css-1d391kg {  /* card background for result container */
        background: var(--card-bg);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* Footer Styling */
    .custom-footer {
        text-align: center;
        padding: 10px 0;
        background: var(--card-bg);
        font-size: 1rem;
        font-weight: 600;
        color: var(--primary);
        box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
    }

    /* Responsive Fix for footer position */
    @media screen and (min-height: 800px) {
        .footer-container {
            position: fixed;
            bottom: 0;
            width: 100%;
        }
    }
</style>
""", unsafe_allow_html=True)

# API key setup
key = os.getenv("GOOGLE_API_KEY")

# Initialize the AI model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=key)

# Page Header and Lottie Animation
st.markdown('<p class="title-text">📚 AI-Powered English Grammar Tutor</p>', unsafe_allow_html=True)
if lottie_animation_header:
    st_lottie(lottie_animation_header, height=250, key="lottie-header")

st.markdown("""
<div style="text-align: center; margin-bottom: 30px; color: var(--primary); font-size: 1.2rem;">
    Perfect your English writing with instant AI feedback and detailed explanations.
</div>
""", unsafe_allow_html=True)

# Example sentences for inspiration
with st.expander("💡 Need inspiration? Try these examples:"):
    col1, col2, col3 = st.columns(3)
    examples = [
        "She don't like apples.",
        "Their going to the park later.",
        "He has many book in his bag."
    ]
    for col, example in zip([col1, col2, col3], examples):
        with col:
            if st.button(example, use_container_width=True):
                st.session_state.user_input = example

# User input area
user_input = st.text_area(
    label="✍️ Enter your text here:",
    placeholder="Type or paste your English text here...",
    height=150,
    key="user_input"
)

# Process input when button is clicked
if st.button("✨ Analyze My Writing"):
    if not user_input.strip():
        st.markdown("""
        <div class="error-box">
            🚨 Please enter some text to analyze.
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("Analyzing your text for improvements..."):
            # Delay to simulate processing (or avoid rate limits)
            time.sleep(1)
            # Define enhanced AI prompt
            messages = [
                ("system", """You are an expert English tutor. Analyze the user's text and:
1. Identify grammatical errors.
2. Provide a corrected version.
3. Explain the corrections in simple terms.
4. If no errors are found, explain why the text is correct.

Format your response as follows:
Correction: [corrected text]
Explanation: [detailed explanation]"""),
                ("user", user_input)
            ]
            try:
                response = llm.invoke(messages)
                content = response.content

                # Parse the response into correction and explanation if possible
                if "Correction:" in content and "Explanation:" in content:
                    correction = content.split("Correction:")[1].split("Explanation:")[0].strip()
                    explanation = content.split("Explanation:")[1].strip()
                else:
                    correction = content
                    explanation = "No specific errors found. Great job!"

                st.markdown(f"""
                <div class="success-box">
                    <div style="font-size: 1.3rem; color: var(--primary); margin-bottom: 15px;">
                        🎉 Improved Version
                    </div>
                    <div style="background: #fff; padding: 15px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                        {correction}
                    </div>
                    <div style="font-size: 1.2rem; color: var(--secondary); margin-bottom: 10px;">
                        📚 Explanation
                    </div>
                    <div style="color: #555; line-height: 1.5;">
                        {explanation}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                    ⚠️ Error processing your request: {str(e)}
                </div>
                """, unsafe_allow_html=True)
                st.info("Please try again later or contact support if the issue persists.")

# Footer Section with Lottie Animation
if lottie_animation_footer:
    st_lottie(lottie_animation_footer, height=150, key="lottie-footer")

# Centered footer container
footer_html = """
<div class="footer-container">
    <div class="custom-footer">
        Designed & Developed by <b>Muhammad Shahroz</b>
    </div>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
