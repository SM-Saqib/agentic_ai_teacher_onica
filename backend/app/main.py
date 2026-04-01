"""FastAPI Main Application Entry Point"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config.settings import settings
from app.config.constants import API_PREFIX, WEBSOCKET_PREFIX
from app.database.connection import init_db, close_db
from app.core.exceptions import AITeacherException

# Import routers
from app.api.v1.routes import auth, health, chat, slides
from app.api.v1.websocket import router as ws_router

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("Starting up AI Teacher application...")
    await init_db()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Teacher application...")
    await close_db()
    logger.info("Database connection closed")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered teaching platform with LLM integration",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(AITeacherException)
async def ai_teacher_exception_handler(request, exc: AITeacherException):
    """Handle custom AI Teacher exceptions"""
    return JSONResponse(
        status_code=400,
        content={"detail": exc.detail},
    )


# Include routers
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(slides.router)
app.include_router(health.router)
app.include_router(ws_router.router)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AI Teacher API",
        "docs": "/docs",
        "api_prefix": API_PREFIX,
        "websocket_prefix": WEBSOCKET_PREFIX,
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
    )
