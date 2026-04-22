import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة والستايل المتكامل (UI Dark Neon)
st.set_page_config(
    page_title="Fekra AI",
    page_icon="💡",
    layout="centered"
)

# ستايل احترافي لمنع الحتت البيضا وتحسين الوضوح
st.markdown("""
    <style>
    /* 1. السيطرة على الخلفية بالكامل ومنع أي مساحات بيضا */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {
        background-color: #0E1117 !important;
    }
    
    /* 2. جعل النصوص واضحة جداً باللون الأبيض النقي */
    p, span, div, label {
        color: #FFFFFF !important;
        font-weight: 500;
    }

    /* 3. ستايل العنوان النيوني مع تحسين الظل */
    h1 {
        color: #00F2FF !important;
        text-shadow: 0px 0px 15px #00F2FF;
        font-family: 'Segoe UI', sans-serif;
        text-align: center;
    }

    /* 4. تعديل فقاعات الدردشة لتكون مريحة للعين ومعتمة */
    .stChatMessage {
        background-color: #161B22 !important;
        border: 1px solid #00F2FF33 !important;
        border-radius: 15px !important;
    }

    /* 5. تلوين منطقة الإدخال بالكامل لتختفي الحتت البيضا */
    [data-testid="stChatInput"] {
        background-color: #161B22 !important;
        border: 1px solid #00F2FF !important;
    }
    
    textarea {
        color: #FFFFFF !important;
    }

    /* 6. تحسين شكل الأيقونات والأسماء */
    [data-testid="stChatMessageAvatarUser"] {
        background-color: #FF4B4B !important;
    }
    [data-testid="stChatMessageAvatarAssistant"] {
        background-color: #00F2FF !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💡 Fekra AI")
st.markdown("<p style='text-align: center; color: #808495 !important;'>نسخة الحريف الشاملة | المستقبل يبدأ هنا</p>", unsafe_allow_html=True)

# 2. جلب مفتاح الـ API
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("تأكد من إضافة GROQ_API_KEY في Secrets!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 3. تهيئة الذاكرة والدستور
if "messages" not in st.session_state:
    st.session_state.messages = []

system_identity = """
أنت فكرة AI (Fekra AI)، مساعد ذكي طوره أحمد وائل الحريف.
ردودك يجب أن تكون ذكية، سريعة، وبأسلوب عصري.
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
            
