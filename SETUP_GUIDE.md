# Complete Setup Guide - Running the Full AI Teacher Stack

This guide walks you through setting up and running the entire AI Teacher platform with all required services.

## 🎯 Overview

The AI Teacher platform consists of:

1. **Backend** - FastAPI server on port 8000
2. **Frontend** - React app on port 3000
3. **PostgreSQL** - Database on port 5432
4. **Redis** - Cache on port 6379
5. **ChromaDB** - Vector store on port 8000 (or 8001)
6. **LLM Service** - Ollama on 11434 (optional) OR OpenRouter API key

## 📋 Setup Checklist

- [ ] Clone repository
- [ ] Set up backend virtual environment and dependencies
- [ ] Set up frontend with Node.js and npm
- [ ] Ensure PostgreSQL is running
- [ ] Ensure Redis is running
- [ ] Ensure ChromaDB is running
- [ ] Configure LLM provider (Ollama or OpenRouter)
- [ ] Start backend server
- [ ] Start frontend development server
- [ ] Run database migrations
- [ ] Test endpoints
- [ ] Create test user and verify chat functionality

## 🚀 Option 1: Docker Compose (Fastest - Recommended)

### Requirements

- Docker installed and running
- Docker Compose installed
- 8GB RAM available

### Steps

```bash
# 1. Clone and navigate to project root
git clone https://github.com/SM-Saqib/agentic_ai_teacher_onica.git
cd agentic_ai_teacher_onica

# 2. Pull latest images
docker-compose pull

# 3. Start all services
docker-compose up -d

# 4. Wait for services to be healthy (30-60 seconds)
docker-compose ps  # Check status

# 5. Run database migrations
docker-compose exec backend alembic upgrade head

# 6. Access applications:
# - Frontend: http://localhost:3000
# - API Docs: http://localhost:8000/docs
# - PostgreSQL: localhost:5432
# - Redis: localhost:6379
```

### View Logs

```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# View recent logs only
docker-compose logs -f --tail=50
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (DELETE DATA!)
docker-compose down -v

# Restart services
docker-compose restart
```

---

## 🚀 Option 2: Local Setup (Recommended for Development)

### 1. Install System Dependencies

#### On macOS
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install PostgreSQL
brew install postgresql@16
brew services start postgresql@16

# Install Redis
brew install redis
brew services start redis

# Install Node.js (LTS)
brew install node

# Install Python 3.12
brew install python@3.12
```

#### On Ubuntu/Debian
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y
sudo systemctl start postgresql

# Install Redis
sudo apt install redis-server -y
sudo systemctl start redis-server

# Install Node.js (LTS)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Install Python 3.12
sudo apt install python3.12 python3.12-venv -y
```

#### On Windows
```powershell
# Install Chocolatey if not installed
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex

# Install using Chocolatey
choco install postgresql-14 redis-64 nodejs python3 -y

# Start services
pg_ctl -D "C:\Program Files\PostgreSQL\14\data" start
redis-server
```

### 2. Clone Repository

```bash
git clone https://github.com/SM-Saqib/agentic_ai_teacher_onica.git
cd agentic_ai_teacher_onica
```

### 3. Setup PostgreSQL

```bash
# Create database and user
psql -U postgres << EOF
CREATE DATABASE ai_teacher;
CREATE USER ai_teacher_user WITH PASSWORD 'password123';
ALTER ROLE ai_teacher_user SET client_encoding TO 'utf8';
ALTER ROLE ai_teacher_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ai_teacher_user SET default_transaction_deferrable TO on;
ALTER ROLE ai_teacher_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ai_teacher TO ai_teacher_user;
EOF

# Verify connection
psql -U ai_teacher_user -d ai_teacher -h localhost
# Exit with: \q
```

### 4. Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv

# Activate venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies (takes 2-3 minutes)
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run database migrations
alembic upgrade head

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

Open new terminal for next steps.

### 5. Setup Frontend

```bash
# From project root (new terminal)
cd frontend

# Install dependencies (takes 1-2 minutes)
npm install

# Create .env file if needed
# cp .env.example .env

# Start development server
npm run dev
```

**Expected output:**
```
VITE v5.0.0  ready in 123 ms

➜  Local:   http://localhost:3000/
```

### 6. Setup ChromaDB (Vector Store)

```bash
# Option A: Docker container (easiest)
docker run -d \
  -p 8000:8000 \
  ghcr.io/chroma-core/chroma:latest

# Option B: Local Python installation
pip install chromadb

# Then in Python:
import chromadb
client = chromadb.Client()
```

### 7. Setup LLM Provider

**Option A: Ollama (Free, Local)**

```bash
# Install from https://ollama.ai
# On macOS: brew install ollama
# On Linux: curl https://ollama.ai/install.sh | sh
# On Windows: Download installer

# Start Ollama
ollama serve

# In another terminal, pull a model
ollama pull mistral
# or
ollama pull llama2

# Update backend .env
# LLM_PROVIDER=ollama
# OLLAMA_BASE_URL=http://localhost:11434
# OLLAMA_MODEL=mistral
```

**Option B: OpenRouter (Free tier, no setup)**

```bash
# 1. Sign up at https://openrouter.ai
# 2. Copy your API key
# 3. Update backend .env:
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-your-key-here
OPENROUTER_MODEL=openrouter/free

# 4. That's it! Uses free tier automatically
```

### 8. Verify Everything is Running

```bash
# Check backend
curl http://localhost:8000/health
# Should return: {"status": "healthy", ...}

# Check frontend
curl http://localhost:3000
# Should return HTML

# Check PostgreSQL
psql -U ai_teacher_user -d ai_teacher -h localhost -c "SELECT 1"
# Should return: 1

# Check Redis
redis-cli ping
# Should return: PONG

# Check ChromaDB
curl http://localhost:8000/api/v1
# Should return API info

# Check Ollama (if using)
curl http://localhost:11434/api/tags
# Should return list of models
```

---

## 🌐 First-Time User Setup

### 1. Open Application

Visit `http://localhost:3000` in your browser.

### 2. Create Account

1. Click "Register"
2. Enter email and password
3. Click "Create Account"

### 3. Login

1. Enter your credentials
2. Click "Login"
3. You should see the teaching interface

### 4. Create a Conversation

1. Click "New Conversation"
2. Give it a title (e.g., "Math")
3. Click "Create"

### 5. Send First Message

1. Type a question (e.g., "What is calculus?")
2. Click "Send"
3. Watch for AI response streaming in real-time

### 6. Test Features

- Create multiple conversations
- Ask follow-up questions
- View chat history
- Delete conversations

---

## 🧪 Testing with curl

### Health Check

```bash
curl http://localhost:8000/health
```

### Register User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'
```

### Login

```bash
# Replace with your email/password
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }' | jq -r '.access_token')

echo "Token: $TOKEN"
```

### Create Conversation

```bash
# Replace TOKEN with actual token from login
curl -X POST http://localhost:8000/api/v1/chat/conversations \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Math Questions"
  }'
```

### Send Message

```bash
curl -X POST http://localhost:8000/api/v1/chat/message \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": 1,
    "content": "What is the Pythagorean theorem?"
  }'
```

---

## 📊 System Architecture

```
┌─────────────────────────────────────────┐
│     Browser (http://localhost:3000)     │
│         React Frontend                  │
└────────────────┬────────────────────────┘
                 │ HTTP/WebSocket
                 ▼
┌─────────────────────────────────────────┐
│   FastAPI Backend (localhost:8000)      │
│  - User Authentication                  │
│  - Chat Management                      │
│  - LLM Integration                      │
│  - WebSocket Events                     │
└────┬──────────┬──────────┬──────────────┘
     │          │          │
     ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────────┐
│  PG   │ │ Redis  │ │ ChromaDB   │
│ Data  │ │ Cache  │ │ Vectors    │
└───────┘ └────────┘ └────────────┘
     │
     ▼
┌────────────────────────────────────┐
│   LLM Provider                     │
│   - Ollama (local)                 │
│   - OpenRouter (cloud)             │
└────────────────────────────────────┘
```

---

## 📝 Environment Variables Summary

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/ai_teacher

# LLM
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-your-key
OPENROUTER_MODEL=openrouter/free

# Services
REDIS_URL=redis://localhost:6379/0
VECTOR_STORE_HOST=localhost
VECTOR_STORE_PORT=8000

# Security
SECRET_KEY=change-me-in-production

# Server
DEBUG=True
PORT=8000
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
VITE_DEBUG=true
```

---

## 🔍 Troubleshooting

### Services Won't Start

```bash
# Check if ports are in use
lsof -i :3000      # Frontend
lsof -i :8000      # Backend
lsof -i :5432      # PostgreSQL
lsof -i :6379      # Redis

# Kill process using port (if needed)
lsof -ti:3000 | xargs kill -9
```

### Database Connection Error

```bash
# Test PostgreSQL connection
psql -U postgres -h localhost

# Check connection string in .env
# Format: postgresql+asyncpg://user:password@host:port/database
```

### LLM Not Responding

```bash
# For Ollama:
curl http://localhost:11434/api/tags

# For OpenRouter:
curl -H "authorization: Bearer $OPENROUTER_API_KEY" \
  https://openrouter.ai/api/v1/models
```

### Frontend Won't Connect to Backend

1. Check backend is running on 8000
2. Check VITE_API_URL in frontend .env
3. check for CORS errors in browser console
4. Test with curl: `curl http://localhost:8000/health`

### Redux DevTools

1. Install Redux DevTools browser extension
2. Open DevTools (F12)
3. Go to Redux tab
4. View all state and actions

---

## 📚 Detailed Documentation

For more detailed information, see:

- [Backend README](./backend/README.md) - Full backend setup and API docs
- [Frontend README](./frontend/README.md) - Full frontend setup and development guide
- [Main README](./README.md) - Overall project overview
- [Plan](./plan.md) - Detailed architecture and roadmap
- [QUICKSTART](./QUICKSTART.md) - Quick reference guide

---

## ✅ Success Checklist

- [ ] All services running without errors
- [ ] Can access frontend at http://localhost:3000
- [ ] Can access API docs at http://localhost:8000/docs
- [ ] Can register and login
- [ ] Can create conversations
- [ ] Can send messages and get responses
- [ ] Chat displays streaming responses
- [ ] No errors in browser console
- [ ] No errors in backend logs

---

## 🎯 Next Steps

1. **Development**
   - Read backend development guide
   - Read frontend development guide
   - Familiarize yourself with codebase

2. **Customization**
   - Modify styling in frontend
   - Add new chat features
   - Customize LLM prompts

3. **Deployment**
   - Set up production environment
   - Configure SSL certificates
   - Deploy to cloud (AWS, Heroku, etc.)

4. **Testing**
   - Write unit tests
   - Test all endpoints
   - Load testing

---

## 🆘 Getting Help

- **Issues?** Check Troubleshooting section
- **Questions?** Read the detailed READMEs
- **Code help?** Check source comments
- **API docs?** Visit http://localhost:8000/docs

---

**Happy coding! 🚀**
