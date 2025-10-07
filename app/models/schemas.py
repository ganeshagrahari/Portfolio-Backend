"""
Pydantic models for request/response validation
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., min_length=1, max_length=1000, description="User's message")
    session_id: Optional[str] = Field(None, description="Optional session ID for conversation tracking")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What are Ganesh's main skills?",
                "session_id": "abc123"
            }
        }


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str = Field(..., description="AI assistant's response")
    sources: List[str] = Field(default_factory=list, description="Sources used to generate the response")
    session_id: Optional[str] = Field(None, description="Session ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "Ganesh has advanced skills in Python, Machine Learning, Deep Learning...",
                "sources": ["about_ganesh.txt", "projects.txt"],
                "session_id": "abc123"
            }
        }


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    environment: str = Field(..., description="Environment (development/production)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "environment": "production"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid request",
                "detail": "Message cannot be empty"
            }
        }
