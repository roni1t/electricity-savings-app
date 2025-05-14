
import streamlit as st
from electricity_calculator import analyze_consumption
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="מחשבון חיסכון בחשמל", layout="wide")
st.title("🔌 מחשבון חיסכון בצריכת חשמל לפי מסלולים")
st.markdown("העלה את דוח הצריכה מחברת החשמל (CSV) וחשב את העלות החודשית לפי כל מסלול")

uploaded_file = st.file_uploader("📤 העלה קובץ צריכה", type="csv")

if uploaded_file:
    with open("uploaded.csv", "w", encoding="utf-8") as f:
        f.write(uploaded_file.getvalue().decode("utf-8"))

    df_result = analyze_consumption("uploaded.csv")

    st.subheader("📊 תוצאות לפי חודש:")
    st.dataframe(df_result)

    st.subheader("📈 גרף השוואה בין מסלולים:")
    fig, ax = plt.subplots(figsize=(12, 5))
    df_result.set_index('חודש')[['עלות רגילה (₪)', 'הייטק', 'לילה', 'משפחה', 'כללי']].plot(ax=ax)
    ax.set_ylabel("עלות חודשית (₪)")
    ax.set_title("השוואת עלות חודשית לפי מסלולי חשמל")
    ax.grid(True)
    st.pyplot(fig)

    csv = df_result.to_csv(index=False).encode('utf-8-sig')
    st.download_button("⬇️ הורד את הדוח כקובץ Excel", data=csv, file_name="תוצאות_חיסכון.csv", mime='text/csv')
else:
    st.info("העלה קובץ כדי להתחיל לחשב")
