import streamlit as st
from groq import Groq
from datetime import datetime

# 1. إعدادات الصفحة وواجهة المستخدم (UI/UX)
st.set_page_config(
    page_title="Fekra AI",
    page_icon="💡",
    layout="centered"
)

# الستايل اللي حفظناه (إخفاء الإعلانات + ضبط الألوان + وضوح الكتابة)
st.markdown("""
    <style>
    footer {visibility: hidden; height: 0%;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    [data-testid="stStatusWidget"] {visibility: hidden;}

    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0E1117 !important;
    }
    
    p, span, div, label {
        color: #FFFFFF !important;
        font-weight: 500;
    }

    h1 {
        color: #00F2FF !important;
        text-shadow: 0px 0px 15px #00F2FF;
        font-family: 'Segoe UI', sans-serif;
        text-align: center;
        margin-top: -50px;
    }

    .stChatMessage {
        background-color: #161B22 !important;
        border: 1px solid #00F2FF33 !important;
        border-radius: 15px !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #000000 !important;
        background-color: #FFFFFF !important;
        caret-color: #000000 !important;
    }
    
    [data-testid="stChatInput"] button {
        color: #00F2FF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# تحضير الوقت والتاريخ
now = datetime.now()
current_time_info = now.strftime("%A, %d %B %Y | %I:%M %p")

st.title("💡 Fekra AI")
st.markdown("<p style='text-align: center; color: #808495 !important;'>نسخة الحريف الشاملة | ذكاء بلا حدود</p>", unsafe_allow_html=True)

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("تأكد من إضافة GROQ_API_KEY في Secrets!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# الدستور الذكي: يعرف المعلومة ويستخدمها عند الحاجة فقط (تم إصلاح الأقواس)
system_identity = f"أنت فكرة AI (Fekra AI)، مساعد ذكي ومبتكر طوره أحمد وائل الحريف. معلومات الوقت الآن: {current_time_info}. لا تذكر الوقت إلا لو سألك المستخدم عنه. اسمك هو Fekra AI."

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("بماذا تفكر يا حريف؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            messages_to_send = [{"role": "system", "content": system_identity}] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile", 
                messages=messages_to_send,
                stream=True,
            )

            for chunk in completion:
                content = chunk.choices[0].delta.content
                if content:
                    full_response += str(content)
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"حدث خطأ يا حريف: {str(e)}")
            
