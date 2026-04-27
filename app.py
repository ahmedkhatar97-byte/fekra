import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Fekra AI",
    page_icon="💡",
    layout="centered"
)

# الستايل النيون (Ultra Clean) - إخفاء كل براندات استريمليت والحواف البيضاء
st.markdown(r"""
    <style>
    /* 1. إخفاء زوائد استريمليت */
    footer {visibility: hidden; height: 0%;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important; display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {visibility: hidden; display: none !important;}
    .stDeployButton {display:none !important;}

    /* 2. توحيد الخلفية السودة في كل مكان */
    [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"], 
    [data-testid="stMainViewContainer"],
    [data-testid="stBottom"],
    [data-testid="stBottomBlockContainer"] {
        background-color: #0E1117 !important;
    }
    
    /* 3. نصوص واضحة نيون */
    p, span, div, label {
        color: #FFFFFF !important;
        font-weight: 500;
    }

    /* 4. العنوان النيوني */
    h1 {
        color: #00F2FF !important;
        text-shadow: 0px 0px 15px #00F2FF;
        text-align: center;
        margin-top: -50px;
    }

    /* 5. فقاعات الدردشة النيون */
    .stChatMessage {
        background-color: #161B22 !important;
        border: 1px solid #00F2FF33 !important;
        border-radius: 15px !important;
        box-shadow: 0 0 10px #00F2FF11;
    }

    /* 6. إخفاء حاوية الإدخال البيضاء تماماً */
    div[data-testid="stChatInputContainer"] {
        background-color: transparent !important;
        border: none !important;
        padding: 10px 0px !important;
    }

    /* 7. ستايل مستطيل الكتابة النيون */
    [data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
        background-color: #161B22 !important;
        border: 1px solid #00F2FF33 !important;
        border-radius: 20px !important;
        caret-color: #00F2FF !important;
        box-shadow: 0 0 15px #00F2FF22 !important;
    }
    
    [data-testid="stChatInput"] button {
        color: #00F2FF !important;
        background-color: transparent !important;
    }

    /* 8. الشاشة الافتتاحية (Splash Screen) */
    #splash-screen {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #0E1117;
        display: flex; flex-direction: column;
        justify-content: center; align-items: center;
        z-index: 9999;
        animation: fadeOut 2.5s forwards;
        pointer-events: none;
    }

    @keyframes fadeOut {
        0% { opacity: 1; }
        85% { opacity: 1; }
        100% { opacity: 0; visibility: hidden; }
    }

    .neon-text {
        font-size: 50px;
        color: #00F2FF;
        text-shadow: 0 0 20px #00F2FF, 0 0 40px #00F2FF;
        font-family: 'Segoe UI', sans-serif;
        font-weight: bold;
    }
    </style>

    <div id="splash-screen">
        <div class="neon-text">💡 FEKRA AI</div>
        <p style="margin-top: 15px; color: #808495 !important; font-size: 18px;">Created by Al-Hareef</p>
    </div>
    """, unsafe_allow_html=True)

st.title("💡 Fekra AI")
st.markdown("<p style='text-align: center; color: #808495 !important;'>نسخة الحريف الشاملة | ذكاء بلا حدود</p>", unsafe_allow_html=True)

# 2. جلب مفتاح الـ API
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("تأكد من إضافة GROQ_API_KEY في Secrets!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 3. تهيئة الذاكرة والدستور الصارم جداً
if "messages" not in st.session_state:
    st.session_state.messages = []

# تحديث الدستور لضمان نظافة المخرجات
system_identity = """
أنت فكرة AI (Fekra AI)، المساعد الذكي والمبتكر الذي طوره المبرمج أحمد وائل (الحريف).
قواعد العمل الإلزامية:
1. اللغة الأساسية: اللهجة المصرية المفهومة "الحريفة".
2. ممنوعات لغوية: يمنع منعاً باتاً استخدام أي رموز صينية، يابانية، أو رموز غريبة غير مفهومة.
3. دقة الإملاء: يجب أن تكون الإجابات خالية تماماً من الأخطاء الإملائية وال
