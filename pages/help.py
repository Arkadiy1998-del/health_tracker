import streamlit as st

st.set_page_config(page_title = "Помощь", layout = "wide")

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

st.write("Привет")
