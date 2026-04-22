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

if "user_name" not in st.session_state:
    st.session_state.user_name = load_mem()["user_name"]

# 2. الاستايل النيون + حل مشكلة السكرول والرموز
st.markdown("""
<style>
    /* إخفاء الزوائد */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* سواد تام ومنع الـ Restart عند الشد */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0E1117 !important;
        overscroll-behavior-y: none !important;
    }

    /* جعل الشات قابل للسكرول بحرية */
    [data-testid="stMainViewContainer"] {
        overflow-y: auto !important;
    }

    /* ستايل الشات النيون الأصلي */
    h1 { color: #00F2FF !important; text-shadow: 0 0 15px #00F2FF; text-align: center; }
    .stChatMessage { background: #161B22 !important; border: 1px solid #00F2FF33 !important; border-radius: 15px !important; box-shadow: 0 0 10px #00F2FF11; }
    
    /* نسف السطر الأبيض */
    div[data-testid="stChatInputContainer"] {
        background-color: #0E1117 !important;
        border: none !important;
    }
    
    /* زرار الصعود للأعلى (تصميم نيون مطور) */
    .up-btn {
        position: fixed;
        right: 25px;
        bottom: 120px;
        width: 50px;
        height: 50px;
        background: transparent;
        border: 2px solid #00F2FF;
        border-radius: 50%;
        color: #00F2FF;
        text-shadow: 0 0 5px #00F2FF;
        box-shadow: 0 0 10px #00F2FF, inset 0 0 5px #00F2FF;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 999999;
        text-decoration: none !important;
        font-size: 24px;
        font-weight: bold;
    }

    /* شاشة الدخول */
    #splash {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: #0E1117; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 9999;
        animation: out 2.2s forwards; pointer-events: none;
    }
    @keyframes out { 0%, 80% {opacity: 1;} 100% {opacity: 0; visibility: hidden;} }
    
    p, span, div { color: #FFF !important; }
</style>

<div id="splash">
    <div style="font-size: 50px; color: #00F2FF; text-shadow: 0 0 20px #00F2FF;">💡 FEKRA AI</div>
    <p style="color: #808495 !important; margin-top: 10px;">Designed by Harreef</p>
</div>

<div id="top"></div>
<a href="#top" class="up-btn">↑</a>
""", unsafe_allow_html=True)

# 3. المنطق البرمجي والوقت
now = datetime.now()
current_time_info = now.strftime("%A, %d %B %Y | %I:%M %p")

st.title("💡 Fekra AI")
st.markdown("<p style='text-align: center; color: #808495 !important;'>نسخة الحريف | ذكاء بلا حدود</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# إدخال المستخدم والرد
if prompt := st.chat_input("بماذا تفكر يا حريف؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            # محرك البحث
            s_info = ""
            if any(w in prompt.lower() for w in ["بحث", "اخبار", "سعر", "مين هو"]):
                with DDGS() as ddgs:
                    results = [r['body'] for r in ddgs.text(prompt, max_results=3)]
                    s_info = "\n".join(results)

            # الح
            
