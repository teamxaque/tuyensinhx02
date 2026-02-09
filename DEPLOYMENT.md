# Deployment Guide - GitHub & Vercel

Hướng dẫn chi tiết để deploy OpenAI Agent Chat Interface lên GitHub và Vercel.

---

## 📋 Tổng quan

- **Frontend**: Deploy lên Vercel (miễn phí, tự động CI/CD)
- **Backend**: Deploy lên Railway hoặc Render (có free tier)
- **Source Code**: Lưu trữ trên GitHub

---

## 🔧 Phần 1: Chuẩn bị dự án

### 1.1. Cập nhật .gitignore

File `.gitignore` đã được tạo sẵn, đảm bảo các file sau KHÔNG được commit:
- `.env` (chứa API keys)
- `__pycache__/`, `*.pyc`
- `node_modules/`
- `venv/`, `env/`

### 1.2. Tạo file cấu hình production

Các file cấu hình đã được tạo:
- `vercel.json` - Cấu hình Vercel cho Frontend
- `backend/Procfile` - Cấu hình cho Railway/Render
- `backend/runtime.txt` - Chỉ định Python version

---

## 🐙 Phần 2: Push lên GitHub

### 2.1. Khởi tạo Git repository (nếu chưa có)

```bash
cd d:\AI\TuyenSinhX02
git init
git add .
git commit -m "Initial commit: OpenAI Agent Chat Interface"
```

### 2.2. Tạo GitHub repository

1. Truy cập https://github.com/new
2. Tạo repository mới:
   - **Repository name**: `openai-agent-chat`
   - **Description**: "OpenAI Agent Chat Interface with function calling"
   - **Visibility**: Public hoặc Private (tùy chọn)
   - **KHÔNG** chọn "Initialize with README" (vì đã có sẵn)

3. Copy URL của repository (ví dụ: `https://github.com/username/openai-agent-chat.git`)

### 2.3. Push code lên GitHub

```bash
# Thêm remote repository
git remote add origin https://github.com/username/openai-agent-chat.git

# Push code
git branch -M main
git push -u origin main
```

> ⚠️ **Quan trọng**: Đảm bảo file `.env` KHÔNG được push lên GitHub (đã có trong `.gitignore`)

---

## 🚀 Phần 3: Deploy Backend

### Option 1: Railway (Khuyến nghị)

**Ưu điểm:**
- Free tier: $5 credit/tháng
- Tự động deploy từ GitHub
- Hỗ trợ Python tốt
- Dễ setup environment variables

**Các bước:**

1. **Đăng ký Railway**
   - Truy cập https://railway.app
   - Sign up với GitHub account

2. **Tạo New Project**
   - Click "New Project"
   - Chọn "Deploy from GitHub repo"
   - Chọn repository `openai-agent-chat`

3. **Cấu hình deployment**
   - Railway tự động detect Python project
   - Root Directory: `backend`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Setup Environment Variables**
   
   Vào Settings → Variables, thêm:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key
   MODEL_NAME=gpt-4o
   MAX_CONTEXT_MESSAGES=20
   CORS_ORIGINS=https://your-frontend-url.vercel.app
   ```

5. **Deploy**
   - Railway tự động deploy
   - Lấy URL backend (ví dụ: `https://your-app.railway.app`)

### Option 2: Render

**Các bước:**

1. **Đăng ký Render**
   - Truy cập https://render.com
   - Sign up với GitHub

2. **Tạo Web Service**
   - New → Web Service
   - Connect GitHub repository
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables**
   
   Thêm các biến:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key
   MODEL_NAME=gpt-4o
   MAX_CONTEXT_MESSAGES=20
   CORS_ORIGINS=https://your-frontend-url.vercel.app
   ```

4. **Deploy**
   - Render tự động deploy
   - Free tier có giới hạn (sleep sau 15 phút không dùng)

---

## 🎨 Phần 4: Deploy Frontend lên Vercel

### 4.1. Cập nhật API URL trong Frontend

Tạo file `frontend/.env.production`:

```env
VITE_API_URL=https://your-backend-url.railway.app
```

Cập nhật `frontend/src/utils/sseClient.js`:

```javascript
// Thay đổi URL từ localhost sang environment variable
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export function sendChatMessage(message, sessionId, callbacks) {
  const client = new SSEClient(`${API_URL}/api/chat`, {
    // ... rest of code
  });
}
```

### 4.2. Deploy lên Vercel

**Option A: Qua Vercel Dashboard (Dễ nhất)**

1. **Đăng ký Vercel**
   - Truy cập https://vercel.com
   - Sign up với GitHub account

2. **Import Project**
   - Click "Add New..." → "Project"
   - Import repository `openai-agent-chat`

3. **Cấu hình Project**
   - Framework Preset: **Vite**
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

4. **Environment Variables**
   
   Thêm:
   ```
   VITE_API_URL=https://your-backend-url.railway.app
   ```

5. **Deploy**
   - Click "Deploy"
   - Vercel tự động build và deploy
   - Lấy URL (ví dụ: `https://openai-agent-chat.vercel.app`)

**Option B: Qua Vercel CLI**

```bash
# Cài đặt Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel

# Production deploy
vercel --prod
```

### 4.3. Cập nhật CORS trong Backend

Sau khi có URL Vercel, cập nhật environment variable trong Railway/Render:

```
CORS_ORIGINS=https://your-app.vercel.app
```

---

## 🔄 Phần 5: CI/CD Tự động

### 5.1. GitHub Actions (Optional)

Tạo `.github/workflows/deploy.yml` để tự động test trước khi deploy:

```yaml
name: CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          # Add your tests here
          python -c "import main; print('Backend OK')"

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Build
        run: |
          cd frontend
          npm run build
```

### 5.2. Tự động Deploy

- **Vercel**: Tự động deploy khi push lên `main` branch
- **Railway/Render**: Tự động deploy khi push lên `main` branch

---

## ✅ Phần 6: Verification

### 6.1. Kiểm tra Backend

```bash
# Test health endpoint
curl https://your-backend-url.railway.app/api/health

# Expected response:
# {"status":"healthy","model":"gpt-4o","active_sessions":0}
```

### 6.2. Kiểm tra Frontend

1. Truy cập `https://your-app.vercel.app`
2. Gửi tin nhắn test
3. Kiểm tra:
   - ✅ UI hiển thị đúng
   - ✅ Kết nối backend thành công
   - ✅ Streaming hoạt động
   - ✅ Tool calling hoạt động

### 6.3. Kiểm tra CORS

Mở Developer Console, kiểm tra không có lỗi CORS.

---

## 🔒 Phần 7: Bảo mật Production

### 7.1. Environment Variables

- ✅ KHÔNG commit `.env` lên GitHub
- ✅ Sử dụng environment variables trong Railway/Vercel
- ✅ Rotate API keys định kỳ

### 7.2. Rate Limiting (Optional)

Thêm rate limiting vào Backend để tránh abuse:

```python
# backend/main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/chat")
@limiter.limit("10/minute")  # 10 requests per minute
async def chat(request: Request, chat_request: ChatRequest):
    # ... existing code
```

### 7.3. HTTPS

- ✅ Vercel tự động cung cấp HTTPS
- ✅ Railway/Render tự động cung cấp HTTPS

---

## 📊 Phần 8: Monitoring

### 8.1. Vercel Analytics

- Vào Vercel Dashboard → Analytics
- Xem traffic, performance metrics

### 8.2. Railway/Render Logs

- Vào Dashboard → Logs
- Xem real-time logs, errors

### 8.3. OpenAI Usage

- Vào https://platform.openai.com/usage
- Monitor API usage và costs

---

## 🔄 Phần 9: Updates và Maintenance

### 9.1. Update Code

```bash
# Local development
git add .
git commit -m "Update: description of changes"
git push origin main
```

→ Vercel và Railway/Render tự động deploy

### 9.2. Rollback

**Vercel:**
- Dashboard → Deployments
- Chọn deployment trước đó → "Promote to Production"

**Railway:**
- Dashboard → Deployments
- Chọn deployment trước đó → "Redeploy"

---

## 💰 Chi phí ước tính

### Free Tier

- **Vercel**: 
  - ✅ Unlimited deployments
  - ✅ 100GB bandwidth/month
  - ✅ Serverless Functions

- **Railway**:
  - ✅ $5 credit/month
  - ✅ ~500 hours runtime

- **OpenAI API**:
  - ⚠️ Pay-per-use
  - GPT-4o: ~$2.50/1M input tokens, ~$10/1M output tokens

### Ước tính chi phí thực tế

Với ~1000 messages/tháng:
- Vercel: **$0** (free tier)
- Railway: **$0** (trong free tier)
- OpenAI: **~$5-10/tháng** (tùy usage)

**Tổng: ~$5-10/tháng**

---

## 🆘 Troubleshooting

### Lỗi: "Build failed" trên Vercel

- Kiểm tra `package.json` có đúng dependencies
- Kiểm tra Node version (cần 18+)
- Xem build logs để debug

### Lỗi: "Application Error" trên Railway

- Kiểm tra logs trong Dashboard
- Verify environment variables
- Kiểm tra `Procfile` và start command

### Lỗi: CORS

- Cập nhật `CORS_ORIGINS` trong backend
- Thêm đầy đủ URL Vercel (bao gồm https://)

### Lỗi: "OpenAI API Error"

- Kiểm tra API key có đúng không
- Verify API key có quyền truy cập GPT-4o
- Kiểm tra billing trong OpenAI dashboard

---

## 📚 Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Render Documentation](https://render.com/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)

---

## ✅ Checklist Deploy

- [ ] Push code lên GitHub
- [ ] Deploy Backend lên Railway/Render
- [ ] Setup environment variables cho Backend
- [ ] Lấy Backend URL
- [ ] Cập nhật Frontend với Backend URL
- [ ] Deploy Frontend lên Vercel
- [ ] Setup environment variables cho Frontend
- [ ] Cập nhật CORS trong Backend
- [ ] Test production deployment
- [ ] Setup monitoring
- [ ] Document production URLs

---

**Chúc bạn deploy thành công! 🚀**
