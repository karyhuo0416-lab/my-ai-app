import streamlit as st
import google.generativeai as genai

# --- 1. 页面样式与手机端适配 ---
st.set_page_config(page_title="Kary的灵感实验室", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3.5em;
        background-color: #007AFF;
        color: white;
        font-weight: bold;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 载入 AI 引擎 (修复 404 错误的关键) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # 使用通用的模型标识符，AI 库会自动映射到最新版本
    model = genai.GenerativeModel('gemini-1.5-flash') 
except Exception as e:
    st.error(f"大脑启动失败，请检查 Secrets 配置：{e}")

# --- 3. 侧边栏（你的分类收藏功能） ---
with st.sidebar:
    st.title("🗂️ 知识分组")
    category = st.selectbox(
        "当前记录至：", 
        ["💡 随想灵感", "📖 读书笔记", "🛠️ 工作复盘", "🌟 其他"]
    )
    st.divider()
    st.info("📌 使用技巧：\n1. 直接使用手机键盘语音输入。\n2. 点击提炼，AI 会自动整理。\n3. 长按下方结果即可复制收藏。")

# --- 4. 主界面设计 ---
st.title("🧠 灵感提炼实验室")
st.caption(f"当前分类：{category}")

user_input = st.text_area(
    "粘贴想法或点击话筒说话：", 
    placeholder="今天有什么感悟？在此写下...", 
    height=200
)

if st.button("✨ 立即智能提炼"):
    if user_input.strip():
        with st.spinner('AI 正在深度思考并延展知识...'):
            try:
                # 设定 AI 专家角色和指令
                prompt = f"""
                你是一个知识管理专家。请对以下内容进行深度处理：
                1. 【核心提炼】：用极简的一句话总结其本质。
                2. 【逻辑要点】：拆解出 3 个核心逻辑点。
                3. 【知识延展】：提供一个相关的理论、心理学概念或深度案例。
                
                内容：{user_input}
                """
                response = model.generate_content(prompt)
                
                # 美化结果展示
                st.markdown("---")
                st.subheader("📝 提炼结果")
                st.success(response.text)
                st.balloons() # 成功撒花
            except Exception as e:
                st.error(f"AI 响应失败。可能是 API 权限问题。")
                st.info(f"错误详情：{e}")
    else:
        st.warning("请先输入内容再点击提炼哦！")

# --- 5. 页脚 ---
st.divider()
st.caption("Designed by Kary | 灵感实时提炼中")
