# Local-RAG: A Lightweight Data Science Assistant
A high-performance GenAI architecture optimized for low-resource environments (4GB RAM).

## Key Features
*   **Hybrid RAG Engine**: Combines Python-based keyword filtering (Logic Gate) with LLM inference to prevent hallucinations and timeouts.
*   **Context Sandwiching**: Optimized prompting technique for small models (Llama 3.2 1B) to ensure grounding.
*   **Security First**: Implemented API Key authentication and a "Thin Client" architecture.
*   **Multi-Mode Personas**: Specialized modes for SQL, Coding, and Mentorship.

## Architecture


1. **Client**: Python-based CLI handling streaming responses and slash commands.
2. **API**: FastAPI server managing session state and persona-based system prompts.
3. **Storage**: Local `.txt` knowledge base chunked for semantic retrieval.
4. **Inference**: Ollama running Llama 3.2 1B.