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
    # Исключаем столбцы по названию
    columns_to_search = [col for col in df.columns if col not in ['ԱՐԺԵՔ', 'ՏԵՂԱԴՐՈՒՄ']]

    # Функция для поиска только по непустым значениям
    def row_contains(row, keyword):
        for val in row:
            if pd.notna(val) and keyword.lower() in str(val).lower():
                return True
        return False

    # Применяем фильтр только к выбранным столбцам
    filtered = df[df[columns_to_search].apply(lambda row: row_contains(row, search), axis=1)]

    st.subheader(f"Результаты поиска по '{search}' (без столбцов ԱՐԺԵՔ и ՏԵՂԱԴՐՈՒՄ)")
    st.dataframe(filtered)
