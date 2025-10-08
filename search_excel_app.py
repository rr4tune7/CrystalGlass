import streamlit as st
import pandas as pd

st.set_page_config(page_title="Поиск по Excel", layout="wide")
st.title("🔍 KMK 04.10.2025" )

# Ссылка на Excel
url = "https://www.dropbox.com/scl/fi/8ncsz4wpl94owruvmv4l2/.xlsx?rlkey=hhmc41roywrr5qzmvor5rxlbx&st=wcpqphai&dl=1"

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
    # 1. Поиск в АՆՎԱՆՈՒՄ
    df_filtered = df[df['ԱՆՎԱՆՈՒՄ'].astype(str).str.contains(search, case=False, na=False)]

    # 2. Столбцы для проверки непустоты (все кроме ԱՐԺԵՔ и ՏԵՂԱԴՐՈՒՄ и ԱՆՎԱՆՈՒՄ)
    columns_to_check = [col for col in df_filtered.columns if col not in ['ԱՐԺԵՔ', 'ՏԵՂԱԴՐՈՒՄ', 'ԱՆՎԱՆՈՒՄ']]

    # 3. Оставляем только строки, где хотя бы одно значение в этих столбцах не пустое
    df_non_empty_rows = df_filtered[df_filtered[columns_to_check].notna().any(axis=1)]

    # 4. Оставляем только столбцы, где есть хотя бы одно непустое значение
    df_non_empty = df_non_empty_rows.loc[:, df_non_empty_rows.notna().any(axis=0)]

    st.subheader(f"Результаты поиска по '{search}' в ԱՆՎԱՆՈՒՄ")
    st.dataframe(df_non_empty)




