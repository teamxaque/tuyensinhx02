# 🎓 TuyenSinhX02 - Chatbot Tư vấn Tuyển sinh

Chatbot AI hỗ trợ tư vấn tuyển sinh cho Bộ Công an, sử dụng OpenAI Agent SDK với khả năng tìm kiếm tài liệu và trả lời câu hỏi dựa trên dữ liệu tuyển sinh chính thức.

## 🌟 Tính năng

- ✅ Tích hợp OpenAI Agent SDK với File Search
- ✅ Streaming responses qua Server-Sent Events (SSE)
- ✅ Quản lý session để duy trì lịch sử hội thoại
- ✅ Giao diện chat hiện đại, responsive
- ✅ Hỗ trợ nhúng vào website khác qua iframe
- ✅ Deploy backend lên Render, frontend lên Vercel

## 📁 Cấu trúc dự án

```
TuyenSinhX02/
├── backend/
│   ├── agent/
│   │   ├── agent.py          # Định nghĩa OpenAI Agent
│   │   └── session.py        # Quản lý session
│   ├── main.py               # FastAPI server
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile           # Docker configuration
│   └── .env.example         # Environment variables template
├── frontend/
│   ├── index.html           # Chat interface
│   └── vercel.json          # Vercel deployment config
├── render.yaml              # Render deployment config
└── README.md
```

## 🚀 Cài đặt Local

### Backend

1. **Clone repository và di chuyển vào thư mục backend:**
   ```bash
   cd d:\AI\TuyenSinhX02\backend
   ```

2. **Tạo virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

3. **Cài đặt dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Tạo file `.env` từ template:**
   ```bash
   copy .env.example .env
   ```

5. **Cập nhật `.env` với API key của bạn:**
   ```env
   OPENAI_API_KEY=sk-your-actual-api-key-here
   VECTOR_STORE_ID=vs_6985d783d1f4819198426676c1a25886
   ```

6. **Chạy server:**
   ```bash
   uvicorn main:app --reload
   ```

   Server sẽ chạy tại: `http://localhost:8000`

### Frontend

1. **Mở file `frontend/index.html` trong trình duyệt**

2. **Hoặc sử dụng Live Server (VS Code extension):**
   - Cài đặt extension "Live Server"
   - Right-click vào `index.html` → "Open with Live Server"

3. **Cập nhật backend URL nếu cần:**
   - Mở `index.html`
   - Tìm dòng: `const BACKEND_URL = window.BACKEND_URL || "https://tuyensinhx02.onrender.com";`
   - Đổi thành: `const BACKEND_URL = "http://localhost:8000";` cho local testing

## 🌐 Deployment

### Deploy Backend lên Render

1. **Push code lên GitHub**

2. **Tạo Web Service trên Render:**
   - Đăng nhập vào [Render](https://render.com)
   - Click "New" → "Web Service"
   - Connect GitHub repository
   - Render sẽ tự động phát hiện `render.yaml`

3. **Thêm Environment Variables:**
   - Vào Dashboard → Environment
   - Thêm `OPENAI_API_KEY` với giá trị thực

4. **Deploy:**
   - Render sẽ tự động build và deploy
   - URL sẽ có dạng: `https://tuyensinhx02.onrender.com`

### Deploy Frontend lên Vercel

1. **Cài đặt Vercel CLI (optional):**
   ```bash
   npm install -g vercel
   ```

2. **Deploy qua Vercel Dashboard:**
   - Đăng nhập vào [Vercel](https://vercel.com)
   - Click "Add New" → "Project"
   - Import GitHub repository
   - Set Root Directory: `frontend`
   - Deploy

3. **Hoặc deploy qua CLI:**
   ```bash
   cd frontend
   vercel
   ```

4. **Cập nhật backend URL:**
   - Sau khi có URL backend từ Render
   - Cập nhật trong `index.html`:
     ```javascript
     const BACKEND_URL = "https://your-backend-url.onrender.com";
     ```
   - Commit và push để Vercel tự động redeploy

## 🔧 API Documentation

### POST `/chat/stream`

Gửi tin nhắn và nhận response streaming qua SSE.

**Request Body:**
```json
{
  "message": "Tôi muốn biết về ngành An ninh mạng",
  "session_id": "uuid-or-null"
}
```

**Response:** Server-Sent Events stream

**Events:**
- `session`: Trả về session ID
- `tool`: Thông báo khi agent đang sử dụng tool
- `data`: Delta text của response
- `end`: Kết thúc stream
- `error`: Thông báo lỗi

**Example:**
```
event: session
data: 123e4567-e89b-12d3-a456-426614174000

event: tool
data: 🔧 Đang tra cứu tài liệu...

data: Chào bạn! 
data: Ngành An ninh mạng...

event: end
data: [DONE]
```

## 🎨 Nhúng Chatbot vào Website

Thêm code sau vào website của bạn:

```html
<iframe 
  src="https://your-frontend-url.vercel.app" 
  width="400" 
  height="600" 
  frameborder="0"
  style="border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
</iframe>
```

Hoặc tạo popup chatbot:

```html
<button onclick="openChat()">💬 Tư vấn tuyển sinh</button>

<div id="chat-popup" style="display:none; position:fixed; bottom:20px; right:20px; z-index:9999;">
  <iframe 
    src="https://your-frontend-url.vercel.app" 
    width="400" 
    height="600" 
    frameborder="0"
    style="border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.2);">
  </iframe>
</div>

<script>
function openChat() {
  document.getElementById('chat-popup').style.display = 'block';
}
</script>
```

## 🛠️ Troubleshooting

### Backend không khởi động được

- **Lỗi:** `ModuleNotFoundError: No module named 'agents'`
  - **Giải pháp:** Cài đặt lại dependencies: `pip install -r requirements.txt`

- **Lỗi:** `openai.AuthenticationError`
  - **Giải pháp:** Kiểm tra `OPENAI_API_KEY` trong file `.env`

### Frontend không kết nối được backend

- **Lỗi CORS:** Kiểm tra CORS middleware đã được thêm vào `main.py`
- **Backend URL sai:** Kiểm tra `BACKEND_URL` trong `index.html`
- **Render service đang sleep:** Free tier của Render sẽ sleep sau 15 phút không hoạt động, request đầu tiên sẽ mất ~30s để wake up

### Tin nhắn không hiển thị

- Mở Developer Console (F12) để xem lỗi
- Kiểm tra Network tab để xem SSE connection
- Verify session ID được trả về đúng

## 📝 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key | ✅ Yes | - |
| `VECTOR_STORE_ID` | Vector store ID từ OpenAI | ✅ Yes | `vs_6985d783d1f4819198426676c1a25886` |

## 🔐 Security Notes

- ⚠️ Không commit file `.env` lên Git
- ⚠️ Trong production, cấu hình CORS chỉ cho phép origins cụ thể
- ⚠️ Rotate API keys định kỳ
- ⚠️ Sử dụng HTTPS cho cả backend và frontend

## 📄 License

MIT License - Free to use for educational purposes.

## 👥 Support

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra phần Troubleshooting ở trên
2. Xem logs trên Render Dashboard
3. Kiểm tra Browser Console để debug frontend

---

**Phát triển bởi:** Team TuyenSinhX02  
**Công nghệ:** OpenAI Agent SDK, FastAPI, Vanilla JS
