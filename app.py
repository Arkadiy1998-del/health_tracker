# импорты библиотек
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
import psycopg2
import os
import streamlit as st
from datetime import datetime, date
import random

# определяем даты и часы
today = date.today()
hour = datetime.now().hour

# создание функции соединения с Streamlit
def get_key(key):
    return st.secrets[key]

# пользователи
usermap = {"Лена" : 1, "Вика" : 2}

# фон
bg_image = "https://raw.githubusercontent.com/Arkadiy1998-del/health_tracker/main/Images/IMG_20260316_114430_151.jpg"

# дизайн
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{bg_image}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Задаём функцию для создания словарей по метрикам
def create_dict(metric_name, saving, metric):
    if 'dict' not in st.session_state: st.session_state.dict = None
    st.session_state.dict = {metric_name : metric}
    return st.session_state.dict

# Создаём функцию для соединения с streamlit, кеширования ресурсов
@st.cache_resource
def connect():
    con = create_engine(
     "postgresql+psycopg2://",
       creator = lambda : psycopg2.connect(
    user = get_key("DB_USERNAME"),
    password = get_key("DB_PASSWORD"),
    host = get_key("DB_HOST"),
    port = get_key("DB_PORT"),
    dbname = get_key("DB_NAME")
    ),
    poolclass = NullPool
)
    return con

# Задаём функцию для проверки повторного ввода
def already_exists(con, metric, date, user_id):
    sql_data = pd.read_sql(f"SELECT {metric} FROM data_lake.raw_data WHERE date = %s AND user_id = %s LIMIT 1"
                           , con
                           , params=(date, usermap[user]))
    return not sql_data.empty

# Задаём функцию отрисовки UI при повторном вводе
def choise(metric_name):
    key = f'saving_{metric_name}'
    if "key" not in st.session_state: st.session_state.key = None
    st.warning("За этот день уже есть данные")
    user_choise = st.radio("Перезаписать?", ["...", "Да", "Нет"], key = key)
    if user_choise != "...":
        st.session_state.key = user_choise
    return st.session_state.key

# Задаём функцию сохранения в базу через upsert
def upsert(con, date, user_id, metric_name, value):

    query = f"""
INSERT INTO data_lake.raw_data (date, user_id, {metric_name})
VALUES (:date, :user_id, :value)
ON CONFLICT (date, user_id)
DO UPDATE SET 
    {metric_name} = COALESCE(EXCLUDED.{metric_name}, data_lake.raw_data.{metric_name})"""

    with con.connect() as conn:
        conn.execute(text(query), {"date" : date, "user_id" : user_id, "value" : value})
        conn.commit()


# Создаём флаг ввода данных по метрике
def change(metric):
    st.session_state[f'{metric}_flag'] = True

# задаём показатели и их параметры для цикла
weight = {"name" : "weight", 
          "widget" : st.number_input, 
          "args" : {"label" : "Вес", "step" : 1, "on_change" : change, 
                    "args" : ("weight",)}}                                        
sleep_hours = {"name" : "sleep_hours", 
               "widget" : st.number_input, 
               "args" : {"label" : "Сон, часов", "step" : 1, "on_change" : change, 
                         "args" : ("sleep_hours",)}}
mood = {"name" : "mood", 
        "widget" : st.slider, 
        "args" : {"label" : "Настроение", "min_value" : -1, "max_value" : 10, "on_change" : change, 
                  "args" : ("mood",)}}
sport_activ = {"name" : "sport_activ", 
               "widget" : st.selectbox, 
               "args" : {"label" : "Физическая активность", "options" : ["Не выбрано", "Relax", "Лёгкие нагрузки", "Тренировка", "Интенсивная тренировка"], "on_change" : change,
                         "args" : ("sport_activ",)}}

metrics = [weight, sleep_hours, mood, sport_activ]


# Задаём заголовок
if  5 < hour <= 12:
    daytime = 'morning'
    st.title("Доброе утро!")
elif 12 < hour <= 17:
    daytime = 'afternoon'
    st.title("Добрый день!")
elif 17 < hour <= 22:
    daytime = 'evening'
    st.title("Добрый вечер!")
else:
    daytime = 'night'
    st.title("Доброй ночи!")

con = connect()

date = st.date_input("Выбор даты...", value = today, max_value=today)
user = st.selectbox("Пользователь", ["Лена", "Вика"])

if "saving_dict" not in st.session_state: st.session_state.saving_dict = {}

for m in metrics:
    value = m["widget"](**m["args"]) 
    if st.session_state.get(f'{m["name"]}_flag'):
        if "saving" not in st.session_state: st.session_state.saving = None
        if already_exists(con, m["name"], date, usermap[user]):
            st.session_state.saving = choise(m["name"])
        else:
            st.session_state.saving = "Да"
        st.session_state.saving_dict[m["name"]] = {"saving" : st.session_state.saving, "value" : value}

if st.button("Сохранить"):
    with st.spinner("Сохраняю..."):
        for key, data in st.session_state.saving_dict.items():
            if data["saving"] == "Да":
                upsert(con, date, usermap[user], key, data["value"])
    st.toast("Данные сохранены! Хорошего дня:)", icon="✅")    
