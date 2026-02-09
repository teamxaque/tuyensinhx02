# OpenAI Agent Chat Interface

[![CI/CD](https://github.com/username/openai-agent-chat/actions/workflows/ci.yml/badge.svg)](https://github.com/username/openai-agent-chat/actions)
[![Deploy](https://img.shields.io/badge/Deploy-Vercel-black?logo=vercel)](https://your-app.vercel.app)

> 🤖 Hệ thống Chat Interface tích hợp OpenAI Agent SDK với function calling, streaming responses, và giao diện hiện đại.

## 🌟 Demo

- **Live Demo**: [https://your-app.vercel.app](https://your-app.vercel.app)
- **API Backend**: [https://your-backend.railway.app](https://your-backend.railway.app)

## ✨ Tính năng

- 🤖 **OpenAI Agent SDK** - GPT-4o với function calling
- 🛠️ **Smart Tools** - Weather API & Database Search
- 📡 **Real-time Streaming** - Server-Sent Events (SSE)
- 💾 **Session Management** - Context-aware conversations
- 🎨 **Modern UI** - Dark theme với glassmorphism
- 📝 **Markdown Support** - Syntax highlighting cho code
- 🔧 **Tool Visualization** - Hiển thị tool execution

## 🚀 Quick Start

### Development

```bash
# Clone repository
git clone https://github.com/username/openai-agent-chat.git
cd openai-agent-chat

# Setup environment
cp .env.template .env
# Thêm OPENAI_API_KEY vào .env

# Backend
cd backend
pip install -r requirements.txt
python main.py

# Frontend (terminal mới)
cd frontend
npm install
npm run dev
```

Xem chi tiết trong [QUICKSTART.md](QUICKSTART.md)

## 📦 Tech Stack

**Backend:**
- FastAPI
- OpenAI Agent SDK
- Python 3.10+
- SSE Streaming

**Frontend:**
- React 18
- Vite
- React Markdown
- Lucide Icons

**Deployment:**
- Vercel (Frontend)
- Railway/Render (Backend)
- GitHub Actions (CI/CD)

## 📖 Documentation

- [📘 Quick Start Guide](QUICKSTART.md) - Hướng dẫn nhanh
- [📗 Deployment Guide](DEPLOYMENT.md) - Deploy lên production
- [📙 Walkthrough](walkthrough.md) - Chi tiết implementation

## 🏗️ Architecture

```
User → React Frontend → FastAPI Backend → OpenAI Agent → GPT-4o
                              ↓
                        Session Manager
                              ↓
                          Tools Layer
                    (Weather, Database)
```

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```env
OPENAI_API_KEY=sk-your-key
MODEL_NAME=gpt-4o
MAX_CONTEXT_MESSAGES=20
CORS_ORIGINS=http://localhost:5173
```

**Frontend (.env.production):**
```env
VITE_API_URL=https://your-backend-url.railway.app
```

## 🌐 Deployment

### Deploy Frontend (Vercel)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/username/openai-agent-chat)

### Deploy Backend (Railway)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template)

Xem chi tiết trong [DEPLOYMENT.md](DEPLOYMENT.md)

## 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest

# Frontend build test
cd frontend
npm run build
```

## 📊 Project Structure

```
openai-agent-chat/
├── backend/              # FastAPI backend
│   ├── main.py          # API endpoints
│   ├── agent.py         # OpenAI Agent
│   ├── tools.py         # Function tools
│   └── ...
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # UI components
│   │   └── utils/       # SSE client
│   └── ...
├── .github/             # GitHub Actions
├── DEPLOYMENT.md        # Deployment guide
└── README.md           # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- OpenAI for the Agent SDK
- FastAPI for the amazing framework
- React team for the UI library

## 📧 Contact

- GitHub: [@username](https://github.com/username)
- Email: your.email@example.com

---

**Built with ❤️ using OpenAI Agent SDK, FastAPI, and React**
