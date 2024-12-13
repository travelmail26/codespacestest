from serpapi import GoogleSearch
import os

from serpapi import GoogleSearch

def search_youtube_shorts(query, limit=20):
    """
    Search YouTube Shorts using SerpAPI
    Args:
        query (str): Search term
        limit (int): Maximum number of results to return
    """
    try:
        params = {
            "engine": "youtube",
            "search_query": query,
            "api_key": "5dfc2b51a4c7d1866b5aca18c49f902cec425ca083affe953bfa5b0c9767de07"
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        # Simply return the shorts_results key if it exists
        if "shorts_results" in results:
            shorts = results["shorts_results"]
            for result in shorts:
                print(result)
            return shorts[:limit] if limit else shorts
        else:
            print("No shorts found for this query.")
            return []

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []



search_youtube_shorts('recipes for meat stuffed cabbage or cabbage balls', 20)

# if __name__ == "__main__":
#     while True:
#         # Get search query from user
#         query = input("\nEnter search term (or 'quit' to exit): ")

#         if query.lower() == 'quit':
#             break

#         # Get number of results
#         try:
#             limit = int(input("How many results to display? (default 5): ") or 5)
#         except ValueError:
#             limit = 5

#         # Perform search
#         results = search_youtube_shorts(query, limit)