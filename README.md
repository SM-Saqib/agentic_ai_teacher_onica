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

## 📋 Phase 1-2: Foundation & Chat (Complete ✅)

### ✅ Completed Tasks (Phase 1 & 2)

**Phase 1 - Foundation**
1. **Backend Structure** - FastAPI-based modular architecture with 15+ specialized modules
2. **Frontend Setup** - React 18 with TypeScript, Redux Toolkit, and Tailwind CSS
3. **Database & Models** - PostgreSQL async with 10+ SQLAlchemy models
4. **JWT Authentication** - Access/refresh tokens with secure password hashing
5. **WebSocket Infrastructure** - Real-time event-based messaging system
6. **Docker Compose** - Containerized environment (PostgreSQL, Redis, ChromaDB, Backend, Frontend)

**Phase 2 - Chat System & LLM Integration**
1. **Multi-Provider LLM** - Support for Ollama (local) and OpenRouter (cloud/free models)
2. **Chat Service** - Conversations, message history, context management
3. **LLM Providers** - Base interface + Ollama + OpenRouter implementations
4. **Free Model Support** - 13 free OpenRouter models (GPT-OSS, Llama, Mistral, etc.)
5. **WebSocket Chat** - Real-time streaming responses
6. **Background Package** - Scripts for data processing, web crawling, vector indexing
7. **Frontend Chat Components** - ChatWindow, Messages, Input, History, SlideViewer
8. **Chat API Endpoints** - 5+ REST endpoints for conversation management

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

### ⚡ Fastest Way: Docker (Recommended)
**Complete platform in 2 commands:**
```bash
# Start all services
docker-compose up -d

# Run migrations
docker-compose exec backend alembic upgrade head
```
Then visit: **http://localhost:3000**

👉 **[See SETUP_GUIDE.md for details →](./SETUP_GUIDE.md)**

### 💻 Local Development Setup
**Manual setup for customization and development:**
```bash
# Backend (terminal 1)
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (terminal 2)
cd frontend && npm install && npm run dev
```

👉 **[Full Backend Setup →](./backend/README.md) | [Full Frontend Setup →](./frontend/README.md)**

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

### Getting Started
- **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** - 📖 **START HERE!** Complete step-by-step guide to run the entire platform (Docker or local)
- **[Backend README](./backend/README.md)** - 🔧 Detailed backend setup, configuration, API testing, and troubleshooting
- **[Frontend README](./frontend/README.md)** - 🎨 Detailed frontend setup, development guide, and deployment
- **[QUICKSTART.md](./QUICKSTART.md)** - ⚡ Quick reference guide & tips

### Reference
- **[plan.md](./plan.md)** - 📋 Complete development plan, architecture, and 8-phase roadmap
- **[FastAPI Interactive Docs](http://localhost:8000/docs)** - 📖 Live API documentation (when server running)

## 🔄 Development Roadmap

| Phase | Focus | Duration | Status |
|-------|-------|----------|--------|
| 1 | Foundation, Auth, WebSocket, DB | Weeks 1-2 | ✅ Complete |
| 2 | Chat System, LLM Integration, Multi-Provider | Weeks 3-4 | ✅ Complete |
| 3 | Knowledge Retrieval (RAG), ChromaDB Integration | Weeks 5-6 | 📅 Next |
| 4 | Slide Management System | Weeks 7-8 | 📅 Planned |
| 5 | Voice Interface (STT/TTS) | Weeks 9-10 | 📅 Planned |
| 6 | Avatar System (Tiered) | Weeks 11-12 | 📅 Planned |
| 7 | Testing & Optimization | Weeks 13-14 | 📅 Planned |
| 8 | Deployment & Scaling | Week 15 | 📅 Planned |

## 🎯 Key Features

### Phase 1-2: Implemented ✅
- ✅ User registration & login with JWT
- ✅ WebSocket real-time communication
- ✅ PostgreSQL async database with migrations
- ✅ Docker containerization (all services)
- ✅ Chat system with message history
- ✅ Multi-provider LLM support (Ollama + OpenRouter)
- ✅ Free OpenRouter models (13+ options)
- ✅ WebSocket streaming responses
- ✅ React 18 frontend with TypeScript
- ✅ Redux state management
- ✅ Background scripts package (for data processing)

### Phase 3-8: Upcoming 📅
- Knowledge retrieval system (RAG + ChromaDB)
- Slide management system
- Voice interface (STT/TTS)
- Avatar system (tiered: basic → premium → enterprise)
- Advanced analytics & metrics
- Performance optimization
- Production deployment

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

Open source under LICENSE file.

---

**Start building your intelligent teaching platform today! 🚀**
