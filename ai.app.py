import streamlit as st
import google.generativeai as genai

# --- 1. 页面设置 ---
st.set_page_config(page_title="灵感实验室", layout="centered")

# --- 2. 核心修复：安全配置 (强制剔除多余符号) ---
def init_ai():
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("❌ 钥匙没插好！请去 Secrets 检查配置。")
        return None
    try:
        # 自动清洗：去掉可能误带的引号、空格、换行符
        raw_key = st.secrets["GOOGLE_API_KEY"].strip().replace('"', '').replace("'", "")
        genai.configure(api_key=raw_key)
        # 强制指定 gemini-1.5-flash，不加任何 models/ 前缀
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"大脑启动失败：{e}")
        return None

model = init_ai()

# --- 3. 界面设计 ---
st.title("🧠 灵感提炼实验室")
user_input = st.text_area("输入你的观点：", placeholder="今天有什么新发现？", height=250)

if st.button("✨ 立即智能提炼"):
    if not user_input.strip():
        st.warning("写点什么吧！")
    elif not model:
        st.error("AI 引擎未准备好。")
    else:
        with st.spinner('正在接入神经元...'):
            try:
                # 简单直接的指令
                response = model.generate_content(f"请提炼这段话的逻辑和核心：{user_input}")
                st.markdown("---")
                st.success(response.text)
                st.balloons()
            except Exception as e:
                # 如果还是报错，这里会打印出最真实的后台原因
                st.error("提炼失败。")
                st.info(f"病根在这里：{str(e)}")
