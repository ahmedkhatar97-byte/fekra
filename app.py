import streamlit as st
from groq import Groq
from tavily import TavilyClient
from datetime import datetime

# 1. إعدادات الستايل (نفس الستايل النيون بتاعك يا حريف)
st.set_page_config(page_title="Fekra AI", page_icon="💡", layout="centered")
st.markdown(r"""
    <style>
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stChatMessage { background-color: #161B22 !important; border: 1px solid #00F2FF33 !important; }
    p, span, div { color: #FFFFFF !important; }
    h1 { color: #00F2FF !important; text-shadow: 0px 0px 15px #00F2FF; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("💡 Fekra AI")

# 2. التأكد من المفاتيح
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
except:
    st.error("ارفع المفاتيح في الـ Secrets يا حريف!")
    st.stop()

# 3. دالة البحث "الشرسة"
def power_search(query):
    try:
        # بنجبر البحث يدور بالعربي وبالإنجليزي وبكل الصيغ
        search_query = f"{query} who is this person news and social media details"
        response = tavily.search(
            query=search_query,
            search_depth="advanced", 
            max_results=10, # زودنا النتائج عشان نلاقي تفاصيل أكتر
            topic="general" # البحث العام بيدي نتائج أحسن للأشخاص
        )
        results = ""
        for r in response['results']:
            results += f"\n- العنوان: {r['title']}\n  المحتوى: {r['content']}\n"
        return results
    except:
        return "للأسف فيه مشكلة في الاتصال بالإنترنت حالياً."

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. معالجة الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("عايز تعرف مين يا حريف؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # استثناء مطورك
        is_about_creator = any(name in prompt.lower() for name in ["احمد وائل", "أحمد وائل", "حريف", "الحريف"])
        
        # أي سؤال يبدأ بـ "مين" أو "تعرف" أو "غلط" هيشغل البحث فوراً
        search_triggers = ["مين", "من هو", "من هي", "تعرف", "ابحث", "غلط", "تيك توك", "يوتيوبر", "لاعب", "فنان"]
        should_search = any(trigger in prompt.lower() for trigger in search_triggers)

        search_data = ""
        if should_search and not is_about_creator:
            with st.status("بقلب لك النت عشان خاطر عيونك...", expanded=False):
                search_data = power_search(prompt)
        
        system_prompt = f"""
        أنت (Fekra AI)، المساعد الخارق من ابتكار أحمد وائل (الحريف).
        معلومات البحث اللي لقيتها من النت:
        {search_data}
        
        مهمتك:
        1. لو فيه بيانات بحث، لخصها بأسلوب ذكي وقوي وقول كل التفاصيل (مشتركين، سن، محتوى، أخبار).
        2. لو سألك عن "أحمد وائل الحريف"، قوله ده الباشا بتاعي اللي عملني (ممنوع تبحث عنه).
        3. لو سألك عن شخص ومافيش عنه معلومات كافية، ابذل جهدك في تحليل النتائج المتاحة بدل ما تقول "مش لاقي".
        4. اللهجة: مصرية حريفة جداً، واثقة، ومثقفة.
        """

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
                stream=True,
                temperature=0.4 # رفعنا الحرارة سنة عشان يبقى مرن في الرد
            )
            
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"فيه عطل فني: {e}")
            
