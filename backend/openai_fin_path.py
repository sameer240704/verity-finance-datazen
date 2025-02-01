import os
import re
import json
from dotenv import load_dotenv
from openai_model import OpenAIModel

load_dotenv()

#Initialize OpenAI model
openai_model = OpenAIModel(api_key=os.environ["AZURE_OPENAI_API_KEY"])

#AZURE_OPENAI_API_KEY = "9u5AZGVVwyvMgWskHIV91P85D5imtqIj9K963WlsQfv3eeEKl2fhJQQJ99AKACHrzpqXJ3w3AAABACOGLd7I"

#openai_model = OpenAIModel(api_key=["AZURE_OPENAI_API_KEY"])

# System instruction similar to Gemini's
SYSTEM_INSTRUCTION = """You are a personal financial advisor dedicated to helping in financial journey. Focus on providing guidance on budgeting, investing, retirement planning, debt management, and wealth building strategies. Be precise and practical in your advice while considering individual circumstances.

Key areas of expertise:
- Budgeting and expense tracking
- Investment strategies and portfolio management
- Retirement planning
- Debt management and elimination
- Tax planning considerations
- Emergency fund planning
- Risk management and insurance

Provide balanced, ethical financial advice and acknowledge when certain situations may require consultation with other financial professionals.

You can increase the number of nodes and edges in the response if needed.

For the given user query you have to response a proper output by giving proper response in the following format
Strictly follow the given format only:

{
  "nodes": [
    {
      "id": "start",
      "position": { "x": 250, "y": 50 },
      "data": { "label": "Investment\n₹1,00,000" },
      "style": {
        "background": "bg-blue-100",
        "border": "border-blue-500"
      }
    }
  ],
  "edges": [
    {
      "id": "e-index",
      "source": "start",
      "target": "index",
      "label": "40%",
      "style": { "stroke": "stroke-indigo-500" }
    }
  ]
}"""

def get_openai_response(user_input: str, risk: str) -> str:
    """
    Get financial advice response from OpenAI model.
    
    Args:
        user_input (str): User's financial question
        risk (str): User's risk profile
    
    Returns:
        dict: JSON response containing nodes and edges for financial flow diagram
    """
    # Combine user input with risk profile and system instruction
    prompt = f"{SYSTEM_INSTRUCTION}\n\nUser Query: {user_input}\nRisk Profile: {risk}"
    
    # Get response from OpenAI
    response = openai_model.get_json_response(prompt)
    
    try:
        # Parse the JSON response
        if isinstance(response, str):
            # If the response is a string, try to extract JSON from it
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if json_match:
                resp = json.loads(json_match.group(1))
            else:
                # Try parsing the entire response as JSON
                resp = json.loads(response)
        else:
            resp = response
            
        return resp
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return {
            "nodes": [],
            "edges": []
        }

if __name__ == "__main__":
    # Sample test query
    test_query = "I have around ten lakh rupees where should I invest them"
    test_risk = "moderate"
    print("Test Query:", test_query)
    response = get_openai_response(test_query, test_risk)
    print("Response:", response)
