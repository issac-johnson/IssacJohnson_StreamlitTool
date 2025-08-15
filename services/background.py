import streamlit as st

def set_full_background():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.pexels.com/photos/925743/pexels-photo-925743.jpeg");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }

        .block-container {
            background-color: transparent !important;
            padding: 2rem;
        }

        header[data-testid="stHeader"] {
            background: transparent !important;
        }

        [data-testid="stToolbar"], .main, .block-container, .css-1lcbmhc, .css-18ni7ap {
            background-color: transparent !important;
        }

        [data-testid="stSidebar"] {
            background-image: url("https://images.pexels.com/photos/925743/pexels-photo-925743.jpeg");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }

        [data-testid="stSidebar"] .block-container {
            background-color: transparent !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
