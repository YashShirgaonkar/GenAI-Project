import ollama
import os
from dotenv import load_dotenv
from app.exceptions import OllamaServiceError

load_dotenv()

def call_llm(user_prompt_and_history: list, system_instruction: str):
    try:
        # System Promt
        system_prompt = {'role':'system', 'content': 'system_instruction'}
        
        # Combining System prompt with user history
        full_context = [system_prompt] + user_prompt_and_history

        response = ollama.chat(
            model=os.getenv("MODEL_NAME", "llama3.2:1b"),
            messages= full_context,
            stream=True,
            options = {'num_predict': 150} # Small limit due to resource constraint
        )
        
        for chunk in response:
            yield chunk['message']['content']
    
    except Exception as e:
        raise OllamaServiceError(f"Ollama failed to respond: {str(e)}")