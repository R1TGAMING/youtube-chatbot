from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from tools import video_context, process_youtube_video
from core import get_agent
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn
import os
import asyncio

load_dotenv()


if os.environ.get("OPENAI_API_KEY") is None:
    print("API KEY is not available")

app = FastAPI(debug=True)

## SYSTEM PROMPT
SYSTEM_PROMPT = """
kamu memiliki kemampuan untuk mengambil youtube link yang diberikan oleh user dan gunakan tools yang disediakan. 
jawab dengan singkat, padat dan jelas gunakan bahasa formal.

Tools:
    process_youtube_video -> dict = Process from url youtube video and split to the documents then change it into vector save into chromaDB
    video_context -> dict = Get context from youtube video based on query. Return of the context 
"""

agent = get_agent(
    system_prompt=SYSTEM_PROMPT, tools=[video_context, process_youtube_video]
)


class ChatRequest(BaseModel):
    text: str


class ChatResponse(BaseModel):
    status_code: int
    status: str
    text: str


@app.post("/chat", response_model=ChatResponse)
def chat(chat: ChatRequest):
    try:
        response = agent.invoke(
            {"messages": [HumanMessage(chat.text)]},
            config={"configurable": {"thread_id": "user"}},
        )

        return ChatResponse(
            text=response["messages"][-1].content, status="success", status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/stream")
async def chat_strem(chat: ChatRequest):
    try:
        stream = agent.stream_events(
            {"messages": [HumanMessage(chat.text)]},
            config={"configurable": {"thread_id": "user"}},
            version="v3",
        )

        async def generate_stream():
            for message in stream.messages:
                for token in message.text:
                    yield token
                    await asyncio.sleep(0.5)

        return StreamingResponse(generate_stream(), media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
