class StockFinancialAnalysisAgent:
    def __init__(self, openai_model, data_validation_agent):
        self.openai_model = openai_model
        self.data_validation_agent = data_validation_agent
        self.prompt_template = """
        You are a Financial Analysis Agent.
        Your task is to perform a detailed financial analysis of a company based on the provided data.
        Include ratio analysis, profitability assessment, and valuation metrics.
        Input: {data}
        Output the analysis in the following format (STRICTLY FOLLOW THE GIVEN FORMAT):
        ```json
        {{
            "ratio_analysis": {{ /* ... */ }},
            "profitability": "...",
            "valuation": "..."
        }}
        ```
        """

    def run(self, data):
        """
        Performs financial analysis on the given data.
        """
        prompt = self.prompt_template.format(data=data)
        response = self.openai_model.get_json_response(prompt)
        return response