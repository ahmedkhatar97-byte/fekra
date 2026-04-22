import streamlit as st
from groq import Groq
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Fekra AI", page_icon="💡", layout="centered")

# 2. الستايل (نسف البياض + تحويل الفقاعة للسواد النيون)
st.markdown("""
<style>
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* توحيد الخلفية السوداء */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stBottom"] {
        background-color: #0E1117 !important;
    }

    /* تحويل فقاعة الكتابة للسواد مع إطار نيون */
    div[data-testid="stChatInputContainer"] {
        background-color: #0E1117 !important;
        border-top: 1px solid #00F2FF22 !important;
    }

    [data-testid="stChatInput"] {
        background-color: #161B22 !important;
        border: 1px solid #00F2FF44 !important;
        border-radius: 10px !important;
    }

    /* تغيير لون نص الكتابة للأبيض داخل الفقاعة السوداء */
    [data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
        background-color: #161B22 !important;
        caret-color: #00F2FF !important;
    }

    /* شاشة الدخول */
    #splash {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: #0E1117; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 9999;
        animation: out 2.5s forwards; pointer-events: none;
    }
    @keyframes out { 0%, 80% {opacity: 1;} 100% {opacity: 0; visibility: hidden;} }
    
    /* ستايل الرسايل */
    h1 { color: #00F2FF !important; text-shadow: 0 0 15px #00F2FF; text-align: center; }
    .stChatMessage { background: #161B22 !important; border: 1px solid #00F2FF33 !important; border-radius: 15px !important; }
    p, span, div { color: #FFF !important; }
</style>
<div id="splash">
    <div style="font-size: 50px; color: #00F2FF; text-shadow: 0 0 20px #00F2FF;">💡 FEKRA AI</div>
    <p style="color: #808495 !important; margin-top: 20px;">Designed by Harreef</p>
</div>
""", unsafe_allow_html=True)

# 3. المنطق والوقت
now = datetime.now()
current_time_info = now.strftime("%A, %d %B %Y | %I:%M %p")

st.title("💡 Fekra AI")
st.markdown("<p style='text-align: center; color: #808495 !important;'>نسخة الحريف | ذكاء بلا حدود</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("بماذا تفكر يا حريف؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            api_key = st.secrets["GROQ_API_KEY"]
            client = Groq(api_key=api_key)
            history = [{"role": "system", "content": f"أنت Fekra AI، صممك أحمد وائل الحريف. الوقت: {current_time_info}."}] + st.session_state.messages
            
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
            
