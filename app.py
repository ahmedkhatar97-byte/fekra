import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="Fekra AI", page_icon="💡")

st.title("💡 Fekra AI")
st.caption("النسخة الأحدث والأكثر استقراراً")

# 2. جلب المفتاح
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("تأكد من إضافة GROQ_API_KEY في Secrets!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. معالجة الشات
if prompt := st.chat_input("بماذا تفكر يا هريف؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # الموديل المستقر والمدعوم حالياً
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile", 
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )

            for chunk in completion:
                # حماية إضافية لضمان أن النص ليس كائن (Object)
                if chunk.choices[0].delta.content:
                    content = str(chunk.choices[0].delta.content)
                    full_response += content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"حدث خطأ في النظام: {str(e)}")
            
