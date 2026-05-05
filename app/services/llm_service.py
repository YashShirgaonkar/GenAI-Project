import ollama
from app.exceptions import OllamaServiceError

def call_llm(user_prompt_and_history: list):
    try:
        # System Promt
        system_prompt = {'role':'system', 'content':'You are a Senior Data Engineer mentor. Use technical language, mention tolls like Python and SQL when relevant, and always provide a one-sentence tip for a fresher.'}
        
        # Combining System prompt with user history
        full_context = [system_prompt] + user_prompt_and_history

        response = ollama.chat(
            model='llama3.2:1b',
            messages= full_context,
            stream=True,
            options = {'num_predict': 150} # Small limit due to resource constraint
        )
        
        for chunk in response:
            yield chunk['message']['content']
    
    except Exception as e:
        raise OllamaServiceError(f"Ollama failed to respond: {str(e)}")