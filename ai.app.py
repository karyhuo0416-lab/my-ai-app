import streamlit as st
import google.generativeai as genai

# --- 1. 页面设置 ---
st.set_page_config(page_title="Kary的灵感实验室", page_icon="🧠")

# 手机端视觉美化
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; background-color: #007AFF; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 载入 AI 引擎 (修复 404 报错的关键) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # 这里我们换成最稳妥的调用方式
    model = genai.GenerativeModel(model_name='gemini-1.5-flash') 
except Exception as e:
    st.error(f"大脑启动失败，请检查配置：{e}")

# --- 3. 侧边栏 ---
with st.sidebar:
    st.title("📂 知识分组")
    category = st.selectbox("当前记录至：", ["💡 随想灵感", "📖 读书笔记", "🛠️ 工作复盘", "🌟 其他"])
    st.divider()
    st.info("提示：直接点击手机键盘的小话筒即可语音输入。")

# --- 4. 主界面 ---
st.title("🧠 灵感提炼实验室")
st.caption(f"当前分类：{category}")

user_input = st.text_area("输入或粘贴你的想法：", height=200, placeholder="写下此刻的灵感...")

if st.button("✨ 立即智能提炼"):
    if user_input:
        with st.spinner('AI 正在翻阅知识库...'):
            try:
                # 增强版指令
                prompt = f"你是一个知识管理专家。请对以下内容进行提炼、逻辑梳理和知识延展。内容如下：{user_input}"
                
                # 修复点：强制使用生成功能
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.subheader("📝 提炼结果")
                st.success(response.text)
                st.balloons() # 成功后撒个花
            except Exception as e:
                # 如果 flash 模型还是不行，我们给出一个备选方案提示
                st.error(f"AI 响应失败。原因：{e}")
                st.info("建议：如果持续报错，可能是 API 密钥权限问题，请确保在 Google AI Studio 中启用了 Gemini 1.5 Flash。")
    else:
        st.warning("请先输入内容哦！")

st.divider()
st.caption("Designed by Kary | 灵感实时提炼中")
