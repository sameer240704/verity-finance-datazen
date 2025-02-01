class StockReportingAgent:
    def __init__(self, openai_model):
        self.openai_model = openai_model
        self.prompt_template = """
        You are a Stock Reporting Agent.
        Your task is to compile a comprehensive report based on the findings from the Stock Data Collection, Financial Analysis, News and Sentiment Analysis, and Data Validation Agents.
        Generate a JSON report with the following structure:
        {{
          "stock_chart": " /* Base64 encoded image data or URL of the stock chart, from Stock Data Collection Agent */ ",
          "company_details": {{ /* Company information from YFinance/RapidAPI, from Stock Data Collection Agent */ }},
          "financial_analysis": {{ /* Ratio analysis, valuation, etc., from Financial Analysis Agent */ }},
          "news_and_sentiment": " /* Analysis of news and sentiment, from News and Sentiment Analysis Agent */ ",
          "tavily_report": " /* Summary of relevant information from Tavily, from Stock Data Collection Agent */ ",
          "rag_report": " /* Summary of relevant information from RAG, from Stock Data Collection Agent */ ",
          "sources": [ /* URLs from Tavily and other sources, from Stock Data Collection Agent */ ],
          "overall_assessment": " /* Buy/Sell/Hold recommendation with justification, based on all agents' data */ "
        }}
        Input:
        {{
            "stock_data": {stock_data_output},
            "financial_analysis": {financial_analysis_output},
            "news_sentiment": {news_sentiment_output}
        }}
        """

    def run(self, stock_data_output, financial_analysis_output, news_sentiment_output):
        """
        Generates the final stock analysis report.
        """
        prompt = self.prompt_template.format(
            stock_data_output=stock_data_output,
            financial_analysis_output=financial_analysis_output,
            news_sentiment_output=news_sentiment_output
        )
        response = self.openai_model.get_json_response(prompt)
        return response