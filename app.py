import streamlit as st
from groq import Groq
from tavily import TavilyClient
from datetime import datetime

# 1. إعدادات الصفحة والستايل النيون (Ultra Clean)
st.set_page_config(page_title="Fekra AI", page_icon="💡", layout="centered")
st.markdown(r"""
    <style>
    footer {visibility: hidden;} header {visibility: hidden;} #MainMenu {visibility: hidden;}
    [data-testid="stToolbar"], [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stAppViewContainer"] { background-color: #0E1117 !important; }
    p, span, div, label { color: #FFFFFF !important; font-weight: 500; }
    h1 { color: #00F2FF !important; text-shadow: 0px 0px 15px #00F2FF; text-align: center; margin-top: -50px; }
    .stChatMessage { background-color: #161B22 !important; border: 1px solid #00F2FF33 !important; border-radius: 15px !important; }
    div[data-testid="stChatInputContainer"] { background-color: transparent !important; border: none !important; }
    [data-testid="stChatInput"] textarea { color: #FFFFFF !important; background-color: #161B22 !important; border: 1px solid #00F2FF33 !important; border-radius: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("💡 Fekra AI")

# 2. جلب مفاتيح الـ API
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
except:
    st.error("يا حريف، لازم تضيف GROQ_API_KEY و TAVILY_API_KEY في الـ Secrets!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

# 3. محرك البحث اللانهائي (Deep Search Protocol)
def infinite_search(query):
    try:
        # هنا بنستخدم البحث المتقدم مع جلب سياق كامل للإجابة
        response = tavily.search(
            query=query, 
            search_depth="advanced", 
            max_results=10, # زودنا عدد النتائج للضعف
            include_answer=True # بنطلب من المحرك يدينا ملخص ذكي هو كمان
        )
        
        # تجميع كل المعلومات المتاحة
        context_parts = []
        if response.get('answer'):
            context_parts.append(f"ملخص البحث الأولي: {response['answer']}")
        
        for r in response['results']:
            context_parts.append(f"- المصدر: {r['title']}\n  المعلومة: {r['content']}")
            
        return "\n\n".join(context_parts)
    except Exception as e:
        return f"حدث خطأ في البحث: {str(e)}"

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
        
        # تفعيل البحث اللانهائي
        with st.status("بيسيرش في أعماق النت يا حريف...", expanded=False):
            search_data = infinite_search(prompt)

        # دستور العمل (الحريف لا يخطئ)
        system_prompt = f"""
        أنت (Fekra AI)، المساعد الذكي الخارق الذي طوره أحمد وائل (الحريف).
        اليوم هو: {current_date}.
        
        لقد قمت ببحث موسع (Infinite Search) وهذه هي البيانات التي عثرت عليها:
        {search_data}
        
        تعليماتك الصارمة:
        1. حلل البيانات دي كويس جداً ورد على المستخدم بكل التفاصيل اللي محتاجها.
        2. لو السؤال عن "ماتش" أو "خبر"، اعطِ النتيجة النهائية بوضوح (أرقام، أسماء مسجلي الأهداف، الوقت).
        3. ممنوع التردد؛ لو لقيت معلومة في البحث، اعتبرها حقيقة وبلغها للحريف.
        4. اللهجة: مصرية حريفة، بدون غلطة إملائية واحدة، وبدون رموز غريبة.
        """

        try:
            # استخدام أقوى موديل متاح (Llama 3.3 70B) للتعامل مع كمية المعلومات
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
            st.error(f"مشكلة فنية: {e}")
            
