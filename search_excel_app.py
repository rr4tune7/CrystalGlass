import streamlit as st
import pandas as pd

st.set_page_config(page_title="Поиск по Excel", layout="wide")
st.title("🔍 Мгновенный поиск по Excel")

# Вставь сюда свою прямую ссылку на Excel
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
    # Убираем строки, где все значения пустые или None
    df_non_empty = df.dropna(how='all')

    # Фильтруем строки, где есть совпадения во всех столбцах
    filtered = df_non_empty[df_non_empty.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]

    st.subheader(f"Результаты поиска по '{search}'")
    st.dataframe(filtered)
