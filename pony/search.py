from serpapi import GoogleSearch
import os

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def search_reviews(bag_name, num_results=10):
    """
    Search Google for luxury bag reviews and
    return snippets.
    """

    params = {
        "engine": "google",
        "q": f"{bag_name} review",
        "api_key": SERPAPI_KEY,
        "num": num_results,
    }

    search = GoogleSearch(params)

    results = search.get_dict()

    snippets = []

    if "organic_results" in results:

        for item in results["organic_results"]:

            if "snippet" in item:

                snippets.append(item["snippet"])

    return snippets
