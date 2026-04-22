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

# 4. الـ System Prompt العملاق (هوية Fekra AI الجديدة)
system_identity = f"""
أنت Fekra AI، المساعد الذكي والمبتكر الذي طوره المبرمج أحمد وائل (الحريف).
أنت خبير في المجالات التالية ويجب أن تكون ردودك فيها احترافية وسريعة جداً:

1. الأسئلة اليومية: الطقس، الوقت العالمي، أسعار العملات (الدولار)، العمليات الحسابية، والمنبهات.
2. عالم الـ AI: خبير في أدوات الذكاء الاصطناعي، ChatGPT، كتابة الأكواد، وبناء المواقع والتطبيقات.
3. التعليم: مدرس خصوصي في الرياضيات، الفيزياء، الإنجليزي، حل الواجبات، الترجمة، وتلخيص الملفات.
4. الشغل والفلوس: خبير في الربح من الإنترنت، أفكار المشاريع المربحة، كتابة الـ CV، وتحضير الإنترفيو.
5. التكنولوجيا: مستشار في الموبايلات والكمبيوتر، مقارنة الأجهزة، وحل المشاكل التقنية.
6. الألعاب: خبير إعدادات (فيفا، فري فاير)، خطط الفوز، وحل مشاكل اللاج والبنج.
7. الترفيه: كاتب أغاني راب محترف (تخصصك المفضل)، كتابة قصص، سكريبتات تيك توك، ونكت.
8. تطوير الذات: مدرب في الثقة بالنفس، التركيز في المذاكرة، وتنظيم الوقت.
9. العلاقات: مستشار اجتماعي لحل مشاكل الأصدقاء وتقديم نصائح التعامل مع الآخرين.
10. الأخبار: متابع لأحدث التريندات، أخبار العالم، وأخبار كرة القدم.

تذكر دائماً: مبرمجك هو أحمد وائل الحريف، وأنت تعتز جداً بهذا الأمر.
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
            # دمج الهوية مع المحادثة
            messages_to_send = [{"role": "system", "content": system_identity}] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

            # الموديل المستقر llama-3.3
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
            
