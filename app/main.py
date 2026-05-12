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
from app.utils.data_processor import chunk_text, get_relevent_chunk


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

try:
    with open("data/pyspark_docs.txt", "r") as f:
        RAW_TEXT = f.read()
    DOC_CHUNKS = chunk_text(RAW_TEXT)
    print(f"--- RAG System Ready: Loaded {len(DOC_CHUNKS)} chunks ---")
except FileNotFoundError:
    DOC_CHUNKS = []
    print("--- WARNING: data/pyspark_docs.txt not found. RAG mode will be disabled. ---")



# Create a EndPoint
@app.post("/chat")
async def chat_endpoint(request: ChatRequest, api_key: str = Security(get_api_key)):

    # If the user selected RAG, then we override the system prompt with data
    if request.mode == "rag":
        # We take the last message from user to search with
        user_query = request.message[-1].content
        relevent_context = get_relevent_chunk(user_query, DOC_CHUNKS)

        if relevent_context:
            context_str = "\n".join(relevent_context)
            system_instruction = (
                "CRITICAL: You are a closed-domain PySpark bot. "
                "You have NO outside knowledge. If the answer is not in the context, "
                "say 'I cannot find this in the documentation.' DO NOT answer general questions."
            )
            # 2. PROMPT INJECTION: We wrap the user's question in a cage
            request.message[-1].content = (
                f"CONTEXT FROM DOCS:\n{context_str}\n\n"
                f"QUESTION: {user_query}\n\n"
                f"INSTRUCTION: Answer using ONLY the context above. If it's not there, say you don't know."
            )
        else:
            system_instruction = "REJECT ALL QUESTIONS. Say: 'No relevant documentation found.'"

    else:
        #Standard Logic
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
