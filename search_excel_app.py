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
    # Выбираем все столбцы кроме последних двух
    columns_to_search = df.columns[:-2]

    # Функция для поиска только по непустым значениям
    def row_contains(row, keyword):
        for val in row:
            if pd.notna(val) and keyword.lower() in str(val).lower():
                return True
        return False

    # Применяем фильтр только к выбранным столбцам
    filtered = df[df[columns_to_search].apply(lambda row: row_contains(row, search), axis=1)]

    st.subheader(f"Результаты поиска по '{search}' (без последних двух столбцов)")
    st.dataframe(filtered)
