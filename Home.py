import streamlit as st
from services.background import set_full_background

st.set_page_config(page_title="The Data Platform", page_icon="🔎", layout="wide")


st.title("Welcome to Data Lens AI")
st.header("The complete toolkit for interactive data cleansing, in-depth profiling, and prediciton using machine learning.")


st.markdown(
    """
    <div style='font-size:21px; color:green; margin: 0;'>
       Created as part of the assignment 'Streamlit Data-Cleansing, Profiling & ML Tool' 
       <span style='color:red; font-weight:bold;'>Author : Issac Johnson</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
✨ **Welcome!**  
This tool lets you:

1. Upload and interactively clean large CSV files using Polars.  
2. Create detailed profiling reports with ydata_profiling.  
3. Build and use a simple machine learning model for predictions.  

Please navigate using the menu on the left:  

📁 **Upload & Clean**
📊 **Profile**  🧠 **ML Predict**
""")

set_full_background()
