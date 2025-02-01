class StockNewsSentimentAnalysisAgent:
    def __init__(self, openai_model, data_validation_agent):
        self.openai_model = openai_model
        self.data_validation_agent = data_validation_agent
        self.prompt_template = """
        You are a News and Sentiment Analysis Agent.
        Your task is to analyze news sentiment and its potential impact on a stock based on the provided data.
        Input: {data}
        Output the analysis in the following format (STRICTLY FOLLOW THE GIVEN FORMAT):
        ```json
        {{
            "news_sentiment": "...",
            "potential_impact": "..."
        }}
        ```
        """

    def run(self, data):
        """
        Performs news and sentiment analysis on the given data.
        """
        prompt = self.prompt_template.format(data=data)
        response = self.openai_model.get_json_response(prompt)
        return response