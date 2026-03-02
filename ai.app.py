import streamlit as st
import google.generativeai as genai

# --- 1. 页面视觉与手机端优化 ---
st.set_page_config(
    page_title="Kary 的灵感实验室",
    page_icon="🧠",
    layout="centered"
)

# 自定义 App 样式，让界面更精致
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
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stTextArea>div>div>textarea {
        border-radius: 12px;
        border: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 载入 AI 大脑 (API Key 安全检查) ---
def load_model():
    try:
        # 从 Streamlit Secrets 中读取钥匙
        if "GOOGLE_API_KEY" not in st.secrets:
            st.error("❌ 未在 Secrets 中找到 GOOGLE_API_KEY，请检查设置。")
            return None
        
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # 修复关键点：使用最稳健的模型名称 'gemini-1.5-flash'
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"❌ AI 初始化失败: {e}")
        return None

model = load_model()

# --- 3. 侧边栏设计（满足你的分组诉求） ---
with st.sidebar:
    st.title("🗂️ 知识分组")
    category = st.selectbox(
        "当前记录至：",
        ["💡 随想灵感", "📖 读书笔记", "🛠️ 工作复盘", "🌟 其他"]
    )
    st.divider()
    st.info("📌 **使用技巧：**\n1. 直接使用手机键盘语音输入。\n2. 点击提炼，AI 会自动整理。\n3. 长按结果即可复制收藏。")

# --- 4. 主界面设计 ---
st.title("🧠 灵感提炼实验室")
st.caption(f"当前分类：{category}")

# 核心输入框
user_input = st.text_area(
    "在这里输入想法，或点击话筒说话：",
    placeholder="今天有什么新感悟？...",
    height=250
)

# 提炼按钮
if st.button("✨ 立即智能提炼"):
    if not model:
        st.error("AI 引擎未就绪，请检查 API Key 配置。")
    elif user_input.strip() == "":
        st.warning("请先输入内容再点击提炼哦！")
    else:
        with st.spinner('AI 正在深度思考并延展知识...'):
            try:
                # 增强版 AI 指令
                prompt = f"""
                你是一个知识管理专家。请对以下内容进行深度处理：
                1. 【核心提炼】：用极简的一句话总结其本质。
                2. 【逻辑要点】：拆解出 3 个核心逻辑点。
                3. 【知识延展】：提供一个相关的深度概念、理论或对比案例。
                
                内容如下：{user_input}
                """
                response = model.generate_content(prompt)
                
                # 展示结果
                if response.text:
                    st.markdown("---")
                    st.subheader("📝 提炼结果")
                    st.success(response.text)
                    st.balloons() # 成功后的小特效
                else:
                    st.error("AI 暂时没有给出回应，请换个描述再试。")
            except Exception as e:
                st.error(f"⚠️ AI 响应失败。请检查 API Key 是否正确。\n(错误详情: {e})")

# --- 5. 页脚 ---
st.divider()
st.caption("Designed by Kary | 灵感实时提炼中")
