import streamlit as st
import google.generativeai as genai

# --- 1. 页面极简配置 ---
st.set_page_config(page_title="灵感实验室", layout="centered")

# 自定义样式：蓝色大按钮
st.markdown("""
    <style>
    .stButton>button {
        width: 100%; border-radius: 15px; height: 3.5em;
        background-color: #007AFF; color: white; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 安全读取 Key（增加自动去空格功能，杀灭 400 错误） ---
def init_model():
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("❌ 请在 Streamlit 控制台配置 Secrets")
        return None
    try:
        # 核心修复点：使用 .strip() 彻底删除复制 Key 时可能带上的隐形空格
        key = st.secrets["GOOGLE_API_KEY"].strip().strip('"').strip("'")
        genai.configure(api_key=key)
        # 修复 404 错误：直接指定模型名称
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"大脑配置失败：{e}")
        return None

model = init_model()

# --- 3. 界面设计 ---
st.title("🧠 灵感提炼实验室")

with st.sidebar:
    st.title("🗂️ 分类管理")
    category = st.selectbox("记录至：", ["随想灵感", "读书笔记", "工作复盘"])
    st.info("提示：直接点击手机键盘话筒即可语音输入。")

user_input = st.text_area("输入你的观点：", placeholder="在此输入你的感悟...", height=200)

if st.button("✨ 立即智能提炼"):
    if not user_input.strip():
        st.warning("写点什么再提炼吧！")
    elif not model:
        st.error("AI 引擎未就绪，请检查 Secrets 配置。")
    else:
        with st.spinner('正在提炼中...'):
            try:
                # 使用最直接的提炼指令
                response = model.generate_content(f"你是一个知识专家，请提炼以下内容的逻辑要点和深度延展：{user_input}")
                st.markdown("---")
                st.success("提炼成功！")
                st.write(response.text)
                st.balloons() # 成功特效
            except Exception as e:
                st.error("提炼失败了，这通常是 API Key 填写错误。")
                st.info(f"详细报错：{str(e)}")

st.caption(f"当前分类：{category} | Designed by Kary")
