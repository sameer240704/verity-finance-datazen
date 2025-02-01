from flask import Flask, request, jsonify
from onboard import *
from flask_cors import CORS
import re
from openai_model import OpenAIModel
import gemini_fin_path
import os
from tavily import TavilyClient

app = Flask(__name__)
CORS(app)

# Initialize OpenAIModel
api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai_model = OpenAIModel(api_key)

# Initialize Tavily Client
tavily_api_key = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=tavily_api_key)

@app.route('/', methods=['GET', 'POST'])
def home():
    print("Request received at /")
    print("Method:", request.method)
    print("Headers:", request.headers)
    print("Data:", request.get_data())

    if request.method == 'POST':
        return jsonify({"message": "POST request received at /"})
    else:
        return jsonify("HI")

# =================== DYNAMIC APIS ===================
@app.route('/agent', methods=['POST'])
def agent():
    inp = request.form.get('input')
    if not inp:
        return jsonify({"error": "No input provided"}), 400

    print("Input query:", inp)

    try:
        # Use Tavily Search for financial queries
        search_result = tavily_client.search(query=inp, search_depth="advanced", max_results=5)

        print("Tavily Search Results:", search_result)  # Debugging

        # Extract relevant information from Tavily results
        tavily_response = ""
        if search_result and search_result['results']:
          for res in search_result['results']:
              tavily_response += f"Source: {res['url']}\nContent: {res['content']}\n\n"
        else:
            tavily_response = "Could not find relevant information from Tavily Search."

        # Use OpenAI to summarize the findings (optional)
        final_answer = openai_model.get_response(
            f"Based on the user query '{inp}', here is the information from Tavily Search:\n\n{tavily_response}\n\nPlease provide a concise and helpful answer to the user."
        )
        print("Final Answer from OpenAI:", final_answer)

        return jsonify({'output': final_answer, 'thought': tavily_response})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred while processing your request."}), 500

@app.route('/ai-financial-path', methods=['POST'])
def ai_financial_path():
    if 'input' not in request.form:
        return jsonify({'error': 'No input provided'}), 400

    input_text = request.form.get('input', '')
    risk = request.form.get('risk', 'conservative')
    print(input_text)
    try:
        response = gemini_fin_path.get_gemini_response(input_text, risk)
        return jsonify(response)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Something went wrong'}), 500

# =================== STATIC APIS ===================
@app.route('/auto-bank-data', methods=['get'])
def AutoBankData():
    return bank_data

@app.route('/auto-mf-data', methods=['get'])
def AutoMFData():
    return mf_data

if __name__ == "__main__":
    app.run(debug=True)