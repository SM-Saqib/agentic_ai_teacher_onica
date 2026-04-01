# AI Teacher - Intelligent Teaching Platform

> An open-source, self-hosted AI-powered teaching platform combining pre-built educational content, real-time LLM interactions, and advanced voice/avatar interfaces.

## 🚀 Quick Overview

**AI Teacher** is a comprehensive platform designed to revolutionize student learning through:

- 🤖 **AI-Powered Responses**: Integration with local LLM models (Mistral, Llama 2) via Ollama
- 📚 **Pre-Built Curriculum**: Pre-written explanations for slides + RAG for knowledge retrieval
- 🎙️ **Voice Interface**: Speech-to-text and text-to-speech capabilities
- 👤 **Avatar System**: Tiered avatar experience (basic → premium → enterprise)
- ⚡ **Real-time Communication**: WebSocket-based architecture for instant responses
- 🏗️ **Modular Architecture**: Zero-cost monolithic backend designed for future microservice extraction

## 📋 Phase 1: Foundation (Complete ✅)

### ✅ Completed Tasks

1. **Backend Structure** - FastAPI-based modular architecture with 11+ specialized modules
2. **Frontend Setup** - React 18 with TypeScript, Redux, and Tailwind CSS
3. **Database & Models** - PostgreSQL schema with 10+ SQLAlchemy models
4. **Authentication** - JWT-based access/refresh tokens with secure password hashing
5. **WebSocket Infrastructure** - Real-time event-based messaging system
6. **Docker Compose** - Complete containerized environment (PostgreSQL, Redis, ChromaDB, FastAPI, React)

## 🛠 Technology Stack (100% OPEN-SOURCE)

| Component | Tool | Cost |
|-----------|------|------|
| Backend Framework | FastAPI | Free |
| Database | PostgreSQL | Free |
| Vector Store | ChromaDB / Qdrant | Free |
| LLM | Ollama + Mistral/Llama2 | Free |
| Cache | Redis | Free |
| Frontend | React 18 + TypeScript | Free |
| Build Tool | Vite | Free |
| Container | Docker | Free |

## 💰 Annual Savings vs Proprietary Stack

**$7,400+/year saved** by using open-source alternatives to OpenAI APIs, Pinecone, and hosted services!

## 🚀 Getting Started

### Quick Start (Docker)
```bash
cd /workspaces/agentic_ai_teacher_onica
docker-compose up -d
docker-compose exec backend alembic upgrade head

# Access:
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

### Local Development

**Backend:**
```bash
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt && alembic upgrade head
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend && npm install && npm run dev
```

## 📁 Project Structure

```
backend/              # FastAPI application
├── app/              # Core application code
│   ├── auth/         # Authentication
│   ├── chat/         # Chat module
│   ├── slides/       # Slide management
│   ├── knowledge/    # Knowledge retrieval (RAG)
│   ├── llm/          # LLM integration
│   ├── websocket/    # Real-time communication
│   └── ...          # Other modules
├── database/         # Alembic migrations
└── requirements.txt

frontend/             # React application
├── src/
│   ├── components/   # React components
│   ├── pages/        # Page components
│   ├── store/        # Redux state management
│   ├── services/     # API services
│   └── types/        # TypeScript types
└── package.json

docker-compose.yml    # Multi-container setup
plan.md              # Detailed architecture & roadmap
QUICKSTART.md        # Getting started guide
```

## 📚 Documentation

- **[plan.md](./plan.md)** - Complete development plan with architecture
- **[QUICKSTART.md](./QUICKSTART.md)** - Quick start guide & troubleshooting
- **[FastAPI Interactive Docs](http://localhost:8000/docs)** - API documentation

## 🔄 Development Roadmap

| Phase | Duration | Focus | Status |
|-------|----------|-------|--------|
| 1 | Weeks 1-2 | Foundation, Auth, WebSocket | ✅ Complete |
| 2 | Weeks 3-4 | Chat System LLM Integration | 📅 Next |
| 3 | Weeks 5-6 | Knowledge Retrieval (RAG) | 📅 Planned |
| 4 | Weeks 7-8 | Slide Management | 📅 Planned |
| 5 | Weeks 9-10 | Voice Interface | 📅 Planned |
| 6 | Weeks 11-12 | Avatar System | 📅 Planned |
| 7 | Weeks 13-14 | Testing & Optimization | 📅 Planned |
| 8 | Week 15 | Deployment | 📅 Planned |

## 🎯 Key Features (Planned)

### Implemented ✅
- User registration & login
- JWT authentication
- WebSocket real-time communication
- Database models & migrations
- Docker containerization

### In Development 📅
- Chat system with LLM integration
- Knowledge retrieval (RAG)
- Slide management system
- Voice interface (STT/TTS)
- Avatar system (tiered)
- Advanced analytics

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

Open source under LICENSE file.

---

**Start building your intelligent teaching platform today! 🚀**
