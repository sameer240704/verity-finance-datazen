from utils.tavily_api import TavilyAPI
# from utils.faiss_index import FAISSIndex
from models.gemini_model import GeminiModel
import json
import ast
import json
from typing import Dict
from utils.data_processing import clean_response_string

class SectorDataCollectionAgent:
    def __init__(self, gemini_model, sector_name, brief_aim, data_validation_agent):
        self.gemini_model = gemini_model
        self.sector_name = sector_name
        self.brief_aim = brief_aim
        self.tavily_api = TavilyAPI()
        # self.faiss_index = FAISSIndex()
        self.data_validation_agent = data_validation_agent
        self.prompt_template = """
        You are a Data Collection Agent for sector analysis.
        Your goal is to gather the latest news, articles, and data related to the '{sector_name}' sector.
        Focus on collecting quantitative data and key market trends.
        Use the Tavily Search API to find recent information.
        Process and synthesize the collected information, paying close attention to quantitative data and market trends.
        Aim: {brief_aim}

        Tavily Search API:
        - Use the search query: "Latest news and trends in {sector_name}"

        Provide your response as a detailed paragraph or a bulleted list. DO NOT FORMAT THE RESPONSE AS JSON.
        """

    def run(self):
        prompt = self.prompt_template.format(sector_name=self.sector_name, brief_aim=self.brief_aim)

        tavily_query = f"Latest news and trends in {self.sector_name}"
        tavily_results = self.tavily_api.search(tavily_query)

        # Combine and process data using Gemini
        combined_data = {
            "prompt": prompt,
            "tavily_results": tavily_results,
        }

        combined_data_str = str(combined_data)

        gemini_response = self.gemini_model.get_response(combined_data_str)
        print("Raw Gemini Response (Sector):", gemini_response)

        # Return the raw Gemini response (no cleaning or parsing needed)
        return gemini_response