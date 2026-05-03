import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from datetime import datetime # عشان التاريخ يبقى مظبوط بالملي

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Fekra AI",
    page_icon="💡",
    layout="centered"
)

# الستايل النيون (المعتمد والأنيق)
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
st.markdown("<p style='text-align: center; color: #808495 !important;'>نسخة الحريف الذكية | بحث مباشر</p>", unsafe_allow_html=True)

# 2. جلب مفتاح الـ API
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("يا حريف، ضيف مفتاح الـ API في الـ Secrets!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 3. دالة البحث المحسنة
def get_latest_info(query):
    try:
        with DDGS() as ddgs:
            # زودنا عدد النتائج وبحثنا بشكل أدق
            results = [f"- {r['body']}" for r in ddgs.text(query, max_results=5)]
            return "\n".join(results)
    except Exception:
        return "للأسف مش قادر أوصل للإنترنت حالياً يا حريف."

# 4. تهيئة الذاكرة والدستور الصارم
if "messages" not in st.session_state:
    st.session_state.messages = []

# الحصول على تاريخ اللحظة الحالية
current_date = datetime.now().strftime("%Y-%m-%d")

system_identity = f"""
أنت (Fekra AI)، مساعد ذكي ابتكره أحمد وائل (الحريف).
قواعد صارمة:
1. التاريخ الحالي هو: {current_date}. اعتمد عليه دائماً لمعرفة الأيام.
2. إذا سألك المستخدم عن أخبار أو نتائج ماتشات أو أي شيء حديث، اعتمد كلياً على "نتائج البحث" التي سأزودك بها وتجاهل معلوماتك القديمة.
3. اللغة: مصرية حريفة، واضحة، وبدون أخطاء إملائية نهائياً.
4. الجودة: ممنوع الحروف الصينية أو الرموز الغريبة.
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
        
        # تحسين ذكاء البحث
        search_results = ""
        if any(word in prompt.lower() for word in ["ماتش", "الاهلي", "نتيجة", "اخبار", "سعر", "النهاردة", "امبارح"]):
            with st.status("بيجيب لك الخلاصة يا حريف...", expanded=False):
                search_results = get_latest_info(prompt)
                st.write("تم البحث وتحديث المعلومات!")

        # دمج نتائج البحث في سياق الموديل بشكل إجباري
        full_context = system_identity
        if search_results:
            full_context += f"\n\nأحدث معلومات من الإنترنت بخصوص سؤال المستخدم:\n{search_results}\n\nالتزم بالمعلومات دي في ردك."

        try:
            messages_to_send = [{"role": "system", "content": full_context}] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile", 
                messages=messages_to_send,
                stream=True,
                temperature=0.3, # قللنا الحرارة أكتر لمنع التخريف
            )

            for chunk in completion:
                content = chunk.choices[0].delta.content
                if content:
                    full_response += str(content)
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"حصلت مشكلة: {str(e)}")
            
