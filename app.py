import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Fekra AI",
    page_icon="💡",
    layout="centered"
)

# الستايل النيون (Final Version) - إبادة اللون الأبيض تماماً من الأسفل
st.markdown(r"""
    <style>
    /* 1. إخفاء الزوائد والاسبينر */
    footer {visibility: hidden; height: 0%;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    [data-testid="stStatusWidget"] {visibility: hidden; display: none !important;}

    /* 2. توحيد الخلفية السودة في كل مكان */
    [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"], 
    [data-testid="stMainViewContainer"],
    [data-testid="stBottom"] {
        background-color: #0E1117 !important;
    }
    
    /* 3. الحل السحري لإخفاء المستطيل الأبيض الكبير اللي ورا الشات */
    div[data-testid="stBottomBlockContainer"] {
        background-color: transparent !important;
    }

    /* 4. جعل النصوص واضحة باللون الأبيض */
    p, span, div, label {
        color: #FFFFFF !important;
        font-weight: 500;
    }

    /* 5. ستايل العنوان النيوني */
    h1 {
        color: #00F2FF !important;
        text-shadow: 0px 0px 15px #00F2FF;
        text-align: center;
        margin-top: -50px;
    }

    /* 6. فقاعات الدردشة */
    .stChatMessage {
        background-color: #161B22 !important;
        border: 1px solid #00F2FF33 !important;
        border-radius: 15px !important;
        box-shadow: 0 0 10px #00F2FF11;
    }

    /* 7. تظبيط مستطيل الكتابة النيون وإلغاء أي حواف بيضاء */
    div[data-testid="stChatInputContainer"] {
        background-color: transparent !important;
        border: none !important;
        padding: 10px 0px !important;
    }

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

    /* 8. الشاشة الافتتاحية النيون */
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
    st.error("يا حريف، ضيف مفتاح الـ API في الـ Secrets الأول!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 3. تهيئة الذاكرة والدستور الصارم
if "messages" not in st.session_state:
    st.session_state.messages = []

# الدستور لمنع الصيني والرموز وضمان جودة الإملاء
system_identity = """
أنت فكرة AI (Fekra AI)، المساعد الذكي والمبتكر الذي طوره المبرمج أحمد وائل (الحريف).
قواعد صارمة:
1. اللغة: تحدث بلهجة مصرية واضحة وذكية تناسب شخصية الحريف.
2. الجودة: ممنوع استخدام أي حروف صينية أو يابانية أو رموز غريبة.
3. الإملاء: اكتب لغة عربية سليمة إملائياً بدون أخطاء.
4. الهوية: إذا سُئلت، أنت "فكرة AI" من تطوير أحمد وائل الحريف.
"""

# 4. عرض رسائل الدردشة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة الإدخال والرد
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
            st.error(f"حصلت مشكلة فنية يا حريف: {str(e)}")
            
