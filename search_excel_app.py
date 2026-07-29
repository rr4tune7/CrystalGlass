import streamlit as st
import pandas as pd
from rapidfuzz import fuzz

st.set_page_config(page_title="Поиск по Excel", layout="wide")
st.title("🔍 KMK 28.07.2026")

# Ссылка на Excel
url = "https://www.dropbox.com/scl/fi/w2qukfr4frqchaaerf1vk/.xlsx?rlkey=qddf4fxqf4n4vyzhnhsavokkf&st=cx02jqav&dl=1"

# Загрузка Excel
try:
    df = pd.read_excel(url)
except Exception as e:
    st.error(f"Не удалось загрузить Excel файл: {e}")
    st.stop()

st.subheader("Все данные")
st.dataframe(df)

def normalize_text(value):
    if pd.isna(value):
        return ""

    value = str(value).lower().strip()

    return "".join(
        symbol for symbol in value
        if symbol.isalnum() or symbol.isspace()
    )


def fuzzy_match(value, search_text, similarity=75):
    value = normalize_text(value)
    search_text = normalize_text(search_text)

    if not value or not search_text:
        return False

    # Сначала проверяем обычное совпадение
    if search_text in value:
        return True

    # Сравниваем запрос с каждым словом
    words = value.split()

    scores = [
        fuzz.ratio(search_text, word)
        for word in words
    ]

    # Также сравниваем со всем названием
    scores.append(
        fuzz.partial_ratio(search_text, value)
    )

    return max(scores) >= similarity

# Ввод ключевого слова
search = st.text_input("Введите ключевое слово для поиска в ԱՆՎԱՆՈՒՄ:")

if search:
    # 1. Поиск в ԱՆՎԱՆՈՒՄ
    df_filtered = df[
    df['ԱՆՎԱՆՈՒՄ'].apply(
        lambda value: fuzzy_match(
            value,
            search,
            similarity=80
        )
    )
]

    # 2. Столбцы, которые нужно проверять на непустые значения (все кроме ԱՐԺԵՔ и ՏԵՂԱԴՐՈՒՄ и АՆՎԱՆՈՒՄ)
    columns_to_check = [col for col in df.columns if col not in ['ԱՐԺԵՔ', 'ՏԵՂԱԴՐՈՒՄ', 'ԱՆՎԱՆՈՒՄ']]

    # 3. Оставляем только строки, где хотя бы одно значение в этих столбцах не пустое
    df_non_empty = df_filtered[df_filtered[columns_to_check].notna().any(axis=1)]

    st.subheader(f"Результаты поиска по '{search}' в ԱՆՎԱՆՈՒՄ")
    st.dataframe(df_non_empty)





