import streamlit as st
import streamlit.components.v1 as components
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

# 2. الستايل وحل مشكلة السكرول والرموز
st.markdown("""
<style>
    footer {visibility: hidden;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* سواد تام ومنع الـ Pull-to-refresh */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0E1117 !important;
        overscroll-behavior-y: none !important;
    }

    [data-testid="stMainViewContainer"] {
        overflow-y: auto !important;
    }

    /* نسف السطر الأبيض */
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
    .scroll-btn {
        position: fixed;
        right: 20px;
        bottom: 110px;
        width: 50px;
        height: 50px;
        background: #00F2FF;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0 0 15px #00F2FF;
        cursor: pointer;
        z-index: 999999;
        border: none;
        color: #0E1117;
        font-size: 24px;
        font-weight: bold;
    }

    /* شاشة الدخول */
    #splash {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        
