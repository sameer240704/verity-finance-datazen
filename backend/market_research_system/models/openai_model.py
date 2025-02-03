import requests
import json
import logging
logger = logging.getLogger(__name__)

class OpenAIModel:
    def __init__(self, api_key):
        """
        Initialize the OpenAIModel with the API key and endpoint URL.

        Parameters:
        api_key (str): The API key for authenticating requests to the OpenAI API.
        endpoint_url (str): The URL of the OpenAI API endpoint for chat completions.
        """
        self.api_key = api_key
        self.endpoint_url = '(your_openai_endpoint)'
        self.headers = {
            'Content-Type': 'application/json',
            'api-key': self.api_key,
        }

    def get_response(self, prompt, temperature=1.0, max_tokens=3026):
        """
        Return the complete response from the OpenAI API without streaming.

        Parameters:
        prompt (str): The user prompt to be sent to the OpenAI API.

        Returns:
        str: The complete message content from the API response, or an error message if the request fails.
        """
        messages = [{"role": "user", "content": prompt}]
        request_body = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False  # Disable streaming
        }
        request_body_json = json.dumps(request_body)

        response = requests.post(self.endpoint_url, headers=self.headers, data=request_body_json)
        if response.status_code == 200:
            response_json = response.json()
            if response_json['choices']:
                return response_json['choices'][0]['message']['content']  # Return the complete message content
            else:
                return "No choices available in the response."
        else:
            return f"Error: {response.status_code}, Response: {response.text}"
        
    def get_json_response(self, prompt):
        """
        Return the complete response from the OpenAI API without streaming.

        Parameters:
        prompt (str): The user prompt to be sent to the OpenAI API.

        Returns:
        str: The complete message content from the API response, or an error message if the request fails.
        """
        messages = [{"role": "user", "content": prompt}]
        request_body = {
            "response_format": {"type": "json_object"},
            "messages": messages,
            "stream": False  # Disable streaming
        }
        request_body_json = json.dumps(request_body)

        response = requests.post(self.endpoint_url, headers=self.headers, data=request_body_json)
        if response.status_code == 200:
            response_json = response.json()
            if response_json['choices']:
                return response_json['choices'][0]['message']['content']  # Return the complete message content
            else:
                return "No choices available in the response."
        else:
            return f"Error: {response.status_code}, Response: {response.text}"

    def stream_response(self, prompt, temprature=0.7, max_tokens=None):
        """
        Yield tokens from the streamed response based on the given prompt.

        Parameters:
        prompt (str): The user prompt to be sent to the OpenAI API.

        Yields:
        str: Each token of the response content as it is received from the API.
        """
        messages = [{"role": "user", "content": prompt}]
        request_body = {
            "messages": messages,
            "temperature": temprature,
            "max_tokens": max_tokens,
            "stream": True  # Enable streaming
        }
        request_body_json = json.dumps(request_body)

        with requests.post(self.endpoint_url, headers=self.headers, data=request_body_json, stream=True) as response:
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        line_decoded = line.decode('utf-8')
                        if line_decoded.startswith("data: "):
                            json_data = line_decoded[len("data: "):]
                            try:
                                response_json = json.loads(json_data)
                                if response_json['choices']:
                                    content = response_json['choices'][0]['delta'].get('content', '')
                                    if content:
                                        yield content  # Yield the content instead of printing
                            except json.JSONDecodeError:
                                print("Error decoding JSON:", json_data)
                            except IndexError:
                                print("No choices available in the response.")
            else:
                print(f"Error: {response.status_code}, Response: {response.text}")

class OpenAITTSModel:
    def __init__(self, api_key):
        """
        Initialize the OpenAI TTS Model with the API key and endpoint URL.

        Parameters:
        api_key (str): The API key for authenticating requests to the OpenAI API.
        endpoint_url (str): The URL of the OpenAI API endpoint for chat completions.
        """
        self.api_key = api_key
        self.endpoint_url = 'https://chira-m335jmgy-northcentralus.openai.azure.com/openai/deployments/tts-hd/audio/speech?api-version=2024-05-01-preview'
        self.headers = {
            'Content-Type': 'application/json',
            'api-key': self.api_key,
        }

    def generate_audio(self, input_text):
        """
        Sends a request to the Azure TTS model and returns the audio data.

        Parameters:
            text (str): The text to convert to speech.

        Returns:
            bytes: The audio data as a byte array.
        """

        request_body = {
            "model": 'tts-hd',
            "voice": 'nova',
            "input": input_text,
        }

        response = requests.post(self.endpoint_url, headers=self.headers, json=request_body)

        if response.status_code == 200:
            return response.content
        else:
            return f"Error: {response.status_code}, Response: {response.text}"