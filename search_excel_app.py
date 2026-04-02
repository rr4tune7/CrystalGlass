import streamlit as st
import pandas as pd

st.set_page_config(page_title="Поиск по Excel", layout="wide")
st.title("🔍 KMK 01.04.2026")

# Ссылка на Excel
url = "https://www.dropbox.com/scl/fi/8q5vwwwb3iwc1pahkdtg6/.xlsx?rlkey=y2c5f99s1bq97ab94vlsc5lw0&st=9twbfjzy&dl=1"

# Загрузка Excel
try:
    df = pd.read_excel(url)
except Exception as e:
    st.error(f"Не удалось загрузить Excel файл: {e}")
    st.stop()

st.subheader("Все данные")
st.dataframe(df)

# Ввод ключевого слова
search = st.text_input("Введите ключевое слово для поиска в ԱՆՎԱՆՈՒՄ:")

if search:
    # 1. Поиск в ԱՆՎԱՆՈՒՄ
    df_filtered = df[df['ԱՆՎԱՆՈՒՄ'].astype(str).str.contains(search, case=False, na=False)]

    # 2. Столбцы, которые нужно проверять на непустые значения (все кроме ԱՐԺԵՔ и ՏԵՂԱԴՐՈՒՄ и АՆՎԱՆՈՒՄ)
    columns_to_check = [col for col in df.columns if col not in ['ԱՐԺԵՔ', 'ՏԵՂԱԴՐՈՒՄ', 'ԱՆՎԱՆՈՒՄ']]

    # 3. Оставляем только строки, где хотя бы одно значение в этих столбцах не пустое
    df_non_empty = df_filtered[df_filtered[columns_to_check].notna().any(axis=1)]

    st.subheader(f"Результаты поиска по '{search}' в ԱՆՎԱՆՈՒՄ")
    st.dataframe(df_non_empty)





