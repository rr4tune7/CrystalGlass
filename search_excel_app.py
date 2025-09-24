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

# Выбор столбца для поиска
columns = df.columns.tolist()
column_to_search = st.selectbox("Выберите столбец для поиска", ["Все столбцы"] + columns)

# Ввод ключевого слова
search = st.text_input("Введите ключевое слово для поиска:")

if search:
    if column_to_search == "Все столбцы":
        filtered = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
