"""
Function Tools cho OpenAI Agent
Định nghĩa các công cụ mà Agent có thể sử dụng
"""
from typing import Literal
import random


def get_weather(
    location: str,
    unit: Literal["celsius", "fahrenheit"] = "celsius"
) -> dict:
    """
    Lấy thông tin thời tiết cho một địa điểm.
    
    Tool này mô phỏng việc gọi API thời tiết thực tế.
    Trong production, bạn có thể tích hợp với OpenWeatherMap, WeatherAPI, v.v.
    
    Args:
        location: Tên thành phố hoặc địa điểm (ví dụ: "Hà Nội", "Ho Chi Minh City")
        unit: Đơn vị nhiệt độ - "celsius" hoặc "fahrenheit"
    
    Returns:
        Dictionary chứa thông tin thời tiết:
        - location: Địa điểm
        - temperature: Nhiệt độ
        - condition: Tình trạng thời tiết
        - humidity: Độ ẩm
        - wind_speed: Tốc độ gió
    """
    # Dữ liệu mẫu - trong thực tế sẽ gọi API thật
    conditions = ["Nắng", "Nhiều mây", "Mưa nhẹ", "Mưa", "Sấm sét", "Quang đãng"]
    
    # Sinh dữ liệu ngẫu nhiên để demo
    temp_c = random.randint(20, 35)
    temp_f = int(temp_c * 9/5 + 32)
    
    return {
        "location": location,
        "temperature": temp_f if unit == "fahrenheit" else temp_c,
        "unit": "°F" if unit == "fahrenheit" else "°C",
        "condition": random.choice(conditions),
        "humidity": f"{random.randint(50, 90)}%",
        "wind_speed": f"{random.randint(5, 25)} km/h",
        "forecast": f"Dự báo: {random.choice(conditions)} trong 24h tới"
    }


def search_database(
    query: str,
    category: Literal["all", "products", "users", "orders"] = "all"
) -> list:
    """
    Tìm kiếm thông tin trong database mẫu.
    
    Tool này mô phỏng việc truy vấn database.
    Trong production, bạn có thể kết nối với PostgreSQL, MongoDB, v.v.
    
    Args:
        query: Từ khóa tìm kiếm
        category: Danh mục cần tìm - "all", "products", "users", hoặc "orders"
    
    Returns:
        List các kết quả tìm kiếm, mỗi kết quả là một dictionary
    """
    # Database mẫu
    mock_database = {
        "products": [
            {"id": 1, "name": "Laptop Dell XPS 15", "price": "45,000,000 VNĐ", "stock": 15},
            {"id": 2, "name": "iPhone 15 Pro Max", "price": "35,000,000 VNĐ", "stock": 8},
            {"id": 3, "name": "Samsung Galaxy S24", "price": "25,000,000 VNĐ", "stock": 20},
            {"id": 4, "name": "MacBook Pro M3", "price": "55,000,000 VNĐ", "stock": 5},
            {"id": 5, "name": "iPad Air", "price": "18,000,000 VNĐ", "stock": 12},
        ],
        "users": [
            {"id": 1, "name": "Nguyễn Văn A", "email": "nguyenvana@example.com", "role": "admin"},
            {"id": 2, "name": "Trần Thị B", "email": "tranthib@example.com", "role": "user"},
            {"id": 3, "name": "Lê Văn C", "email": "levanc@example.com", "role": "user"},
            {"id": 4, "name": "Phạm Thị D", "email": "phamthid@example.com", "role": "moderator"},
        ],
        "orders": [
            {"id": 1, "customer": "Nguyễn Văn A", "product": "Laptop Dell XPS 15", "status": "Đã giao"},
            {"id": 2, "customer": "Trần Thị B", "product": "iPhone 15 Pro Max", "status": "Đang xử lý"},
            {"id": 3, "customer": "Lê Văn C", "product": "Samsung Galaxy S24", "status": "Đã giao"},
            {"id": 4, "customer": "Phạm Thị D", "product": "MacBook Pro M3", "status": "Chờ thanh toán"},
        ]
    }
    
    results = []
    query_lower = query.lower()
    
    # Xác định categories cần tìm
    categories_to_search = [category] if category != "all" else ["products", "users", "orders"]
    
    # Tìm kiếm trong từng category
    for cat in categories_to_search:
        if cat in mock_database:
            for item in mock_database[cat]:
                # Tìm kiếm trong tất cả các field của item
                if any(query_lower in str(value).lower() for value in item.values()):
                    results.append({
                        "category": cat,
                        **item
                    })
    
    return results if results else [{"message": f"Không tìm thấy kết quả nào cho '{query}'"}]


# Định nghĩa tools schema cho OpenAI
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Lấy thông tin thời tiết hiện tại cho một địa điểm cụ thể",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Tên thành phố hoặc địa điểm, ví dụ: 'Hà Nội', 'Ho Chi Minh City'"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Đơn vị nhiệt độ"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_database",
            "description": "Tìm kiếm thông tin trong database về sản phẩm, người dùng, hoặc đơn hàng",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Từ khóa tìm kiếm"
                    },
                    "category": {
                        "type": "string",
                        "enum": ["all", "products", "users", "orders"],
                        "description": "Danh mục cần tìm kiếm"
                    }
                },
                "required": ["query"]
            }
        }
    }
]


# Mapping function names to actual functions
TOOL_FUNCTIONS = {
    "get_weather": get_weather,
    "search_database": search_database
}
