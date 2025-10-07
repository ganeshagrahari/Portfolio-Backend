"""
Main FastAPI application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api import chat, health

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered chatbot that knows all about Ganesh Agrahari - his skills, projects, and experience",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])


@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint - redirect to docs"""
    return JSONResponse({
        "message": "Welcome to Ganesh's AI Assistant API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/api/health"
    })


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📝 Environment: {settings.ENVIRONMENT}")
    print(f"🌐 CORS Origins: {settings.cors_origins_list}")
    
    # Initialize the chatbot (loads vector store)
    try:
        from app.core.rag import get_chatbot
        chatbot = get_chatbot()
        print("✅ RAG Chatbot initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("👋 Shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=True if settings.ENVIRONMENT == "development" else False
    )
