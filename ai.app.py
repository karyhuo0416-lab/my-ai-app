import streamlit as st
import google.generativeai as genai
import os

# --- 1. 页面设置 ---
st.set_page_config(page_title="Kary的灵感实验室", page_icon="🧠", layout="centered")

# 手机端视觉美化
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; background-color: #007AFF; color: white; height: 3.5em; font-weight: bold; border: none; }
    .stTextArea>div>div>textarea { border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 启动 AI 引擎 (修复 404 报错的关键) ---
try:
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("❌ 未在 Secrets 中找到密钥，请检查 Streamlit 设置。")
    else:
        api_key = st.secrets["GOOGLE_API_KEY"]
        # 核心修复点：明确初始化设置
        genai.configure(api_key=api_key)
        
        # 修复点：直接使用模型简称，系统会自动匹配最新稳定版
        model = genai.GenerativeModel('gemini-1.5-flash') 
except Exception as e:
    st.error(f"大脑启动失败：{e}")

# --- 3. 侧边栏 ---
with st.sidebar:
    st.title("🗂️ 知识分组")
    category = st.selectbox("当前记录至：", ["💡 随想灵感", "📖 读书笔记", "🛠️ 工作复盘", "🌟 其他"])
    st.divider()
    st.info("📌 使用技巧：\n1. 直接使用手机语音输入。\n2. 点击提炼，AI 会自动整理。")

# --- 4. 主界面 ---
st.title("🧠 灵感提炼实验室")
st.caption(f"当前分类：{category}")

user_input = st.text_area("输入你的想法：", height=200, placeholder="写下此刻的灵感...")

if st.button("✨ 立即智能提炼"):
    if user_input.strip():
        with st.spinner('AI 正在接入神经元...'):
            try:
                # 设定指令
                prompt = f"你是一个知识管理专家。请对以下内容进行核心提炼、逻辑梳理和知识延展。内容：{user_input}"
                
                # 调用生成
                response = model.generate_content(prompt)
                
                if response.text:
                    st.markdown("---")
                    st.subheader("📝 提炼结果")
                    st.success(response.text)
                    st.balloons() # 撒花庆祝
            except Exception as e:
                # 最后的容错提示
                st.error("AI 响应失败，这通常是 API 权限或版本不匹配。")
                st.info(f"详细错误详情（请截图给我）：{str(e)}")
    else:
        st.warning("请先输入内容哦！")

# --- 5. 页脚 ---
st.divider()
st.caption("Designed by Kary | 灵感实时提炼中")
