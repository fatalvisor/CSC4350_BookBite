import os
import json
import random
import requests


def book_search(theme):
    """Finds and returns the title and cover image URL of a randomly selected book falling under a certain theme. For now, only one book is randomly chosen."""
    try:
        BASE_URL = "https://reststop.randomhouse.com/resources/titles"

        # "start", "max", and "expandlevel" are required parameters.
        query_params = {"start": 0, "max": 100, "expandlevel": 1, "theme": str(theme)}

        response = requests.get(
            BASE_URL, params=query_params, headers={"Accept": "application/json"}
        )

        response_json = response.json()
        book_selection = int(random.randint(0, 99))
        book_title = response_json["title"][book_selection]["titleweb"]
        img_url = BASE_URL + "/" + response_json["title"][book_selection]["isbn"]

        return book_title, img_url

    except:
        return (
            "Sample Title",
            "https://reststop.randomhouse.com/resources/titles/9781400079148",
        )
