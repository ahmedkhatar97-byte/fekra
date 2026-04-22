import streamlit as st
import g4f
from g4f.client import Client

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Fekra AI",
    page_icon="💡",
    layout="centered"
)

# 2. تحسين شكل الشات بـ CSS
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 10px;
    }
    /* إخفاء القائمة العلوية لـ Streamlit لمظهر احترافي */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("💡 Fekra AI")
st.caption("Powered by Blackbox Engine (Free GPT-4o)")

# 3. تهيئة الذاكرة (Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة الشات والرد
if prompt := st.chat_input("بماذا تفكر يا هريف؟"):
    # عرض رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد رد الذكاء الاصطناعي
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            client = Client()
            # استخدمنا هنا Blackbox لأنه أثبت كفاءة ومن غير طلبات معقدة
            response = client.chat.completions.create(
                model="gpt-4o",
                provider=g4f.Provider.Blackbox,
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
                    # علامة الـ cursor عشان يحسس المستخدم إنه بيكتب لايف
                    message_placeholder.markdown(full_response + "▌")
            
            # عرض الرد النهائي وحفظه في الذاكرة
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            # لو الـ Blackbox واجه مشكلة، جرب مزود احتياطي فوراً
            st.error(f"حصل مشكلة بسيطة، جاري المحاولة مرة أخرى...")
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    provider=g4f.Provider.DarkAI, # مزود احتياطي
                    messages=[{"role": "user", "content": prompt}]
                )
                full_response = response.choices[0].message.content
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except:
                st.error("المزودين مشغولين حالياً، جرب كمان دقيقة.")
                    
