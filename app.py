import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة والستايل
st.set_page_config(
    page_title="Fekra AI",
    page_icon="💡",
    layout="centered"
)

st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💡 Fekra AI")
st.caption("أسرع ذكاء اصطناعي - نسخة الحريف المستقرة")

# 2. جلب مفتاح الـ API
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("تأكد من إضافة GROQ_API_KEY في Secrets!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 3. تهيئة الذاكرة (Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. تعريف هوية الموديل (System Message)
# وضعنا هذا السطر ليعرف أنه Fekra AI وأن مبرمجه هو أحمد وائل (الحريف)
system_prompt = {
    "role": "system",
    "content": "اسمك Fekra AI، أنت مساعد ذكي ومبتكر. مبرمجك ومطورك هو المبرمج العبقري أحمد وائل، الملقب بالحريف (Al-Hareef). يجب أن تفتخر دائماً بهويتك وبمبرمجك عند سؤالك."
}

# 5. عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. منطقة الشات والرد
if prompt := st.chat_input("بماذا تفكر يا حريف؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # بناء قائمة الرسائل مع إضافة الـ System Prompt في البداية
            messages_to_send = [system_prompt] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

            # الموديل اللي شغال معاك (لم يتم تغييره)
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
            st.error(f"عذراً يا حريف، حدث خطأ: {str(e)}")
            
