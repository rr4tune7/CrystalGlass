import streamlit as st
import pandas as pd

st.set_page_config(page_title="Поиск по Excel", layout="wide")
st.title("🔍 KMK 21.04.2026")

# Ссылка на Excel
url = "https://www.dropbox.com/scl/fi/7o6x2u8ze7xa5yroi575w/KMK.xlsx?rlkey=js7z4un9mhxsf8nl928pduw81&st=fmsq651d&dl=1"

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





