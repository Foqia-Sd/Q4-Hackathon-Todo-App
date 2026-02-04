from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.v1.router import api_router
from .api import auth, tasks
from .utils.logger import app_logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(api_router, prefix=settings.API_V1_STR, tags=["api-v1"])  # v1 includes chat
app.include_router(tasks.router, prefix=f"{settings.API_V1_STR}/tasks", tags=["tasks"])

@app.get("/")
def root():
    app_logger.info("Root endpoint accessed", extra={"endpoint": "/"})
    return {"message": "Welcome to Phase 3 Todo API with AI Chat"}

@app.get("/health")
def health_check():
    app_logger.info("Health check endpoint accessed", extra={"endpoint": "/health"})
    return {"status": "healthy", "service": "todo-backend"}

# Import and add WebSocket endpoint separately
from .api.realtime import websocket_endpoint
