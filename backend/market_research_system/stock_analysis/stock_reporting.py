import re
import json
import os

class StockReportingAgent:
    def __init__(self, openai_model):
        self.openai_model = openai_model
        self.prompt_template = """
        You are a Stock Reporting Agent.
        Your task is to compile a comprehensive report based on the findings from the Stock Data Collection, Financial Analysis, News and Sentiment Analysis, and Data Validation Agents.
        Generate a report with the following structure:

        # Stock Analysis Report: [Stock Name] ([Ticker Symbol])

        ## 1. Stock Chart

        Provide a link to the stock chart or a brief description of the chart's data (e.g., price movement, trends).

        ## 2. Company Details

        Provide key details about the company. Use the following format:

        - **Company Name:** (Full name of the company)
        - **Sector:** (The sector the company operates in)
        - **Industry:** (The specific industry within the sector)
        - **Exchange:** (The stock exchange the company is listed on, e.g., NYSE, NASDAQ)

        ## 3. Financial Analysis

        Provide a detailed financial analysis. Include:

        - **Ratio Analysis:** (e.g., P/E, P/B, Debt/Equity, EPS)
        - **Profitability:** (e.g., Gross Margin, Operating Margin, Net Profit Margin)
        - **Valuation:** (Assessment of whether the stock is overvalued, undervalued, or fairly valued)

        ## 4. News and Sentiment

        Provide an analysis of the news sentiment. Include:

        - **Recent News:** (Summary of recent news articles about the company)
        - **Sentiment Analysis:** (Overall sentiment from the news - Positive, Negative, Neutral)
        - **Potential Impact:** (How the news might impact the stock price)

        ## 5. Tavily Report

        Summarize the key findings from the Tavily data collection. Include:

        - **Key Insights:** (Bullet points of the most important information from Tavily)

        ## 6. Sources

        List all the sources used to gather the data. Provide the full URL for each source. Use the following format:

        - Source Name 1 (Full URL 1)
        - Source Name 2 (Full URL 2)
        - ...

        ## 7. Overall Assessment

        Provide an overall assessment of the stock with a clear recommendation. Use the following format:

        - **Recommendation:** (Buy, Sell, or Hold)
        - **Justification:** (Detailed reasoning for the recommendation)

        Input:
        {stock_data_output}
        {financial_analysis_output}
        {news_sentiment_output}
        """

    def run(self, stock_data_output, financial_analysis_output, news_sentiment_output, agent_name="StockReport"):
        """
        Generates the final stock analysis report.
        """

        # Convert inputs to strings if they are not already
        if not isinstance(stock_data_output, str):
            stock_data_output = json.dumps(stock_data_output)
        if not isinstance(financial_analysis_output, str):
            financial_analysis_output = json.dumps(financial_analysis_output)
        if not isinstance(news_sentiment_output, str):
            news_sentiment_output = json.dumps(news_sentiment_output)

        # Double escape braces if the input is potentially a JSON string
        if isinstance(stock_data_output, str):
            stock_data_output = stock_data_output.replace("{", "{{").replace("}", "}}")
        if isinstance(financial_analysis_output, str):
            financial_analysis_output = financial_analysis_output.replace("{", "{{").replace("}", "}}")
        if isinstance(news_sentiment_output, str):
            news_sentiment_output = news_sentiment_output.replace("{", "{{").replace("}", "}}")

        print("stock_data_output:", stock_data_output)
        print("financial_analysis_output:", financial_analysis_output)
        print("news_sentiment_output:", news_sentiment_output)
        
        prompt = self.prompt_template.format(
            stock_data_output=stock_data_output,
            financial_analysis_output=financial_analysis_output,
            news_sentiment_output=news_sentiment_output
        )
        response = self.openai_model.get_response(prompt)

        # Debugging: Print the generated report to the terminal
        print("*" * 30)
        print("Generated Stock Analysis Report:")
        print(response)
        print("*" * 30)

        # Save the text report
        report_filepath = os.path.join("reports", f"{agent_name}_report.txt")
        os.makedirs(os.path.dirname(report_filepath), exist_ok=True)  # Create directory if it doesn't exist
        with open(report_filepath, "w") as f:
            f.write(response)

        return response