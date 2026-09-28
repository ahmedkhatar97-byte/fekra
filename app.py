 

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
uploaded_file = st.sidebar.file_uploa
