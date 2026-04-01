# Backend - AI Teacher FastAPI Server

Complete FastAPI backend for the AI Teacher platform with authentication, chat system, LLM integration, and WebSocket support.

## 📋 Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Services](#running-services)
- [Starting the Server](#starting-the-server)
- [API Documentation](#api-documentation)
- [Testing Endpoints](#testing-endpoints)
- [Database Management](#database-management)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)

## 🔧 Requirements

### System Dependencies

- **Python 3.10+** (3.12 recommended)
- **PostgreSQL 14+** (or SQLite for development)
- **Redis 7+** (for caching)
- **LLM Service** (Ollama or OpenRouter API key)

### Python Dependencies

All Python dependencies are listed in `requirements.txt`:
- FastAPI & Uvicorn
- SQLAlchemy (async)
- Pydantic
- PostgreSQL driver (asyncpg)
- Redis client (aioredis)
- LLM clients (httpx for API integration)
- And more

## 📦 Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/SM-Saqib/agentic_ai_teacher_onica.git
cd agentic_ai_teacher_onica/backend
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Install all dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment

Copy the example environment file and configure:

```bash
cp .env.example .env
```

Edit `.env` with your settings (see [Configuration](#configuration) section).

## ⚙️ Configuration

### Environment Variables

Create/edit `.env` file in the backend directory:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ai_teacher
# For development with SQLite:
# DATABASE_URL=sqlite+aiosqlite:///./test.db

REDIS_URL=redis://localhost:6379/0

# LLM Provider Configuration
LLM_PROVIDER=openrouter              # or 'ollama'

# For OpenRouter (Free Models)
OPENROUTER_API_KEY=sk-or-YOUR-KEY-HERE
OPENROUTER_MODEL=openrouter/free     # Uses free tier with auto-routing

# For Ollama (Local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Vector Store Configuration
VECTOR_STORE_TYPE=chromadb
VECTOR_STORE_HOST=localhost
VECTOR_STORE_PORT=8000
CHROMADB_PERSIST_DIRECTORY=./data/chromadb

# Embedding Model
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Security
SECRET_KEY=your-super-secret-key-change-in-production

# Server Configuration
DEBUG=True                    # Set to False in production
ENVIRONMENT=development       # or 'production'
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO

# Database
DATABASE_ECHO=False           # Log SQL queries
```

### Configuration Guide

| Variable | Description | Default | Options |
|----------|-------------|---------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required | PostgreSQL URL or SQLite path |
| `LLM_PROVIDER` | Which LLM provider to use | `ollama` | `ollama`, `openrouter` |
| `OPENROUTER_API_KEY` | OpenRouter API key | Empty | Get from https://openrouter.ai |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` | Ollama endpoint |
| `VECTOR_STORE_TYPE` | Vector database | `chromadb` | `chromadb`, `qdrant` |
| `SECRET_KEY` | JWT signing key | Empty | Change in production! |
| `DEBUG` | Debug mode | `True` | `True` or `False` |

## 🚀 Running Services

### Option 1: Using Docker Compose (Recommended)

Run all services in containers:

```bash
# From project root
cd ..
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f backend
```

**Services started:**
- PostgreSQL (port 5432)
- Redis (port 6379)
- ChromaDB (port 8000)
- FastAPI Backend (port 8000, exposed as 8001 in docker-compose)
- React Frontend (port 3000)

### Option 2: Running Services Locally

Start each service separately for development:

#### PostgreSQL

```bash
# Using Homebrew (Mac)
brew services start postgresql

# Using Docker
docker run -d \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=ai_teacher \
  -p 5432:5432 \
  postgres:16-alpine

# Or use native installation
createdb ai_teacher -U postgres
```

#### Redis

```bash
# Using Homebrew (Mac)
brew services start redis

# Using Docker
docker run -d \
  -p 6379:6379 \
  redis:7-alpine

# Or use native installation
redis-server
```

#### ChromaDB (Vector Store)

```bash
# Using Docker
docker run -d \
  -p 8000:8000 \
  ghcr.io/chroma-core/chroma:latest
```

#### Ollama (If using local LLM)

```bash
# Install from https://ollama.ai
ollama serve

# In another terminal, pull a model
ollama pull mistral
# or
ollama pull llama2
```

## ▶️ Starting the Server

### Development Mode (with auto-reload)

```bash
# From backend directory with venv activated
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Expected output:
```
INFO:     Will watch for changes in these directories: ['/path/to/backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Production Mode

```bash
# Without reload, with workers
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### With Environment File

```bash
# Ensure .env is loaded
python -m uvicorn app.main:app --env-file .env --reload
```

## 📖 API Documentation

### OpenAPI Documentation (Swagger UI)

Once server is running, visit:

```
http://localhost:8000/docs
```

Here you can:
- View all available endpoints
- See request/response schemas
- Test endpoints directly with "Try it out"

### ReDoc Alternative

Alternative API documentation view:

```
http://localhost:8000/redoc
```

## 🧪 Testing Endpoints

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "timestamp": "2024-04-01T10:00:00"}
```

### User Registration

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepassword123",
    "full_name": "Test User"
  }'
```

### User Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepassword123"
  }'
```

Response includes `access_token` - save this for authenticated requests.

### Get Current User

```bash
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Create Conversation

```bash
curl -X POST http://localhost:8000/api/v1/chat/conversations \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Math Concepts",
    "slide_id": 1
  }'
```

### Send Chat Message

```bash
curl -X POST http://localhost:8000/api/v1/chat/message \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": 1,
    "content": "Explain the quadratic formula"
  }'
```

### List Conversations

```bash
curl http://localhost:8000/api/v1/chat/conversations \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🗄️ Database Management

### Initial Setup

```bash
# Run all pending migrations
alembic upgrade head

# Create new migration (if schema changes)
alembic revision --autogenerate -m "Add new table"

# Downgrade to previous version
alembic downgrade -1
```

### Database Operations

```bash
# Connect to PostgreSQL
psql -U postgres -d ai_teacher

# List tables
\dt

# Exit
\q
```

### Reset Database

```bash
# Drop and recreate (CAUTION: Deletes all data!)
psql -U postgres << EOF
DROP DATABASE ai_teacher;
CREATE DATABASE ai_teacher;
EOF

# Apply migrations
alembic upgrade head
```

## 🏗️ Architecture

### Module Structure

```
app/
├── api/                    # API routes
│   └── v1/
│       ├── routes/         # Endpoint definitions
│       │   ├── auth.py
│       │   ├── chat.py
│       │   ├── slides.py
│       │   └── health.py
│       ├── schemas/        # Pydantic models
│       └── websocket/      # WebSocket handlers
│
├── auth/                   # Authentication
│   ├── models.py          # User model
│   ├── schemas.py         # Auth schemas
│   └── service.py         # Auth logic
│
├── chat/                   # Chat functionality
│   ├── models.py          # Conversation, Message models
│   └── service.py         # Chat logic
│
├── llm/                    # LLM Integration
│   ├── providers/          # Provider implementations
│   │   ├── base.py        # Abstract interface
│   │   ├── ollama.py      # Ollama provider
│   │   └── openrouter.py  # OpenRouter provider
│   ├── client.py          # Factory function
│   ├── embeddings.py      # Text embeddings
│   └── prompts.py         # Prompt templates
│
├── database/               # Database
│   ├── models.py          # SQLAlchemy models
│   └── connection.py      # Database connection
│
├── config/                 # Configuration
│   ├── settings.py        # Environment settings
│   └── constants.py       # App constants
│
├── core/                   # Core utilities
│   ├── exceptions.py      # Custom exceptions
│   │── security.py        # Auth utilities
│   └── middleware.py      # Request middlewares
│
└── main.py                # Application entry point
```

### Request Flow

1. **Request** → FastAPI route handler
2. **Authentication** → JWT validation
3. **Validation** → Pydantic schema validation
4. **Processing** → Service layer logic
5. **Database** → SQLAlchemy async queries
6. **Response** → JSON serialization

### LLM Integration Flow

1. **Chat message** from user
2. **Retrieve** conversation history
3. **Format prompt** with context
4. **Call LLM provider** (Ollama or OpenRouter)
5. **Stream response** via WebSocket
6. **Store message** in database

## 🔧 Troubleshooting

### Database Connection Error

```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Fix:**
```bash
# Ensure PostgreSQL is running
psql -U postgres -c "SELECT version();"

# Check DATABASE_URL in .env
# Format: postgresql+asyncpg://user:password@host:port/database
```

### LLM Service Unavailable

```
Failed to connect to LLM provider
```

**For Ollama:**
```bash
# Ensure Ollama is running
curl http://localhost:11434/api/tags

# Pull a model
ollama pull mistral
```

**For OpenRouter:**
```bash
# Verify API key in .env
OPENROUTER_API_KEY=sk-or-YOUR-KEY

# Test API key
curl https://openrouter.ai/api/v1/models \
  -H "authorization: Bearer $OPENROUTER_API_KEY"
```

### Port Already in Use

```
Address already in use: ('0.0.0.0', 8000)
```

**Fix:**
```bash
# Change port in .env or command line
uvicorn app.main:app --port 8001

# Or kill existing process
lsof -ti:8000 | xargs kill -9
```

### Module Import Error

```
ModuleNotFoundError: No module named 'app'
```

**Fix:**
```bash
# Ensure you're in correct directory
cd /path/to/backend

# Activate venv
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Run from backend directory
python -m uvicorn app.main:app --reload
```

### WebSocket Connection Failures

Check that:
1. Server is running with WebSocket support
2. Frontend is using correct WebSocket URL
3. Authorization token is valid
4. No proxy/firewall blocking WebSocket connections

## 📝 Environment Variables Reference

```env
# REQUIRED
DATABASE_URL=postgresql+asyncpg://...
SECRET_KEY=your-secret-key

# LLM (choose one)
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-...
# OR
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434

# OPTIONAL (has defaults)
REDIS_URL=redis://localhost:6379/0
VECTOR_STORE_TYPE=chromadb
VECTOR_STORE_HOST=localhost
VECTOR_STORE_PORT=8000
EMBEDDING_MODEL=all-MiniLM-L6-v2
DEBUG=True
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

## 🎯 Next Steps

1. ✅ Install dependencies and configure environment
2. ✅ Start all required services (PostgreSQL, Redis, Ollama/OpenRouter)
3. ✅ Run migrations (`alembic upgrade head`)
4. ✅ Start the server
5. ✅ Test endpoints via Swagger UI or curl
6. ⏭️ Connect frontend to backend
7. ⏭️ Test WebSocket communication

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async Guide](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [OpenRouter API Docs](https://openrouter.ai/docs)
- [Ollama Documentation](https://github.com/jmorganca/ollama)

## 🤝 Contributing

To contribute to the backend:

1. Create a feature branch
2. Make your changes
3. Test with provided test endpoints
4. Submit a pull request

## 📄 License

See LICENSE file in project root.
