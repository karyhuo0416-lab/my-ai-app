import streamlit as st
import google.generativeai as genai

# --- 1. 页面设置 ---
st.set_page_config(page_title="Kary的灵感实验室", page_icon="🧠", layout="centered")

# 手机端视觉美化（让它看起来像个真 App）
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; background-color: #007AFF; color: white; height: 3em; font-weight: bold; border: none; }
    .stTextArea>div>div>textarea { border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 启动 AI 引擎 (修复 404 错误的关键) ---
try:
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("❌ 未在 Secrets 中找到 GOOGLE_API_KEY，请检查设置。")
    else:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        # 使用最标准的模型名称
        model = genai.GenerativeModel('gemini-1.5-flash') 
except Exception as e:
    st.error(f"大脑启动失败：{e}")

# --- 3. 侧边栏（你的分类收藏功能） ---
with st.sidebar:
    st.title("🗂️ 知识分组")
    category = st.selectbox("当前记录至：", ["💡 随想灵感", "📖 读书笔记", "🛠️ 工作复盘", "🌟 其他"])
    st.divider()
    st.info("📌 使用技巧：\n1. 直接使用手机语音输入。\n2. 点击提炼，AI 会自动整理。\n3. 长按结果即可复制收藏。")

# --- 4. 主界面 ---
st.title("🧠 灵感提炼实验室")
st.caption(f"当前分类：{category}")

user_input = st.text_area("输入想法或粘贴内容：", height=200, placeholder="写下此刻的感悟...")

if st.button("✨ 立即智能提炼"):
    if user_input.strip():
        with st.spinner('AI 正在深度思考中...'):
            try:
                # 设定 AI 专家指令
                prompt = f"""
                你是一个知识管理专家。请对以下内容进行深度处理：
                1. 【核心提炼】：用极简的一句话总结其本质。
                2. 【逻辑要点】：拆解出 3 个核心逻辑点。
                3. 【知识延展】：提供一个相关的理论、心理学概念或深度案例。
                
                内容：{user_input}
                """
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.subheader("📝 提炼结果")
                # 成功显示结果
                st.success(response.text)
                st.balloons() # 撒花庆祝
            except Exception as e:
                st.error("AI 响应失败，可能需要检查 API Key 是否有权限使用 1.5 Flash。")
                st.info(f"详细错误：{e}")
    else:
        st.warning("请先输入内容哦！")

# --- 5. 页脚 ---
st.divider()
st.caption("Designed by Kary | 灵感实时提炼中")
