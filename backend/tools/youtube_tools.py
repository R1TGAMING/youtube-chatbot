from langchain.tools import tool
from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from core import embeddings, chroma


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
