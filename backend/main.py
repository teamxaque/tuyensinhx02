import os
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv

from agent.agent import chat_agent
from agent.session import SessionStore
from openai.agents import Runner

load_dotenv()

app = FastAPI()
session_store = SessionStore()

@app.post("/chat/stream")
async def chat_stream(request: Request):
    body = await request.json()
    user_message = body.get("message")
    session_id = body.get("session_id")

    session_id, history = session_store.get_session(session_id)
    session_store.append(session_id, "user", user_message)

    async def event_generator():
        yield f"event:session\ndata:{session_id}\n\n"

        result = Runner.run_streamed(
            chat_agent,
            input=history + [{"role": "user", "content": user_message}],
        )

        async for event in result.stream_events():
            if event.type == "response.output_text.delta":
                yield f"data:{event.delta}\n\n"

            elif event.type == "tool.call.started":
                yield f"event:tool\ndata:🔧 Đang gọi công cụ...\n\n"

            elif event.type == "response.completed":
                session_store.append(
                    session_id,
                    "assistant",
                    event.response.output_text
                )
                yield f"event:end\ndata:[DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
