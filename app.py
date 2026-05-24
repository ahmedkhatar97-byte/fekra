import streamlit as st
from groq import Groq
from tavily import TavilyClient
from datetime import datetime
import base64 # مهمة لتحليل الصور
from PIL import Image # مهمة لعرض الصورة

# 1. إعدادات الصفحة والستايل النيون الكامل المتطور (The Signature v2)
st.set_page_config(page_title="Fekra AI Vision v2", page_icon="💡", layout="centered")

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

    /* ستايل الدردشة المطور */
    .stChatMessage { background-color: #161B22 !important; border: 1px solid #00F2FF33 !important; border-radius: 15px !important; }
    [data-testid="stChatInput"] textarea { color: #FFFFFF !important; background-color: #161B22 !important; border-radius: 20px !important; }

    /* ستايل الصورة في الدردشة */
    .stChatMessage img { border-radius: 10px; margin-top: 10px; border: 1px solid #00F2FF33; }

    /* --- الأنيميشن النيون الجديد المتطور (The New Splash Screen Animation) --- */
    #splash-screen {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #0E1117;
        display: flex; flex-direction: column;
        justify-content: center; align-items: center;
        z-index: 9999;
        animation: fadeOut 2.8s cubic-bezier(0.1, 0.8, 0.25, 1) forwards;
        pointer-events: none;
    }
    
    /* أنيميشن نبض النيون وتقريب الاسم */
    @keyframes neonPulse {
        0%, 100% { text-shadow: 0 0 15px #00F2FF, 0 0 30px #00F2FF; transform: scale(0.98); }
        50% { text-shadow: 0 0 30px #00F2FF, 0 0 60px #00F2FF, 0 0 80px #00F2FF; transform: scale(1.02); }
    }
    
    @keyframes fadeOut {
        0% { opacity: 1; }
        85% { opacity: 1; }
        100% { opacity: 0; visibility: hidden; }
    }
    
    .neon-text-new {
        font-size: 55px;
        color: #00F2FF;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 900;
        letter-spacing: 2px;
        animation: neonPulse 1.5s infinite ease-in-out;
    }

    /* شريط تحميل نيون سفلي ناعم */
    .loader-bar {
        width: 200px;
        height: 3px;
        background: rgba(0, 242, 255, 0.1);
        margin-top: 25px;
        border-radius: 10px;
        overflow: hidden;
        position: relative;
    }
    .loader-progress {
        width: 100%;
        height: 100%;
        background: #00F2FF;
        box-shadow: 0 0 10px #00F2FF;
        position: absolute;
        transform: translateX(-100%);
        animation: loading 2.2s ease-in-out forwards;
    }
    @keyframes loading {
        0% { transform: translateX(-100%); }
        50% { transform: translateX(-30%); }
        100% { transform: translateX(0%); }
    }
    </style>

    <div id="splash-screen">
        <div class="neon-text-new">💡 FEKRA AI</div>
        <p style="margin-top: 15px; color: #808495 !important; font-size: 16px; letter-spacing: 1px;">SYSTEM READY | CREATED BY AL-HAREEF</p>
        <div class="loader-bar">
            <div class="loader-progress"></div>
        </div>
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
def power_search(query):
    try:
        # تحسين الكويري عشان يجيب معلومات حقيقية ومحدثة عن الشخصية المشهورة
        search_query = f"{query} biography profile news updates"
        response = tavily.search(query=search_query, search_depth="advanced", max_results=8, topic="general")
        results = ""
        for r in response['results']:
            results += f"\n- العنوان: {r['title']}\n  المحتوى: {r['content']}\n"
        return results
    except:
        return ""

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# 4. الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. واجهة المستخدم
st.sidebar.markdown(r"""
    <h3 style='color: #00F2FF; text-shadow: 0 0 10px #00F2FF;'>🖼️ إضافة صورة للتحليل</h3>
    """, unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("", type=["jpg", "png", "jpeg"])

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image_b64" in message:
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
        st.session_state.messages[-1]["image_b64"] = base64_image
        with st.chat_message("user"):
            st.image(uploaded_file)
        uploaded_file = None

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        search_data = ""
        
        # كشف ذكي متطور لاسم المطور لضمان السرية والأمان الكامل
        is_about_creator = any(name in prompt.lower() for name in ["احمد وائل", "أحمد وائل", "حريف", "الحريف", "elhareef"])
        
        # محفزات البحث عن الشخصيات المشهورة أو المعلومات العامة
        search_triggers = ["مين", "من هو", "من هي", "تعرف", "ابحث", "غلط", "تيك توك", "يوتيوبر", "لاعب", "فنان", "مشخصية", "مشاهير"]
        should_search_text = any(trigger in prompt.lower() for trigger in search_triggers)

        if not base64_image and should_search_text and not is_about_creator:
            with st.status("بقلب لك النت عشان خاطر عيونك وجايبلك الخلاصة الحقيقية...", expanded=False):
                search_data = power_search(prompt)
        
        # دستور فكرة AI المتطور - نسخة صفر أخطاء إملائية وتنظيم كامل
        system_prompt = f"""
        أنت (Fekra AI)، المساعد الخارق والذكاء الاصطناعي الأكثر تطوراً وتنظيماً من ابتكار المبرمج أحمد وائل الحريف.
        اللهجة الحالية: مصرية حريفة، ذكية، واثقة، ومرحة.
        
        ⚠️ قواعد صارمة لمنع الأخطاء الإملائية واللغوية:
        - راجع الكلمات لغوياً وإملائياً قبل كتابتها؛ ممنوع تماماً إنتاج كلمات مكسرة، أو حروف ناقصة، أو دمج كلمات ببعضها.
        - اكتب العامية المصرية بطريقة صحيحة ومفهومة (مثل كتابة "عشان" بدلاً من "عسأن"، و"بصورة" بدلاً من "بصوره").
        
        قواعد التنسيق والترتيب الإلزامية:
        - ممنوع نهائياً كتابة الإجابة كلها ككتلة نصية واحدة (دش كلام).
        - استخدم العناوين الكبيرة والفرعية (مثل ## و ###) لتقسيم الموضوعات بوضوح.
        - استخدم الخطوط الفاصلة (---) للفصل بين الأفكار الرئيسية.
        - استخدم القوائم النقطية (*) لعرض العناصر والمعلومات بطريقة يسهل قراءتها في لمح البصر.
        - استخدم الخط العريض (**الكلمة**) لتمييز المصطلحات الهامة والعبارات المفتاحية.
        
        القواعد العامة:
        1. نادِ المستخدم دائمًا بـ "يا حريف".
        2. أحمد وائل الحريف هو صانعك ومطورك الأساسي، لو سألك عنه المستخدم أو تلمح له بأي شكل، قوله بكل فخر واعتزاز: "ده الباشا الكبير ومطور فكرة وممنوع البحث عنه لأن بياناته مشفرة تماماً!".
        3. التزم ببيانات البحث المرفقة التزاماً تاماً لتقديم معلومات حقيقية وصحيحة وصادقة عن الشخصيات المشهورة، وممنوع التأليف أو قول كلام عشوائي بدون دليل من السيرش.
        """

        # 9. تنفيذ الرد
        try:
            if base64_image:
                model_to_use = "llama-3.2-90b-vision-preview"
                messages = [
                    {"role": "system", "content": system_prompt + "\n4. فيه صورة مرفقة، حللها بدقة متناهية، ونظم إجابتك بعناوين ونقاط واضحة، والتزم تماماً بصفر أخطاء إملائية بأسلوب حريف."},
                    {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}
                ]
            else:
                model_to_use = "llama-3.3-70b-versatile"
                # هنا التعديل: لو فيه بيانات بحث، بنحقنها مباشرة في الـ System عشان الـ Model يبني عليها الرد وميخرفش
                current_system = system_prompt
                if search_data:
                    current_system += f"\n\n🚨 [معلومات بحث حقيقية ومحدثة]:\n{search_data}\n\nتنبيه: يجب استخدام هذه البيانات فقط للإجابة عن الشخصية المطلوبة بشكل دقيق وبدون أي تزييف."
                
                messages = [{"role": "system", "content": current_system}] + st.session_state.messages

            response = client.chat.completions.create(
                model=model_to_use,
                messages=messages,
                stream=True,
                temperature=0.3 # قللنا الـ temperature شوية عشان نزود الدقة والالتزام بالبيانات
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
            
