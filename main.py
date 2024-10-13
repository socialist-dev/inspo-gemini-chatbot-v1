import google.generativeai as genai
from dotenv import load_dotenv
import os
import streamlit as st

# Tải các biến môi trường từ tệp .env
load_dotenv()

# Cấu hình API key cho Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

INITIAL_RESPONSE = os.getenv("INITIAL_RESPONSE", "Hello! I'm your AI assistant. How can I help you today?")
INITIAL_MSG = os.getenv("INITIAL_MSG", "What do you need help with?")
CHAT_CONTEXT = os.getenv("CHAT_CONTEXT", "You are an AI assistant that helps with various tasks.")


# streamlit page configuration
st.set_page_config(
    page_title="INSPO - AI Productivity Assistant",
    page_icon="https://i.gifer.com/3OqCv.gif",
    layout="centered"
)

# Ẩn menu và footer của Streamlit
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    button[title^=Exit]+div [data-testid=stImage]{
        text-align: center;
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 100%;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Page title
st.image("https://i.gifer.com/3OqCo.gif", use_column_width="always", caption="INSPO™")
st.title("Hello!")
st.write("Today is a good day to work!")
st.caption("INSPO AI Chatbot | Model: gemini-1.5-flash")

# Khởi tạo lịch sử chat trong session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": INITIAL_RESPONSE}
    ]

# Hiển thị lịch sử chat
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "assistant" else "user"
    avatar_url = 'https://pub-821312cfd07a4061bf7b99c1f23ed29b.r2.dev/v1/dynamic/color/flash-dynamic-color.png'
    with st.chat_message(role, avatar=avatar_url):
        st.markdown(message["content"])

# Nhập nội dung từ người dùng
user_prompt = st.chat_input("Try: What I need to do?...")

if user_prompt:
    # Hiển thị tin nhắn của người dùng
    with st.chat_message("user", avatar="🗨️"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt}
    )

    # Gửi yêu cầu đến mô hình Gemini để tạo phản hồi
    model = genai.GenerativeModel("gemini-1.5-flash")
    messages = [
        {"role": "system", "content": CHAT_CONTEXT},
        {"role": "assistant", "content": INITIAL_MSG},
        *st.session_state.chat_history
    ]
    response = model.generate_content(user_prompt)

    # Hiển thị phản hồi của AI
    with st.chat_message("assistant", avatar=avatar_url):
        st.markdown(response.text)
    
    # Lưu phản hồi vào lịch sử
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response.text}
    )
