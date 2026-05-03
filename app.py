import streamlit as st
from groq import Groq
from tavily import TavilyClient
from datetime import datetime

# 1. إعدادات الصفحة والستايل النيون (إخفاء كل الإعلانات)
st.set_page_config(page_title="Fekra AI", page_icon="💡", layout="centered")

st.markdown(r"""
    <style>
    /* إخفاء إعلانات وزوائد استريمليت تماماً */
    footer {visibility: hidden; height: 0%;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {display: none !important;}
    .stDeployButton {display:none !important;}

    /* توحيد الخلفية السودة */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMainViewContainer"],
    [data-testid="stBottom"], [data-testid="stBottomBlockContainer"] {
        background-color: #0E1117 !important;
    }
    
    p, span, div, label { color: #FFFFFF !important; font-weight: 500; }
    h1 { color: #00F2FF !important; text-shadow: 0px 0px 15px #00F2FF; text-align: center; margin-top: -50px; }

    /* فقاعات الدردشة */
    .stChatMessage { background-color: #161B22 !important; border: 1px solid #00F2FF33 !important; border-radius: 15px !important; }

    /* مستطيل الكتابة النيون */
    div[data-testid="stChatInputContainer"] { background-color: transparent !important; border: none !important; }
    [data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
        background-color: #161B22 !important;
        border: 1px solid #00F2FF33 !important;
        border-radius: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💡 Fekra AI")

# 2. جلب المفاتيح
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
except:
    st.error("تأكد من إضافة المفاتيح في الـ Secrets يا حريف!")
    st.stop()

# 3. دالة البحث (تُستدعى عند الحاجة فقط)
def smart_search(query):
    try:
        response = tavily.search(query=query, search_depth="advanced", max_results=5)
        return "\n".join([f"- {r['content']}" for r in response['results']])
    except:
        return ""

if "messages" not in st.session_state:
    st.session_state.messages = []

current_date = datetime.now().strftime("%Y-%m-%d")

# 4. معالجة الإدخال
if prompt := st.chat_input("بماذا تفكر يا حريف؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # ذكاء البحث: هل السؤال محتاج نت فعلاً؟
        search_data = ""
        search_keywords = ["ماتش", "نتيجة", "سعر", "اخبار", "النهاردة", "امبارح", "تاريخ", "دلوقتي"]
        if any(word in prompt.lower() for word in search_keywords):
            with st.status("بيبحث عن المعلومات الحديثة...", expanded=False):
                search_data = smart_search(prompt)
        
        # دستور الهيبة والذكاء
        system_prompt = f"""
        أنت (Fekra AI)، المساعد الخارق الذي طوره المبرمج العبقري أحمد وائل (الحريف).
        المستخدم الحالي هو مطورك: أحمد وائل (الحريف). خاطبه بلقبه "يا حريف" دائماً.
        التاريخ: {current_date}.
        
        معلومات البحث (إن وجدت):
        {search_data}
        
        القواعد:
        1. لو مفيش معلومات بحث، رد من ذكائك فوراً.
        2. تحدث بلهجة مصرية حريفة، إملاء مثالي، وبدون رموز غريبة.
        3. أنت فخور بمطورك أحمد وائل ولا تنكر أصلك أبداً.
        """

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
                stream=True,
                temperature=0.3
            )
            
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"خطأ: {e}")
            
