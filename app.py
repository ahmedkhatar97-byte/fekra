import streamlit as st
from groq import Groq
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Fekra AI", page_icon="💡", layout="centered")

# 2. الستايل القاتل للبياض (استهداف شامل)
st.markdown("""
<style>
    /* إخفاء إضافات ستريم ليت */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* توحيد السواد في كل مكان */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stBottom"] {
        background-color: #0E1117 !important;
    }

    /* نسف السطر الأبيض تماماً */
    div[data-testid="stChatInputContainer"] {
        background-color: #0E1117 !important;
        border: none !important;
        padding: 15px !important;
    }
    
    /* ضمان سواد الحاوية السفلية */
    [data-testid="stBottomBlockContainer"] {
        background-color: #0E1117 !important;
        border: none !important;
    }

    /* شاشة الدخول */
    #splash {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: #0E1117; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 9999;
        animation: out 2.5s forwards; pointer-events: none;
    }
    @keyframes out { 0%, 80% {opacity: 1;} 100% {opacity: 0; visibility: hidden;} }
    
    /* ستايل الشات */
    h1 { color: #00F2FF !important; text-shadow: 0 0 15
