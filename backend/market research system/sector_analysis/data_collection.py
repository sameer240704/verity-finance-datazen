from utils.tavily_api import TavilyAPI
from utils.faiss_index import FAISSIndex
from models.gemini_model import GeminiModel

class SectorDataCollectionAgent:
    def __init__(self, gemini_model, sector_name, brief_aim, data_validation_agent):
        self.gemini_model = gemini_model
        self.sector_name = sector_name
        self.brief_aim = brief_aim
        self.tavily_api = TavilyAPI()
        self.faiss_index = FAISSIndex(index_path="backend/market research system/utils/faiss_index")
        self.data_validation_agent = data_validation_agent
        self.prompt_template = """
        You are a Data Collection Agent for sector analysis.
        Your goal is to gather the latest news, articles, and data related to the '{sector_name}' sector.
        Focus on collecting quantitative data and key market trends.
        Use the Tavily Search API to find recent information.
        Perform Retrieval-Augmented Generation (RAG) using the FAISS index with recent articles relevant to '{sector_name}'.
        Process and synthesize the collected information, paying close attention to quantitative data and market trends.
        Aim: {brief_aim}

        Tavily Search API:
        - Use the search query: "Latest news and trends in {sector_name}"

        FAISS RAG:
        - Use relevant documents from the FAISS index for '{sector_name}' to augment your response.

        Output the collected data in the following format:
        {{
            "quantitative_data": {{ /* Quantitative data related to the sector */ }},
            "qualitative_data": {{ /* Qualitative data (news, trends, opinions) */ }},
            "tavily_results": [ /* Raw results from Tavily */ ],
            "faiss_rag_results": [ /* Raw results from FAISS RAG */ ]
        }}
        """

    def run(self):
        """
        Runs the data collection process.
        """
        prompt = self.prompt_template.format(sector_name=self.sector_name, brief_aim=self.brief_aim)
        
        tavily_query = f"Latest news and trends in {self.sector_name}"
        tavily_results = self.tavily_api.search(tavily_query)

        # Assuming FAISS index is pre-populated and can be queried based on sector name
        faiss_rag_results = self.faiss_index.query_index(self.sector_name)

        # Combine and process data using Gemini
        # Construct a message that includes the prompt, Tavily results, and FAISS results
        combined_data = {
            "prompt": prompt,
            "tavily_results": tavily_results,
            "faiss_rag_results": faiss_rag_results
        }

        # Convert combined data to a string format suitable for Gemini input
        # This step depends on how you want to structure the input for Gemini
        # You might need to serialize the data or format it according to Gemini's expectations
        combined_data_str = str(combined_data)  # Simplified for demonstration

        # Use Gemini to process the combined data
        gemini_response = self.gemini_model.get_response(combined_data_str)

        # Assuming Gemini's response is in the desired format, you can now validate it
        # Or, if further processing is needed, you can add that logic here
        validated_response = self.data_validation_agent.validate(gemini_response)
        
        # Return the validated response
        return validated_response