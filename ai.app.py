import streamlit as st
import google.generativeai as genai

# --- 1. 页面配置 ---
st.set_page_config(page_title="灵感实验室", layout="centered")

# --- 2. 核心修复：安全初始化 ---
def init_brain():
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("❌ 还没在 Secrets 里找到钥匙！")
        return None
    try:
        # 自动清理：去掉引号和多余空格
        key = st.secrets["GOOGLE_API_KEY"].strip().replace('"', '').replace("'", "")
        genai.configure(api_key=key)
        # 强制指定最稳的模型名称
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"🧠 大脑初始化失败: {e}")
        return None

model = init_brain()

# --- 3. 界面设计 ---
st.title("🧠 灵感提炼实验室")

user_input = st.text_area("输入你的想法：", placeholder="今天有什么新感悟？", height=250)

if st.button("✨ 立即智能提炼"):
    if not user_input.strip():
        st.warning("写点什么再提炼吧！")
    elif not model:
        st.error("AI 引擎未就绪。")
    else:
        with st.spinner('正在提炼中...'):
            try:
                # 简单直接的指令，成功率最高
                response = model.generate_content(f"请提炼以下内容的逻辑要点：{user_input}")
                st.markdown("---")
                st.subheader("📝 提炼结果")
                st.success(response.text)
                st.balloons()
            except Exception as e:
                st.error("提炼失败了，这通常是 API Key 权限问题。")
                st.info(f"诊断详情: {str(e)}")

st.caption("Designed by Kary | Powered by Gemini 1.5 Flash")
