import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiModel:
    def __init__(self):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])

        # Create the model with gemini-2.0-flash-exp
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }

        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",  # Updated model name
            generation_config=generation_config
        )

        self.chat_session = self.model.start_chat(history=[])

    def get_response(self, user_input: str) -> str:
        """
        Gets a direct response from the Gemini model without any special formatting.

        Args:
            user_input: The input string from the user.

        Returns:
            The raw text response from the Gemini model.
        """
        response = self.chat_session.send_message(user_input)
        return response.text  # Directly return the text response