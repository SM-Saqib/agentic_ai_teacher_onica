"""Application Constants"""

# API Constants
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# WebSocket Constants
WEBSOCKET_PREFIX = f"/ws/{API_VERSION}"

# Chat Constants
DEFAULT_CHAT_MAX_TOKENS = 1024
DEFAULT_CHAT_TEMPERATURE = 0.7
DEFAULT_RAG_CONTEXT_CHUNKS = 5
DEFAULT_RAG_SIMILARITY_THRESHOLD = 0.5

# Voice Constants
SUPPORTED_VOICE_FORMATS = ["wav", "mp3", "ogg"]
MAX_VOICE_DURATION_SECONDS = 300
VOICE_SAMPLE_RATE = 16000

# Vector Store Constants
EMBEDDING_DIMENSION = 384  # For all-MiniLM-L6-v2
VECTOR_STORE_BATCH_SIZE = 100

# Slide Constants
MAX_SLIDES_PER_LESSON = 100
SLIDE_GENERATION_TIMEOUT_SECONDS = 60

# Avatar Constants
AVATAR_TIERS = {
    "free": {"name": "Static", "features": ["basic_expressions"]},
    "premium": {"name": "Animated", "features": ["lip_sync", "animations"]},
    "enterprise": {"name": "Custom", "features": ["custom_avatar", "advanced_animations"]},
}

# Error Messages
ERROR_MESSAGES = {
    "invalid_credentials": "Invalid username or password",
    "invalid_token": "Invalid or expired token",
    "user_not_found": "User not found",
    "user_already_exists": "User already exists",
    "unauthorized": "Unauthorized access",
    "forbidden": "Access forbidden",
    "not_found": "Resource not found",
    "server_error": "Internal server error",
}

# Success Messages
SUCCESS_MESSAGES = {
    "login_success": "Login successful",
    "registration_success": "Registration successful",
    "data_saved": "Data saved successfully",
}
