import streamlit as st
import g4f
from g4f.client import Client

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Fekra AI",
    page_icon="💡",
    layout="centered"
)

# 2. إضافة ستايل (التصحيح هنا)
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💡 Fekra AI")
st.caption("Powered by Free GPT-4 Engine")

# 3. تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة الإدخال والرد
if prompt := st.chat_input("بماذا تفكر؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            client = Client()
            response = client.chat.completions.create(
                model=g4f.models.gpt_4o,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )

            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"حدث خطأ: {str(e)}")
            
