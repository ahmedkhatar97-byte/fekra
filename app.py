import streamlit as st
from groq import Groq
from datetime import datetime
import json
import os
from duckduckgo_search import DDGS

# 1. إعدادات الصفحة
st.set_page_config(page_title="Fekra AI", page_icon="💡", layout="centered")

# --- نظام الذاكرة المستديمة (المتطور) ---
def load_memory():
    if os.path.exists("memory.json"):
        try:
            with open("memory.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"user_name": "يا حريف", "facts": []}

def save_memory(data):
    with open("memory.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

# --- محرك البحث ---
def web_search(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n".join(results) if results else ""
    except: return ""

# 2. الستايل (حل مشكلة الـ Scroll والـ Restart)
st.markdown("""
<style>
    footer {visibility: hidden;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* تثبيت الخلفية وسواد تام */
    .stApp {
        background-color: #0E1117 !important;
    }

    /* حل مشكلة السكرول: جعل منطقة الرسائل قابلة للتحريك بسلاسة */
    [data-testid="stMainViewContainer"] {
        overflow-y: auto !important;
    }

    /* تثبيت مستطيل الكتابة تحت تماماً */
    div[data-testid="stBottom"] {
        background-color: #0E1117 !important;
    }

    div[data-testid="stChatInputContainer"] {
        background-color: #161B22 !important;
        border: 1px solid #00F2FF44 !important;
        border-radius: 15px !important;
        margin-bottom: 20px !important;
    }

    /* شاشة الدخول */
    #splash {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: #0E1117; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 9999;
        animation: out 2.5s forwards; pointer-events: none;
    }
    @keyframes out { 0%, 80% {opacity: 1;} 100% {opacity: 0; visibility: hidden;} }
    
    h1 { color: #00F2FF !important; text-shadow: 0 0 15px #00F2FF; text-align: center; }
    .stChatMessage { background: #161B22 !important; border: 1px solid #00F2FF22 !important; border-radius: 15px !important; margin-bottom: 10px !important; }
    [data-testid="stChatInput"] textarea { color: #FFFFFF !important; background: transparent !important; }
    p, span, div { color: #FFF !important; }
</style>
<div id="splash">
    <div style="font-size: 50px; color: #00F2FF; text-shadow: 0 0 20px #00F2FF;">💡 FEKRA AI</div>
    <p style="color: #808495 !important; margin-top: 20px;">Designed by Harreef</p>
</div>
""", unsafe_allow_html=True)

# 3. المنطق البرمجي
now = datetime.now()
current_time_info = now.strftime("%I:%M %p")

st.title("💡 Fekra AI")
st.markdown(f"<p style='text-align: center; color: #808495 !important;'>نسخة الحريف | ذكاء بلا حدود</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# إدخال المستخدم
if prompt := st.chat_input("بماذا تفكر يا حريف؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            # الهوية الصارمة
            system_prompt = f"""
            أنت Fekra AI، مساعد ذكي صممه أحمد وائل الحريف. 
            أنت الآن تخاطب: {st.session_state.memory['user_name']}.
            تحدث دائماً بلهجة مصرية ذكية.
            إذا عرف المستخدم نفسه، احفظ الاسم فوراً.
            """
            
            search_data = ""
            if any(word in prompt.lower() for word in ["بث", "search", "اخبار", "سعر", "مين هو"]):
                with st.spinner("🔍 Fekra AI يبحث الآن..."):
                    search_data = web_search(prompt)

            history = [{"role": "system", "content": system_prompt}] + st.session_state.messages[:-1]
            final_input = f"{prompt}\n\n[Context]: {search_data}" if search_data else prompt
            history.append({"role": "user", "content": final_input})

            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=history, stream=True)
            
            full_res = ""
            placeholder = st.empty()
            for chunk in res:
                if chunk.choices[0].delta.content:
                    full_res += chunk.choices[0].delta.content
                    placeholder.markdown(full_res + "▌")
            placeholder.markdown(full_res)
            
            # تحديث الاسم بذكاء
            if "اسمي" in prompt or "ناديني" in prompt:
                name_found = prompt.replace("اسمي", "").replace("ناديني", "").replace("بـ", "").strip()
                if name_found:
                    st.session_state.memory["user_name"] = name_found
                    save_memory(st.session_state.memory)
            
            st.session_state.messages.append({"role": "assistant", "content": full_res})
        except Exception as e:
            st.error(f"Error: {e}")
            
