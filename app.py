import streamlit as st
from groq import Groq
from datetime import datetime

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="Fekra AI",
    page_icon="💡",
    layout="centered"
)

# 2. الستايل النهائي (حل مشكلة البياض + الدخلة الشيك)
st.markdown("""
<style>
    /* إخفاء أدوات ستريم ليت */
    footer {visibility: hidden; height: 0%;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    [data-testid="stStatusWidget"] {visibility: hidden;}

    /* توحيد الخلفية السوداء */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0E1117 !important;
    }

    /* القضاء على البياض في أسفل الشاشة تماماً */
    [data-testid="stBottom"] {
        background-color: #0E1117 !important;
    }
    
    div[data-testid="stChatInputContainer"] {
        background-color: #0E1117 !important;
        padding: 10px !important;
        border-top: 1px solid #00F2FF22 !important;
    }

    /* شاشة الدخول (Splash Screen) */
    #splash-screen {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: #0E1117;
        display: flex; flex-direction: column;
        justify-content: center; align-items: center;
        z-index: 9999;
        animation: fadeOut 2.5s forwards;
        pointer-events: none;
    }

    .splash-logo {
        font-size: 50px;
        color: #00F2FF;
        text-shadow: 0 0 20px #00F2FF;
        font-family: 'Segoe UI', sans-serif;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(1); opacity: 0.8; }
    }

    @keyframes fadeOut {
        0% { opacity: 1; }
        80% { opacity: 1; }
        100% { opacity: 0; visibility: hidden; }
    }

    /* ستايل الشات */
    h1 {
        color: #00F2FF !important;
        text-shadow: 0px 0px 15px #00F2FF;
        text-align: center;
    }

    .stChatMessage {
        background-color: #161B22 !important;
        border: 1px solid #00F2FF33 !important;
        border-radius: 15px !important;
    }

    /* مستطيل الكتابة */
    [data-testid="stChatInput"] textarea {
        color: #000000 !important;
        background-color: #FFFFFF !important;
        caret-color: #000000 !important;
    }
    
    p, span, div, label { color: #FFFFFF !important; font-weight: 500; }
</style>

<div id="splash-screen">
    <div class="splash-logo">💡 FEKRA AI</div>
    <p style="color: #808495 !important; margin-top: 20px;">Designed by Harreef</p>
</div>
""", unsafe_allow_html=True)

# تحضير معلومات الوقت
now = datetime.now()
current_time_info = now.strftime("%A, %d %B %Y | %I:%M %p")

st.title("💡 Fekra AI")
st.markdown("<p style='text-align: center; color: #808495 !important;'>نسخة الحريف الشاملة | ذكاء بلا حدود</p>", unsafe_allow_html=True)

# التحقق من الـ API Key
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api
    
