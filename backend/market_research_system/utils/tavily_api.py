import os
from tavily import TavilyClient

class TavilyAPI:
    def __init__(self):
        self.client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    def search(self, query):
        """
        Searches using the Tavily API.

        Args:
            query: The search query.

        Returns:
            The search results.
        """
        search_response = self.client.search(query=query)
        return search_response