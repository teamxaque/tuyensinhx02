"""
Configuration Management
Quản lý các biến môi trường và cấu hình hệ thống
"""
import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Cấu hình ứng dụng từ environment variables"""
    
    # OpenAI Configuration
    openai_api_key: str
    model_name: str = "gpt-4o"
    
    # Session Management
    max_context_messages: int = 20
    
    # CORS Configuration
    cors_origins: str = "http://localhost:5173"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Chuyển đổi CORS origins string thành list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Singleton instance
settings = Settings()
