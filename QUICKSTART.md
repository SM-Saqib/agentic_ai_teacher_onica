# Quick Start Guide for AI Teacher Project

## Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)
- Ollama (optional, for local LLM - download from ollama.ai)

## Quick Start with Docker Compose

### 1. Clone the Repository
```bash
cd /workspaces/agentic_ai_teacher_onica
```

### 2. Set Environment Variables (Optional)
```bash
cp backend/.env.example backend/.env
cp frontend/.env.local frontend/.env
```

### 3. Start Services
```bash
docker-compose up -d
```

### 4. Initialize Database
```bash
docker-compose exec backend alembic upgrade head
```

### 5. Access the Applications
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ChromaDB**: http://localhost:8000 (embedded in Chroma service)

## Development Setup (Local)

### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your settings, especially OLLAMA_BASE_URL

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

## Project Structure
```
├── backend/          # FastAPI application
│   ├── app/         # Application code
│   ├── tests/       # Test suite
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/        # React/Vite application
│   ├── src/         # Source code
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
├── plan.md          # Project planning document
└── README.md
```

## Key Technologies
- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Frontend**: React, TypeScript, Redux, Tailwind CSS
- **Database**: PostgreSQL
- **Vector Store**: ChromaDB
- **LLM**: Ollama (local)
- **Cache**: Redis
- **Communication**: WebSockets

## Configuration

### LLM Models (Ollama)
Download models using Ollama CLI:
```bash
ollama pull mistral
ollama pull llama2
```

### Vector Store (ChromaDB)
Vector store persistence is handled by ChromaDB. Data is stored in `chromadb_data` volume.

## Common Commands

### Docker Compose
```bash
# Start services in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Access backend shell
docker-compose exec backend bash

# Access database
docker-compose exec postgres psql -U postgres -d ai_teacher
```

### Database Migrations (Backend)
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Frontend
```bash
npm run dev       # Development server
npm run build     # Production build
npm run lint      # Run linter
npm run type-check  # TypeScript check
```

## Testing
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test
```

## API Endpoints (Phase 1)

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Get current user
- `GET /api/v1/health` - Health check

### WebSocket
- `WS /ws/v1/chat/{token}` - Chat websocket

## Next Steps (Phases 2-8)

1. **Phase 2**: Complete chat system with LLM integration
2. **Phase 3**: Knowledge retrieval (RAG) system
3. **Phase 4**: Slide management
4. **Phase 5**: Voice interface
5. **Phase 6**: Avatar system
6. **Phase 7**: Testing & optimization
7. **Phase 8**: Deployment

See `plan.md` for detailed timeline and requirements.

## Troubleshooting

### Cannot connect to Ollama
- Ensure Ollama is running: `ollama serve`
- Check `OLLAMA_BASE_URL` in environment variables
- For Docker, use `http://host.docker.internal:11434` on Mac/Windows

### Database connection issues
- Ensure PostgreSQL is running
- Check `DATABASE_URL` format
- Verify database exists: `createdb ai_teacher`

### Port conflicts
- Check which process is using ports: `lsof -i :8000`, `lsof -i :3000`
- Change ports in docker-compose.yml or environment variables

## Contributing

1. Create a new branch for your feature
2. Follow PEP 8 for Python, Prettier/ESLint for JavaScript
3. Write tests for new functionality
4. Create a pull request with detailed description

## Support

For issues and questions, please refer to:
- Backend issues: Check FastAPI documentation
- Frontend issues: Check React/Vite documentation
- Architecture: Refer to plan.md for design decisions
