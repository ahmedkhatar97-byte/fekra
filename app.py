import streamlit as st
from groq import Groq
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Fekra AI",
    page_icon="💡",
    layout="centered"
)

# الستايل النهائي الموحد (إخفاء البياض + الدخلة الشيك + الستايل النيون)
st.markdown(""
    <style>
    /* إخفاء إضافات ستريم ليت */
    footer {visibility: hidden; height: 0%;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    [data-testid="stStatusWidget"] {visibility: hidden;}

    /* توحيد لون الخلفية في كل مكان */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0E1117 !important;
    }

    /* حل مشكلة الجزء الأبيض تحت مستطيل الكتابة */
    div[data-testid="stChatInputContainer"] {
        background-color: #0E1117 !important;
        padding-bottom: 20px !important
        
