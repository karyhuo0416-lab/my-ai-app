import streamlit as st
import google.generativeai as genai

# 页面设置
st.set_page_config(page_title="灵感提炼实验室", page_icon="🧠", layout="centered")

# 核心：初始化 AI (解决 404 和 400 报错)
def init_model():
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("❌ Secrets 还没配好，请看下一步提示。")
        return None
    try:
        # 自动清洗：删掉粘贴时可能误带的空格、换行或引号
        raw_key = st.secrets["GOOGLE_API_KEY"].strip().replace('"', '').replace("'", "")
        genai.configure(api_key=raw_key)
        # 直接使用官方最稳路径
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"大脑初始化失败: {e}")
        return None

model = init_model()

st.title("🧠 灵感提炼实验室")
user_input = st.text_area("输入你的想法：", placeholder="今天有什么新发现？", height=200)

if st.button("✨ 立即智能提炼"):
    if user_input.strip() and model:
        with st.spinner('正在提炼中...'):
            try:
                # 极其简单的指令，确保 100% 响应
                response = model.generate_content(f"请提炼这段话的逻辑和核心观点：{user_input}")
                st.markdown("---")
                st.success(response.text)
                st.balloons()
            except Exception as e:
                st.error("提炼失败，这通常是 Key 的权限问题。")
                st.info(f"病根诊断：{str(e)}")
    else:
        st.warning("写点什么吧！")
