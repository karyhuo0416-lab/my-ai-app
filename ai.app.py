import streamlit as st
import google.generativeai as genai

# 页面基础设置
st.set_page_config(page_title="灵感实验室", page_icon="🧠")

# 从 Secrets 获取并配置 Key
if "GOOGLE_API_KEY" in st.secrets:
    try:
        # 清除 Key 左右可能存在的空格（这是导致 400 报错的常见原因）
        api_key = st.secrets["GOOGLE_API_KEY"].strip()
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"AI 配置失败: {e}")
else:
    st.error("❌ 未在 Secrets 中找到 GOOGLE_API_KEY")

st.title("🧠 灵感提炼实验室")

user_input = st.text_area("输入你的想法：", height=200, placeholder="粘贴文字或点击话筒输入...")

if st.button("✨ 立即智能提炼"):
    if user_input.strip():
        with st.spinner('AI 正在思考中...'):
            try:
                # 简单直接的指令，成功率最高
                response = model.generate_content(f"请提炼这段话的逻辑和核心观点：{user_input}")
                st.markdown("---")
                st.success("提炼成功！")
                st.write(response.text)
                st.balloons()
            except Exception as e:
                st.error("提炼失败了。")
                st.info(f"详细原因：{str(e)}")
    else:
        st.warning("写点什么再提炼吧！")
