import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS  # مكتبة البحث

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Fekra AI",
    page_icon="💡",
    layout="centered"
)

# الستايل النيون (المعتمد)
st.markdown(r"""
    <style>
    footer {visibility: hidden; height: 0%;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important; display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {visibility: hidden; display: none !important;}
    .stDeployButton {display:none !important;}

    [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"], 
    [data-testid="stMainViewContainer"],
    [data-testid="stBottom"],
    [data-testid="stBottomBlockContainer"] {
        background-color: #0E1117 !important;
    }
    
    p, span, div, label {
        color: #FFFFFF !important;
        font-weight: 500;
    }

    h1 {
        color: #00F2FF !important;
        text-shadow: 0px 0px 15px #00F2FF;
        text-align: center;
        margin-top: -50px;
    }

    .stChatMessage {
        background-color: #161B22 !important;
        border: 1px solid #00F2FF33 !important;
        border-radius: 15px !important;
        box-shadow: 0 0 10px #00F2FF11;
    }

    div[data-testid="stChatInputContainer"] {
        background-color: transparent !important;
        border: none !important;
        padding: 10px 0px !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
        background-color: #161B22 !important;
        border: 1px solid #00F2FF33 !important;
        border-radius: 20px !important;
        caret-color: #00F2FF !important;
        box-shadow: 0 0 15px #00F2FF22 !important;
    }
    
    [data-testid="stChatInput"] button {
        color: #00F2FF !important;
        background-color: transparent !important;
    }

    #splash-screen {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #0E1117;
        display: flex; flex-direction: column;
        justify-content: center; align-items: center;
        z-index: 9999;
        animation: fadeOut 2.5s forwards;
        pointer-events: none;
    }

    @keyframes fadeOut {
        0% { opacity: 1; }
        85% { opacity: 1; }
        100% { opacity: 0; visibility: hidden; }
    }

    .neon-text {
        font-size: 50px;
        color: #00F2FF;
        text-shadow: 0 0 20px #00F2FF, 0 0 40px #00F2FF;
        font-family: 'Segoe UI', sans-serif;
        font-weight: bold;
    }
    </style>

    <div id="splash-screen">
        <div class="neon-text">💡 FEKRA AI</div>
        <p style="margin-top: 15px; color: #808495 !important; font-size: 18px;">Created by Al-Hareef</p>
    </div>
    """, unsafe_allow_html=True)

st.title("💡 Fekra AI")
st.markdown("<p style='text-align: center; color: #808495 !important;'>نسخة الحريف المتصلة بالإنترنت</p>", unsafe_allow_html=True)

# 2. جلب مفتاح الـ API
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("يا حريف، تأكد من إضافة GROQ_API_KEY في Secrets!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 3. دالة البحث في الإنترنت
def search_the_web(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n".join(results)
    except:
        return "عذراً يا حريف، لم أستطع الوصول للإنترنت حالياً."

# 4. تهيئة الذاكرة ودستور الجودة
if "messages" not in st.session_state:
    st.session_state.messages = []

system_identity = """
أنت (Fekra AI)، المساعد الذكي المتصل بالإنترنت الذي صممه أحمد وائل (الحريف).
بروتوكول الرد:
1. اللغة: لهجة مصرية "حريفة" ونظيفة جداً بلا أخطاء إملائية.
2. البحث: استخدم المعلومات المتاحة لك من الإنترنت للرد على الأخبار أو المعلومات الحديثة.
3. الجودة: ممنوع تكرار الحروف أو استخدام حروف صينية/يابانية نهائياً.
4. الإيجاز: كن ذكياً ومباشراً في إجاباتك.
"""

# 5. عرض رسائل الدردشة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. منطقة الإدخال والرد
if prompt := st.chat_input("بماذا تفكر يا حريف؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # خطوة البحث: لو السؤال محتاج معلومات حديثة
        search_context = ""
        if any(word in prompt.lower() for word in ["اخبار", "سعر", "ماتش", "طقس", "اليوم", "مين", "ايه هو"]):
            with st.spinner("بيبحث عشانك يا حريف..."):
                search_context = f"\n\nمعلومات من الإنترنت للرد على المستخدم:\n{search_the_web(prompt)}"

        try:
            messages_to_send = [{"role": "system", "content": system_identity + search_context}] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile", 
                messages=messages_to_send,
                stream=True,
                temperature=0.4,
            )

            for chunk in completion:
                content = chunk.choices[0].delta.content
                if content:
                    full_response += str(content)
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"حدث خطأ فني: {str(e)}")
            
