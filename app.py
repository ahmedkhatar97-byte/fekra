import streamlit as st
from groq import Groq
from datetime import datetime
import json
import os
from duckduckgo_search import DDGS

# 1. إعدادات الصفحة
st.set_page_config(page_title="Fekra AI", page_icon="💡", layout="centered")

# --- نظام الذاكرة المستديمة (مخفي وآمن) ---
def get_memory():
    if os.path.exists("memory.json"):
        try:
            with open("memory.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"user_name": "يا حريف"}

def save_memory(name):
    with open("memory.json", "w", encoding="utf-8") as f:
        json.dump({"user_name": name}, f, ensure_ascii=False)

if "user_name" not in st.session_state:
    st.session_state.user_name = get_memory()["user_name"]

# 2. الستايل (حل نهائي للسكرول والـ Restart)
st.markdown("""
<style>
    footer {visibility: hidden;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* منع الـ Rerun عند السحب (Scroll) */
    .main { overflow: auto !important; }
    
    .stApp { background-color: #0E1117 !important; }

    /* تثبيت مستطيل الكتابة ومنع تداخل السكرول */
    div[data-testid="stBottom"] {
        background-color: #0E1117 !important;
        position: fixed;
        bottom: 0;
    }

    /* ستايل فقاعة الكتابة (سودة نيون) */
    div[data-testid="stChatInputContainer"] {
        background-color: #161B22 !important;
        border: 1px solid #00F2FF44 !important;
        border-radius: 15px !important;
    }

    /* شاشة الدخول */
    #splash {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: #0E1117; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 9999;
        animation: out 2.2s forwards; pointer-events: none;
    }
    @keyframes out { 0%, 80% {opacity: 1;} 100% {opacity: 0; visibility: hidden;} }
    
    h1 { color: #00F2FF !important; text-shadow: 0 0 15px #00F2FF; text-align: center; }
    .stChatMessage { background: #161B22 !important; border: 1px solid #00F2FF22 !important; border-radius: 15px !important; }
    [data-testid="stChatInput"] textarea { color: #FFFFFF !important; background: transparent !important; }
    p, span, div { color: #FFF !important; }
</style>
<div id="splash">
    <div style="font-size: 50px; color: #00F2FF; text-shadow: 0 0 20px #00F2FF;">💡 FEKRA AI</div>
    <p style="color: #808495 !important; margin-top: 20px;">Designed by Harreef</p>
</div>
""", unsafe_allow_html=True)

# 3. المنطق البرمجي
st.title("💡 Fekra AI")
st.markdown("<p style='text-align: center; color: #808495 !important;'>نسخة الحريف | ذكاء بلا حدود</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الشات
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# الإدخال
if prompt := st.chat_input("بماذا تفكر يا حريف؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            # معالجة الاسم بذكاء بدون "هبل"
            if "اسمي" in prompt or "ناديني" in prompt:
                new_name = prompt.split()[-1].strip("؟!.")
                st.session_state.user_name = new_name
                save_memory(new_name)

            # محرك البحث التلقائي
            search_context = ""
            if any(x in prompt.lower() for x in ["بحث", "اخبار", "مين هو", "سعر"]):
                with DDGS() as ddgs:
                    results = [r['body'] for r in ddgs.text(prompt, max_results=3)]
                    search_context = "\n".join(results)

            system_msg = f"أنت Fekra AI، صممك أحمد وائل الحريف. تنادي المستخدم بـ: {st.session_state.user_name}. تتحدث بالمصرية."
            history = [{"role": "system", "content": system_msg}] + st.session_state.messages[:-1]
            history.append({"role": "user", "content": f"{prompt}\n\n[Search]: {search_context}"})

            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=history, stream=True)
            
            full_res = ""
            placeholder = st.empty()
            for chunk in res:
                if chunk.choices[0].delta.content:
                    full_res += chunk.choices[0].delta.content
                    placeholder.markdown(full_res + "▌")
            placeholder.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
        except Exception as e:
            st.error(f"Error: {e}")
            
