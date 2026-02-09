"""
Session Manager
Quản lý sessions và conversation context
"""
from typing import Dict, List
from datetime import datetime
import uuid


class SessionManager:
    """
    Quản lý các session chat và lịch sử hội thoại.
    
    Mỗi session được xác định bởi session_id duy nhất.
    Lưu trữ lịch sử messages để duy trì context trong cuộc trò chuyện.
    """
    
    def __init__(self, max_messages: int = 20):
        """
        Args:
            max_messages: Số lượng messages tối đa lưu trữ cho mỗi session
        """
        self.sessions: Dict[str, List[dict]] = {}
        self.max_messages = max_messages
        self.session_metadata: Dict[str, dict] = {}
    
    def create_session(self) -> str:
        """
        Tạo session mới với ID duy nhất.
        
        Returns:
            session_id: ID của session mới được tạo
        """
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = []
        self.session_metadata[session_id] = {
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "message_count": 0
        }
        return session_id
    
    def get_session(self, session_id: str) -> List[dict]:
        """
        Lấy lịch sử messages của một session.
        
        Args:
            session_id: ID của session
            
        Returns:
            List các messages trong session
        """
        if session_id not in self.sessions:
            # Tạo session mới nếu chưa tồn tại
            self.sessions[session_id] = []
            self.session_metadata[session_id] = {
                "created_at": datetime.now().isoformat(),
                "last_activity": datetime.now().isoformat(),
                "message_count": 0
            }
        
        return self.sessions[session_id]
    
    def add_message(self, session_id: str, role: str, content: str):
        """
        Thêm message mới vào session.
        
        Args:
            session_id: ID của session
            role: Role của message ("user" hoặc "assistant")
            content: Nội dung message
        """
        if session_id not in self.sessions:
            self.get_session(session_id)  # Tạo session nếu chưa tồn tại
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        self.sessions[session_id].append(message)
        
        # Giới hạn số lượng messages để tránh context quá dài
        if len(self.sessions[session_id]) > self.max_messages:
            # Giữ lại max_messages messages gần nhất
            self.sessions[session_id] = self.sessions[session_id][-self.max_messages:]
        
        # Cập nhật metadata
        self.session_metadata[session_id]["last_activity"] = datetime.now().isoformat()
        self.session_metadata[session_id]["message_count"] = len(self.sessions[session_id])
    
    def clear_session(self, session_id: str):
        """
        Xóa toàn bộ lịch sử của một session.
        
        Args:
            session_id: ID của session cần xóa
        """
        if session_id in self.sessions:
            self.sessions[session_id] = []
            self.session_metadata[session_id]["message_count"] = 0
    
    def delete_session(self, session_id: str):
        """
        Xóa hoàn toàn một session.
        
        Args:
            session_id: ID của session cần xóa
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
        if session_id in self.session_metadata:
            del self.session_metadata[session_id]
    
    def get_session_info(self, session_id: str) -> dict:
        """
        Lấy thông tin metadata của session.
        
        Args:
            session_id: ID của session
            
        Returns:
            Dictionary chứa metadata của session
        """
        return self.session_metadata.get(session_id, {})
    
    def list_sessions(self) -> List[str]:
        """
        Lấy danh sách tất cả session IDs.
        
        Returns:
            List các session IDs
        """
        return list(self.sessions.keys())


# Singleton instance
session_manager = SessionManager()
