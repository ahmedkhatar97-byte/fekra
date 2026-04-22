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

# 2. الستايل (إضافة الزر العايم وحل السكرول)
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

    /* زرار التحكم العايم في الجنب */
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

<div class="floating-control" onclick="window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });">
    <span style="color: #0E1117; font-size: 24px; font-weight: bold;">↓</span>
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
            
            if any(x in prompt for x in ["اسمي", "ناديني"]):
                new_n = prompt.split()[-1].strip("!؟.")
                st.session_state.user_name = new_n
                save_mem(new_n)

            s_info = ""
            if any(w in prompt.lower() for w in ["بحث", "اخبار", "سعر", "مين هو"]):
                with DDGS() as ddgs:
                    results = [r['body'] for r in ddgs.text(prompt, max_results=3)]
                    s_info = "\n".join(results)

            sys_p = f"""أنت Fekra AI، صممك أحمد وائل الحريف. 
            تنادي المستخدم بـ: {st.session_state.user_name}. 
            تحدث بلهجة مصرية واضحة، تجنب الرموز الغريبة. 
            الوقت: {current_time_info}."""
            
            history = [{"role": "system", "content": sys_p}] + st.session_state.messages[:-1]
            history.append({"role": "user", "content": f"{prompt}\n\n[Context]: {s_info}"})
            
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=history, stream=True)
            
            full_r = ""
            p_holder = st.empty()
            for chunk in res:
                if chunk.choices[0].delta.content:
                    full_r += chunk.choices[0].delta.content
                    p_holder.markdown(full_r + "▌")
            p_holder.markdown(full_r)
            st.session_state.messages.append({"role": "assistant", "content": full_r})
        except Exception as e:
            st.error(f"Error: {e}")
            
