import streamlit as st
from groq import Groq
from datetime import datetime
import json
import os
from duckduckgo_search import DDGS

# 1. إعدادات الصفحة
st.set_page_config(page_title="Fekra AI", page_icon="💡", layout="centered")

# --- نظام الذاكرة (Memory System) ---
def load_memory():
    if os.path.exists("memory.json"):
        with open("memory.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {"user_name": "يا حريف", "facts": []}

def save_memory(data):
    with open("memory.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

# --- أداة البحث (Search Engine) ---
def web_search(query):
    with DDGS() as ddgs:
        results = [r['body'] for r in ddgs.text(query, max_results=3)]
        return "\n".join(results) if results else "لم أجد نتائج."

# 2. الستايل (بدون أي تغيير في الشكل اللي بتحبه)
st.markdown("""
<style>
    footer {visibility: hidden;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stBottom"] {
        background-color: #0E1117 !important;
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
    #splash {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: #0E1117; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 9999;
        animation: out 2.5s forwards; pointer-events: none;
    }
    @keyframes out { 0%, 80% {opacity: 1;} 100% {opacity: 0; visibility: hidden;} }
    h1 { color: #00F2FF !important; text-shadow: 0 0 15px #00F2FF; text-align: center; }
    .stChatMessage { background: #161B22 !important; border: 1px solid #00F2FF33 !important; border-radius: 15px !important; }
    [data-testid="stChatInput"] textarea { color: #000 !important; background: #FFF !important; }
    p, span, div { color: #FFF !important; }
</style>
<div id="splash">
    <div style="font-size: 50px; color: #00F2FF; text-shadow: 0 0 20px #00F2FF;">💡 FEKRA AI</div>
    <p style="color: #808495 !important; margin-top: 20px;">Designed by Harreef</p>
</div>
""", unsafe_allow_html=True)

# 3. المنطق البرمجي
now = datetime.now()
current_time_info = now.strftime("%A, %d %B %Y | %I:%M %p")

st.title("💡 Fekra AI")
st.markdown(f"<p style='text-align: center; color: #808495 !important;'>أهلاً بك يا {st.session_state.memory['user_name']}</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input(f"بماذا تفكر يا {st.session_state.memory['user_name']}؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            api_key = st.secrets["GROQ_API_KEY"]
            client = Groq(api_key=api_key)
            
            # --- ذكاء البحث والذاكرة ---
            system_prompt = f"""
            أنت Fekra AI، صممك أحمد وائل الحريف. 
            اسم المستخدم الحالي: {st.session_state.memory['user_name']}.
            معلومات محفوظة عن المستخدم: {st.session_state.memory['facts']}.
            الوقت الحالي: {current_time_info}.
            إذا سألك المستخدم عن شيء جديد أو معلومات حالية، ابحث في الإنترنت.
            إذا أخبرك المستخدم باسمه أو معلومة عنه، احفظها بدقة.
            """
            
            # قرار البحث (تلقائي)
            search_data = ""
            if any(word in prompt.lower() for word in ["بث", "search", "اخبار", "مين هو", "سعر", "تاريخ"]):
                with st.status("🔍 جاري البحث في الويب..."):
                    search_data = web_search(prompt)

            full_prompt = f"{prompt}\n\n[نتائج البحث من الويب]:\n{search_data}" if search_data else prompt
            
            history = [{"role": "system", "content": system_prompt}]
            for msg in st.session_state.messages[:-1]:
                history.append(msg)
            history.append({"role": "user", "content": full_prompt})

            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=history, stream=True)
            
            full_res = ""
            placeholder = st.empty()
            for chunk in res:
                if chunk.choices[0].delta.content:
                    full_res += chunk.choices[0].delta.content
                    placeholder.markdown(full_res + "▌")
            placeholder.markdown(full_res)
            
            # --- تحديث الذاكرة تلقائياً ---
            if "اسمي" in prompt or "ناديني" in prompt:
                # محاولة استخراج الاسم (بسيطة)
                new_name = prompt.split()[-1]
                st.session_state.memory["user_name"] = new_name
                save_memory(st.session_state.memory)
            
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            
        except Exception as e:
            st.error(f"Error: {e}")
            
