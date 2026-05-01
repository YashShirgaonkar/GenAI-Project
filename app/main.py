from fastapi import FastAPI
from pydantic import BaseModel
from app.services.llm_service import call_llm

# Initializing app
app = FastAPI(title = "GenAI Assistant")

# Defining data structure
class ChatRequest(BaseModel):
    message: str

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
