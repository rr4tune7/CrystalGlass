import streamlit as st
import pandas as pd

st.set_page_config(page_title="Поиск по Excel", layout="wide")
st.title("🔍 Мгновенный поиск по Excel")

# Ссылка на Excel в облаке
url = "https://1drv.ms/x/c/b60f28aad5a7d4ea/ET1PdWh7DL5LjVqLVjBfdqoByfstGjjZMe_bvxY_6SKkKg"  # вставь свою ссылку

# Загрузка Excel
try:
    df = pd.read_excel(url)
except Exception as e:
    st.error(f"Не удалось загрузить Excel файл: {e}")
    st.stop()

# Показ всех данных
st.subheader("Все данные")
st.dataframe(df)

# Поиск по ключевым словам
search = st.text_input("Введите ключевое слово для поиска:")

if search:
    filtered = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
    st.subheader(f"Результаты поиска по '{search}'")
    st.dataframe(filtered)

