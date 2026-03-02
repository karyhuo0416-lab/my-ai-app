import streamlit as st
import google.generativeai as genai

# --- 1. 页面视觉设置 ---
st.set_page_config(
    page_title="Kary 的灵感实验室",
    page_icon="🧠",
    layout="centered"
)

# 自定义 App 样式（手机端适配）
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 3.5em;
        background-color: #007AFF;
        color: white;
        font-weight: bold;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 载入 AI 大脑 (API Key) ---
try:
    # 从 Streamlit Secrets 读取
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # 使用最稳定的模型名称，修复 NotFound 报错
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"⚠️ 配置出错了：{e}")

# --- 3. 侧边栏设计（分组功能） ---
with st.sidebar:
    st.title("🗂️ 知识分组")
    category = st.selectbox(
        "当前记录至：",
        ["💡 随想灵感", "📖 读书笔记", "🛠️ 工作复盘", "🌟 其他"]
    )
    st.divider()
    st.info("📌 使用技巧：\n1. 直接使用手机语音输入。\n2. 点击提炼，AI 会自动整理。")

# --- 4. 主界面设计 ---
st.title("🧠 灵感提炼实验室")
st.caption(f"当前分类：{category}")

user_input = st.text_area(
    "输入你的想法：",
    placeholder="今天有什么新感悟？...",
    height=200
)

if st.button("✨ 立即智能提炼"):
    if user_input:
        with st.spinner('AI 正在思考中...'):
            try:
                # 设定 AI 的提炼逻辑
                prompt = f"你是一个知识管理专家。请对以下内容进行：1.核心提炼 2.要点拆解 3.知识延展。内容：{user_input}"
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.subheader("📝 提炼结果")
                st.success(response.text)
                st.balloons() # 成功撒花
            except Exception as e:
                st.error(f"AI 响应失败，请检查 API Key：{e}")
    else:
        st.warning("请先输入内容哦！")
