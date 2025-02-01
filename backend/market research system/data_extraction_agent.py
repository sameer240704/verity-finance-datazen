import re
import json
import os
from models.gemini_model import GeminiModel
from utils.yfinance_api import YFinanceAPI
from utils.rapidapi_api import RapidAPI

class DataExtractionAgent:
    def __init__(self):
        self.gemini_model = GeminiModel()
        self.yfinance_api = YFinanceAPI()
        self.rapidapi_api = RapidAPI()
        self.initial_prompt_template = """
        You are a Data Extraction Agent. Your task is to extract specific information from a text report and structure it into a JSON format.

        The report follows a consistent structure with sections for Market Metrics, Sources, and Top 5 Performing Stocks.

        Your output MUST be valid JSON in the following format:

        ```json
        {{
          "market_metrics": {{
            "metric_1_name": "metric_1_value",
            "metric_2_name": "metric_2_value",
            ...
          }},
          "sources": [
            {{
              "name": "source_1_name",
              "url": "source_1_url"
            }},
            {{
              "name": "source_2_name",
              "url": "source_2_url"
            }},
            ...
          ],
          "top_5_stocks": [
            {{
              "stock_name": "stock_1_name",
              "ticker": "stock_1_ticker",
              "current_price": "stock_1_current_price",
              "30_day_performance": "stock_1_30_day_performance",
              "justification": "stock_1_justification"
            }},
            {{
              "stock_name": "stock_2_name",
              "ticker": "stock_2_ticker",
              "current_price": "stock_2_current_price",
              "30_day_performance": "stock_2_30_day_performance",
              "justification": "stock_2_justification"
            }},
            ...
          ]
        }}
        ```

        **Instructions:**

        1. **Market Metrics:** Extract all numerical data from the "Market Metrics" section. The keys should be descriptive metric names (e.g., "market_size", "growth_rate"), and the values should be the corresponding numerical values as strings (e.g., "1.5 Trillion USD", "7.5%").

        2. **Sources:** Extract the source names and URLs from the "Sources" section. Use regular expressions to find the URLs.

        3. **Top 5 Performing Stocks:** Extract the stock name, ticker, and justification from the "Top 5 Performing Stocks" section. For each stock, use yfinance or RapidAPI to get the current price and 30-day performance (percentage change).

        **Input Report:**

        {report_text}
        """

    def run(self, report_filepath, agent_name="ExtractedData"):
        """
        Extracts data from the given report file and saves it as a JSON file.

        Args:
            report_filepath: The path to the text report file.
            agent_name: The name of the agent (used for the output filename).
        """
        try:
            with open(report_filepath, "r") as f:
                report_text = f.read()
        except FileNotFoundError:
            print(f"Error: Report file not found at {report_filepath}")
            return

        prompt = self.initial_prompt_template.format(report_text=report_text)
        response = self.gemini_model.get_response(prompt)

        print("-" * 30)
        print("Initial Data Extraction Agent Output:")
        print(response)
        print("-" * 30)

        # Save the Gemini output to a text file
        reports_dir = "reports"
        os.makedirs(reports_dir, exist_ok=True)
        output_filepath = os.path.join(reports_dir, f"{agent_name}_json.txt")
        with open(output_filepath, "w") as f:
            f.write(response)
        print(f"Gemini output saved to {output_filepath}")

        return response


# import re
# import json
# import os
# from models.gemini_model import GeminiModel
# from utils.yfinance_api import YFinanceAPI
# from utils.rapidapi_api import RapidAPI

# class DataExtractionAgent:
#     def __init__(self):
#         self.gemini_model = GeminiModel()
#         self.yfinance_api = YFinanceAPI()
#         self.rapidapi_api = RapidAPI()
#         self.initial_prompt_template = """
#         You are a Data Extraction Agent. Your task is to extract specific information from a text report and structure it into a JSON format.

#         The report follows a consistent structure with sections for Market Metrics, Sources, and Top 5 Performing Stocks.

#         Your output MUST be valid JSON in the following format:

#         ```json
#         {{
#           "market_metrics": {{
#             "metric_1_name": "metric_1_value",
#             "metric_2_name": "metric_2_value",
#             ...
#           }},
#           "sources": [
#             {{
#               "name": "source_1_name",
#               "url": "source_1_url"
#             }},
#             {{
#               "name": "source_2_name",
#               "url": "source_2_url"
#             }},
#             ...
#           ],
#           "top_5_stocks": [
#             {{
#               "stock_name": "stock_1_name",
#               "ticker": "stock_1_ticker",
#               "current_price": "stock_1_current_price",
#               "30_day_performance": "stock_1_30_day_performance",
#               "justification": "stock_1_justification"
#             }},
#             {{
#               "stock_name": "stock_2_name",
#               "ticker": "stock_2_ticker",
#               "current_price": "stock_2_current_price",
#               "30_day_performance": "stock_2_30_day_performance",
#               "justification": "stock_2_justification"
#             }},
#             ...
#           ]
#         }}
#         ```

#         **Instructions:**

#         1. **Market Metrics:** Extract all numerical data from the "Market Metrics" section. The keys should be descriptive metric names (e.g., "market_size", "growth_rate"), and the values should be the corresponding numerical values as strings (e.g., "1.5 Trillion USD", "7.5%").

#         2. **Sources:** Extract the source names and URLs from the "Sources" section. Use regular expressions to find the URLs.

#         3. **Top 5 Performing Stocks:** Extract the stock name, ticker, and justification from the "Top 5 Performing Stocks" section. For each stock, use yfinance or RapidAPI to get the current price and 30-day performance (percentage change).

#         **Input Report:**

#         {report_text}
#         """
#         self.refinement_prompt_template = """
#         You are a JSON Refinement Agent. Your task is to take an existing JSON output from a Data Extraction Agent, and refine it to ensure it is perfectly formatted and contains all required data types.

#         **Input JSON:**

#         ```json
#         {input_json}
#         ```

#         **Instructions:**

#         1. **Validate the JSON:** Ensure the input is a valid JSON object.
#         2. **Correct any formatting errors:** Fix any issues with the structure, such as missing commas, incorrect quotes, or invalid key-value pairs.
#         3. **Verify data types:** Make sure all values have the correct data types as specified in the original prompt.
#         4. **Add missing data:** If any required data is missing, use your knowledge or reasoning to fill in the gaps as best as possible.
#         5. **Output:** Generate a new, perfectly formatted JSON object that strictly adheres to the following format:

#         ```json
#         {{
#           "market_metrics": {{
#             "metric_1_name": "metric_1_value",
#             "metric_2_name": "metric_2_value",
#             ...
#           }},
#           "sources": [
#             {{
#               "name": "source_1_name",
#               "url": "source_1_url"
#             }},
#             {{
#               "name": "source_2_name",
#               "url": "source_2_url"
#             }},
#             ...
#           ],
#           "top_5_stocks": [
#             {{
#               "stock_name": "stock_1_name",
#               "ticker": "stock_1_ticker",
#               "current_price": "stock_1_current_price",
#               "30_day_performance": "stock_1_30_day_performance",
#               "justification": "stock_1_justification"
#             }},
#             {{
#               "stock_name": "stock_2_name",
#               "ticker": "stock_2_ticker",
#               "current_price": "stock_2_current_price",
#               "30_day_performance": "stock_2_30_day_performance",
#               "justification": "stock_2_justification"
#             }},
#             ...
#           ]
#         }}
#         ```

#         **Strictly adhere to the JSON format and data types. Do not include any text outside of the JSON object.**
#         """

#     def run(self, report_filepath, agent_name="ExtractedData"):
#         """
#         Extracts data from the given report file, refines it using Gemini, and saves it as a JSON file.

#         Args:
#             report_filepath: The path to the text report file.
#             agent_name: The name of the agent (used for the output filename).
#         """
#         try:
#             with open(report_filepath, "r") as f:
#                 report_text = f.read()
#         except FileNotFoundError:
#             print(f"Error: Report file not found at {report_filepath}")
#             return

#         # Initial data extraction using the first prompt
#         initial_prompt = self.initial_prompt_template.format(report_text=report_text)
#         initial_response = self.gemini_model.get_response(initial_prompt)

#         print("-" * 30)
#         print("Initial Data Extraction Agent Output:")
#         print(initial_response)
#         print("-" * 30)

#         try:
#             # Attempt to parse the initial response as JSON
#             initial_data_json = json.loads(initial_response)
#             print("Successfully parsed initial Gemini response as JSON.")
#         except json.JSONDecodeError:
#             print("Error: Initial Gemini response is not valid JSON. Using regex as fallback.")
#             initial_data_json = self.extract_data_to_json_with_regex(report_text)

#         # Fetch stock data and update the JSON
#         initial_data_json = self.fetch_stock_data(initial_data_json)

#         # Refine the JSON using the second prompt
#         refinement_prompt = self.refinement_prompt_template.format(input_json=json.dumps(initial_data_json))
#         refined_response = self.gemini_model.get_response(refinement_prompt)

#         print("-" * 30)
#         print("Refined Data Extraction Agent Output:")
#         print(refined_response)
#         print("-" * 30)

#         try:
#             # Attempt to parse the refined response as JSON
#             data_json = json.loads(refined_response)
#             print("Successfully parsed refined Gemini response as JSON.")
#         except json.JSONDecodeError:
#             print("Error: Refined Gemini response is not valid JSON. Using initial data as fallback.")
#             data_json = initial_data_json

#         # Save the JSON to a file
#         self.save_data_to_file(data_json, agent_name)

#         return data_json

#     def extract_data_to_json_with_regex(self, report_text):
#         """
#         Extracts data from the report text using regex and creates a JSON object. This is a fallback method.
#         """
#         data_json = {
#             "market_metrics": {},
#             "sources": [],
#             "top_5_stocks": []
#         }

#         # Market Metrics
#         market_metrics_section = re.search(r"# Market Metrics(.*?)(?=#|$)", report_text, re.DOTALL)
#         if market_metrics_section:
#             market_metrics_text = market_metrics_section.group(1)
#             for line in market_metrics_text.split("\n"):
#                 if ":" in line:
#                     key, value = line.split(":", 1)
#                     data_json["market_metrics"][key.strip()] = value.strip()

#         # Sources
#         sources_section = re.search(r"# Sources(.*?)(?=#|$)", report_text, re.DOTALL)
#         if sources_section:
#             sources_text = sources_section.group(1)
#             data_json["sources"] = self.extract_sources(sources_text)

#         # Top 5 Performing Stocks
#         top_stocks_section = re.search(r"# Top 5 Performing Stocks(.*?)(?=#|$)", report_text, re.DOTALL)
#         if top_stocks_section:
#             top_stocks_text = top_stocks_section.group(1)
#             data_json["top_5_stocks"] = self.extract_top_stocks(top_stocks_text)

#         return data_json

#     def extract_sources(self, text):
#         """
#         Extracts source URLs using regex.
#         """
#         sources = []
#         source_matches = re.findall(r"(\S+)\s+\((https?://.*?)\)", text)
#         for source_name, url in source_matches:
#             sources.append({"name": source_name, "url": url})
#         return sources
    
#     def extract_top_stocks(self, text):
#         """
#         Extracts top stock information using regex.
#         """
#         stocks = []
#         stock_matches = re.findall(r"-\s*\*\*([A-Za-z\s&.]+)\s*\((\w+)\):\*\*\s*(.*?)(?=-|$)", text, re.DOTALL)
#         for stock_name, ticker, justification in stock_matches:
#             stocks.append({
#                 "stock_name": stock_name.strip(),
#                 "ticker": ticker.strip(),
#                 "justification": justification.strip()
#             })
#         return stocks

#     def fetch_stock_data(self, data_json):
#         """
#         Fetches current price and 30-day performance for each stock using yfinance or RapidAPI.
#         """
#         if "top_5_stocks" not in data_json:
#             return data_json
        
#         for stock_data in data_json["top_5_stocks"]:
#             ticker = stock_data["ticker"]
#             try:
#                 # Try yfinance first
#                 current_price = self.yfinance_api.get_current_price(ticker)
#                 if current_price is None:
#                     raise ValueError("yfinance did not return a current price.")
#                 stock_data["current_price"] = current_price

#                 performance_30d = self.yfinance_api.get_performance(ticker, period="30d")
#                 if performance_30d is None:
#                   raise ValueError("yfinance did not return a 30-day performance.")
#                 stock_data["30_day_performance"] = performance_30d

#             except Exception as e:
#                 print(f"Error fetching stock data from yfinance for {ticker}: {e}")
#                 try:
#                     # Fallback to RapidAPI
#                     current_price = self.rapidapi_api.get_current_price(ticker)
#                     if current_price is None:
#                         raise ValueError("RapidAPI did not return a current price.")
#                     stock_data["current_price"] = current_price

#                     performance_30d = self.rapidapi_api.get_performance(ticker, period="30d")
#                     if performance_30d is None:
#                         raise ValueError("RapidAPI did not return a 30-day performance.")
#                     stock_data["30_day_performance"] = performance_30d

#                 except Exception as e_rapid:
#                     print(f"Error fetching stock data from RapidAPI for {ticker}: {e_rapid}")
#                     stock_data["current_price"] = "N/A"
#                     stock_data["30_day_performance"] = "N/A"

#         return data_json

#     def save_data_to_file(self, data_json, agent_name):
#         """
#         Saves the extracted data to a JSON file.
#         """
#         reports_dir = "reports"
#         os.makedirs(reports_dir, exist_ok=True)

#         filename = f"{agent_name}_report.json"
#         filepath = os.path.join(reports_dir, filename)

#         try:
#             with open(filepath, "w") as f:
#                 json.dump(data_json, f, indent=4)
#             print(f"Data saved to {filepath}")
#         except Exception as e:
#             print(f"Error saving JSON to file: {e}")