class QuantitativeAnalysisAgent:
    def __init__(self, openai_model, data_validation_agent):
        self.openai_model = openai_model
        self.data_validation_agent = data_validation_agent
        self.prompt_template = """
        You are a Quantitative Analysis Agent.
        Your task is to perform in-depth quantitative analysis on the data provided.
        Calculate market size, growth rates, market share, financial ratios, and other relevant metrics.
        Input: {data}
        Output the analysis in the following format:
        {{
            "market_size": "...",
            "growth_rate": "...",
            "market_share": {{ /* ... */ }},
            "financial_ratios": {{ /* ... */ }},
            "other_metrics": {{ /* ... */ }}
        }}
        """

    def run(self, data):
        """
        Performs quantitative analysis on the given data.
        """
        prompt = self.prompt_template.format(data=data)
        response = self.openai_model.get_response(prompt)
        return response