import streamlit as st
import pandas as pd

st.set_page_config(page_title="Поиск по Excel", layout="wide")
st.title("🔍 Мгновенный поиск по Excel")

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
search = st.text_input("Введите ключевое слово для поиска:")

if search:
    # Исключаем столбцы, которые не хотим искать
    columns_to_search = [col for col in df.columns if col not in ['ԱՐԺԵՔ', 'ՏԵՂԱԴՐՈՒՄ']]

    # Фильтруем строки, где хотя бы одно значение не None и не пустое
    df_non_empty = df[df[columns_to_search].apply(lambda row: row.dropna().astype(str).str.strip().any(), axis=1)]

    # Функция для поиска совпадений только в непустых значениях
    def row_contains(row, keyword):
        for val in row:
            if pd.notna(val) and str(val).strip() != '' and keyword.lower() in
