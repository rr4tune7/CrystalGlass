import streamlit as st
import pandas as pd

st.set_page_config(page_title="Поиск по Excel", layout="wide")
st.title("🔍 Поиск по ԱՆՎԱՆՈՒՄ с фильтром непустых строк")

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
    # 1. Фильтруем строки по совпадению в столбце ԱՆՎԱՆՈՒՄ
    mask_name = df['ԱՆՎԱՆՈՒՄ'].astype(str).str.contains(search, case=False, na=False)
    df_filtered = df[mask_name]

    # 2. Исключаем столбцы ԱՐԺԵՔ и ՏԵՂԱԴՐՈՒՄ для проверки на пустоту
    columns_to_check = [col for col in df.columns if col not in ['ԱՐԺԵՔ', 'ՏԵՂԱԴՐՈՒՄ']]

    # 3. Оставляем только строки, где есть хотя бы одно непустое значение в остальных столбцах
    df_non_empty = df_filtered[df_filtered[columns_to_check].apply(lambda row: row.notna().any(), axis=1)]

    st.subheader(f"Результаты поиска по '{search}' в ԱՆՎԱՆՈՒՄ (пустые строки убраны)")
    st.dataframe(df_non_empty)
