import streamlit as st
from electricity_calculator import analyze_consumption
import pandas as pd
from io import StringIO

st.set_page_config(page_title="מחשבון חשמל", layout="wide")
st.title("מחשבון חיסכון בחשמל לפי מסלול")

uploaded_file = st.file_uploader("העלה קובץ צריכת חשמל (CSV)", type="csv")

if uploaded_file:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    with open("uploaded.csv", "w", encoding="utf-8") as f:
        f.write(stringio.getvalue())

    df_result = analyze_consumption("uploaded.csv")
    st.success("החישוב הושלם!")
    st.dataframe(df_result)

    csv = df_result.to_csv(index=False).encode('utf-8-sig')
    st.download_button("הורד כקובץ Excel", data=csv, file_name="תוצאות_חיסכון.csv", mime='text/csv')
