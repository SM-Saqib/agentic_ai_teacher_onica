# AI Teacher Project - Development Plan

## Project Overview

**Goal**: Build an intelligent AI-powered teaching platform that leverages pre-built slide explanations, real-time LLM interactions, and knowledge management systems to assist student learning.

**Architecture**: Monolithic backend with microservice-like module separation + React-based frontend with WebSocket communication.

**Key Features**:
- Pre-built slide content with LLM-powered explanations
- Real-time student Q&A and knowledge retrieval
- Voice and chat interfaces
- Optional tiered avatar system
- Scalable knowledge management (databases + vector stores)

---

## Technology Stack

### Backend
- **Framework**: FastAPI (async, WebSocket support) - Free/Open-source
- **Language**: Python 3.10+ - Free/Open-source
- **Database**: PostgreSQL (primary data store) - Free/Open-source
- **Vector Store**: Qdrant / Milvus / ChromaDB (knowledge embeddings) - Free/Open-source alternatives
- **LLM Integration**: Ollama (local LLM runner) + Open-source models (Llama 2, Mistral, Zephyr)
- **Caching**: Redis (chat history, session management) - Free/Open-source
- **Task Queue**: Celery (async operations like slide generation) - Free/Open-source
- **ORM**: SQLAlchemy (database abstraction) - Free/Open-source
- **WebSocket Library**: FastAPI native WebSockets - Free/Open-source
- **Speech-to-Text**: Whisper (OpenAI's open-source STT) - Free/Open-source
- **Text-to-Speech**: Pyttsx3 / Espeak (offline TTS) - Free/Open-source

### Frontend
- **Framework**: React 18+ - Free/Open-source
- **Language**: TypeScript - Free/Open-source
- **State Management**: Redux Toolkit / Zustand - Free/Open-source
- **WebSocket Client**: Native WebSocket API - Free/Built-in
- **UI Framework**: Shadcn/ui / Material-UI / Chakra UI - Free/Open-source
- **Voice**: Web Audio API + Whisper.cpp (WebAssembly port) - Free/Open-source
- **Avatar**: Three.js / Babylon.js - Free/Open-source
- **Animation**: MediaPipe (pose estimation for avatar expressions) - Free/Open-source
- **Build Tool**: Vite - Free/Open-source

---

## Backend Architecture (Modular Monolith)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI app entry point
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py                  # Environment variables
│   │   └── constants.py                 # App constants
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py                  # Auth, JWT, WebSocket auth
│   │   ├── exceptions.py                # Custom exceptions
│   │   └── dependencies.py              # FastAPI dependencies
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py                # DB connection pool
│   │   ├── models.py                    # SQLAlchemy models
│   │   └── migrations/                  # Alembic migrations
│   │
│   ├── vector_store/
│   │   ├── __init__.py
│   │   ├── client.py                    # Vector store abstraction
│   │   ├── embeddings.py                # Embedding generation
│   │   └── indexing.py                  # Index management
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── client.py                    # LLM API abstraction
│   │   ├── prompts.py                   # Prompt templates
│   │   ├── response_generator.py        # Response generation logic
│   │   └── context_manager.py           # Conversation context
│   │
│   ├── knowledge/
│   │   ├── __init__.py
│   │   ├── repository.py                # Data retrieval layer
│   │   ├── retrieval.py                 # Knowledge retrieval (RAG)
│   │   └── indexing.py                  # Knowledge indexing
│   │
│   ├── slides/
│   │   ├── __init__.py
│   │   ├── models.py                    # Slide data models
│   │   ├── service.py                   # Slide business logic
│   │   ├── generator.py                 # Dynamic slide generation
│   │   └── repository.py                # Slide data access
│   │
│   ├── chat/
│   │   ├── __init__.py
│   │   ├── models.py                    # Chat models
│   │   ├── service.py                   # Chat logic
│   │   ├── repository.py                # Chat history storage
│   │   └── handlers.py                  # WebSocket handlers
│   │
│   ├── voice/
│   │   ├── __init__.py
│   │   ├── service.py                   # Voice processing
│   │   ├── speech_to_text.py            # STT integration
│   │   └── text_to_speech.py            # TTS integration
│   │
│   ├── avatar/
│   │   ├── __init__.py
│   │   ├── service.py                   # Avatar logic
│   │   ├── animation.py                 # Animation data
│   │   └── tiering.py                   # Feature gating
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── service.py                   # User authentication
│   │   ├── repository.py                # User data access
│   │   └── models.py                    # Auth models
│   │
│   ├── websocket/
│   │   ├── __init__.py
│   │   ├── manager.py                   # WebSocket connection management
│   │   ├── events.py                    # Event definitions
│   │   └── middleware.py                # WebSocket middleware
│   │
│   └── api/
│       ├── __init__.py
│       ├── v1/
│       │   ├── __init__.py
│       │   ├── routes/
│       │   │   ├── __init__.py
│       │   │   ├── slides.py            # Slides REST endpoints
│       │   │   ├── knowledge.py         # Knowledge endpoints
│       │   │   ├── chat.py              # Chat endpoints
│       │   │   ├── voice.py             # Voice endpoints
│       │   │   ├── avatar.py            # Avatar endpoints
│       │   │   ├── auth.py              # Auth endpoints
│       │   │   └── health.py            # Health check
│       │   └── websocket/
│       │       ├── __init__.py
│       │       └── router.py            # WebSocket routes
│       │
│       └── schemas/
│           ├── __init__.py
│           ├── chat.py                  # Chat request/response
│           ├── slides.py                # Slide schemas
│           ├── voice.py                 # Voice schemas
│           ├── avatar.py                # Avatar schemas
│           └── common.py                # Common schemas
│
├── tests/                               # Test suite (mirrors app structure)
├── requirements.txt
├── .env.example
├── docker-compose.yml                  # Services: DB, Redis, Vector Store
└── alembic.ini                         # DB migrations config
```

---

## Frontend Architecture

```
frontend/
├── public/
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   │
│   ├── assets/
│   │   ├── images/
│   │   ├── icons/
│   │   └── styles/
│   │
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── Loading.tsx
│   │   │
│   │   ├── chat/
│   │   │   ├── ChatWindow.tsx
│   │   │   ├── ChatMessage.tsx
│   │   │   ├── MessageInput.tsx
│   │   │   └── ChatHistory.tsx
│   │   │
│   │   ├── slides/
│   │   │   ├── SlideViewer.tsx
│   │   │   ├── SlideNavigation.tsx
│   │   │   ├── SlideSelector.tsx
│   │   │   └── SlideThumbnailList.tsx
│   │   │
│   │   ├── voice/
│   │   │   ├── VoiceButton.tsx
│   │   │   ├── VoiceIndicator.tsx
│   │   │   └── VoiceSettings.tsx
│   │   │
│   │   ├── avatar/
│   │   │   ├── AvatarDisplay.tsx
│   │   │   ├── AvatarSelector.tsx
│   │   │   └── AvatarAnimation.tsx
│   │   │
│   │   └── auth/
│   │       ├── LoginForm.tsx
│   │       ├── RegisterForm.tsx
│   │       └── ProtectedRoute.tsx
│   │
│   ├── pages/
│   │   ├── TeachingPage.tsx              # Main teaching interface
│   │   ├── StudentDashboard.tsx
│   │   ├── LoginPage.tsx
│   │   ├── SettingsPage.tsx
│   │   └── NotFoundPage.tsx
│   │
│   ├── services/
│   │   ├── websocket.ts                  # WebSocket client manager
│   │   ├── api.ts                        # REST API calls
│   │   ├── auth.ts                       # Auth service
│   │   ├── chat.ts                       # Chat logic
│   │   ├── voice.ts                      # Voice service
│   │   ├── slides.ts                     # Slide service
│   │   └── avatar.ts                     # Avatar service
│   │
│   ├── hooks/
│   │   ├── useWebSocket.ts
│   │   ├── useChat.ts
│   │   ├── useVoice.ts
│   │   ├── useAuth.ts
│   │   └── useSlides.ts
│   │
│   ├── store/
│   │   ├── index.ts                      # Redux store setup
│   │   ├── slices/
│   │   │   ├── authSlice.ts
│   │   │   ├── chatSlice.ts
│   │   │   ├── slideSlice.ts
│   │   │   ├── voiceSlice.ts
│   │   │   ├── avatarSlice.ts
│   │   │   └── uiSlice.ts
│   │   └── selectors/
│   │       └── index.ts
│   │
│   ├── types/
│   │   ├── index.ts
│   │   ├── chat.ts
│   │   ├── slides.ts
│   │   ├── api.ts
│   │   └── websocket.ts
│   │
│   ├── utils/
│   │   ├── formatting.ts
│   │   ├── validation.ts
│   │   ├── storage.ts
│   │   └── constants.ts
│   │
│   └── config/
│       ├── api.ts                        # API URLs
│       └── theme.ts                      # Theme configuration
│
├── package.json
└── vite.config.ts
```

---

## WebSocket Communication Protocol

### Connection Lifecycle
```
1. Client connects → Backend validates JWT token
2. Backend creates connection context with user/session info
3. Client subscribes to relevant event channels
4. Bidirectional event streaming begins
5. On disconnect → Clean up context, save state
```

### Event Types

#### Client → Server (Requests)
```
chat.message      // Send chat question
chat.follow_up    // Follow-up question
slides.select      // Select a slide
slides.generate    // Request dynamic slide generation
voice.start_recording // Initiate voice input
voice.stop_recording  // End voice input
avatar.request    // Request avatar animation/response
knowledge.search  // Direct knowledge search
```

#### Server → Client (Responses)
```
chat.response     // AI teacher text response
chat.thinking     // Agent thinking/processing indicator
slides.updated    // Slide content loaded
slides.generated  // New slide ready
voice.transcribed // STT result
avatar.animate    // Avatar animation data
connection.ready  // Connection established
error.message     // Error notification
```

---

## Core Features & Modules

### 1. Slide Management Module
- Store pre-built slides in database
- Link slides with pre-written explanations
- Dynamic slide generation using LLM
- Slide versioning and analytics

### 2. Knowledge Management (RAG)
- Vectorize slide content and pre-built explanations
- Index in vector store
- Semantic search for relevant context
- Hybrid search (keyword + semantic)

### 3. Chat & Conversation
- Store conversation history in PostgreSQL
- Context window management
- Knowledge retrieval for Q&A
- Multi-turn conversation handling

### 4. Voice Interface
- Speech-to-text (STT)
- Text-to-speech (TTS) with natural voice
- Real-time audio streaming
- Voice quality selection (tiered)

### 5. Avatar System (Tiered)
- Basic: Static avatar with expression changes
- Premium: Animated avatar with lip-sync
- Enterprise: Custom avatar with advanced animations

### 6. Authentication & Authorization
- JWT token-based WebSocket auth
- Role-based access control
- User session management
- Subscription tier management

---

## Open-Source Tool Recommendations

### LLM Models (via Ollama)
**Ollama** (https://ollama.ai) - Free, open-source LLM runner for local machine inference

Recommended Models:
- **Mistral 7B** - Best balance of speed and quality for teaching context
- **Llama 2 7B** - Solid general-purpose model
- **Neural Chat** - Optimized for conversational AI
- **Zephyr** - Better instruction-following capabilities

**Advantages**:
- Run locally on your machine (no API costs)
- Data privacy (no data sent to external servers)
- Instant responses
- Offline capability

### Vector Store Options (Comparison)

| Tool | Pros | Cons | Recommended For |
|------|------|------|-----------------|
| **Qdrant** | Fast, scalable, easy to use | Requires more resources | Production deployments |
| **ChromaDB** | Lightweight, simple Python API | Limited scalability | Development/small projects |
| **Milvus** | Highly scalable, feature-rich | Complex setup | Large-scale deployments |
| **Weaviate (Open-source)** | Full-featured, good docs | Heavier footprint | Mid to large projects |

**Recommendation for this project**: Start with **ChromaDB** for development, migrate to **Qdrant** for production.

### Speech Processing

- **Whisper (OpenAI's open-source STT)**: Uses Whisper.cpp for local inference
- **Pyttsx3 (TTS)**: Offline text-to-speech, works with system voices
- **Espeak (TTS)**: Fast, lightweight alternative

### Embedding Models

All models from **Sentence-Transformers** (https://www.sbert.net/):
- Pre-trained, free to use
- Run locally without API calls
- Multiple languages supported
- Trade-off between speed and quality

---

```sql
-- Users & Auth
users (id, email, password_hash, created_at, tier)
user_sessions (id, user_id, token, expires_at)

-- Slides
slides (id, title, content, is_prebuilt, created_at, version)
slide_explanations (id, slide_id, explanation, embedding_id)

-- Knowledge
knowledge_base (id, content, source_type, created_at)
knowledge_embeddings (id, knowledge_id, embedding_vector)

-- Chat
conversations (id, user_id, slide_id, created_at)
messages (id, conversation_id, role, content, created_at)

-- Voice
voice_logs (id, user_id, transcription, duration)

-- Avatar
avatar_configs (id, user_id, avatar_type, settings)
```

---

## Vector Store Schema

```
Index: "knowledge"
  - Document ID
  - Content (slide text, explanations)
  - Embedding vector (384-dim or 768-dim from open-source models like all-MiniLM-L6-v2)
  - Metadata: {source, slide_id, type}

Index: "explanations"
  - Pre-built explanation content
  - Embedding vector (from sentence-transformers or similar)
  - Metadata: {slide_id, language}
```

**Embedding Models (Free/Open-source)**:
- `all-MiniLM-L6-v2` (384-dim, lightweight, fast)
- `all-mpnet-base-v2` (768-dim, higher quality)
- `multilingual-e5-large` (1024-dim, multilingual support)

---

## Development Phases

### Phase 1: Foundation (Weeks 1-2)
- [ ] Set up project structure (backend + frontend)
- [ ] Configure FastAPI + React setup
- [ ] Implement basic authentication & JWT
- [ ] Set up PostgreSQL & initial migrations
- [ ] Basic WebSocket connection

### Phase 2: Core Chat System (Weeks 3-4)
- [ ] Implement WebSocket event handling
- [ ] Connect LLM (OpenAI/Hugging Face)
- [ ] Create chat service with context management
- [ ] Store chat history in database
- [ ] Build chat UI components

### Phase 3: Knowledge & Retrieval (Weeks 5-6)
- [ ] Set up vector store (Qdrant / Milvus / ChromaDB - all open-source)
- [ ] Implement RAG retrieval system
- [ ] Index pre-built slide explanations
- [ ] Implement semantic search
- [ ] Knowledge repository service

### Phase 4: Slide Management (Weeks 7-8)
- [ ] Build slide database & repository
- [ ] Implement slide selection API
- [ ] Create dynamic slide generation
- [ ] Build slide viewer UI
- [ ] Link slides to chat context

### Phase 5: Voice Integration (Weeks 9-10)
- [ ] Implement STT (Web Speech API / Whisper)
- [ ] Implement TTS (Web Audio API / external API)
- [ ] Voice button & recording UI
- [ ] Real-time transcription display
- [ ] Voice quality settings

### Phase 6: Avatar System (Weeks 11-12)
- [ ] Design avatar models (basic tier)
- [ ] Implement avatar display (Three.js)
- [ ] Create expression/animation system
- [ ] Implement tiering logic
- [ ] Premium avatar animations

### Phase 7: Optimization & Testing (Weeks 13-14)
- [ ] Performance optimization
- [ ] Load testing
- [ ] Comprehensive test suite
- [ ] Security hardening
- [ ] Documentation

### Phase 8: Deployment (Week 15)
- [ ] Docker containerization
- [ ] CI/CD pipeline setup
- [ ] Production deployment
- [ ] Monitoring & logging

---

## Deployment Architecture

### Single Machine Monolith
```
Docker Compose Services:
├── fastapi-backend           (port 8000)
├── react-frontend            (port 3000 / nginx on 80)
├── postgresql                (port 5432)
├── redis                     (port 6379)
├── qdrant / chromadb         (port 6333 or embedded)
└── ollama                    (port 11434 - optional, can run separately)
```

**All services are free and open-source - no licensing costs!**

### Scalability Approach
- Modular structure allows easy extraction to microservices later
- Each module (chat, slides, voice, avatar) is independent
- Clear interfaces between modules
- Async/await for concurrent operations
- Celery for background tasks (slide generation, indexing)

---

## Key Design Decisions

1. **Monolith with Modular Structure**: Easier deployment initially, clean separation for future microservice extraction
2. **WebSocket for Real-time**: Lower latency for chat, voice, and avatar interactions
3. **RAG for Knowledge**: Combine pre-built content with LLM for accurate, grounded responses
4. **Vector Store**: Semantic search for better knowledge retrieval
5. **Async Processing**: FastAPI's async support for high concurrency
6. **Tiered Features**: Avatar and voice quality monetization strategy

---

## Security Considerations

- JWT token validation on WebSocket connections
- Rate limiting on API endpoints
- Input validation on all endpoints
- SQL injection prevention (SQLAlchemy ORM)
- CORS configuration for cross-origin requests
- Secure password hashing (bcrypt)
- Environment-based configuration (no secrets in code)
- Logging & monitoring for anomalies

---

## Cost Analysis: All Open-Source Tools

| Component | Proprietary Option | Open-Source Alternative | Annual Savings |
|-----------|-------------------|------------------------|-----------------|
| LLM APIs | OpenAI ($0.002+ per token) | Ollama + Local Models | ~$5,000+ |
| Vector Store | Pinecone ($0.004+ per 1K vectors) | Qdrant/ChromaDB | ~$2,000+ |
| Speech APIs | Google Cloud STT ($0.024 per 15s) | Whisper | ~$1,500+ |
| TTS APIs | AWS Polly ($4+ per 1M chars) | Pyttsx3/Espeak | ~$500+ |
| **Total Potential Savings** | | | **~$9,000+/year** |

**Bottom Line**: Complete functionality achievable with **ZERO** recurring cloud costs. Only pay for hosting infrastructure (server, bandwidth).

---

## Monitoring & Logging

- Application logs (structured logging with JSON)
- Performance metrics (response times, token usage)
- Error tracking (Sentry integration)
- User analytics (usage patterns, engagement)
- Database query logging
- WebSocket connection health monitoring

---

## Next Steps

1. Create backend FastAPI project scaffold
2. Set up PostgreSQL database & migrations
3. Implement authentication system
4. Create basic WebSocket infrastructure
5. Build chat service with LLM integration
6. Parallel frontend setup with React + TypeScript
7. Implement knowledge retrieval system
8. Build slide management features
