import streamlit as st
import google.generativeai as genai

# 获取你在 Streamlit 设置中填写的 API Key
api_key = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("💡 我的灵感提炼库")
user_input = st.text_area("输入或语音转文字：", height=150)

if st.button("✨ 立即提炼"):
    if user_input:
        with st.spinner('AI 思考中...'):
            prompt = f"你是一个知识管理专家。请提炼以下内容的核心观点、逻辑要点和知识延展：{user_input}"
            response = model.generate_content(prompt)
            st.info(response.text)
    else:
        st.warning("内容不能为空哦！")
