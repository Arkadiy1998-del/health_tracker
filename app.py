import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
import psycopg2
import os
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime
import random

load_dotenv()

def get_key(key):
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key)

usermap = {"Лена" : 1, "Вика" : 2}

bg_image = "https://raw.githubusercontent.com/Arkadiy1998-del/health_tracker/main/Images/IMG_20260316_114430_151.jpg"

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

@st.cache_resource
def connect():
    engine = create_engine(
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
    return engine

def save(data, param):
    if param == 'm':
        data.to_sql(
            'streamlit_raw_data_m',
            con = engine,
            schema = 'data_lake',
            if_exists = 'append',
            index = False,
            method = None,
        )
    if param == 'e':
        data.to_sql(
            'streamlit_raw_data_e',
            con = engine,
            schema = 'data_lake',
            if_exists = 'append',
            index = False,
            method = None,
        )
daytime = None
hour = datetime.now().hour

if 5 < hour <= 12:
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

if daytime in ['morning','afternoon']:
    date = st.date_input("Выбрать дату...", max_value=today)
    user = st.selectbox("Пользователь", ["Лена", "Вика"])
    weight = st.number_input("Вес", step = 1)
    sleep_hours = st.number_input("Сон, часов", step = 1)
else:
    date = st.date_input("Выбрать дату...", max_value=today)
    user = st.selectbox("Пользователь", ["Лена", "Вика"])
    mood = st.slider("Настроение", 0, 10)
    sport_activ = st.selectbox("Физическая активность за день", ["Relax", "Лёгкие нагрузки", "Тренировка", "Интенсивная тренировка"])

if st.button("Сохранить"):
    engine = connect()
    with st.spinner("Сохраняю..."):
        if daytime in ['morning','afternoon']:
            temp = pd.DataFrame({
                'date' : [date],
                'user_id' : [usermap[user]],
                'weight' : [weight],
                'sleep_hours' : [sleep_hours]
            })
            save(temp, 'm')
        else:
            temp = pd.DataFrame({
                'date' : [date],
                'user_id' : [usermap[user]],
                'mood' : [mood],
                'sport_activ' : [sport_activ]
            })
            save(temp, 'e')
    st.toast("Данные сохранены! Хорошего дня:)", icon="✅")

    
