import json
from typing import Any

import ollama
import os



def get_generic_prompt():
    """Retrieves the generic prompt which has the guidelines for the llm"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "generic_prompt.txt")
    with open(file_path, "r", encoding="utf-8") as file:
        prompt = file.read()
    return prompt


def get_llm_response(description: str) -> dict[str, Any]:
    """Combines the description text and prompt and pass it to Ollama LLM
     to retrieve the required fields"""
    generic_prompt = get_generic_prompt()
    combined_prompt = generic_prompt + description
    client =  ollama.Client()
    model = "gemma3n:latest"
    response = client.generate(model=model, prompt=combined_prompt,format='json')
    response_json = json.loads(response.response)
    return response_json
