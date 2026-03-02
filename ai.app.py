import streamlit as st
import google.generativeai as genai

# --- 页面基础设置 ---
st.set_page_config(page_title="Kary的灵感实验室", page_icon="🧠")

# --- 载入 AI 引擎 ---
def init_model():
    try:
        # 从 Secrets 读取 Key
        key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=key)
        # 强制指定模型，不带任何前缀
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"大脑连不上线：{e}")
        return None

model = init_model()

# --- 侧边栏 ---
with st.sidebar:
    st.title("🗂️ 知识分组")
    category = st.selectbox("当前记录至：", ["💡 随想灵感", "📖 读书笔记", "🛠️ 工作复盘"])

# --- 主界面 ---
st.title("🧠 灵感提炼实验室")
user_input = st.text_area("输入你的想法：", placeholder="今天有什么新发现？", height=200)

if st.button("✨ 立即智能提炼"):
    if not user_input.strip():
        st.warning("请先写点什么吧！")
    elif not model:
        st.error("AI 引擎未就绪")
    else:
        with st.spinner('正在提炼...'):
            try:
                # 极其简单的 Prompt 确保响应率
                prompt = f"请对以下内容进行核心提炼和逻辑梳理：{user_input}"
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.subheader("📝 提炼结果")
                st.success(response.text)
                st.balloons()
            except Exception as e:
                # 这里会打印出最真实的报错原因
                st.error("AI 响应失败了。")
                st.info(f"详细错误诊断：{str(e)}")

st.caption(f"当前分类：{category} | Powered by Gemini 1.5 Flash")
