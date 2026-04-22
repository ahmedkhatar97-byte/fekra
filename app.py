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
    h1 { color: #00F2FF !important; text-shadow: 0 0 15px #00F2
    
