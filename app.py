import streamlit as st
from groq import Groq
from datetime import datetime
import json
import os
from duckduckgo_search import DDGS

# 1. إعدادات الصفحة
st.set_page_config(page_title="Fekra AI", page_icon="💡", layout="centered")

# --- نظام الذاكرة الآمن ---
def load_mem():
    if os.path.exists("memory.json"):
        try:
            with open("memory.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"user_name": "يا حريف"}

def save_mem(name):
    with open("memory.json", "w", encoding="utf-8") as f:
        json.dump({"user_name": name}, f, ensure_ascii=False)

if "user_name" not in st.session_state:
    st.session_state.user_name = load_mem()["user_name"]

# 2. الستايل (تعديل زر الصعود لأعلى)
st.markdown("""
<style>
    footer {visibility: hidden;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0E1117 !important;
        overscroll-behavior-y: none !important;
    }

    [data-testid="stMainViewContainer"] {
        overflow-y: auto !important;
    }

    div[data-testid="stChatInputContainer"] {
        background-color: #0E1117 !important;
        border: none !important;
        padding: 15px !important;
    }
    
    [data-testid="stBottomBlockContainer"] {
        background-color: #0E1117 !important;
        border: none !important;
    }

    /* زرار الصعود للأعلى النيون */
    .floating-control {
        position: fixed;
        right: 20px;
        bottom: 100px;
        width: 50px;
        height: 50px;
        background: #00F2FF;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0 0 15px #00F2FF;
        cursor: pointer;
        z-index: 10000;
        transition: 0.3s;
    }
    .floating-control:hover { transform: scale(1.1); }

    #splash {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: #0E1117; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 9999;
        animation: out 2.5s forwards; pointer-events: none;
    }
    @keyframes out { 0%, 80% {opacity: 1;} 100% {opacity: 0; visibility: hidden;} }
    
    h1 { color: #00F2FF !important; text-shadow: 0 0 15px #00F2FF; text-align: center; }
    .stChatMessage { background: #161B22 !important; border: 1px solid #00F2FF33 !important; border-radius: 15px !important; }
    
    [data-testid="stChatInput"] textarea { color: #FFFFFF !important; background: #161B22 !important; }
    p, span, div { color: #FFF !important; }
</style>

<div class="floating-control" onclick="window.scrollTo({ top: 0, behavior: 'smooth' });">
    <span style="color: #0E1117; font-size: 24px; font-weight: bold;">↑</span>
</div>

<div id="splash">
    <div style="font-size: 50px; color: #00F2FF; text-shadow: 0 0 20px #00F2FF;">💡 FEKRA AI</div>
    <p style="color: #808495 !important; margin-top: 20px;">Designed by Harreef</p>
</div>
""", unsafe_allow_html=True)

# 3. المنطق البرمجي
now = datetime.now()
current_time_info = now.strftime("%A, %d %B %Y | %I:%M %p")

st.title("💡 Fekra AI")
st.markdown("<p style='text-align: center; color: #808495 !important;'>نسخة الحريف | ذكاء بلا حدود</p
            
