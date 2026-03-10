import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
import pg8000
import os
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime

load_dotenv()

def get_key(key):
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key)

@st.cache_resource
def connect():
    engine = create_engine(
     "postgresql+pg8000://",
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

weight = st.number_input("Вес")
calories = st.number_input("Калории")
cycle_day = st.selectbox("День цикла", [0, 1, 2, 3, 4, 5])
mood = st.slider("Настроение", 0, 10)
if st.button("Сохранить"):
    engine = connect()
    temp = pd.DataFrame({
        'date' : [datetime.now()],
        'weight' : [weight],
        'calories' : [calories], 
        'cycle_day' : [cycle_day], 
        'mood' : [mood]})
    temp.to_sql(
        'streamlit_raw_data',
        con = engine,
        schema = 'data_lake',
        if_exists = 'append',
        index = False,
        method = None,
    )
    st.write("Данные отправлены!")

    




