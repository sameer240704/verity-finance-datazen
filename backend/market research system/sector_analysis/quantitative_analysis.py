class QuantitativeAnalysisAgent:
    def __init__(self, openai_model, data_validation_agent):
        self.openai_model = openai_model
        self.data_validation_agent = data_validation_agent
        self.prompt_template = """
        You are a Quantitative Analysis Agent.
        Your task is to perform in-depth quantitative analysis on the data provided.
        Calculate market size, growth rates, market share, financial ratios, and other relevant metrics.
        
        Input: 
        {data}

        Output:
        Provide a detailed analysis in text format. Use clear headings for each metric:

        ## Market Size
        (Provide market size data and analysis)

        ## Growth Rate
        (Provide growth rate data and analysis)

        ## Market Share
        (Provide market share data and analysis)

        ## Financial Ratios
        (Provide relevant financial ratios and analysis)

        ## Other Metrics
        (Provide any other relevant quantitative metrics and analysis)

        Do not output the response as JSON or in a dictionary format. Use paragraphs and bullet points to present your analysis.
        """

    def run(self, data):
        """
        Performs quantitative analysis on the given data.
        """
        prompt = self.prompt_template.format(data=data)
        response = self.openai_model.get_response(prompt)
        return response