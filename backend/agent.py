"""
OpenAI Agent Module
Khởi tạo và quản lý OpenAI Agent với function calling
"""
from openai import OpenAI
from typing import Generator, Dict, Any
import json

from config import settings
from tools import TOOLS, TOOL_FUNCTIONS


class AgentManager:
    """
    Quản lý OpenAI Agent với khả năng function calling và streaming.
    """
    
    def __init__(self):
        """Khởi tạo OpenAI client và cấu hình Agent"""
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.model_name
        
        # Instructions cho Agent (System prompt)
        self.instructions = """Bạn là một trợ lý AI thông minh và hữu ích, có khả năng sử dụng các công cụ để hỗ trợ người dùng.

Nhiệm vụ của bạn:
1. Trả lời câu hỏi của người dùng một cách chính xác và hữu ích
2. Sử dụng các công cụ (tools) khi cần thiết để cung cấp thông tin chính xác
3. Giải thích rõ ràng kết quả từ các công cụ
4. Giao tiếp bằng tiếng Việt một cách tự nhiên và thân thiện

Các công cụ bạn có thể sử dụng:
- get_weather: Lấy thông tin thời tiết cho một địa điểm
- search_database: Tìm kiếm thông tin về sản phẩm, người dùng, hoặc đơn hàng

Hãy luôn:
- Trả lời ngắn gọn, súc tích nhưng đầy đủ thông tin
- Sử dụng Markdown để format câu trả lời (headings, lists, code blocks, v.v.)
- Khi sử dụng công cụ, hãy giải thích kết quả một cách dễ hiểu
- Thân thiện và chuyên nghiệp
"""
    
    def chat_stream(
        self,
        messages: list,
        session_id: str
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Xử lý chat request với streaming response.
        
        Args:
            messages: Lịch sử hội thoại (list of message dicts)
            session_id: ID của session hiện tại
            
        Yields:
            Dictionary chứa streaming events:
            - type: "text" | "tool_call" | "tool_result" | "done" | "error"
            - content: Nội dung tương ứng
        """
        try:
            # Chuẩn bị messages với system instruction
            full_messages = [
                {"role": "system", "content": self.instructions}
            ] + messages
            
            # Gọi OpenAI API với streaming
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                tools=TOOLS,
                stream=True,
                temperature=0.7
            )
            
            # Biến để theo dõi tool calls
            current_tool_calls = {}
            accumulated_content = ""
            
            for chunk in stream:
                if not chunk.choices:
                    continue
                
                delta = chunk.choices[0].delta
                finish_reason = chunk.choices[0].finish_reason
                
                # Xử lý text content
                if delta.content:
                    accumulated_content += delta.content
                    yield {
                        "type": "text",
                        "content": delta.content
                    }
                
                # Xử lý tool calls
                if delta.tool_calls:
                    for tool_call in delta.tool_calls:
                        idx = tool_call.index
                        
                        if idx not in current_tool_calls:
                            current_tool_calls[idx] = {
                                "id": "",
                                "name": "",
                                "arguments": ""
                            }
                        
                        if tool_call.id:
                            current_tool_calls[idx]["id"] = tool_call.id
                        
                        if tool_call.function.name:
                            current_tool_calls[idx]["name"] = tool_call.function.name
                            # Thông báo bắt đầu gọi tool
                            yield {
                                "type": "tool_call_start",
                                "content": {
                                    "name": tool_call.function.name
                                }
                            }
                        
                        if tool_call.function.arguments:
                            current_tool_calls[idx]["arguments"] += tool_call.function.arguments
                
                # Khi finish, xử lý tool calls nếu có
                if finish_reason == "tool_calls" and current_tool_calls:
                    # Thực thi các tool calls
                    tool_messages = []
                    
                    for tool_call in current_tool_calls.values():
                        function_name = tool_call["name"]
                        function_args = json.loads(tool_call["arguments"])
                        
                        # Gọi function
                        if function_name in TOOL_FUNCTIONS:
                            yield {
                                "type": "tool_call",
                                "content": {
                                    "name": function_name,
                                    "arguments": function_args
                                }
                            }
                            
                            function_response = TOOL_FUNCTIONS[function_name](**function_args)
                            
                            yield {
                                "type": "tool_result",
                                "content": {
                                    "name": function_name,
                                    "result": function_response
                                }
                            }
                            
                            # Thêm vào messages để gọi lại API
                            tool_messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call["id"],
                                "content": json.dumps(function_response, ensure_ascii=False)
                            })
                    
                    # Gọi lại API với kết quả từ tools
                    if tool_messages:
                        # Thêm assistant message với tool calls
                        full_messages.append({
                            "role": "assistant",
                            "content": None,
                            "tool_calls": [
                                {
                                    "id": tc["id"],
                                    "type": "function",
                                    "function": {
                                        "name": tc["name"],
                                        "arguments": tc["arguments"]
                                    }
                                }
                                for tc in current_tool_calls.values()
                            ]
                        })
                        
                        # Thêm tool responses
                        full_messages.extend(tool_messages)
                        
                        # Gọi lại API để lấy final response
                        second_stream = self.client.chat.completions.create(
                            model=self.model,
                            messages=full_messages,
                            stream=True,
                            temperature=0.7
                        )
                        
                        for second_chunk in second_stream:
                            if second_chunk.choices and second_chunk.choices[0].delta.content:
                                content = second_chunk.choices[0].delta.content
                                accumulated_content += content
                                yield {
                                    "type": "text",
                                    "content": content
                                }
                
                # Khi hoàn thành
                if finish_reason == "stop":
                    yield {
                        "type": "done",
                        "content": accumulated_content
                    }
        
        except Exception as e:
            yield {
                "type": "error",
                "content": str(e)
            }


# Singleton instance
agent_manager = AgentManager()
