import streamlit as st
import google.generativeai as genai

# 1. 页面极简配置
st.set_page_config(page_title="灵感提炼实验室", page_icon="🧠", layout="centered")

# 2. 核心修复：安全配置 (自动杀灭 400 和 404 报错)
def init_model():
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("❌ 钥匙没插好！请在 Secrets 检查配置。")
        return None
    try:
        # 【核心修复】：自动删掉粘贴时可能带上的隐形空格、引号
        api_key = st.secrets["GOOGLE_API_KEY"].strip().replace('"', '').replace("'", "")
        genai.configure(api_key=api_key)
        # 强制指定最稳版本，避开 v1beta 的坑
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"大脑初始化失败：{e}")
        return None

model = init_model()

# 3. 界面显示
st.title("🧠 灵感提炼实验室")
user_input = st.text_area("输入你的想法：", placeholder="在此输入你的感悟...", height=200)

if st.button("✨ 立即智能提炼"):
    if not user_input.strip():
        st.warning("写点什么再提炼吧！")
    elif not model:
        st.error("AI 引擎未就绪。")
    else:
        with st.spinner('正在提炼中...'):
            try:
                # 简单直接的指令
                response = model.generate_content(f"请提炼这段话的逻辑和核心：{user_input}")
                st.markdown("---")
                st.success(response.text)
                st.balloons()
            except Exception as e:
                st.error("提炼失败。")
                st.info(f"详细报错信息：{str(e)}")

st.caption("Designed by Kary | Powered by Gemini 1.5 Flash")
