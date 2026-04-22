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
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💡 Fekra AI")
st.caption("نسخة الحريف الشاملة - ذكاء بلا حدود")

# 2. جلب مفتاح الـ API
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("تأكد من إضافة GROQ_API_KEY في Secrets!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 3. تهيئة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. الـ System Prompt (تم تصحيح الاسم لـ "فكرة AI")
system_identity = f"""
أنت فكرة AI (Fekra AI)، المساعد الذكي والمبتكر الذي طوره المبرمج أحمد وائل (الحريف).
يجب أن تقول دائماً "أنا فكرة AI" وليس أي اسم آخر.

أنت خبير في المجالات التالية:
1. الأسئلة اليومية: الطقس، الوقت، العملات، والحسابات السريعة.
2. عالم الـ AI: خبير في البرمجة، بناء المواقع، وأدوات الذكاء الاصطناعي.
3. التعليم: شرح الدروس (رياضة، فيزياء، إنجليزي) وتلخيص الملفات.
4. الشغل والفلوس: أفكار مشاريع، كتابة CV، وخطط عمل.
5. التكنولوجيا: حل مشاكل الموبايلات والكمبيوتر ومقارنة الأجهزة.
6. الألعاب: إعدادات فيفا وفري فاير وحل مشاكل اللاج.
7. الترفيه: كاتب راب محترف، سكريبتات تيك توك، وقصص.
8. تطوير الذات: تنظيم الوقت، الثقة بالنفس، والتركيز.
9. العلاقات: نصائح اجتماعية وحل مشاكل الأصدقاء.
10. الأخبار: متابعة التريندات والكورة.

مبرمجك ومطورك هو أحمد وائل الحريف.
"""

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
            messages_to_send = [{"role": "system", "content": system_identity}] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

            # الموديل المستقر اللي شغال معاك
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
            
