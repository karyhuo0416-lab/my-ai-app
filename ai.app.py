import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="灵感实验室", layout="centered")

# 大脑初始化逻辑
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # 强制指定稳定版模型
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("请在 Settings -> Secrets 中配置 API Key")
except Exception as e:
    st.error(f"大脑连不上: {e}")

st.title("🧠 灵感提炼实验室")

# 侧边栏分组（虽然目前不存数据库，但视觉先给到）
with st.sidebar:
    st.title("🗂️ 分组")
    category = st.selectbox("选择分类", ["💡 随想", "📖 笔记", "🛠️ 工作"])

user_input = st.text_area("输入你的想法：", height=200)

if st.button("✨ 立即提炼"):
    if user_input.strip():
        with st.spinner('AI 正在思考...'):
            try:
                # 简单直接的指令，成功率最高
                response = model.generate_content(f"请提炼以下内容的逻辑要点：{user_input}")
                st.success("提炼成功！")
                st.write(response.text)
                st.balloons()
            except Exception as e:
                st.error("提炼失败了...")
                st.info(f"请检查 Key 是否有效。具体原因：{e}")
    else:
        st.warning("写点什么吧！")
