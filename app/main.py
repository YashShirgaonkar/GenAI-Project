from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse 
from pydantic import BaseModel
from typing import List
from app.services.llm_service import call_llm
from app.exceptions import OllamaServiceError
import logging


# Initializing app
app = FastAPI(title = "GenAI Assistant - Robust Version")

logging.basicConfig(level= logging.INFO)
logger = logging.getLogger(__name__)

# Error Handler
@app.exception_handler(OllamaServiceError)
async def ollama_exception_handler(request: Request, exc: OllamaServiceError):

    # Logging error to server side so we can track it
    logger.error(f"AI Service Error: {exc.message}") 
    
    return JSONResponse(
        status_code= 503,   # 503 means "Service Unavailable"
        content={
            "status": "error",
            "message": exc.message,
            "suggestion": "Check if Ollama is running in your System Tray."
        }
    )

# Defining structure of single message
class Message(BaseModel):
    role: str   #user or system or assistant, etc.
    content: str

# Defining request body to accept a list of those messages 
class ChatRequest(BaseModel):
    message: List[Message]

# Create a EndPoint
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    return StreamingResponse(
        call_llm(request.message),
        media_type="text/event_stream"
    )

# Root Endpoint for Health CheckUp
@app.get("/")
def read_root():
    return {"message": "API is live and healthy"}
