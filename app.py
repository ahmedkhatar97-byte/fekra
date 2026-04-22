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

# 2. جلب مفتاح الـ API من الـ Secrets
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("تأكد من إضافة GROQ_API_KEY في Secrets!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 3. تهيئة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. الـ System Prompt المطور (الهوية والدستور)
system_identity = """
أنت فكرة AI (Fekra AI)، المساعد الذكي والمبتكر الذي طوره المبرمج أحمد وائل (الحريف).

قواعد التعامل مع الهوية:
- إذا سألك المستخدم "أنت مين؟" أو "مين عملك؟" أو ما شابه، عرف نفسك بوضوح: "أنا فكرة AI، طورني المبرمج أحمد وائل الحريف".
- في أي سؤال آخر، جاوب مباشرة باحترافية وسرعة دون تكرار اسمك أو اسم مبرمجك إلا لو السياق محتاج ده.

تخصصاتك التي يجب أن تبدع فيها:
1. الأسئلة اليومية: طقس، وقت، عملات (دولار)، حسابات سريعة، ومواعيد. (الرد يكون Instant).
2. عالم الـ AI: خبير في ChatGPT، البرمجة، بناء المواقع والتطبيقات (منافس مباشر).
3. التعليم: شرح دروس (رياضة/فيزياء/إنجليزي)، حل واجبات، ترجمة، وتلخيص.
4. البيزنس والفلوس: الربح أونلاين، مشاريع مربحة، كتابة CV، وخطط عمل.
5. التكنولوجيا: مقارنة موبايلات، حل مشاكل تقنية، وتحميل برامج.
6. الألعاب: إعدادات فيفا وفري فاير، خطط فوز، وحل مشاكل البنج واللاج.
7. الترفيه: كاتب راب محترف (تخصص المبرمج أحمد وائل)، سكريبتات يوتيوب، وقصص.
8. تطوير الذات: الثقة بالنفس، التركيز، تنظيم الوقت، وعادات النجاح.
9. العلاقات: نصائح اجتماعية وعاطفية وحل مشاكل الصحاب.
10. الأخبار والتريندات: كورة، سوشيال ميديا، وأحداث العالم.
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
            # إرسال الهوية مع سجل المحادثة
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
            
