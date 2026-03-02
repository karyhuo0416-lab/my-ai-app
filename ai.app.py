import streamlit as st
import google.generativeai as genai

# 1. 页面极简配置
st.set_page_config(page_title="灵感实验室", layout="centered")

# 2. 安全读取 Key（增加自动去空格功能，杀灭 400 错误）
if "GOOGLE_API_KEY" in st.secrets:
    try:
        # 核心修复：.strip() 会删掉你复制 Key 时不小心带上的隐形空格
        raw_key = st.secrets["GOOGLE_API_KEY"].strip().replace('"', '').replace("'", "")
        genai.configure(api_key=raw_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"大脑配置失败：{e}")
else:
    st.error("❌ 请在 Streamlit 控制台配置 GOOGLE_API_KEY")

# 3. 界面设计
st.title("🧠 灵感提炼实验室")

with st.sidebar:
    st.title("🗂️ 分类管理")
    category = st.selectbox("灵感归类：", ["随想", "读书", "工作"])

user_input = st.text_area("输入你的观点：", placeholder="在此输入...", height=200)

if st.button("✨ 立即智能提炼"):
    if user_input.strip():
        with st.spinner('AI 正在深度思考...'):
            try:
                # 使用最直接的提炼指令
                response = model.generate_content(f"请提炼这段内容的逻辑要点：{user_input}")
                st.markdown("---")
                st.success("提炼成功！")
                st.write(response.text)
                st.balloons()
            except Exception as e:
                st.error("AI 响应失败了，请检查 Key 的权限。")
                st.info(f"详细报错：{str(e)}")
    else:
        st.warning("写点什么再提炼吧！")
