import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة وواجهة المستخدم (UI Customization)
st.set_page_config(
    page_title="Fekra AI",
    page_icon="💡",
    layout="centered"
)

# ستايل احترافي عشان الواجهة تليق على اللوجو
st.markdown("""
    <style>
    /* تغيير لون الخلفية الأساسية */
    .stApp {
        background-color: #0E1117;
    }
    
    /* ستايل لعنوان الصفحة */
    h1 {
        color: #00F2FF; /* لون نيوني زي اللوجو */
        text-shadow: 0px 0px 10px #00F2FF;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* ستايل فقاعات الدردشة */
    .stChatMessage {
        background-color: #1A1C24;
        border: 1px solid #00F2FF33;
        border-radius: 20px;
        color: white;
    }

    /* ستايل منطقة الإدخال */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    
    /* تحسين شكل النصوص المساعدة */
    .stCaption {
        color: #808495;
    }
    </style>
    """, unsafe_allow_html=True)

# عرض اللوجو في نص الصفحة (اختياري لو عايز ترفعه على GitHub وتحط اللينك)
# st.image("path_to_your_logo.png", width=100)

st.title("💡 Fekra AI")
st.caption("نسخة الحريف الشاملة | المستقبل يبدأ هنا")

# 2. جلب مفتاح الـ API
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("تأكد من إضافة GROQ_API_KEY!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 3. تهيئة الذاكرة والدستور
if "messages" not in st.session_state:
    st.session_state.messages = []

system_identity = """
أنت فكرة AI (Fekra AI)، مساعد ذكي طوره أحمد وائل الحريف.
ردودك يجب أن تكون ذكية، سريعة، وبأسلوب عصري يليق بواجهتك النيونية.
(طبق كل القواعد السابقة بخصوص الهوية والتخصصات الـ 10).
"""

# 4. عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة الشات
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
            
