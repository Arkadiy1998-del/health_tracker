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


images = [
   "https://raw.githubusercontent.com/Arkadiy1998-del/health_tracker/main/Images/28b72de58eddd0a987087eeb5738b5c7.jpg",
   "https://raw.githubusercontent.com/Arkadiy1998-del/health_tracker/main/Images/343b43da25a6e1585e6c390842ef025a.jpg",
   "https://raw.githubusercontent.com/Arkadiy1998-del/health_tracker/main/Images/5fee67d5da2ace52cfb0bd005fb056c7.jpg",
   "https://raw.githubusercontent.com/Arkadiy1998-del/health_tracker/main/Images/maxresdefault.jpg"
]

bg_image = random.choice(images)

st.markdown(
    f"""
    <style>
    .stApp {{
        background: url("{bg_image}") no-repeat center center fixed;
        background-size: cover;
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

user = st.selectbox("Пользователь", ["Лена", "Вика"])
weight = st.number_input("Вес", step = 1)
mood = st.slider("Настроение", 0, 10)
sleep_hours = st.number_input("Сон, часов", step = 1)
sport_activ = st.selectbox("Физическая активность", ["Relax", "Лёгкие нагрузки", "Тренировка", "Интенсивная тренировка"])

if st.button("Сохранить"):
    engine = connect()
    with st.spinner("Сохраняю..."):
        temp = pd.DataFrame({
            'date' : [datetime.now()],
            'weight' : [weight],
            'mood' : [mood],
            'sleep_hours' : [sleep_hours],
            'sport_activ' : [sport_activ]})
        temp.to_sql(
            'streamlit_raw_data',
            con = engine,
            schema = 'data_lake',
            if_exists = 'append',
            index = False,
            method = None,
        )
    
    st.toast("Данные сохранены! Хорошего дня:)", icon="✅")

    
