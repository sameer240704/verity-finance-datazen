import re
import json
import os

class SectorReportingAgent:
    def __init__(self, openai_model):
        self.openai_model = openai_model
        self.prompt_template = """
        You are a Reporting Agent.
        Your task is to compile a comprehensive technical report based on the findings from the Data Collection, Quantitative Analysis, Qualitative Analysis, and Data Validation Agents.

        # Sector Analysis Report

        ## 1. Market Metrics

        Provide a detailed breakdown of quantitative data. Include specific metrics and use the following format for each:

        - **Market Size:** (Total market value or volume, specify the year)
        - **Growth Rate:** (Annual growth rate, specify the period)
        - **Market Share:** (Provide a breakdown of market share by key players or segments, if available)
        - **Financial Ratios:** (Include relevant ratios like Price/Earnings, Price/Sales, etc., if applicable)
        - **Other Metrics:** (Any other relevant quantitative data)

        ## 2. Analysis Report

        Provide a comprehensive technical analysis, combining qualitative and quantitative insights. Discuss:

        - **Overall Market Trends:** (Major trends shaping the sector)
        - **Technological Advancements:** (Key innovations and their impact)
        - **Regulatory Impacts:** (Government policies, regulations, and their effects)
        - **Competitive Landscape:** (Major players, their strategies, and market positioning)
        - **Opportunities:** (Potential growth areas and emerging markets)
        - **Risks:** (Potential challenges and threats to the sector)
        - **Market Sentiment:** (Overall sentiment towards the sector from investors, consumers, etc.)

        ## 3. Sources

        List all the sources used to gather the data. Provide the full URL for each source. Use the following format:

        - Source Name 1 (Full URL 1)
        - Source Name 2 (Full URL 2)
        - ...

        ## 4. Top 5 Performing Stocks

        List the top 5 performing stocks in the sector. Use the following format for each stock:

        - **Stock Name (Ticker Symbol):**
            - **Market Performance:** (e.g., Stock price increase, YTD performance)
            - **Justification:** (Brief explanation of why it's a top performer)

        Input:
        Data Collection: {data_collection_output}
        Quantitative Analysis: {quantitative_analysis_output}
        Qualitative Analysis: {qualitative_analysis_output}
        """

    def run(self, data_collection_output, quantitative_analysis_output, qualitative_analysis_output, agent_name="SectorReport"):
        """
        Generates the final sector analysis report.
        """
        prompt = self.prompt_template.format(
            data_collection_output=data_collection_output,
            quantitative_analysis_output=quantitative_analysis_output,
            qualitative_analysis_output=qualitative_analysis_output
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

        # Market Metrics
        market_metrics_match = re.search(r"## 1\. Market Metrics\n(.*?)\n##", report_text, re.DOTALL)
        if market_metrics_match:
            market_metrics_text = market_metrics_match.group(1)
            report_json["market_metrics"] = self.extract_market_metrics(market_metrics_text)

        # Analysis Report
        analysis_report_match = re.search(r"## 2\. Analysis Report\n(.*?)\n##", report_text, re.DOTALL)
        if analysis_report_match:
            report_json["analysis_report"] = self.extract_analysis_report(analysis_report_match.group(1))

        # Sources
        sources_match = re.search(r"## 3\. Sources\n(.*?)\n##", report_text, re.DOTALL)
        if sources_match:
            sources_text = sources_match.group(1)
            report_json["sources"] = self.extract_sources(sources_text)

        # Top 5 Performing Stocks
        top_stocks_match = re.search(r"## 4\. Top 5 Performing Stocks\n(.*)", report_text, re.DOTALL)
        if top_stocks_match:
            top_stocks_text = top_stocks_match.group(1)
            report_json["top_5_stocks"] = self.extract_top_stocks(top_stocks_text)

        return report_json
    
    def extract_market_metrics(self, text):
        """
        Extracts market metrics using regex.
        """
        metrics = {}
        # Improved regex patterns to capture metrics more accurately
        market_size_match = re.search(r"- \*\*Market Size:\*\* (.*?)(?=-|$)", text, re.DOTALL)
        growth_rate_match = re.search(r"- \*\*Growth Rate:\*\* (.*?)(?=-|$)", text, re.DOTALL)
        market_share_match = re.search(r"- \*\*Market Share:\*\* (.*?)(?=-|$)", text, re.DOTALL)
        financial_ratios_match = re.search(r"- \*\*Financial Ratios:\*\* (.*?)(?=-|$)", text, re.DOTALL)
        other_metrics_match = re.search(r"- \*\*Other Metrics:\*\* (.*?)(?=-|$)", text, re.DOTALL)

        if market_size_match:
            metrics["market_size"] = market_size_match.group(1).strip()
        if growth_rate_match:
            metrics["growth_rate"] = growth_rate_match.group(1).strip()
        if market_share_match:
            metrics["market_share"] = market_share_match.group(1).strip()
        if financial_ratios_match:
            metrics["financial_ratios"] = financial_ratios_match.group(1).strip()
        if other_metrics_match:
            metrics["other_metrics"] = other_metrics_match.group(1).strip()

        return metrics

    def extract_analysis_report(self, text):
        """
        Extracts analysis report sections using regex.
        """
        analysis = {}
        # Define sections to extract
        sections = {
            "Overall Market Trends": "Overall Market Trends",
            "Technological Advancements": "Technological Advancements",
            "Regulatory Impacts": "Regulatory Impacts",
            "Competitive Landscape": "Competitive Landscape",
            "Opportunities": "Opportunities",
            "Risks": "Risks",
            "Market Sentiment": "Market Sentiment"
        }

        for key, section_title in sections.items():
            # Use lookahead to find the start of the next section or the end of the text
            pattern = rf"- \*\*{section_title}:\*\* (.*?)(?=- \*\*|$)"
            match = re.search(pattern, text, re.DOTALL)
            if match:
                analysis[key.lower().replace(" ", "_")] = match.group(1).strip()

        return analysis

    def extract_sources(self, text):
        """
        Extracts source URLs using regex.
        """
        # Improved regex to match the new format
        sources = []
        source_matches = re.findall(r"- (.*?) \((https?://.*?)\)", text)
        for source_name, url in source_matches:
            sources.append({"name": source_name.strip(), "url": url.strip()})

        return sources

    def extract_top_stocks(self, text):
        """
        Extracts top stock information using regex.
        """
        stocks = []
        # Regex to capture stock name, ticker, and details
        stock_matches = re.findall(r"- \*\*(.*?)\s*\((\w+)\):\*\*\n\s+- \*\*Market Performance:\*\* (.*?)\n\s+- \*\*Justification:\*\* (.*?)(?=-|$)", text, re.DOTALL)

        for stock_name, ticker, market_performance, justification in stock_matches:
            stocks.append({
                "stock_name": stock_name.strip(),
                "ticker": ticker.strip(),
                "market_performance": market_performance.strip(),
                "justification": justification.strip()
            })

        return stocks

    def save_report_to_file(self, report_json, agent_name):
        """
        Saves the report JSON to a file.
        """
        filename = f"{agent_name}_report.json"
        filepath = os.path.join(".", filename)  # Save to the current directory
        with open(filepath, "w") as f:
            json.dump(report_json, f, indent=4)
        print(f"Report saved to {filepath}")