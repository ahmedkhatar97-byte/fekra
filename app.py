import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Fekra AI", page_icon="💡", layout="centered")

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
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMainViewContainer"],
    [data-testid="stBottom"], [data-testid="stBottomBlockContainer"] { background-color: #0E1117 !important; }
    p, span, div, label { color: #FFFFFF !important; font-weight: 500; }
    h1 { color: #00F2FF !important; text-shadow: 0px 0px 15px #00F2FF; text-align: center; margin-top: -50px; }
    .stChatMessage { background-color: #161B22 !important; border: 1px solid #00F2FF33 !important; border-radius: 15px !important; }
    div[data-testid="stChatInputContainer"] { background-color: transparent !important; border: none !important; }
    [data-testid="stChatInput"] textarea { color: #FFFFFF !important; background-color: #161B22 !important; border: 1px solid #00F2FF33 !important; border-radius: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("💡 Fekra AI")

# 2. جلب مفتاح الـ API
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("ضيف مفتاح الـ API يا حريف!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 3. دالة البحث المطورة
def super_search(query):
    try:
        with DDGS() as ddgs:
            # بنبحث عن آخر الأخبار ونتايج الماتشات بشكل موسع
            results = ddgs.text(f"{query} news results", max_results=8)
            search_text = "\n".join([f"- {r['body']}" for r in results])
            return search_text
    except:
        return "مش عارف أوصل للنت حالياً."

if "messages" not in st.session_state:
    st.session_state.messages = []

current_date = datetime.now().strftime("%Y-%m-%d")

# 4. منطقة الإدخال
if prompt := st.chat_input("بماذا تفكر يا حريف؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # ذكاء اصطناعي لتقييم هل السؤال محتاج بحث؟
        needs_search = any(word in prompt.lower() for word in ["الاهلي", "ماتش", "نتيجة", "سعر", "اخبار", "النهاردة", "امبارح"])
        
        search_data = ""
        if needs_search:
            with st.status("بجيب لك الخبر اليقين من قلب الحدث...", expanded=False):
                search_data = super_search(prompt)
        
        # الدستور الصارم مع دمج البيانات
        system_prompt = f"""
        أنت (Fekra AI)، مساعد ذكي جداً صممه أحمد وائل (الحريف).
        اليوم هو: {current_date}.
        معلومات البحث المباشرة:
        {search_data}
        
        مهمتك:
        1. لو سألك عن ماتش أو خبر، استخدم "معلومات البحث" اللي فوق دي أساساً لردك.
        2. لو المعلومات مش واضحة، حاول تستنتج النتيجة من الأخبار اللي قدامك (مثلاً: لو لقيت خبر بيقول الأهلي فاز، يبقى الأهلي كسب).
        3. اتكلم مصري حريف، ممنوع الغلطات الإملائية، وممنوع الحروف الصيني.
        """

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
                stream=True,
                temperature=0.2 # درجة حرارة منخفضة جداً عشان الدقة
            )
            
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"في مشكلة حصلت: {e}")
            
