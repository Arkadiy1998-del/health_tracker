import streamlit as st

weight = st.number_input("Вес")
calories = st.number_input("Калории")
cycle_day = st.selectbox("День цикла", [1, 2, 3, 4, 5])
mood = st.slider("Настроение", 0, 10)
if st.button("Сохранить"):
    st.write("Данные отправлены!")