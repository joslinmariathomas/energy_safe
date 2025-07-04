import json

from google import genai
from dotenv import load_dotenv
import os

load_dotenv()


def get_generic_prompt():
    """Retrieves the generic prompt which has the guidelines for the llm"""
    with open("./generic_prompt.txt", "r", encoding="utf-8") as file:
        prompt = file.read()
    return prompt


def get_llm_response(description: str) -> dict:
    """Combines the description text and prompt and pass it to Gemini LLM to retrieve the required fields"""
    generic_prompt = get_generic_prompt()
    combined_prompt = generic_prompt + description
    client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
    config = {
        "response_mime_type": "application/json",
    }
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=combined_prompt, config=config
    )
    response_json = json.loads(response.text)
    return response_json
