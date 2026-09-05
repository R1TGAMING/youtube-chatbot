from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import streamlit as st
from dotenv import load_dotenv
import os
from tools import video_context, process_youtube_video
from core import get_agent

load_dotenv()

## SYSTEM PROMPT
SYSTEM_PROMPT = """
kamu memiliki kemampuan untuk mengambil youtube link yang diberikan oleh user dan gunakan tools yang disediakan. 
jawab dengan singkat, padat dan jelas gunakan bahasa formal.

Tools:
    process_youtube_video -> dict = Process from url youtube video and split to the documents then change it into vector save into chromaDB
    video_context -> dict = Get context from youtube video based on query. Return of the context 
"""


def main():
    # Check the environment
    if os.environ.get("OPENAI_API_KEY") is None:
        print("API KEY is not available")

    # Agent
    llm = ChatOpenAI(base_url=os.environ.get("OPENAI_BASE_URL"), model="cx/gpt-5.5")

    agent = get_agent(
        llm=llm,
        system_prompt=SYSTEM_PROMPT,
        tools=[process_youtube_video, video_context],
    )

    st.title("Youtube Chatbot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(placeholder="Chat here.."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Generating..."):
                response = agent.invoke(
                    {"messages": [HumanMessage(prompt)]},
                    {"configurable": {"thread_id": "user"}},
                )

                st.markdown(response["messages"][-1].content)

        st.session_state.messages.append(
            {"role": "assistant", "content": response["messages"][-1].content}
        )


if __name__ == "__main__":
    main()
