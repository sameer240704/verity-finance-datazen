import os
import google.generativeai as genai
import re
import json
from dotenv import load_dotenv

load_dotenv()

class GeminiModel:
    def __init__(self):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])

        # Create the model
        generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
        }

        self.model = genai.GenerativeModel(
            model_name="gemini-pro",
            generation_config=generation_config
        )

        self.chat_session = self.model.start_chat(history=[])

    def get_response(self, user_input: str) -> str:
        response = self.chat_session.send_message(user_input)
        markdown_text = response.text

        # Try to extract JSON content between ```json and ``` blocks
        json_match = re.search(r'```json\s*(.*?)\s*```', markdown_text, re.DOTALL)
        if json_match:
            try:
                resp = json.loads(json_match.group(1))
                return resp
            except json.JSONDecodeError:
                print("Error decoding JSON from Gemini response.")
        else:
            # If no JSON block is found, return the raw text (or handle as needed)
            print("No JSON block found in Gemini response.")

        return markdown_text  # Return raw text if no JSON or if JSON decoding fails