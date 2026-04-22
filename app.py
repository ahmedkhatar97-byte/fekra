import streamlit as st
from groq import Groq
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Fekra AI",
    page_icon="💡",
    layout="centered"
)

# الستايل النهائي الموحد (إخفاء البياض تماماً + الدخلة الشيك + الستايل النيون)
st.markdown("""
    <style>
    /* إخفاء إضافات ستريم ليت */
    footer {visibility: hidden; height: 0%;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    [data-testid="stStatusWidget"] {visibility: hidden;}

    /* توحيد لون الخلفية في كل مكان */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0E1117 !important;
    }

    /* 2. تعديل منطقة الكتابة السفلية (نهاية البياض) */
    [data-testid="stBottom"] {
        background-color: #0E1117 !important;
    }
    
    div[data-testid="stChatInputContainer"] {
        background-color: #0E1117 !important;
        padding: 10px !important;
        border-top: 1px solid #00F2FF22 !important; /* خط نيون خفيف جداً */
    }

    /* ستايل شاشة الدخول الشيك */
    #splash-screen {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: #0E1117;
        display: flex; flex-direction: column;
        justify-content: center; align-items: center;
        z-index: 9999;
        animation: fadeOut 2.5s forwards;
        pointer-events: none;
    }

    .splash-logo {
        font-size: 50px;
        color: #00F2FF;
        text-shadow: 0 0 20px #00F2FF;
        font-family: 'Segoe UI', sans-serif;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(1); opacity: 0.8; }
    }

    @keyframes fadeOut {
        0% { opacity: 1; }
        80% { opacity: 1; }
        100% { opacity: 0; visibility: hidden; }
    }

    /* ستايل العناوين والشات */
    h1 {
        color: #00F2FF !important;
        text-shadow: 0px 0px 15px #00F2FF;
        text-align: center;
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
    
    p, span, div, label { color: #FFFFFF !important; font-weight: 500; }
    </style>

    <div id="splash-screen">
        <div class="splash-logo">💡 FEKRA AI</div>
        <p style="color: #808495 !important; margin-top: 20px;">Designed by Harreef</p>
    </div>
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

# الدستور الذكي
system_identity = f"أنت فكرة AI (Fekra AI)، مساعد ذكي ومبتكر طوره أحمد وائل الحريف. معلومات الوقت الآن: {current_time_info}. لا تذكر الوقت إلا لو سألك المستخدم عنه."

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
            
