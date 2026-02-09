"""
FastAPI Main Application
API endpoints cho OpenAI Agent Chat Interface
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import json

from config import settings
from agent import agent_manager
from session_manager import session_manager


# Khởi tạo FastAPI app
app = FastAPI(
    title="OpenAI Agent Chat API",
    description="Backend API cho Chat Interface với OpenAI Agent SDK",
    version="1.0.0"
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models cho request/response
class Message(BaseModel):
    """Model cho một message trong chat"""
    role: str  # "user" hoặc "assistant"
    content: str


class ChatRequest(BaseModel):
    """Model cho chat request"""
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Model cho chat response (non-streaming)"""
    response: str
    session_id: str


# ==================== ENDPOINTS ====================

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "OpenAI Agent Chat API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "chat": "/api/chat",
            "health": "/api/health",
            "sessions": "/api/sessions"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model": settings.model_name,
        "active_sessions": len(session_manager.list_sessions())
    }


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Chat endpoint với streaming response.
    
    Nhận tin nhắn từ user, xử lý qua Agent, và stream response về.
    Hỗ trợ function calling và session management.
    """
    try:
        # Lấy hoặc tạo session
        session_id = request.session_id
        if not session_id:
            session_id = session_manager.create_session()
        
        # Thêm user message vào session
        session_manager.add_message(session_id, "user", request.message)
        
        # Lấy lịch sử hội thoại
        messages = session_manager.get_session(session_id)
        
        # Chuẩn bị messages cho OpenAI (chỉ lấy role và content)
        openai_messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in messages
        ]
        
        # Generator function cho SSE
        async def event_generator():
            """Generator để stream events về client"""
            accumulated_response = ""
            
            try:
                # Gửi session_id ngay lập tức
                yield f"data: {json.dumps({'type': 'session', 'session_id': session_id})}\n\n"
                
                # Stream từ Agent
                for event in agent_manager.chat_stream(openai_messages, session_id):
                    event_type = event["type"]
                    
                    if event_type == "text":
                        # Text chunk
                        accumulated_response += event["content"]
                        yield f"data: {json.dumps(event)}\n\n"
                    
                    elif event_type == "tool_call_start":
                        # Bắt đầu gọi tool
                        yield f"data: {json.dumps(event)}\n\n"
                    
                    elif event_type == "tool_call":
                        # Tool call với arguments
                        yield f"data: {json.dumps(event)}\n\n"
                    
                    elif event_type == "tool_result":
                        # Kết quả từ tool
                        yield f"data: {json.dumps(event)}\n\n"
                    
                    elif event_type == "done":
                        # Hoàn thành - lưu assistant response vào session
                        if accumulated_response:
                            session_manager.add_message(
                                session_id,
                                "assistant",
                                accumulated_response
                            )
                        yield f"data: {json.dumps(event)}\n\n"
                    
                    elif event_type == "error":
                        # Lỗi
                        yield f"data: {json.dumps(event)}\n\n"
                
                # Gửi event kết thúc
                yield "data: [DONE]\n\n"
            
            except Exception as e:
                error_event = {
                    "type": "error",
                    "content": f"Stream error: {str(e)}"
                }
                yield f"data: {json.dumps(error_event)}\n\n"
        
        # Trả về StreamingResponse với SSE
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"  # Disable nginx buffering
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sessions")
async def list_sessions():
    """Lấy danh sách tất cả sessions"""
    sessions = session_manager.list_sessions()
    return {
        "sessions": [
            {
                "session_id": sid,
                "info": session_manager.get_session_info(sid)
            }
            for sid in sessions
        ]
    }


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Lấy thông tin chi tiết của một session"""
    messages = session_manager.get_session(session_id)
    info = session_manager.get_session_info(session_id)
    
    return {
        "session_id": session_id,
        "info": info,
        "messages": messages
    }


@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    """Xóa một session"""
    session_manager.delete_session(session_id)
    return {"message": f"Session {session_id} deleted successfully"}


@app.post("/api/sessions/{session_id}/clear")
async def clear_session(session_id: str):
    """Xóa lịch sử chat của một session nhưng giữ session"""
    session_manager.clear_session(session_id)
    return {"message": f"Session {session_id} cleared successfully"}


# ==================== STARTUP/SHUTDOWN ====================

@app.on_event("startup")
async def startup_event():
    """Chạy khi server khởi động"""
    print("🚀 OpenAI Agent Chat API is starting...")
    print(f"📦 Model: {settings.model_name}")
    print(f"🌐 CORS Origins: {settings.cors_origins_list}")


@app.on_event("shutdown")
async def shutdown_event():
    """Chạy khi server tắt"""
    print("👋 OpenAI Agent Chat API is shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
