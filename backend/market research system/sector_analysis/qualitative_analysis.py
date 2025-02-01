class QualitativeAnalysisAgent:
    def __init__(self, openai_model, data_validation_agent):
        self.openai_model = openai_model
        self.data_validation_agent = data_validation_agent
        self.prompt_template = """
        You are a Qualitative Analysis Agent.
        Your task is to analyze the qualitative aspects of the sector based on the provided data.
        Consider technological advancements, regulatory impacts, competitive landscape, and market sentiment.
        Input: {data}
        Output the analysis in the following format (STRICTLY FOLLOW THE GIVEN FORMAT):
        ```json
        {{
            "technological_advancements": "...",
            "regulatory_impacts": "...",
            "competitive_landscape": "...",
            "market_sentiment": "..."
        }}
        ```
        """

    def run(self, data):
        """
        Performs qualitative analysis on the given data.
        """
        prompt = self.prompt_template.format(data=data)
        response = self.openai_model.get_json_response(prompt)
        return response