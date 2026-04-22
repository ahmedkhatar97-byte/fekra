import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة والستايل
st.set_page_config(
    page_title="Fekra AI",
    page_icon="💡",
    layout="centered"
)

# إضافة ستايل لتحسين شكل الرسائل
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💡 Fekra AI")
st.caption("أسرع ذكاء اصطناعي - مستقر وآمن 100%")

# 2. جلب مفتاح الـ API من الـ Secrets (الخزنة)
# تأكد انك ضفت GROQ_API_KEY في إعدادات Streamlit Cloud
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("مفتاح الـ API غير موجود في إعدادات Secrets!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 3. تهيئة الذاكرة (Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة الشات والرد
if prompt := st.chat_input("بماذا تفكر يا هريف؟"):
    # إضافة رسالة المستخدم للسجل
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد رد الذكاء الاصطناعي بنظام الـ Streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            completion = client.chat.completions.create(
                model="llama3-70b-8192", # موديل جبار وسريع جداً
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )

            for chunk in completion:
                content = chunk.choices[0].delta.content
                if content:
                    full_response += content
                    # عرض النص وهو بيتكتب "لايف"
                    message_placeholder.markdown(full_response + "▌")
            
            # عرض الرد النهائي وحفظه في الذاكرة
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"عذراً، حدث خطأ تقني: {str(e)}")
                                                
