import streamlit as st
import pandas as pd
import re

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

def normalize_word(word):
    """
    Преобразует слово в упрощённое написание.
    Например:
    rogue   -> ruj
    camry   -> camri
    alphard -> alfard
    """

    word = str(word).lower().strip()

    # Удаляем знаки и оставляем только буквы и цифры
    word = re.sub(r"[^a-zа-яё0-9]", "", word)

    # Частые варианты написания
    word = word.replace("ph", "f")
    word = word.replace("ck", "k")

    # Rogue -> ruj
    word = re.sub(r"ogue$", "uj", word)

    # Например: range -> ranj
    word = re.sub(r"ge$", "j", word)

    # Camry -> camri
    word = re.sub(r"y$", "i", word)

    return word


def normalize_words(value):
    """
    Разделяет название на слова
    и нормализует каждое слово.
    """

    if pd.isna(value):
        return []

    text = str(value).lower()

    words = re.findall(
        r"[a-zа-яё0-9]+",
        text
    )

    return [
        normalize_word(word)
        for word in words
        if normalize_word(word)
    ]


def smart_exact_search(value, search_text):
    """
    Строгий поиск после преобразования слов.
    Все введённые слова должны присутствовать
    в названии товара.
    """

    excel_words = normalize_words(value)
    search_words = normalize_words(search_text)

    if not excel_words or not search_words:
        return False

    return all(
        search_word in excel_words
        for search_word in search_words
    )

# Ввод ключевого слова
search = st.text_input("Введите ключевое слово для поиска в ԱՆՎԱՆՈՒՄ:")

if search:
    # 1. Поиск в ԱՆՎԱՆՈՒՄ
   df_filtered = df[
    df["ԱՆՎԱՆՈՒՄ"].apply(
        lambda value: smart_exact_search(
            value,
            search
        )
    )
]

    # 2. Столбцы, которые нужно проверять на непустые значения (все кроме ԱՐԺԵՔ и ՏԵՂԱԴՐՈՒՄ и АՆՎԱՆՈՒՄ)
    columns_to_check = [col for col in df.columns if col not in ['ԱՐԺԵՔ', 'ՏԵՂԱԴՐՈՒՄ', 'ԱՆՎԱՆՈՒՄ']]

    # 3. Оставляем только строки, где хотя бы одно значение в этих столбцах не пустое
    df_non_empty = df_filtered[df_filtered[columns_to_check].notna().any(axis=1)]

    st.subheader(f"Результаты поиска по '{search}' в ԱՆՎԱՆՈՒՄ")
    st.dataframe(df_non_empty)





