import streamlit as st
import google.generativeai as genai

# --- 1. 页面极简配置 ---
st.set_page_config(page_title="灵感实验室", layout="centered")

# --- 2. 安全读取与自动清理 (杀灭所有 Key 报错) ---
def init_brain():
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("❌ 还没在 Secrets 里找到钥匙呢！")
        return None
    try:
        # 核心修复：.strip() 会删掉所有看不见的空格，replace 会删掉多余引号
        raw_key = st.secrets["GOOGLE_API_KEY"].strip().replace('"', '').replace("'", "")
        genai.configure(api_key=raw_key)
        # 强制指定最稳的模型
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"🧠 大脑初始化挂了: {e}")
        return None

model = init_brain()

# --- 3. 界面设计 ---
st.title("🧠 灵感提炼实验室")

user_input = st.text_area("输入你的想法：", placeholder="今天有什么新发现？", height=250)

if st.button("✨ 立即智能提炼"):
    if not user_input.strip():
        st.warning("请先写点什么吧！")
    elif not model:
        st.error("AI 引擎没准备好，检查一下钥匙。")
    else:
        with st.spinner('AI 正在接入神经元...'):
            try:
                # 极其简单的指令，降低出错率
                response = model.generate_content(f"请提炼以下内容的逻辑要点：{user_input}")
                if response:
                    st.markdown("---")
                    st.subheader("📝 提炼结果")
                    st.success(response.text)
                    st.balloons()
            except Exception as e:
                st.error("提炼失败了...")
                st.info(f"详细诊断: {str(e)}")

st.caption("Designed by Kary | Powered by Gemini 1.5 Flash")
