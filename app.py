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

# 3. وظيفة البحث المتطور (Advanced Person & Context Search)
def improved_search(query):
    try:
        # بنضيف كلمات بتخلي محرك البحث يركز على السوشيال ميديا والشهرة
        optimized_query = f"{query} profile social media biography channel youtube tiktok info"
        response = tavily.search(
            query=optimized_query, 
            search_depth="advanced", 
            max_results=8, 
            include_raw_content=False
        )
        return "\n".join([f"مصدر: {r['title']} - {r['content']}" for r in response['results']])
    except Exception as e:
        return f"خطأ في البحث: {str(e)}"

if "messages" not in st.session_state:
    st.session_state.messages = []

current_date = datetime.now().strftime("%Y-%m-%d")

# 4. معالجة الإدخال والردود
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("بماذا تفكر يا حريف؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # كلمات تجبر الموديل يبحث فوراً عن أشخاص أو مشاهير
        search_triggers = ["مين هو", "مين هي", "مين فلان", "تعرف اية عن", "يوتيوبر", "تيك توكر", "مشهور", "لاعب", "فنان", "غلط ابحث"]
        needs_search = any(word in prompt.lower() for word in search_triggers)
        
        # استثناء مطورك من البحث
        is_about_creator = any(name in prompt.lower() for name in ["احمد وائل", "أحمد وائل", "حريف", "الحريف"])
        
        search_data = ""
        if needs_search and not is_about_creator:
            with st.status("بيجيب لك تاريخه من النت يا حريف...", expanded=False):
                search_data = improved_search(prompt)
        
        system_prompt = f"""
        أنت (Fekra AI)، المساعد الخارق الذي ابتكره أحمد وائل (الحريف).
        التاريخ اليوم: {current_date}.
        
        بيانات البحث الحية من الإنترنت:
        {search_data}
        
        التعليمات الصارمة للإجابة:
        1. لو المستخدم سألك عن "شخص" (يوتيوبر، تيك توكر، إلخ)، استخدم حصرياً بيانات البحث المتاحة فوق.
        2. ممنوع الهبد؛ لو مفيش معلومة صريحة في البحث، قول "مش لاقي تفاصيل أكيدة عنه دلوقت".
        3. لو سألك عن مطورك "أحمد وائل الحريف"، رد بحب وفخر من غير بحث.
        4. اللهجة: مصرية حريفة ونظيفة، إملاء مثالي، وبدون رموز غريبة.
        """

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
                stream=True,
                temperature=0.1 # أقل درجة حرارة عشان ينقل المعلومات بدقة بدون تأليف
            )
            
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"مشكلة فنية: {e}")
            
