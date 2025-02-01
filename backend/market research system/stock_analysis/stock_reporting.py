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
        {{
            "stock_data": {stock_data_output},
            "financial_analysis": {financial_analysis_output},
            "news_sentiment": {news_sentiment_output}
        }}
        """

    def run(self, stock_data_output, financial_analysis_output, news_sentiment_output, agent_name="StockReport"):
        """
        Generates the final stock analysis report.
        """
        prompt = self.prompt_template.format(
            stock_data_output=stock_data_output,
            financial_analysis_output=financial_analysis_output,
            news_sentiment_output=news_sentiment_output
        )
        response = self.openai_model.get_response(prompt)

        # Extract data using regex and create JSON
        report_json = self.extract_data_to_json(response)

        # Save the JSON to a file
        self.save_report_to_file(report_json, agent_name)

        return response

    def extract_data_to_json(self, report_text):
        """
        Extracts data from the report text using regex and creates a JSON object.
        """
        report_json = {}

        # Stock Chart
        stock_chart_match = re.search(r"## 1\. Stock Chart\n(.*?)\n##", report_text, re.DOTALL)
        if stock_chart_match:
            report_json["stock_chart"] = stock_chart_match.group(1).strip()

        # Company Details
        company_details_match = re.search(r"## 2\. Company Details\n(.*?)\n##", report_text, re.DOTALL)
        if company_details_match:
            report_json["company_details"] = self.extract_company_details(company_details_match.group(1))

        # Financial Analysis
        financial_analysis_match = re.search(r"## 3\. Financial Analysis\n(.*?)\n##", report_text, re.DOTALL)
        if financial_analysis_match:
            report_json["financial_analysis"] = self.extract_financial_analysis(financial_analysis_match.group(1))

        # News and Sentiment
        news_sentiment_match = re.search(r"## 4\. News and Sentiment\n(.*?)\n##", report_text, re.DOTALL)
        if news_sentiment_match:
            report_json["news_and_sentiment"] = self.extract_news_and_sentiment(news_sentiment_match.group(1))

        # Tavily Report
        tavily_report_match = re.search(r"## 5\. Tavily Report\n(.*?)\n##", report_text, re.DOTALL)
        if tavily_report_match:
            report_json["tavily_report"] = self.extract_tavily_report(tavily_report_match.group(1))

        # Sources
        sources_match = re.search(r"## 6\. Sources\n(.*?)\n##", report_text, re.DOTALL)
        if sources_match:
            report_json["sources"] = self.extract_sources(sources_match.group(1))

        # Overall Assessment
        overall_assessment_match = re.search(r"## 7\. Overall Assessment\n(.*)", report_text, re.DOTALL)
        if overall_assessment_match:
            report_json["overall_assessment"] = self.extract_overall_assessment(overall_assessment_match.group(1))

        return report_json

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

    def extract_sources(self, text):
        """
        Extracts source URLs using regex.
        """
        # Regex to match the new format for sources
        sources = []
        source_matches = re.findall(r"- (.*?) \((https?://.*?)\)", text)
        for source_name, url in source_matches:
            sources.append({"name": source_name.strip(), "url": url.strip()})

        return sources

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

    def save_report_to_file(self, report_json, agent_name):
        """
        Saves the report JSON to a file.
        """
        filename = f"{agent_name}_report.json"
        filepath = os.path.join(".", filename)  # Save to the current directory
        with open(filepath, "w") as f:
            json.dump(report_json, f, indent=4)
        print(f"Report saved to {filepath}")