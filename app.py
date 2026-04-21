import streamlit as st
import g4f
from g4f.client import Client

# 1. إعدادات الصفحة والستايل
st.set_page_config(
    page_title="Fekra AI",
    page_icon="💡",
    layout="centered"
)

# إضافة ستايل بسيط لتحسين شكل الشات
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_index=True)

st.title("💡 Fekra AI")
st.caption("Powered by Free GPT-4 Engine")

# 2. تهيئة سجل المحادثة (Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. عرض الرسائل القديمة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. منطقة إدخال المستخدم والرد
if prompt := st.chat_input("بماذا تفكر يا هريف؟"):
    # إضافة رسالة المستخدم للسجل وعرضها
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد رد الذكاء الاصطناعي
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # استخدام الـ Client الجديد لمكتبة g4f لثبات أكتر
            client = Client()
            response = client.chat.completions.create(
                model=g4f.models.gpt_4o, # جرب gpt_4o أسرع وأذكى
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
            # حل مشكلة الـ concatenation اللي ظهرت لك
            error_msg = str(e)
            st.error(f"عذراً، حدث خطأ تقني: {error_msg}")
            # محاولة بديلة لو الـ Streaming فشل
            st.info("جاري محاولة الاتصال بمزود خدمة آخر...")
            
