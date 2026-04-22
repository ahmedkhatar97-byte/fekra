import streamlit as st
from groq import Groq
from datetime import datetime # لإدراك الوقت والتاريخ

# 1. إعدادات الصفحة والستايل المتكامل (النسخة النهائية النظيفة)
st.set_page_config(
    page_title="Fekra AI",
    page_icon="💡",
    layout="centered"
)

st.markdown("""
    <style>
    /* 1. إخفاء أي خلفيات أو حدود للمستطيل الخارجي الكبير */
    [data-testid="stChatInput"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }

    /* 2. جعل مستطيل الكتابة الداخلي (الأسود الشيك) هو الأساس */
    [data-testid="stChatInput"] textarea {
        background-color: #161B22 !important; /* نفس لون فقاعات الشات */
        color: #FFFFFF !important; /* خط أبيض واضح */
        border: 1px solid #00F2FF44 !important; /* حدود نيون خفيفة */
        border-radius: 12px !important;
        padding: 10px !important;
        caret-color: #00F2FF !important; /* لون المؤشر نيون */
    }

    /* 3. تنسيق منطقة الإدخال بالكامل لتختفي الحواف البيضاء */
    section[data-testid="stChatInputContainer"] {
        background-color: transparent !important;
        border: none !important;
    }

    /* 4. التأكيد على إخفاء الإعلانات والفوتر */
    footer {display: none !important;}
    header {display: none !important;}
    #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# معرفة الوقت والتاريخ الحالي لإرساله للموديل
now = datetime.now()
current_time_info = now.strftime("%A, %d %B %Y | %I:%M %p")

st.title("💡 Fekra AI")

# 2. إعداد الـ API
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("تأكد من إضافة المفتاح في Secrets!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. 🔥 الدستور المحدث (الاسم + التاريخ الحقيقي)
system_identity = f"""
أنت فكرة AI (Fekra AI)، المساعد الذكي المبتكر الذي طوره أحمد وائل الحريف.

قواعد صارمة:
1. إذا سألك المستخدم عن اسمك، يجب أن تجيب بـ "Fekra AI" بوضوح.
2. أنت الآن تدرك الوقت والتاريخ تماماً. التاريخ والوقت الحالي هو: {current_time_info}.
3. إذا سألك المستخدم "النهاردة يوم إيه؟" أو "التاريخ كام؟"، جاوب بناءً على المعلومة المذكورة أعلاه.
4. التزم بأسلوبك الذكي والسريع في المجالات الـ 10 التي حددناها سابقاً.
"""

# 4. عرض الرسائل والرد
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("بماذا تفكر يا حريف؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
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
        
