import ollama

def call_llm(user_prompt_and_history: list):
    try:
        # System Promt
        system_prompt = {'role':'system', 'content':'You are a Senior Data Enigneer mentor. Use technical language, mention tolls like Pyspark and SQL when relevant, and always provide a one-sentence tip for a fresher.'}
        
        # Combining System prompt with user history
        full_context = [system_prompt] + user_prompt_and_history

        response = ollama.chat(
            model='llama3.2:1b',
            messages= full_context,
            options = {'num_predict': 100} # Small limit due to resource constraint
        )
        return response['message']['content']

    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}"