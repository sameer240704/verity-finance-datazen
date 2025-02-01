from utils.tavily_api import TavilyAPI
from utils.faiss_index import FAISSIndex
from utils.yfinance_api import YFinanceAPI
from utils.rapidapi_api import RapidAPI
from models.gemini_model import GeminiModel
from utils.faiss_index import FAISSIndex
from models.gemini_model import GeminiModel

class StockDataCollectionAgent:
    def __init__(self, gemini_model, stock_name, brief_aim, data_validation_agent):
        self.gemini_model = gemini_model
        self.stock_name = stock_name
        self.brief_aim = brief_aim
        self.tavily_api = TavilyAPI()
        self.faiss_index = FAISSIndex(index_path="backend/market research system/utils/faiss_index")
        self.yfinance_api = YFinanceAPI()
        self.rapidapi_api = RapidAPI()
        self.data_validation_agent = data_validation_agent
        self.prompt_template = """
        You are a Stock Data Collection Agent.
        Your goal is to gather news, articles, reports, historical stock chart data, and key financial data related to '{stock_name}'.
        Aim: {brief_aim}

        Tasks:
        1. Use the Tavily Search API to find recent information about '{stock_name}'.
           - Search query: "News and reports on {stock_name}"
        2. Perform Retrieval-Augmented Generation (RAG) using the FAISS index with documents relevant to '{stock_name}'.
        3. Retrieve the historical stock chart data for '{stock_name}' using YFinance.
        4. Extract key financial data (revenue, earnings, etc.) and company information for '{stock_name}' using YFinance or RapidAPI. You can use function calling if necessary.

        Output the collected data in the following format:
        {{
            "financial_data": {{ /* Key financial data */ }},
            "news_data": {{ /* News and sentiment data */ }},
            "stock_chart_data": "...", /* Base64 encoded image data or URL of the stock chart */
            "company_details": {{ /* Company information */ }},
            "tavily_results": [ /* Raw results from Tavily */ ],
            "faiss_rag_results": [ /* Raw results from FAISS RAG */ ]
        }}
        """

    def run(self):
        """
        Runs the data collection process for stock analysis.
        """
        prompt = self.prompt_template.format(stock_name=self.stock_name, brief_aim=self.brief_aim)

        tavily_query = f"News and reports on {self.stock_name}"
        tavily_results = self.tavily_api.search(tavily_query)

        faiss_rag_results = self.faiss_index.query_index(self.stock_name)

        stock_chart_data = self.yfinance_api.get_stock_chart(self.stock_name)
        company_details = self.yfinance_api.get_company_info(self.stock_name)
        if company_details == {}:
          company_details = self.rapidapi_api.get_company_info(self.stock_name)
        financial_data = self.yfinance_api.get_financial_data(self.stock_name)
        if financial_data == {}:
          financial_data = self.rapidapi_api.get_financial_data(self.stock_name)

        # Combine and process data using Gemini
        combined_data = {
            "prompt": prompt,
            "tavily_results": tavily_results,
            "faiss_rag_results": faiss_rag_results,
            "stock_chart_data": stock_chart_data,
            "company_details": company_details,
            "financial_data": financial_data
        }
        combined_data_str = str(combined_data)

        gemini_response = self.gemini_model.get_response(combined_data_str)
        validated_response = self.data_validation_agent.validate(gemini_response)

        return validated_response