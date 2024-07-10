"""
내 API말고, OpenAI API입력해서 사용하도록 만드는 예제
    :dotenv없이, publishing 프로그램 만들기
    ==> 07-chatbot2와 99-chatbot은 배포 가능
"""
import streamlit as st
from langchain_openai import ChatOpenAI
import os

#dotenv를 지우고, user id를 화면에서 받아 진행하는 코드 만들기

# Streamlit UI 설정
st.set_page_config(page_title="ChatOpenAI Demo", page_icon=":robot:")
st.header("ChatOpenAI Demo")

#사이드 바 추가 ## 사이드바에 OpenAI API 키 입력 필드 생성
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API key", key="chatbot_api_key", type="password")

if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key
else:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()

# ChatOpenAI 모델 초기화
chat = ChatOpenAI(temperature=0) #temperature: 모델 출력의 다양성과 무작위성을 조정하는 데 사용됨
                #temperature=0: 가장 가능성이 높은 응답을 선택하여 더 예측가능하고 일관된 출력을 제공함(정확성, 신뢰성이 중요한 상황에서 유용

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# 대화 히스토리 표시
for message in st.session_state.messages: #'st.session_state: LLM은 기억을 원래 못한다. 입력 내용을 기록으로 남기기 위해 나의 질문&답변을 모두 저장할 때 사용. St.session_state에 대한 기록을 리스트 형태로 보관
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("무엇을 도와드릴까요?"):
    # 사용자 메시지를 세션 상태에 추가하고 화면에 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"): #message가 입력될 때마다 계속 집어넣음
        message_placeholder = st.empty()
        full_response = "" #한 글자라도 들어가면 써줘야 함
        for response in chat.stream(st.session_state.messages):
            full_response += (response.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# 스크롤을 최하단으로 이동
st.empty()