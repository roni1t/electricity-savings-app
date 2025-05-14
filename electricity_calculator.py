import pandas as pd

TARIFF = 0.6
DISCOUNTS = {
    'הייטק': 0.10,
    'לילה': 0.20,
    'יום': 0.15,
    'משפחה': 0.18,
    'כללי': 0.07
}

def is_hitech(hour): return hour >= 23 or hour < 17
def is_night(hour): return hour >= 23 or hour < 7
def is_day(hour, weekday): return weekday in range(0, 5) and 7 <= hour < 17
def is_family(hour, weekday): return weekday in range(0, 5) and 14 <= hour < 20

def classify_payment(row):
    hour = row['שעה']
    weekday = row['יום בשבוע']
    kwh = row['צריכה בקוט"ש']
    return pd.Series({
        'הייטק': kwh * TARIFF * (1 - DISCOUNTS['הייטק']) if is_hitech(hour) else kwh * TARIFF,
        'לילה': kwh * TARIFF * (1 - DISCOUNTS['לילה']) if is_night(hour) else kwh * TARIFF,
        'יום': kwh * TARIFF * (1 - DISCOUNTS['יום']) if is_day(hour, weekday) else kwh * TARIFF,
        'משפחה': kwh * TARIFF * (1 - DISCOUNTS['משפחה']) if is_family(hour, weekday) else kwh * TARIFF,
        'כללי': kwh * TARIFF * (1 - DISCOUNTS['כללי'])  # תמיד
    })

def analyze_consumption(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    start = next(i for i, line in enumerate(lines) if "תאריך" in line)
    df = pd.read_csv(pd.io.common.StringIO(''.join(lines[start:])))
    df = df.dropna()
    df = df[df['תאריך'].str.contains(r'\\d{2}/\\d{2}/\\d{4}')]
    df['datetime'] = pd.to_datetime(df['תאריך'] + ' ' + df['מועד תחילת הפעימה'], format='%d/%m/%Y %H:%M')
    df['צריכה בקוט"ש'] = pd.to_numeric(df['צריכה בקוט"ש'], errors='coerce')
    df['שעה'] = df['datetime'].dt.hour
    df['יום בשבוע'] = df['datetime'].dt.dayofweek
    df['חודש'] = df['datetime'].dt.to_period('M').astype(str)

    payments = df.apply(classify_payment, axis=1)
    payments['חודש'] = df['חודש']
    numeric_cols = payments.select_dtypes(include='number').columns.tolist()
monthly = payments.groupby('חודש')[numeric_cols].sum()
    monthly_kwh = df.groupby('חודש')['צריכה בקוט"ש'].sum()
    monthly['צריכה בקוט"ש'] = monthly_kwh
    monthly['עלות רגילה (₪)'] = (monthly_kwh * TARIFF).round(2)

    return monthly.reset_index().round(2)
