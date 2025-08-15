import streamlit as st
import pandas as pd
import polars as pl
from services.data_io import (
    load_csv, to_pandas, drop_na, drop_duplicates,
    convert_types, normalize
)
from services.background import set_full_background

st.set_page_config(layout="wide")
st.title("🧽 Data Cleaner")

def handle_missing_values(lf: pl.LazyFrame) -> pl.LazyFrame:
    st.subheader("Missing Values")
    choice = st.radio("How do you want to handle missing values?", ["Ignore", "Delete", "Replace Values"])
    schema = lf.collect().schema
    string_cols, numeric_cols = [], []
    datetime_cols = [c for c, t in schema.items() if isinstance(t, pl.Datetime)]
    for col, _ in schema.items():
        col_vals = lf.select(pl.col(col).cast(pl.Utf8)).collect()[col].to_list()
        non_empty = [v for v in col_vals if v is not None and str(v).strip() != ""]
        if non_empty and all(str(v).replace(".", "", 1).isdigit() for v in non_empty):
            if col not in datetime_cols:
                numeric_cols.append(col)
        elif col not in datetime_cols:
            string_cols.append(col)
    for col in string_cols:
        lf = lf.with_columns(
            pl.when(pl.col(col).cast(pl.Utf8).str.strip_chars().str.len_chars() == 0)
            .then(None)
            .otherwise(pl.col(col))
            .alias(col)
        )
    if choice == "Delete":
        lf = drop_na(lf)
    elif choice == "Replace Values":
        s_val = st.text_input("Replacement for string columns:", "blank")
        n_val = st.number_input("Replacement for numeric columns:", value=0.0)
        for col in string_cols:
            lf = lf.with_columns(pl.col(col).fill_null(s_val))
        for col in numeric_cols:
            lf = lf.with_columns(pl.col(col).fill_null(n_val))
        for col in datetime_cols:
            lf = lf.with_columns(pl.col(col).fill_null(pd.Timestamp("1970-01-01")))
    return lf

def run_filter_ui(lf: pl.LazyFrame, idx: int) -> pl.LazyFrame:
    st.subheader(f"Filter {idx}")
    df_prev = to_pandas(lf)
    if df_prev.empty:
        st.info("No rows to filter.")
        return lf
    col = st.selectbox(f"Filter {idx} - column", options=df_prev.columns, key=f"fcol_{idx}")
    if pd.api.types.is_numeric_dtype(df_prev[col]):
        col_series = df_prev[col].astype(float)
        min_v, max_v = float(col_series.min()), float(col_series.max())
        a, b = st.slider(f"{col} between:", min_v, max_v, (min_v, max_v), key=f"fnum_{idx}")
        lf = lf.filter((pl.col(col) >= a) & (pl.col(col) <= b))
        return lf
    if pd.api.types.is_datetime64_any_dtype(df_prev[col]):
        min_dt, max_dt = df_prev[col].min(), df_prev[col].max()
        start_date = (min_dt if pd.notna(min_dt) else pd.Timestamp.today()).date()
        end_date = (max_dt if pd.notna(max_dt) else pd.Timestamp.today()).date()
        start, end = st.date_input(f"{col} between:", (start_date, end_date), key=f"fdate_{idx}")
        lf = lf.filter(
            (pl.col(col) >= pl.lit(pd.Timestamp(start))) &
            (pl.col(col) <= pl.lit(pd.Timestamp(end)))
        )
        return lf
    txt = st.text_input(f"{col} contains:", key=f"ftext_{idx}")
    if txt:
        lf = lf.filter(pl.col(col).cast(pl.Utf8).str.contains(txt, literal=False))
    return lf

uploaded_file = st.file_uploader("Upload CSV for Cleaning", type=["csv"])

if uploaded_file:
    lf, _ = load_csv(uploaded_file)
    lf = handle_missing_values(lf)
    if st.checkbox("Remove Duplicate Rows"):
        lf = drop_duplicates(lf)
    st.subheader("Select Columns")
    cols_now = list(to_pandas(lf).columns)
    keep = st.multiselect("Columns to keep:", cols_now, default=cols_now)
    if keep:
        lf = lf.select(keep)
    st.subheader("Change Data Types")
    type_map = {"String": pl.Utf8, "Integer": pl.Int64, "Float": pl.Float64, "Datetime": pl.Datetime}
    casts = {}
    cols_after_select = list(to_pandas(lf).columns)
    for c in cols_after_select:
        choice = st.selectbox(f"{c} type:", list(type_map.keys()), key=f"type_{c}")
        casts[c] = type_map[choice]
    lf = convert_types(lf, casts)
    st.subheader("Normalize Numeric Columns")
    df_for_norm = to_pandas(lf)
    numeric_cols = df_for_norm.select_dtypes(include=["number"]).columns.tolist()
    if numeric_cols:
        cols_to_norm = st.multiselect("Columns to normalize:", numeric_cols)
        if cols_to_norm:
            lf = normalize(lf, cols_to_norm)
    else:
        st.caption("No numeric columns available after type conversion.")
    lf = run_filter_ui(lf, 1)
    lf = run_filter_ui(lf, 2)
    st.subheader("Cleansed Final Output")
    final_df = to_pandas(lf)
    st.dataframe(final_df, use_container_width=True)
    csv_bytes = final_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Cleansed CSV",
        data=csv_bytes,
        file_name="cleansed_data.csv",
        mime="text/csv"
    )

set_full_background()
