import streamlit as st
from groq import Groq
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Fekra AI",
    page_icon="💡",
    layout="centered"
)

# الستايل النهائي الموحد (إخفاء البياض تماماً + الدخلة الشيك + الستايل النيون)
st.markdown("""
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

    /* تعديل منطقة الكتابة السفلية لمنع البياض */
    [data-testid="stBottom"] {
        background-color: #0E1117 !important;
    }
    
    div[data-testid="stChatInputContainer"] {
        background-color: #0E1117 !important;
        padding: 10px !important;
        border-top: 1px solid #00F2FF22 !important;
    }

    /* شاشة الدخول الشيك */
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

    h1 {
        color: #00F2FF !important;
        text-shadow: 0px 0px 15px #00F2
        
