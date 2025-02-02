class StockFinancialAnalysisAgent:
    def __init__(self, openai_model, data_validation_agent):
        self.openai_model = openai_model
        self.data_validation_agent = data_validation_agent
        self.prompt_template = """
        You are a Financial Analysis Agent.
        Your task is to perform a detailed financial analysis of a company based on the provided data.
        Include ratio analysis, profitability assessment, and valuation metrics.

        Input: {data}

        Output:
        Provide a detailed financial analysis in text format. Use clear headings for each section:

        ## Ratio Analysis
        (Provide key financial ratios, e.g., P/E, P/B, Debt/Equity, EPS)

        ## Profitability
        (Assess the company's profitability, e.g., Gross Margin, Operating Margin, Net Profit Margin)

        ## Valuation
        (Provide a valuation assessment, e.g., is the stock overvalued, undervalued, or fairly valued)

        Do not output the response as JSON or in a dictionary format. Use paragraphs and bullet points to present your analysis.
        """

    def run(self, data):
        """
        Performs financial analysis on the given data.
        """
        prompt = self.prompt_template.format(data=data)
        response = self.openai_model.get_response(prompt)  # Use get_response instead of get_json_response
        return response