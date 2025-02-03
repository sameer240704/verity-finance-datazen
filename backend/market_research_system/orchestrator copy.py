from sector_analysis.data_collection import SectorDataCollectionAgent
from sector_analysis.quantitative_analysis import QuantitativeAnalysisAgent
from sector_analysis.qualitative_analysis import QualitativeAnalysisAgent
from sector_analysis.reporting import SectorReportingAgent
from stock_analysis.stock_data_collection import StockDataCollectionAgent
from stock_analysis.financial_analysis import StockFinancialAnalysisAgent
from stock_analysis.news_sentiment_analysis import StockNewsSentimentAnalysisAgent
from stock_analysis.stock_reporting import StockReportingAgent
from data_validation_agent import DataValidationAgent
from data_extraction_agent import DataExtractionAgent
from models.openai_model import OpenAIModel
from models.gemini_model import GeminiModel
import os
import json

class OrchestratorAgent:
    def __init__(self):
        self.openai_model = OpenAIModel(api_key=os.environ["AZURE_OPENAI_API_KEY"])
        self.gemini_model = GeminiModel()
        self.data_extraction_agent = DataExtractionAgent()

    def create_and_run_agents(self, agent_type, agent_name, sector_stock_name, brief_aim):
        """
        Creates and runs the appropriate agents based on user input.
        """
        data_validation_agent = DataValidationAgent(self.openai_model)

        if agent_type.lower() == "sector":
            data_collection_agent = SectorDataCollectionAgent(
                self.gemini_model, sector_stock_name, brief_aim, data_validation_agent
            )
            quantitative_analysis_agent = QuantitativeAnalysisAgent(
                self.openai_model, data_validation_agent
            )
            qualitative_analysis_agent = QualitativeAnalysisAgent(
                self.openai_model, data_validation_agent
            )
            reporting_agent = SectorReportingAgent(self.openai_model)

            # Run Sector Analysis Agents
            data_collection_output = data_collection_agent.run()
            
            quantitative_analysis_input = data_validation_agent.validate(data_collection_output)
            qualitative_analysis_input = data_validation_agent.validate(data_collection_output)

            quantitative_analysis_output = quantitative_analysis_agent.run(quantitative_analysis_input)
            qualitative_analysis_output = qualitative_analysis_agent.run(qualitative_analysis_input)

            final_report = reporting_agent.run(
                data_collection_output,
                quantitative_analysis_output,
                qualitative_analysis_output,
                agent_name
            )
            print(final_report)

            # Save the text report
            report_filepath = os.path.join("reports", f"{agent_name}_report.txt")
            os.makedirs(os.path.dirname(report_filepath), exist_ok=True)  # Create directory if it doesn't exist
            with open(report_filepath, "w") as f:
                f.write(final_report)

            # Extract data to JSON using the DataExtractionAgent
            extracted_data = self.data_extraction_agent.run(report_filepath, agent_name)
            print("Extracted JSON:", extracted_data)

        elif agent_type.lower() == "stock":
            stock_data_collection_agent = StockDataCollectionAgent(
                self.gemini_model, sector_stock_name, brief_aim, data_validation_agent
            )
            financial_analysis_agent = StockFinancialAnalysisAgent(
                self.openai_model, data_validation_agent
            )
            news_sentiment_analysis_agent = StockNewsSentimentAnalysisAgent(
                self.openai_model, data_validation_agent
            )
            stock_reporting_agent = StockReportingAgent(self.openai_model)

            # Run Stock Analysis Agents
            stock_data_output = stock_data_collection_agent.run()

            financial_analysis_input = data_validation_agent.validate(stock_data_output)
            news_sentiment_input = data_validation_agent.validate(stock_data_output)

            financial_analysis_output = financial_analysis_agent.run(financial_analysis_input)
            news_sentiment_output = news_sentiment_analysis_agent.run(news_sentiment_input)

            final_report = stock_reporting_agent.run(
                stock_data_output, financial_analysis_output, news_sentiment_output, agent_name
            )
            print(final_report)

            # Save the text report
            report_filepath = os.path.join("reports", f"{agent_name}_report.txt")
            os.makedirs(os.path.dirname(report_filepath), exist_ok=True)  # Create directory if it doesn't exist
            with open(report_filepath, "w") as f:
                f.write(final_report)

            # Extract data to JSON using the DataExtractionAgent
            extracted_data = self.data_extraction_agent.run(report_filepath, agent_name)
            print("Extracted JSON:", extracted_data)

        else:
            print("Invalid agent type.")

