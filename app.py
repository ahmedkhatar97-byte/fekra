import streamlit as st
from groq import Groq
from datetime import datetime

# 1. إعدادات الصفحة والستايل المتكامل (UI Dark Neon)
st.set_page_config(
    page_title="Fekra AI",
    page_icon="💡",
    layout="centered"
)

# ستايل احترافي: إخفاء الإعلانات + فقاعات نيون + منطقة كتابة سودة
st.markdown("""
    <style>
    /* إخفاء إعلانات Streamlit والفوتر */
    footer {display: none !important;}
    header {display: none !important;}
    #MainMenu {visibility: hidden;}

    /* ضبط الخلفية الداكنة للتطبيق بالكامل */
    [data-testid="stAppViewContainer"] {
        background-color: #0E1117 !important;
    }

    /* العنوان النيوني */
    h1 {
        color: #00F2FF !important;
        text-shadow: 0px 0px 15px #00F2FF;
        text-align: center;
    }

    /* 🔥 تنسيق فقاعات الكلام لتكون بأسلوب النيون */
    [data-testid="stChatMessage"] {
        background-color: #161B22 !important; /* لون داكن للفقاعة */
        border: 1px solid #00F2FF33 !important; /* حدود نيون خفيفة جداً */
        border-radius: 15px !important;
        margin-bottom: 10px !important;
        padding: 15px !important;
    }

    /* تمييز فقاعة المساعد بظل نيون خفيف */
    [data-testid="stChatMessageAssistant"] {
        border: 1px solid #00F2FF66 !important;
        box-shadow: 0px 0px 10px #00F2FF11;
    }

    /* جعل النصوص واضحة جداً داخل الفقاعات */
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] span {
        color: #FFFFFF !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
    }

    /* ضبط منطقة الكتابة */
    [data-testid="stChatInput"] {
        background-color: transparent !important;
    }
    [data-testid="stChatInput"] textarea {
        background-color: #161B22 !important;
        color: #FFFFFF !important;
        border: 1px solid #00F2FF44 !important;
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# معرفة الوقت والتاريخ الحالي
now = datetime.now()
current_time_info = now.strftime("%A, %d %B %Y | %I:%M %p")

st.title("💡 Fekra AI")

# 2. إعداد الـ API
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("تأكد من إضافة GROQ_API_KEY في Secrets!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. دستور الموديل
system_identity = f"""
أنت فكرة AI (Fekra AI)، المساعد الذكي الذي طوره أحمد وائل الحريف.
اسمك هو "Fekra AI".
الوقت والتاريخ الحالي: {current_time_info}.
أجب بذكاء وسرعة وبأسلوب يليق بواجهتك العصرية.
"""

# 4. عرض الرسائل بالستايل الجديد
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة الإدخال
if prompt := st.chat_input("بماذا تفكر يا حريف؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
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
        
