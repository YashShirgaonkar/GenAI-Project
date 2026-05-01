from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from app.services.llm_service import call_llm

# Initializing app
app = FastAPI(title = "GenAI Assistant with memory")

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
    # user_input = request.message
    ai_response = call_llm(request.message)
    return {
        "status": "success",
        "response": ai_response
    }

# Root Endpoint for Health CheckUp
@app.get("/")
def read_root():
    return {"message": "API is live and healthy"}
