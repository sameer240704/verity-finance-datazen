class StockNewsSentimentAnalysisAgent:
    def __init__(self, openai_model, data_validation_agent):
        self.openai_model = openai_model
        self.data_validation_agent = data_validation_agent
        self.prompt_template = """
        You are a News and Sentiment Analysis Agent.
        Your task is to analyze news sentiment and its potential impact on a stock based on the provided data.

        Input: {data}

        Output:
        Provide a detailed analysis in text format. Use clear headings for each section:

        ## Recent News
        (Summarize recent news articles about the company)

        ## Sentiment Analysis
        (Analyze the overall sentiment from the news - Positive, Negative, Neutral)

        ## Potential Impact
        (Discuss how the news might impact the stock price)

        Do not output the response as JSON or in a dictionary format. Use paragraphs and bullet points to present your analysis.
        """

    def run(self, data):
        """
        Performs news and sentiment analysis on the given data.
        """
        prompt = self.prompt_template.format(data=data)
        response = self.openai_model.get_response(prompt)  # Use get_response instead of get_json_response
        return response