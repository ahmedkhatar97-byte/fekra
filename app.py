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

# 3. وظيفة تقييم الحاجة للبحث
def check_if_needs_search(user_query):
    # الموديل بيقرر هل السؤال محتاج بحث ولا لأ
    decision_prompt = f"Does the following user query require real-time internet search for up-to-date information (like news, sports results, prices, etc.)? Answer ONLY with 'YES' or 'NO'. Query: {user_query}"
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant", # موديل خفيف وسريع للقرار
        messages=[{"role": "user", "content": decision_prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip().upper()

# 4. دالة البحث المتقدمة
def deep_search(query):
    try:
        response = tavily.search(query=query, search_depth="advanced", max_results=6)
        return "\n".join([f"- {r['content']}" for r in response['results']])
    except:
        return ""

if "messages" not in st.session_state:
    st.session_state.messages = []

current_date = datetime.now().strftime("%Y-%m-%d")

# 5. معالجة الإدخال
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("بماذا تفكر يا حريف؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # استثناء اسم المطور من أي بحث
        is_about_creator = any(name in prompt.lower() for name in ["احمد وائل", "أحمد وائل", "حريف", "الحريف", "مين اللي عملك"])
        
        search_data = ""
        if not is_about_creator:
            # هنا الموديل بيقرر: يبحث ولا ملوش لزمة؟
            with st.spinner("بيفكر هل محتاج يبحث..."):
                needs_search = check_if_needs_search(prompt)
            
            if "YES" in needs_search:
                with st.status("بيجيب لك المعلومات الأكيدة من النت...", expanded=False):
                    search_data = deep_search(prompt)
        
        system_prompt = f"""
        أنت (Fekra AI)، المساعد الذكي الخارق. مطورك هو المبرمج أحمد وائل (الحريف).
        التاريخ الحالي: {current_date}.
        معلومات البحث الحقيقية (إن وجدت):
        {search_data}
        
        القواعد:
        1. خاطب المستخدم بـ "يا حريف".
        2. لو فيه معلومات بحث، التزم بالدقة الإملائية والنتائج الصحيحة 100%.
        3. لو مفيش معلومات بحث، رد من معرفتك فوراً.
        4. اللهجة: مصرية حريفة.
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
            
