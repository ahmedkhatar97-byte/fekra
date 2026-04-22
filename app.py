import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة وواجهة المستخدم (UI/UX)
st.set_page_config(
    page_title="Fekra AI",
    page_icon="💡",
    layout="centered"
)

# الستايل النهائي: إخفاء الإعلانات + ضبط الألوان + وضوح الكتابة
st.markdown("""
    <style>
    /* إخفاء شريط Streamlit السفلي (الإعلانات) والقائمة العلوية */
    footer {visibility: hidden; height: 0%;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    [data-testid="stStatusWidget"] {visibility: hidden;}

    /* السيطرة على الخلفية ومنع أي مساحات بيضاء */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0E1117 !important;
    }
    
    /* جعل النصوص المرسلة واضحة جداً باللون الأبيض */
    p, span, div, label {
        color: #FFFFFF !important;
        font-weight: 500;
    }

    /* ستايل العنوان النيوني */
    h1 {
        color: #00F2FF !important;
        text-shadow: 0px 0px 15px #00F2FF;
        font-family: 'Segoe UI', sans-serif;
        text-align: center;
        margin-top: -50px;
    }

    /* تعديل فقاعات الدردشة */
    .stChatMessage {
        background-color: #161B22 !important;
        border: 1px solid #00F2FF33 !important;
        border-radius: 15px !important;
    }

    /* ضبط لون الكلام "أسود" أثناء الكتابة في المستطيل لزيادة الوضوح */
    [data-testid="stChatInput"] textarea {
        color: #000000 !important;
        background-color: #FFFFFF !important;
        caret-color: #000000 !important;
    }
    
    /* تحسين زر الإرسال */
    [data-testid="stChatInput"] button {
        color: #00F2FF !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💡 Fekra AI")
st.markdown("<p style='text-align: center; color: #808495 !important;'>نسخة الحريف الشاملة | ذكاء بلا حدود</p>", unsafe_allow_html=True)

# 2. جلب مفتاح الـ API من الـ Secrets
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("تأكد من إضافة GROQ_API_KEY في Secrets!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 3. تهيئة الذاكرة والدستور (System Prompt)
if "messages" not in st.session_state:
    st.session_state.messages = []

system_identity = """
أنت فكرة AI (Fekra AI)، المساعد الذكي والمبتكر الذي طوره المبرمج أحمد وائل (الحريف).

قواعد الهوية:
- إذا سألك المستخدم عن اسمك أو من أنت، قل: "أنا فكرة AI، طورني المبرمج أحمد وائل الحريف".
- في الأسئلة العادية، جاوب مباشرة دون تكرار التعريف بنفسك.

أنت خبير في:
1. الأسئلة اليومية السريعة (طقس، دولار، حسابات).
2. الذكاء الاصطناعي (ChatGPT، برمجة، أكواد).
3. التعليم (شرح دروس، ترجمة، ملخصات).
4. البيزنس (أفكار مشاريع، CV، خطط عمل).
5. التكنولوجيا (مقارنة أجهزة، حل مشاكل تقنية).
6. الألعاب (إعدادات فيفا وفري فاير، حل اللاج).
7. الترفيه (كتابة راب، سكريبتات، قصص).
8. تطوير الذات (ثقة، تركيز، تنظيم وقت).
9. العلاقات (نصائح اجتماعية).
10. الأخبار والتريندات الكروية.
"""

# 4. عرض رسائل الدردشة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة الإدخال والرد
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
            
