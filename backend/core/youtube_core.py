from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
import os


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


def get_agent(tools: list[any], system_prompt: str):
    llm = ChatOpenAI(
        base_url=os.environ.get("OPENAI_BASE_URL"),
        model=os.environ.get("OPENAI_BASE_MODEL"),
    )

    return create_agent(
        model=llm,
        system_prompt=system_prompt,
        tools=tools,
        checkpointer=InMemorySaver(),
    )
