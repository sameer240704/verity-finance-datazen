class QualitativeAnalysisAgent:
    def __init__(self, openai_model, data_validation_agent):
        self.openai_model = openai_model
        self.data_validation_agent = data_validation_agent
        self.prompt_template = """
        You are a Qualitative Analysis Agent.
        Your task is to analyze the qualitative aspects of the sector based on the provided data.
        Consider technological advancements, regulatory impacts, competitive landscape, and market sentiment.

        Input:
        {data}

        Output:
        Provide a detailed qualitative analysis in text format. Use clear headings for each aspect:

        ## Technological Advancements
        (Discuss key technological advancements and their impact)

        ## Regulatory Impacts
        (Analyze the impact of regulations and government policies)

        ## Competitive Landscape
        (Describe the competitive environment, major players, and their strategies)

        ## Market Sentiment
        (Assess the overall market sentiment towards the sector)

        Do not output the response as JSON or in a dictionary format. Use paragraphs and bullet points to present your analysis.
        """

    def run(self, data):
        """
        Performs qualitative analysis on the given data.
        """
        prompt = self.prompt_template.format(data=data)
        response = self.openai_model.get_response(prompt)
        return response