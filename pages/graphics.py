import pandas as pd
import psycopg2
import os
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def get_key(key):
    return st.secrets[key]


st.set_page_config(layout="wide")

conn =  psycopg2.connect(
    user = get_key("DB_USERNAME"),
    password = get_key("DB_PASSWORD"),
    host = get_key("DB_HOST"),
    port = get_key("DB_PORT"),
    dbname = get_key("DB_NAME")
    )

data_df = pd.read_sql("SELECT * FROM data_lake.streamlit_raw_data", conn)

data_df['date'] = pd.to_datetime(data_df['date'])

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x = data_df["date"],
        y = data_df["weight"],
        name = "Вес",
        mode = "lines",
        yaxis = "y1"
    )
)

fig.add_trace(
    go.Scatter(
        x = data_df["date"],
        y = data_df["calories"],
        name = "Калории",
        mode = "lines",
        yaxis = "y2"
    )
)

fig.add_trace(
    go.Scatter(
        x = data_df["date"],
        y = data_df["mood"],
        name = "Настроение",
        mode = "markers",
        marker = dict(size = 10),
        yaxis = "y1"
    )
)

fig.update_layout(
    yaxis1 = dict(title = "Вес"),
    yaxis2 = dict(
        title = "Калории",
        overlaying = "y",
        side = "right"
    )
                  
)


st.plotly_chart(fig, use_container_width=True)


