
import streamlit as st
from electricity_calculator import analyze_consumption
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="מחשבון חשמל", page_icon="🔌", layout="wide")

st.markdown(
    '''
    <style>
    body, .css-18e3th9, .css-1d391kg {
        direction: rtl;
        text-align: right;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

st.markdown("# 🔌 מחשבון חיסכון בצריכת חשמל לפי מסלולים")
st.markdown("העלה את קובץ הצריכה שלך (CSV מחברת החשמל) וקבל ניתוח צריכה, חישוב עלויות, גרף ודוח להורדה.")

uploaded_file = st.file_uploader("📤 בחר קובץ צריכה", type="csv")

if uploaded_file:
    with open("uploaded.csv", "w", encoding="utf-8") as f:
        f.write(uploaded_file.getvalue().decode("utf-8"))

    df_result = analyze_consumption("uploaded.csv")

    st.markdown("### 📊 טבלת עלות חודשית לפי מסלולים:")
    styled = df_result.style.background_gradient(cmap='Oranges').format("{:.2f}")
    st.dataframe(styled, use_container_width=True)

    st.markdown("### 📈 גרף השוואת עלויות בין מסלולים:")
    fig, ax = plt.subplots(figsize=(12, 5))
    df_result.set_index('חודש')[['עלות רגילה (₪)', 'הייטק', 'לילה', 'משפחה', 'כללי']].plot(ax=ax)
    ax.set_title("השוואת עלות חודשית לפי מסלולים", fontsize=14)
    ax.set_ylabel("עלות (₪)")
    ax.grid(True)
    st.pyplot(fig)

    st.markdown("### 📥 הורד דוח אקסל")
    csv = df_result.to_csv(index=False).encode('utf-8-sig')
    st.download_button("⬇️ הורד דוח", data=csv, file_name="דו"ח_חיסכון.csv", mime='text/csv')
else:
    st.info("נא להעלות קובץ לצורך חישוב")
