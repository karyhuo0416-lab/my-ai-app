import streamlit as st
import google.generativeai as genai

# 1. 界面基础设置
st.set_page_config(page_title="灵感提炼实验室", page_icon="🧠")

# 2. 载入 AI 引擎
try:
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("请在 Settings -> Secrets 中配置 API Key")
    else:
        # 强制配置
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # 使用最稳定的 1.5-flash 模型
        model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"引擎初始化失败: {e}")

# 3. 界面设计
st.title("🧠 灵感提炼实验室")

with st.sidebar:
    st.title("🗂️ 知识分组")
    category = st.selectbox("当前记录至：", ["💡 随想灵感", "📖 读书笔记", "🛠️ 工作复盘"])

user_input = st.text_area("输入你的想法：", placeholder="写下此刻的感悟...", height=200)

if st.button("✨ 立即智能提炼"):
    if not user_input.strip():
        st.warning("写点什么再提炼吧！")
    else:
        with st.spinner('AI 正在思考...'):
            try:
                # 简单直接的指令，成功率最高
                response = model.generate_content(f"请提炼以下内容的逻辑要点：{user_input}")
                st.markdown("---")
                st.subheader("📝 提炼结果")
                st.success(response.text)
                st.balloons()
            except Exception as e:
                st.error("提炼失败了，这通常是 API Key 填写不规范导致。")
                st.info(f"详细错误诊断：{str(e)}")

st.caption(f"分类：{category} | Powered by Gemini 1.5 Flash")
