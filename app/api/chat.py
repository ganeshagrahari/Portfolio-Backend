"""
Chat API endpoints
"""

import uuid
from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import ChatRequest, ChatResponse, ErrorResponse
from app.core.rag import get_chatbot, RAGChatbot

router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Chat with Ganesh's AI Assistant",
    description="Send a message and get a response from the AI assistant that knows about Ganesh"
)
async def chat(
    request: ChatRequest,
    chatbot: RAGChatbot = Depends(get_chatbot)
) -> ChatResponse:
    """
    Chat endpoint - send a message and get a response
    
    - **message**: Your question or message (1-1000 characters)
    - **session_id**: Optional session ID for conversation tracking
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Get response from chatbot
        result = chatbot.chat(request.message)
        
        return ChatResponse(
            response=result["answer"],
            sources=result["sources"],
            session_id=session_id
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your request: {str(e)}"
        )
