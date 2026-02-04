from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.v1.router import api_router
from .api.v1 import realtime
from .api import auth, tasks

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
app.include_router(realtime.router, prefix=f"{settings.API_V1_STR}/realtime")

@app.get("/dapr/subscribe")
def subscribe():
    return [
        {
            "pubsubname": "task-pubsub",
            "topic": "task-events",
            "route": f"{settings.API_V1_STR}/realtime/events/task"
        }
    ]

@app.get("/")
def root():
    return {"message": "Welcome to Phase 3 Todo API with AI Chat"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": "2026-02-03T13:00:00Z"}
