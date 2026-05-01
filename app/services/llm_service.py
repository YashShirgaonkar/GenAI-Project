import ollama

def call_llm(user_prompt: str):
    try:
        response = ollama.chat(
            model='llama3.2:1b',
            messages=[
                {'role': 'system', 'content':'You are a helpful and concise AI Assistant'},
                {'role': 'user', 'content': user_prompt}
            ]
        )
        if 'message' in response and 'content' in response['message']:
            return response['message']['content']
        else:
            return "Error: Unexpected response format from Ollama"
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}"