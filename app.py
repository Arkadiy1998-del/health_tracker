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
   "https://raw.githubusercontent.com/Arkadiy1998-del/health_tracker/main/Images/5376x3072_1721973_%5Bwww.ArtFile.ru%5D.jpg",
   "https://raw.githubusercontent.com/Arkadiy1998-del/health_tracker/main/Images/Images/AA1M06Xa.jfif",
   "https://raw.githubusercontent.com/Arkadiy1998-del/health_tracker/main/Images/Images/avtor-naarok0fkor-kotiata-milye-boke.webp",
   "https://raw.githubusercontent.com/Arkadiy1998-del/health_tracker/main/Images/Images/ii-art-neiroset-sobaka-shchenok-mordashka-vzgliad-poza-ts-16.webp",
   "https://raw.githubusercontent.com/Arkadiy1998-del/health_tracker/main/Images/Images/maxresdefault.jpg"
]

bg_image = random.choice(images)

st.markdown(
    f'<style>body{{background-image:url("{bg_image}"); background-size:cover;}}</style>',
    unsafe_allow_html=True)

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
    st.write("Данные отправлены!")

    

