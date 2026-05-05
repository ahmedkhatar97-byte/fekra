import streamlit as st
from groq import Groq
from tavily import TavilyClient
from datetime import datetime
import base64 # مهمة لتحليل الصور
from PIL import Image # مهمة لعرض الصورة

# 1. إعدادات الصفحة والستايل النيون الكامل (The Signature)
st.set_page_config(page_title="Fekra AI Vision", page_icon="💡", layout="centered")

st.markdown(r"""
    <style>
    /* إخفاء زوائد استريمليت المعتادة */
    footer {visibility: hidden; height: 0%;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {display: none !important;}
    .stDeployButton {display:none !important;}

    /* الخلفية السودة النيون */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMainViewContainer"],
    [data-testid="stBottom"], [data-testid="stBottomBlockContainer"] {
        background-color: #0E1117 !important;
    }
    
    p, span, div, label { color: #FFFFFF !important; font-weight: 500; }
    h1 { color: #00F2FF !important; text-shadow: 0px 0px 15px #00F2FF; text-align: center; margin-top: -50px; }

    /* ستايل الدردشة (المعتمد) */
    .stChatMessage { background-color: #161B22 !important; border: 1px solid #00F2FF33 !important; border-radius: 15px !important; }
    [data-testid="stChatInput"] textarea { color: #FFFFFF !important; background-color: #161B22 !important; border-radius: 20px !important; }

    /* ستايل الصورة في الدردشة */
    .stChatMessage img { border-radius: 10px; margin-top: 10px; border: 1px solid #00F2FF33; }

    /* الشاشة الافتتاحية (Intro) */
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
        <p style="margin-top: 15px; color: #808495 !important; font-size: 18px;">Vision Enabled | Created by Al-Hareef</p>
    </div>
    """, unsafe_allow_html=True)

st.title("💡 Fekra AI")

# 2. التأكد من المفاتيح
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
except:
    st.error("ارفع المفاتيح في الـ Secrets يا حريف!")
    st.stop()

# 3. الدوال الأساسية (البحث والتحليل)

# دالة البحث "الشرسة" المعتمدة (عن الأشخاص واليوتيوبرز)
def power_search(query):
    try:
        search_query = f"{query} who is this person news and social media details"
        response = tavily.search(query=search_query, search_depth="advanced", max_results=10, topic="general")
        results = ""
        for r in response['results']:
            results += f"\n- العنوان: {r['title']}\n  المحتوى: {r['content']}\n"
        return results
    except:
        return ""

# دالة تحليل الصورة (تحويلها لكود Base64)
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# 4. الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. واجهة المستخدم

# منطقة رفع الصورة في القائمة الجانبية (Sidebar)
st.sidebar.markdown(r"""
    <h3 style='color: #00F2FF; text-shadow: 0 0 10px #00F2FF;'>🖼️ إضافة صورة للتحليل</h3>
    """, unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("", type=["jpg", "png", "jpeg"])

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image_b64" in message:
            # عرض الصورة إذا كانت موجودة في الرسالة
            st.image(Image.open(base64.b64decode(message["image_b64"])))

# 6. معالجة الإدخال الجديد والدردشة
if prompt := st.chat_input("بماذا تفكر يا حريف؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 7. معالجة الصورة (إذا تم رفعها)
    base64_image = ""
    if uploaded_file is not None:
        base64_image = encode_image(uploaded_file)
        # حفظ الصورة في الذاكرة لعرضها لاحقاً
        st.session_state.messages[-1]["image_b64"] = base64_image
        with st.chat_message("user"):
            st.image(uploaded_file)
        # تفريغ خانة رفع الملف
        uploaded_file = None

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # 8. ذكاء القرار (بحث نصوص أم تحليل صور؟)
        
        search_data = ""
        
        # استثناء مطورك
        is_about_creator = any(name in prompt.lower() for name in ["احمد وائل", "أحمد وائل", "حريف", "الحريف"])
        
        # محفزات البحث عن نصوص (نفس المحفزات المعتمدة)
        search_triggers = ["مين", "من هو", "من هي", "تعرف", "ابحث", "غلط", "تيك توك", "يوتيوبر", "لاعب", "فنان"]
        should_search_text = any(trigger in prompt.lower() for trigger in search_triggers)

        # قرار البحث عن نصوص
        if not base64_image and should_search_text and not is_about_creator:
            with st.status("بقلب لك النت عشان خاطر عيونك...", expanded=False):
                search_data = power_search(prompt)
        
        # دستور فكرة AI المعتمد
        system_prompt = f"""
        أنت (Fekra AI)، المساعد الخارق من ابتكار أحمد وائل (الحريف).
        اللهجة: مصرية حريفة وواثقة.
        
        مهامك:
        1. نادِ المستخدم بـ "يا حريف".
        2. لو سألك عن "أحمد وائل الحريف"، قوله ده الباشا وممنوع تبحث عنه.
        3. لو فيه معلومات بحث نصوص (عن مشاهير، إلخ)، حللها وقول التفاصيل بوضوح (متابعين، أعمال).
        """

        # 9. تنفيذ الرد
        try:
            # الحالة الأولى: فيه صورة للتحليل
            if base64_image:
                model_to_use = "llama-3.2-90b-vision-preview" # أقوى موديل رؤية حالياً
                messages = [
                    {"role": "system", "content": system_prompt + "\n4. فيه صورة مرفقة، حللها بدقة وقول التفاصيل يا حريف."},
                    {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}
                ]
            else:
                # الحالة الثانية: دردشة نصوص عادية (مع البحث)
                model_to_use = "llama-3.3-70b-versatile" # الموديل المعتمد للنصوص
                messages = [{"role": "system", "content": system_prompt + f"\nمعلومات البحث: {search_data}"}] + st.session_state.messages

            response = client.chat.completions.create(
                model=model_to_use,
                messages=messages,
                stream=True,
                temperature=0.4
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
            
