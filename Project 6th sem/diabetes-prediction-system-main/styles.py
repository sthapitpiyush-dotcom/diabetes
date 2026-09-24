import streamlit as st

MAIN_CSS = """
    <style>
    * { margin: 0; padding: 0; }
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        padding: 2rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        margin: 2rem 0;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .about-section {
        background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .doctor-card {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #4caf50;
        color: #000000;
    }
    .doctor-card h3, .doctor-card p { color: #000000; }
    .feature-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
        color: #000000;
        transition: box-shadow 0.2s ease;
    }
    .feature-card h3, .feature-card p { color: #000000; }
    </style>
"""


def apply_app_styles():
    st.markdown(MAIN_CSS, unsafe_allow_html=True)
