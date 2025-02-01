class DataValidationAgent:
    def __init__(self, openai_model):
        self.openai_model = openai_model
        self.validation_prompt = """
        You are a Data Validation Agent. Your role is to cross-reference and validate the data provided to you. 
        Ensure the accuracy of the data and minimize any potential hallucinations. 
        Also filter out possible misinformation. 
        If data from multiple sources conflicts, point out the discrepancies and provide a reasoned judgment on which source is more reliable or if a consensus cannot be reached.

        Input: {data}

        Output: (Validated data or a report of discrepancies in the same format as input)
        """

    def validate(self, data):
        """
        Validates the given data.

        Args:
            data: The data to validate (can be string, list or dict).

        Returns:
            Validated data or a report of discrepancies.
        """
        prompt = self.validation_prompt.format(data=data)
        response = self.openai_model.get_response(prompt)
        return response