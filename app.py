import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
import psycopg2
import os
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime

def get_key(key):
        return st.secrets[key]

#python -m streamlit run app.py

@st.cache_resource
def connect():
    engine = create_engine(
        f"postgresql+psycopg2://{get_key('DB_USERNAME')}:{get_key('DB_PASSWORD')}@{get_key('DB_HOST')}:{get_key('DB_PORT')}/{get_key('DB_NAME')}",
        poolclass=NullPool
    )
    return engine

weight = st.number_input("Вес")
calories = st.number_input("Калории")
cycle_day = st.selectbox("День цикла", [1, 2, 3, 4, 5])
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

    



