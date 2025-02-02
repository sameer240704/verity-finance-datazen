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

        # Debugging: Print the generated report to the terminal
        print("*" * 30)
        print("Generated Sector Analysis Report:")
        print(response)
        print("*" * 30)

        # Save the text report
        report_filepath = os.path.join("reports", f"{agent_name}_report.txt")
        os.makedirs(os.path.dirname(report_filepath), exist_ok=True)  # Create directory if it doesn't exist
        with open(report_filepath, "w") as f:
            f.write(response)

        return response