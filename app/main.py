from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import List
from app.services.llm_service import call_llm
from app.exceptions import OllamaServiceError
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
import logging
import os
from app.config import PERSONAS


load_dotenv()
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == os.getenv("API_SECRET_KEY"):
        return api_key
    raise HTTPException(
        status_code= status.HTTP_403_FORBIDDEN,
        detail = "Could not validate Credentials" 
    )

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
    mode: str = "mentor"

# Create a EndPoint
@app.post("/chat")
async def chat_endpoint(request: ChatRequest, api_key: str = Security(get_api_key)):

    # Get system prompt base don requested mode.
    system_instruction = PERSONAS.get(request.mode, PERSONAS["mentor"])

    #passing instructions to the service
    return StreamingResponse(
        call_llm(request.message, system_instruction),
        media_type="text/event_stream"
    )

# Root Endpoint for Health CheckUp
@app.get("/")
def read_root():
    return {"message": "API is live and healthy"}
