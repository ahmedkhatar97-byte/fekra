import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
from datetime import datetime
import json
import os
from duckduckgo_search import DDGS

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="Fekra AI", page_icon="💡", layout="centered")

# --- نظام الذاكرة ---
def load_mem():
    if os.path.exists("memory.json"):
        try:
            with open("memory.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"user_name": "يا حريف"}

if "user_name" not in st.session_state:
    st.session_state.user_name = load_mem()["user_name"]

# 2. الستايل النيون وحل مشكلة السكرول (بدون أخطاء برمجية)
# استخدمنا r قبل النص البرمجي لمنع مشاكل علامات التنصيص
st.markdown(r"""
<style>
    /* إخفاء القوائم الافتراضية */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* الخلفية النيون ومنع الريستارت */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0E1117 !important;
        overscroll-behavior-y: none !important;
    }

    /* جعل منطقة الشات قابلة للسكرول الانسيابي */
    [data-testid="stMainViewContainer"] {
        overflow-y: auto !important;
        scroll-behavior: smooth;
    }

    /* تصميم رسائل الشات النيون */
    .stChatMessage {
        background: #161B22 !important;
        border: 1px solid #00F2FF33 !important;
        border-radius: 15px !important;
        box-shadow: 0 0 10px #00F2FF11;
        margin-bottom: 10px;
    }

    /* زرار الصعود للأعلى النيون */
    #scrollToTopBtn {
        position: fixed;
        right: 20px;
        bottom: 110px;
        width: 50px;
        height: 50px;
        background: transparent;
        border: 2px solid #00F2FF;
        border-radius: 50%;
        color: #00F2FF;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0 0 15px #00F2FF, inset 0 0 10px #00F2FF;
        cursor: pointer;
        z-index: 999999;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: 0.3s;
    }
    #scrollToTopBtn:hover { background: #00F2FF33; }

    /* شاشة الدخول */
    #splash {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: #0E1117; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 9999;
        animation: out 2.2s forwards; pointer-events: none;
    }
    @keyframes out { 0%, 80% {opacity: 1;} 100% {opacity: 0; visibility: hidden;} }
    
    h1 { color: #00F2FF !important; text-shadow: 0 0 15px #00F2FF; text-align: center; }
    p, span, div { color: #FFF !important; }
</style>

<div id="splash">
    <div style="font-size: 50px; color: #00F2FF; text-shadow: 0 0 20px #00F2FF;">💡 FEKRA AI</div>
    <p style="color: #808495 !important; margin-top: 15px;">Designed by Harreef</p>
</div>

<button id="scrollToTopBtn" onclick="window.parent.postMessage('scroll_to_top', '*')">↑</button>
""", unsafe_allow_html=True)

# جافا سكريبت الصعود للأعلى (ربط مباشر بالصفحة الأم)
components.html("""
<script>
    window.parent.addEventListener('message', function(e) {
        if (e.data === 'scroll_to_top') {
            const container = window.parent.document.querySelector('[data-testid="stMainViewContainer"]');
            if (container) {
                container.scrollTo({top: 0, behavior: 'smooth'});
            }
        }
    });
</script>
""", height=0)

# 3. المنطق البرمجي (بناء الشات)
st.title("💡 Fekra AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض تاريخ المحادثة
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# إدخال المستخدم
if prompt := st.chat_input("بماذا تفكر يا حريف؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            # محرك البحث (مفعل فقط عند الضرورة)
            s_info = ""
            search_keywords = ["بحث", "اخبار", "سعر", "مين هو", "اخر تطورات"]
            if any(w in prompt.lower() for w in search_keywords):
                with DDGS() as ddgs:
                    results = [r['body'] for r in ddgs.text(prompt, max_results=3)]
                    s_info = "\n".join(results)

            # تعليمات صارمة للموديل لمنع الصيني والرموز الغريبة
            sys_p = f"""أنت Fekra AI، مساعد ذكي متطور صممك أحمد وائل الحريف. 
            نادِ المستخدم بـ: {st.session_state.user_name}. 
            تحدث بلهجة مصرية سليمة 100%. 
            ممنوع منعاً باتاً استخدام حروف صينية، يابانية، أو رموز غير مفهومة. 
            تأكد من خلو ردودك من أي أخطاء إملائية. الوقت الحالي: {datetime.now().strftime('%I:%M %p')}."""
            
            history = [{"role": "system", "content": sys_p}] + st.session_state.messages[:-1]
            history.append({"role": "user", "content": f"{prompt}\n\n[Context]: {s_info}"})
            
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=history, stream=True)
            
            full_r = ""
            p_holder = st.empty()
            for chunk in res:
                if chunk.choices[0].delta.content:
                    full_r += chunk.choices[0].delta.content
                    p_holder.markdown(full_r + "▌")
            p_holder.markdown(full_r)
            st.session_state.messages.append({"role": "assistant", "content": full_r})
            
        except Exception as e:
            st.error(f"عذراً يا حريف، حصل خطأ في الاتصال: {e}")
            
