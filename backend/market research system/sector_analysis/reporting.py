class SectorReportingAgent:
    def __init__(self, openai_model):
        self.openai_model = openai_model
        self.prompt_template = """
        You are a Reporting Agent.
        Your task is to compile a comprehensive technical report based on the findings from the Data Collection, Quantitative Analysis, Qualitative Analysis, and Data Validation Agents.
        Generate a JSON report with the following structure:
        {{
          "market_metrics": {{ /* Quantitative data and analysis from Quantitative Analysis Agent */ }},
          "analysis_report": " /* Detailed technical analysis (qualitative and quantitative) from Qualitative and Quantitative Analysis Agents */ ",
          "sources": [ /* URLs from Tavily, from Data Collection Agent */ ],
          "top_5_stocks": [ /* Top 5 performing stocks with metrics and justification, derived from all agents' data */ ]
        }}
        Input:
        {{
            "data_collection": {data_collection_output},
            "quantitative_analysis": {quantitative_analysis_output},
            "qualitative_analysis": {qualitative_analysis_output}
        }}
        """

    def run(self, data_collection_output, quantitative_analysis_output, qualitative_analysis_output):
        """
        Generates the final sector analysis report.
        """
        prompt = self.prompt_template.format(
            data_collection_output=data_collection_output,
            quantitative_analysis_output=quantitative_analysis_output,
            qualitative_analysis_output=qualitative_analysis_output
        )
        response = self.openai_model.get_json_response(prompt)
        return response