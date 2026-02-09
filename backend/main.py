import os
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from agent.agent import chat_agent
from agent.session import SessionStore
from agents import Runner

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_store = SessionStore()

@app.get("/")
async def root():
    return {"status": "ok", "message": "TuyenSinhX02 Agent API"}

@app.post("/chat/stream")
async def chat_stream(request: Request):
    try:
        body = await request.json()
        user_message = body.get("message")
        session_id = body.get("session_id")

        if not user_message:
            return {"error": "Message is required"}, 400

        session_id, history = session_store.get_session(session_id)
        
        async def event_generator():
            try:
                # Send session ID first
                yield f"event: session\ndata: {session_id}\n\n"

                # Build conversation history
                conversation_history = []
                for msg in history:
                    conversation_history.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
                
                # Add current user message
                conversation_history.append({
                    "role": "user",
                    "content": user_message
                })

                # Run agent with streaming
                result = Runner.run_streamed(
                    chat_agent,
                    input=conversation_history,
                )

                assistant_response = ""

                async for event in result.stream_events():
                    if event.type == "response.output_text.delta":
                        assistant_response += event.delta
                        yield f"data: {event.delta}\n\n"

                    elif event.type == "tool.call.started":
                        yield f"event: tool\ndata: 🔧 Đang tra cứu tài liệu...\n\n"

                    elif event.type == "response.completed":
                        # Save to session
                        session_store.append(session_id, "user", user_message)
                        session_store.append(session_id, "assistant", assistant_response)
                        yield f"event: end\ndata: [DONE]\n\n"

            except Exception as e:
                yield f"event: error\ndata: Lỗi: {str(e)}\n\n"

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
