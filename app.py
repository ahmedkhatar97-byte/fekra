import streamlit as st
from groq import Groq
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Fekra AI", page_icon="💡", layout="centered")

# 2. الستايل المطور (سواد تام + تثبيت الشات)
st.markdown("""
<style>
    /* إخفاء الزيادات */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* توحيد السواد */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stBottom"] {
        background-color: #0E1117 !important;
    }

    /* تحويل منطقة الشات لمنطقة قابلة للتمرير بسلاسة */
    .stChatMessageContainer {
        padding-bottom: 100px !important;
    }

    /* فقاعة الكتابة السوداء النيون */
    div[data-testid="stChatInputContainer"] {
        background-color: #0E1117 !important;
        border-top: 1px solid #00F2FF22 !important;
        position: fixed;
        bottom: 0;
        z-index: 100;
    }

    [data-testid="stChatInput"] {
        background-color: #161B22 !important;
        border: 1px solid #00F2FF44 !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
    }

    /* منع الـ Restart عند السكرول */
    html {
        scroll-behavior: smooth;
    }
</style>
""", unsafe_allow_html=True)

# 3. المنطق (الذاكرة المؤقتة)
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض اللوجو والترحيب
st.markdown("<h1 style='text-align: center; color: #00F2FF;'>💡 FEKRA AI</h1>", unsafe_allow_html=True)

# عرض المحادثة (الآن مستقرة أكثر)
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# استقبال الرسائل
if prompt := st.chat_input("بماذا تفكر يا حريف؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            # بناء الهوية (السيستم برومبت)
            now = datetime.now().strftime("%I:%M %p")
            history = [{"role": "system", "content": f"أنت Fekra AI، مساعد ذكي صممه أحمد وائل الحريف. الوقت الآن {now}."}] + st.session_state.messages
            
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
            st.error(f"حدث خطأ يا حريف: {e}")
            
