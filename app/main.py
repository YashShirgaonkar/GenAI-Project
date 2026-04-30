from fastapi import FastAPI
from pydantic import BaseModel

# Initializing app
app = FastAPI(title = "GenAI Assistant")

# Defining data structure
class ChatRequest(BaseModel):
    message: str

# Create a EndPoint
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_input = request.message
    return {
        "status": "success",
        "response": f"Server received: {user_input}. Ready for AI Integration"
    }

# Root Endpoint for Health CheckUp
@app.get("/")
def read_root():
    return {"message": "API is live and healthy"}
