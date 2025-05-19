
import streamlit as st
from electricity_calculator import analyze_consumption
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.family'] = 'Arial'

st.set_page_config(page_title="מחשבון חשמל", page_icon="🔌", layout="wide")

# עיצוב RTL + צבעים לטבלה לסירוגין
st.markdown(
    '''
    <style>
    body, .css-18e3th9, .css-1d391kg {
        direction: rtl;
        text-align: right;
    }
    th, td {
        font-weight: bold !important;
        font-size: 16px;
        padding: 6px 10px !important;
        max-width: 110px;
    }
    tbody tr:nth-child(even) {
        background-color: #f0f8ff !important;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

st.markdown("# 🔌 מחשבון חיסכון בצריכת חשמל לפי מסלולים")

st.markdown("מערכת זו מחשבת עבורך את צריכת החשמל החודשית על פי קובץ מחברת החשמל ומשווה בין חמישה מסלולי תעריף.")
st.markdown("הניתוח כולל טבלה חודשית, גרף השוואתי, וחישוב המסלול המשתלם ביותר עבורך לשנה הקרובה.")

uploaded_file = st.file_uploader("📤 בחר קובץ צריכה (CSV)", type="csv")

if uploaded_file:
    with open("uploaded.csv", "w", encoding="utf-8") as f:
        f.write(uploaded_file.getvalue().decode("utf-8"))

    df_result = analyze_consumption("uploaded.csv")

    # ארגון עמודות וסידור מחדש
    df_result = df_result.rename(columns={
        'חודש': 'חודש',
        'צריכה בקוט"ש': 'צריכה (קוט"ש)',
        'עלות רגילה (₪)': 'עלות רגילה (₪)',
        'כללי': 'כללי (₪)',
        'משפחה': 'משפחה (₪)',
        'יום': 'יום (₪)',
        'לילה': 'לילה (₪)',
        'הייטק': 'הייטק (₪)'
    })
    ordered_cols = ['חודש', 'צריכה (קוט"ש)', 'עלות רגילה (₪)', 'כללי (₪)', 'משפחה (₪)', 'יום (₪)', 'לילה (₪)', 'הייטק (₪)']
    df_result = df_result[ordered_cols]

    # חישובי סיכום
    avg_costs = df_result[['כללי (₪)', 'משפחה (₪)', 'יום (₪)', 'לילה (₪)', 'הייטק (₪)']].mean()
    total_costs = df_result[['כללי (₪)', 'משפחה (₪)', 'יום (₪)', 'לילה (₪)', 'הייטק (₪)']].sum()
    best_plan = total_costs.idxmin()
    best_plan_name = best_plan.replace(" (₪)", "")
    best_saving = df_result['עלות רגילה (₪)'].sum() - total_costs.min()

    # הצגת סיכום בראש העמוד
    st.markdown("### 💡 סיכום שנתי:")
    col1, col2, col3 = st.columns(3)
    col1.metric("📉 המסלול המשתלם ביותר", best_plan_name)
    col2.metric('💰 חיסכון צפוי בש"ח', f"{best_saving:,.0f} ₪")
    col3.metric("📆 עלות שנתית ממוצעת", f"{total_costs.min():,.0f} ₪")

    # ⬇️ כפתור הורדה בראש העמוד
    csv = df_result.to_csv(index=False).encode('utf-8-sig')
    st.download_button("⬇️ הורד דוח Excel", data=csv, file_name='דו"ח_חיסכון.csv', mime='text/csv')

    st.markdown("### 📊 טבלת עלות חודשית לפי מסלולים:")
    st.dataframe(df_result, use_container_width=True)

    st.markdown("### 📈 גרף השוואת עלויות בין מסלולים:")
    fig, ax = plt.subplots(figsize=(12, 5))
    df_result_plot = df_result.copy()
    df_result_plot.set_index('חודש')[['עלות רגילה (₪)', 'הייטק (₪)', 'לילה (₪)', 'יום (₪)', 'משפחה (₪)', 'כללי (₪)']].plot(ax=ax)
    ax.set_title("השוואת עלות חודשית לפי מסלולים", fontsize=14, loc='right')
    ax.set_ylabel("עלות חודשית (₪)")
    ax.grid(True)
    ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0), title="מסלול")
    plt.xticks(rotation=45)
    ax.tick_params(axis='x', labelrotation=0)
    st.pyplot(fig)

else:
    st.info("נא להעלות קובץ לצורך ניתוח החשמל שלך")
