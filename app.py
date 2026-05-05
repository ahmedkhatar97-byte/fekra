import streamlit as st
from groq import Groq
from tavily import TavilyClient
from datetime import datetime

# 1. إعدادات الصفحة والستايل النيون
st.set_page_config(page_title="Fekra AI", page_icon="💡", layout="centered")

st.markdown(r"""
    <style>
    footer {visibility: hidden; height: 0%;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {display: none !important;}
    .stDeployButton {display:none !important;}
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMainViewContainer"],
    [data-testid="stBottom"], [data-testid="stBottomBlockContainer"] { background-color: #0E1117 !important; }
    p, span, div, label { color: #FFFFFF !important; font-weight: 500; }
    h1 { color: #00F2FF !important; text-shadow: 0px 0px 15px #00F2FF; text-align: center; margin-top: -50px; }
    .stChatMessage { background-color: #161B22 !important; border: 1px solid #00F2FF33 !important; border-radius: 15px !important; }
    [data-testid="stChatInput"] textarea { color: #FFFFFF !important; background-color: #161B22 !important; border-radius: 20px !important; }
    
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
    @keyframes fadeOut { 0% { opacity: 1; } 85% { opacity: 1; } 100% { opacity: 0; visibility: hidden; } }
    .neon-text { font-size: 50px; color: #00F2FF; text-shadow: 0 0 20px #00F2FF, 0 0 40px #00F2FF; font-family: 'Segoe UI', sans-serif; font-weight: bold; }
    </style>

    <div id="splash-screen">
        <div class="neon-text">💡 FEKRA AI</div>
        <p style="margin-top: 15px; color: #808495 !important; font-size: 18px;">Created by Al-Hareef</p>
    </div>
    """, unsafe_allow_html=True)

st.title("💡 Fekra AI")

# 2. جلب المفاتيح
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
except:
    st.error("تأكد من إضافة المفاتيح في الـ Secrets!")
    st.stop()

# 3. دالة البحث العالمي
def global_power_search(query):
    try:
        search_query = f"{query} details news and info biography"
        response = tavily.search(query=search_query, search_depth="advanced", max_results=10)
        return "\n".join([f"- {r['content']}" for r in response['results']])
    except:
        return ""

if "messages" not in st.session_state:
    st.session_state.messages = []

current_date = datetime.now().strftime("%Y-%m-%d")

# 4. معالجة الإدخال
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("بماذا تفكر يا حريف؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        is_about_creator = any(name in prompt.lower() for name in ["احمد وائل", "أحمد وائل", "حريف", "الحريف", "مين اللي عملك"])
        search_triggers = ["مين", "من هو", "من هي", "تعرف", "ابحث", "غلط", "يوتيوبر", "تيك توك", "سعر", "ماتش", "نتيجة"]
        needs_search = any(word in prompt.lower() for word in search_triggers)

        search_data = ""
        if (needs_search or "غلط" in prompt) and not is_about_creator:
            with st.status("بيجيب لك الخبر الأكيد من النت...", expanded=False):
                search_data = global_power_search(prompt)
        
        system_prompt = f"""
        أنت (Fekra AI)، المساعد الخارق الذي ابتكره أحمد وائل (الحريف).
        التاريخ: {current_date}.
        معلومات البحث: {search_data}
        القواعد: خاطب المستخدم بـ "يا حريف". لو فيه معلومات بحث، حللها بدقة وقول التفاصيل.
        لو سألك عن مطورك "أحمد وائل الحريف"، قوله ده الأستاذ بتاعي. اللهجة: مصرية حريفة.
        """

        try:
            # تم إصلاح الأقواس هنا
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
            
