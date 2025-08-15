import streamlit as st
import pandas as pd
import os
from services.predict_ml import train_and_eval, save_model, load_model
from services.background import set_full_background

st.set_page_config(layout="wide")
st.title("🧠 ML Prediction")

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")

pipe = None

uploaded_file = st.file_uploader("Upload CSV for ML", type=["csv"])
if uploaded_file:
    pdf = pd.read_csv(uploaded_file)

    for col in pdf.columns:
        if pd.api.types.is_numeric_dtype(pdf[col]):
            pdf[col] = pdf[col].fillna(pdf[col].median())
        else:
            pdf[col] = pdf[col].fillna(pdf[col].mode()[0])

    st.write("### Preview", pdf.head())

    target = st.selectbox("Select Target Column", pdf.columns)

    if st.button("Train Model"):
        with st.spinner("Training..."):
            pipe, metrics, task = train_and_eval(pdf, target)
            os.makedirs(MODEL_DIR, exist_ok=True)
            save_model(pipe, MODEL_PATH)
        st.success(f"Trained a {task} model!")
        st.json(metrics)

    if st.button("Load Last Model"):
        if os.path.exists(MODEL_PATH):
            pipe = load_model(MODEL_PATH)
            st.success("Loaded model from file!")
        else:
            st.error("No saved model found. Please train a model first.")

    if pipe is None and os.path.exists(MODEL_PATH):
        pipe = load_model(MODEL_PATH)

    if st.checkbox("Make Predictions"):
        if pipe is None:
            st.warning("Please train or load a model first.")
        else:
            st.write("### Enter values for prediction")
            input_data = {}

            for col in pdf.drop(columns=[target]).columns:
                col_data = pdf[col].dropna()

                if pd.api.types.is_numeric_dtype(col_data):
                    min_val, max_val = float(col_data.min()), float(col_data.max())
                    default_val = float(col_data.median())
                    input_data[col] = st.number_input(
                        col, min_value=min_val, max_value=max_val, value=default_val
                    )

                elif pd.api.types.is_datetime64_any_dtype(col_data):
                    default_date = col_data.iloc[0] if not col_data.empty else pd.Timestamp.today()
                    input_data[col] = st.date_input(col, value=default_date)

                else:
                    unique_vals = sorted(col_data.dropna().unique())
                    if 0 < len(unique_vals) <= 50:
                        input_data[col] = st.selectbox(col, unique_vals)
                    else:
                        default_text = str(col_data.iloc[0]) if not col_data.empty else ""
                        input_data[col] = st.text_input(col, value=default_text)

            if st.button("Predict"):
                input_df = pd.DataFrame([input_data])
                prediction = pipe.predict(input_df)[0]

                if prediction in [0, 1] and target.lower() == "survived":
                    label = "Survived" if prediction == 1 else "Not Survived"
                    st.markdown(
                        f"<span style='color:red; font-size:20px;'>Prediction: <b>{label}</b></span>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"<span style='color:red; font-size:20px;'>Prediction: <b>{prediction}</b></span>",
                        unsafe_allow_html=True
                    )

set_full_background()
