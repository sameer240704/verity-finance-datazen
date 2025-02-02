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
        self.sector_prompt_template = """
        You are a Data Extraction Agent. Your task is to extract specific information from a sector analysis report and structure it into a JSON format.

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

        self.stock_prompt_template = """
        You are a Data Extraction Agent. Your task is to extract specific information from a stock analysis report and structure it into a JSON format.

        The report follows a consistent structure with sections for Company Details, Financial Analysis, News and Sentiment, Tavily Report, Sources, and Overall Assessment.

        Your output MUST be valid JSON in the following format:

        ```json
        {{
          "company_details": {{
            "company_name": "...",
            "sector": "...",
            "industry": "...",
            "exchange": "..."
          }},
          "financial_analysis": {{
            "ratio_analysis": "...",
            "profitability": "...",
            "valuation": "..."
          }},
          "news_and_sentiment": {{
            "recent_news": "...",
            "sentiment_analysis": "...",
            "potential_impact": "..."
          }},
          "tavily_report": {{
            "key_insights": "..."
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
          "overall_assessment": {{
            "recommendation": "...",
            "justification": "..."
          }
        }}
        ```

        **Instructions:**

        1. **Company Details:** Extract the company name, sector, industry, and exchange from the "Company Details" section.

        2. **Financial Analysis:** Extract the ratio analysis, profitability, and valuation information from the "Financial Analysis" section.

        3. **News and Sentiment:** Extract the recent news, sentiment analysis, and potential impact from the "News and Sentiment" section.

        4. **Tavily Report:** Extract the key insights from the "Tavily Report" section.

        5. **Sources:** Extract the source names and URLs from the "Sources" section. Use regular expressions to find the URLs.

        6. **Overall Assessment:** Extract the recommendation and justification from the "Overall Assessment" section.

        **Input Report:**

        {report_text}
        """


    def run(self, report_filepath, agent_name="ExtractedData", agent_type="sector"):
        """
        Extracts data from the given report file, saves the raw Gemini output as a .txt file,
        and then attempts to extract data using regex as a fallback if Gemini's output is not valid JSON.

        Args:
            report_filepath: The path to the text report file.
            agent_name: The name of the agent (used for the output filenames).
            agent_type: The type of agent ("sector" or "stock").
        """
        try:
            with open(report_filepath, "r") as f:
                report_text = f.read()
        except FileNotFoundError:
            print(f"Error: Report file not found at {report_filepath}")
            return

        if agent_type == "sector":
            prompt = self.sector_prompt_template.format(report_text=report_text)
        elif agent_type == "stock":
            prompt = self.stock_prompt_template.format(report_text=report_text)
        else:
            print("Error: Invalid agent type specified.")
            return

        response = self.gemini_model.get_response(prompt)

        print("-" * 30)
        print(f"Data Extraction Agent Output ({agent_type.upper()}):")
        print(response)
        print("-" * 30)

        # Save the raw Gemini output to a text file
        reports_dir = "reports"
        os.makedirs(reports_dir, exist_ok=True)
        raw_output_filepath = os.path.join(reports_dir, f"{agent_name}_raw.txt")
        with open(raw_output_filepath, "w") as f:
            f.write(response)
        print(f"Raw Gemini output saved to {raw_output_filepath}")

        try:
            # Attempt to parse the response as JSON
            data_json = json.loads(response)
            print(f"Successfully parsed Gemini response as JSON ({agent_type.upper()}).")
        except json.JSONDecodeError:
            print(f"Error: Gemini response is not valid JSON ({agent_type.upper()}). Using regex as fallback.")
            if agent_type == "sector":
                data_json = self.extract_data_to_json_with_regex_sector(report_text)
            elif agent_type == "stock":
                data_json = self.extract_data_to_json_with_regex_stock(report_text)
            else:
                print("Error: Invalid agent type specified.")
                return

        # Save the JSON to a file
        self.save_data_to_file(data_json, agent_name)

        return data_json

    def extract_data_to_json_with_regex_sector(self, report_text):
        """
        Extracts data from the sector report text using regex and creates a JSON object. This is a fallback method.
        """
        data_json = {
            "market_metrics": {},
            "sources": [],
            "top_5_stocks": []
        }

        # Market Metrics
        market_metrics_section = re.search(r"# Market Metrics(.*?)(?=#|$)", report_text, re.DOTALL)
        if market_metrics_section:
            market_metrics_text = market_metrics_section.group(1)
            for line in market_metrics_text.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    data_json["market_metrics"][key.strip()] = value.strip()

        # Sources
        sources_section = re.search(r"# Sources(.*?)(?=#|$)", report_text, re.DOTALL)
        if sources_section:
            sources_text = sources_section.group(1)
            data_json["sources"] = self.extract_sources(sources_text)

        # Top 5 Performing Stocks
        top_stocks_section = re.search(r"# Top 5 Performing Stocks(.*?)(?=#|$)", report_text, re.DOTALL)
        if top_stocks_section:
            top_stocks_text = top_stocks_section.group(1)
            data_json["top_5_stocks"] = self.extract_top_stocks(top_stocks_text)

        return data_json

    def extract_data_to_json_with_regex_stock(self, report_text):
        """
        Extracts data from the stock report text using regex and creates a JSON object. This is a fallback method.
        """
        data_json = {}

        # Company Details
        company_details_match = re.search(r"## Company Details(.*?)(?=(##|$))", report_text, re.DOTALL)
        if company_details_match:
            data_json["company_details"] = self.extract_company_details(company_details_match.group(1))

        # Financial Analysis
        financial_analysis_match = re.search(r"## Financial Analysis(.*?)(?=(##|$))", report_text, re.DOTALL)
        if financial_analysis_match:
            data_json["financial_analysis"] = self.extract_financial_analysis(financial_analysis_match.group(1))

        # News and Sentiment
        news_sentiment_match = re.search(r"## News and Sentiment(.*?)(?=(##|$))", report_text, re.DOTALL)
        if news_sentiment_match:
            data_json["news_and_sentiment"] = self.extract_news_and_sentiment(news_sentiment_match.group(1))

        # Tavily Report
        tavily_report_match = re.search(r"## Tavily Report(.*?)(?=(##|$))", report_text, re.DOTALL)
        if tavily_report_match:
            data_json["tavily_report"] = self.extract_tavily_report(tavily_report_match.group(1))

        # Sources
        sources_match = re.search(r"## Sources(.*?)(?=(##|$))", report_text, re.DOTALL)
        if sources_match:
            data_json["sources"] = self.extract_sources(sources_match.group(1))

        # Overall Assessment
        overall_assessment_match = re.search(r"## Overall Assessment(.*?)(?=(##|$))", report_text, re.DOTALL)
        if overall_assessment_match:
            data_json["overall_assessment"] = self.extract_overall_assessment(overall_assessment_match.group(1))

        return data_json

    def extract_company_details(self, text):
        """
        Extracts company details using regex.
        """
        details = {}
        # Improved regex patterns to capture company details
        company_name_match = re.search(r"- \*\*Company Name:\*\* (.*)", text)
        sector_match = re.search(r"- \*\*Sector:\*\* (.*)", text)
        industry_match = re.search(r"- \*\*Industry:\*\* (.*)", text)
        exchange_match = re.search(r"- \*\*Exchange:\*\* (.*)", text)

        if company_name_match:
            details["company_name"] = company_name_match.group(1).strip()
        if sector_match:
            details["sector"] = sector_match.group(1).strip()
        if industry_match:
            details["industry"] = industry_match.group(1).strip()
        if exchange_match:
            details["exchange"] = exchange_match.group(1).strip()

        return details

    def extract_financial_analysis(self, text):
        """
        Extracts financial analysis details using regex.
        """
        analysis = {}
        # Regex patterns to capture financial analysis details
        ratio_analysis_match = re.search(r"- \*\*Ratio Analysis:\*\* (.*?)(?=-|$)", text, re.DOTALL)
        profitability_match = re.search(r"- \*\*Profitability:\*\* (.*?)(?=-|$)", text, re.DOTALL)
        valuation_match = re.search(r"- \*\*Valuation:\*\* (.*?)(?=-|$)", text, re.DOTALL)

        if ratio_analysis_match:
            analysis["ratio_analysis"] = ratio_analysis_match.group(1).strip()
        if profitability_match:
            analysis["profitability"] = profitability_match.group(1).strip()
        if valuation_match:
            analysis["valuation"] = valuation_match.group(1).strip()

        return analysis

    def extract_news_and_sentiment(self, text):
        """
        Extracts news and sentiment details using regex.
        """
        news_sentiment = {}
        # Regex patterns to capture news and sentiment details
        recent_news_match = re.search(r"- \*\*Recent News:\*\* (.*?)(?=-|$)", text, re.DOTALL)
        sentiment_analysis_match = re.search(r"- \*\*Sentiment Analysis:\*\* (.*?)(?=-|$)", text, re.DOTALL)
        potential_impact_match = re.search(r"- \*\*Potential Impact:\*\* (.*?)(?=-|$)", text, re.DOTALL)

        if recent_news_match:
            news_sentiment["recent_news"] = recent_news_match.group(1).strip()
        if sentiment_analysis_match:
            news_sentiment["sentiment_analysis"] = sentiment_analysis_match.group(1).strip()
        if potential_impact_match:
            news_sentiment["potential_impact"] = potential_impact_match.group(1).strip()

        return news_sentiment

    def extract_tavily_report(self, text):
        """
        Extracts key insights from Tavily report using regex.
        """
        tavily_report = {}
        # Regex pattern to capture key insights from Tavily report
        key_insights_match = re.search(r"- \*\*Key Insights:\*\* (.*?)(?=-|$)", text, re.DOTALL)

        if key_insights_match:
            tavily_report["key_insights"] = key_insights_match.group(1).strip()

        return tavily_report

    def extract_overall_assessment(self, text):
        """
        Extracts overall assessment details using regex.
        """
        assessment = {}
        # Regex patterns to capture overall assessment details
        recommendation_match = re.search(r"- \*\*Recommendation:\*\* (.*)", text)
        justification_match = re.search(r"- \*\*Justification:\*\* (.*?)(?=-|$)", text, re.DOTALL)

        if recommendation_match:
            assessment["recommendation"] = recommendation_match.group(1).strip()
        if justification_match:
            assessment["justification"] = justification_match.group(1).strip()

        return assessment

    def extract_sources(self, text):
        """
        Extracts source URLs using regex.
        """
        sources = []
        source_matches = re.findall(r"(\S+)\s+\((https?://.*?)\)", text)
        for source_name, url in source_matches:
            sources.append({"name": source_name, "url": url})
        return sources
    
    def extract_top_stocks(self, text):
        """
        Extracts top stock information using regex.
        """
        stocks = []
        # Regex to find stock name, ticker, and justification
        stock_matches = re.findall(r"-\s*\*\*([A-Za-z\s&.]+)\s*\((\w+)\):\*\*\s*(.*?)(?=-|$)", text, re.DOTALL)
        for stock_name, ticker, justification in stock_matches:
            stocks.append({
                "stock_name": stock_name.strip(),
                "ticker": ticker.strip(),
                "justification": justification.strip()
            })
        return stocks

    def fetch_stock_data(self, data_json):
        """
        Fetches current price and 30-day performance for each stock using yfinance or RapidAPI.
        """
        if "top_5_stocks" not in data_json:
            return data_json
        
        for stock_data in data_json["top_5_stocks"]:
            ticker = stock_data["ticker"]
            try:
                # Try yfinance first
                current_price = self.yfinance_api.get_current_price(ticker)
                if current_price is None:
                    raise ValueError("yfinance did not return a current price.")
                stock_data["current_price"] = current_price

                performance_30d = self.yfinance_api.get_performance(ticker, period="30d")
                if performance_30d is None:
                  raise ValueError("yfinance did not return a 30-day performance.")
                stock_data["30_day_performance"] = performance_30d

            except Exception as e:
                print(f"Error fetching stock data from yfinance for {ticker}: {e}")
                try:
                    # Fallback to RapidAPI
                    current_price = self.rapidapi_api.get_current_price(ticker)
                    if current_price is None:
                        raise ValueError("RapidAPI did not return a current price.")
                    stock_data["current_price"] = current_price

                    performance_30d = self.rapidapi_api.get_performance(ticker, period="30d")
                    if performance_30d is None:
                        raise ValueError("RapidAPI did not return a 30-day performance.")
                    stock_data["30_day_performance"] = performance_30d

                except Exception as e_rapid:
                    print(f"Error fetching stock data from RapidAPI for {ticker}: {e_rapid}")
                    stock_data["current_price"] = "N/A"
                    stock_data["30_day_performance"] = "N/A"

        return data_json

    def save_data_to_file(self, data_json, agent_name):
        """
        Saves the extracted data to a JSON file.
        """
        reports_dir = "reports"
        os.makedirs(reports_dir, exist_ok=True)

        filename = f"{agent_name}_report.json"
        filepath = os.path.join(reports_dir, filename)

        try:
            with open(filepath, "w") as f:
                json.dump(data_json, f, indent=4)
            print(f"Data saved to {filepath}")
        except Exception as e:
            print(f"Error saving JSON to file: {e}")