import streamlit as st
from services.data_io import load_csv, to_pandas
from services.profiling import build_profile_html
from services.background import set_full_background
import streamlit.components.v1 as components

st.title("📋 Data Profiler ")
st.set_page_config(layout="wide")

uploaded_file = st.file_uploader(
    "Upload CSV for Profiling",
    type=["csv"],
    help="Ensure your file is under 1GB"
)

if uploaded_file:
    lf, _ = load_csv(uploaded_file)
    pdf = to_pandas(lf)
    with st.spinner("Generating profile..."):
        profile_html = build_profile_html(pdf)
    components.html(profile_html.replace("200MB", "1GB"), height=800, scrolling=True)

set_full_background()
