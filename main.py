from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import YoutubeLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

## SYSTEM PROMPT
SYSTEM_PROMPT = """
kamu memiliki kemampuan untuk mengambil youtube link yang diberikan oleh user dan gunakan tools yang disediakan. 
jawab dengan singkat, padat dan jelas gunakan bahasa formal.

Tools:
    process_youtube_video -> dict = Process from url youtube video and split to the documents then change it into vector save into chromaDB
    video_context -> dict = Get context from youtube video based on query. Return of the context 
"""


## PRELOAD
def embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name="google/embeddinggemma-300m",
        encode_kwargs={"normalize_embeddings": True},
    )


def chroma(embeddings_model: HuggingFaceEmbeddings) -> Chroma:
    return Chroma(
        collection_name="youtube_data",
        embedding_function=embeddings_model,
        persist_directory="./chroma",
    )


@st.cache_resource
def get_agent(llm: ChatOpenAI, tools: list[any], system_prompt: str):
    return create_agent(
        model=llm,
        system_prompt=system_prompt,
        tools=tools,
        checkpointer=InMemorySaver(),
    )


## TOOLS FUNCTION
@tool
def process_youtube_video(youtube_url: str | list[str]) -> dict:
    """Process from url youtube video or list of url and split to the documents then change it into vector save into chromaDB

    Args:
        youtube_url: str | list[str] = list of youtube url
    """

    try:
        all_documents = []

        if isinstance(youtube_url, str):
            youtube_url = [youtube_url]

        for url in youtube_url:
            loader = YoutubeLoader.from_youtube_url(url, language=["id", "en"])
            documents = loader.load_and_split(
                text_splitter=RecursiveCharacterTextSplitter(
                    chunk_size=1000, chunk_overlap=100
                )
            )
            all_documents.extend(documents)

        embeddings_model = embeddings()
        vector = chroma(embeddings_model=embeddings_model)
        vector.add_documents(all_documents)

        return {
            "status": "success",
            "message": f"{len(documents)} Documents added to ChromaDB",
        }
    except Exception as e:
        return {"status": "error", "message": f"error processing: {str(e)}"}


@tool
def video_context(query: str, filter: dict[str, str] | None) -> dict:
    """Get context from youtube video based on query. Return of the context

    Args:
        query: str = query for the context
        filter: dict[str, str] | None = filter from metadata
    """
    try:

        embeddings_model = embeddings()
        vector = chroma(embeddings_model=embeddings_model)

        query_similarity = vector.similarity_search(query=query, filter=filter)

        return {"status": "success", "context": query_similarity}
    except Exception as e:
        return {"status": "error", "messages": e}


def main():
    # Check the environment
    if os.environ.get("OPENAI_API_KEY") is None:
        print("API KEY is not available")

    # Agent
    llm = ChatOpenAI(base_url="http://localhost:20128/v1", model="cx/gpt-5.5")

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
