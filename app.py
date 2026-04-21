import streamlit as st
import g4f # المكتبة السحرية اللي بتجيب GPT-4 مجاناً

# إعداد واجهة الموقع
st.set_page_config(page_title="Fekra AI - Free", page_icon="💡")
st.title("💡 Fekra AI (Free GPT-4)")

# تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال مدخلات المستخدم
if prompt := st.chat_input("اسأل 'فكرة' أي حاجة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # جلب رد الذكاء الاصطناعي من g4f
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # هنا بنستخدم موديل gpt-4o أو gpt-4 مجاناً
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4, # تقدر تغيره لـ gpt_4o
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            
            for chunk in response:
                if chunk:
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"حصل مشكلة بسيطة: {e}")
          
