import os

def get_ollama_model():
    return os.getenv("OLLAMA_MODEL")

def get_ollama_base_url():
    return os.getenv("OLLAMA_BASE_URL")