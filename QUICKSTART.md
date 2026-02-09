# 🚀 Quick Start Guide

## Bước 1: Cài đặt Dependencies

### Backend
```bash
cd backend
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
```

## Bước 2: Cấu hình API Key

Mở file `.env` và thay đổi:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here  # ⚠️ THAY ĐỔI DÒNG NÀY
```

Lấy API key tại: https://platform.openai.com/api-keys

## Bước 3: Chạy ứng dụng

### Terminal 1 - Backend
```bash
cd backend
python main.py
```
✅ Backend chạy tại: http://localhost:8000

### Terminal 2 - Frontend  
```bash
cd frontend
npm run dev
```
✅ Frontend chạy tại: http://localhost:5173

## Bước 4: Sử dụng

Mở trình duyệt: http://localhost:5173

### Thử các tính năng:

**1. Chat thông thường:**
```
"Xin chào! Bạn có thể làm gì?"
```

**2. Kiểm tra thời tiết:**
```
"Thời tiết ở Hà Nội thế nào?"
```
→ Agent sẽ gọi tool `get_weather`

**3. Tìm kiếm database:**
```
"Tìm sản phẩm laptop"
```
→ Agent sẽ gọi tool `search_database`

**4. Code generation:**
```
"Viết code Python để tính giai thừa"
```
→ Kết quả có syntax highlighting

## 🐛 Troubleshooting

### Lỗi: "OPENAI_API_KEY not found"
→ Kiểm tra file `.env` có đúng API key chưa

### Lỗi: "Port 8000 already in use"
→ Đóng process đang dùng port 8000 hoặc đổi port trong `main.py`

### Frontend không kết nối Backend
→ Kiểm tra Backend đang chạy tại http://localhost:8000
→ Kiểm tra CORS_ORIGINS trong `.env`

## 📚 Tài liệu đầy đủ

Xem [README.md](README.md) và [walkthrough.md](walkthrough.md) để biết thêm chi tiết.

---

**Chúc bạn thành công! 🎉**
