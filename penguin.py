import os
import json
import random
import requests


def book_search(theme):
    """Finds and returns the titles and cover image URLs of randomly selected books falling under a certain theme."""
    try:
        BASE_URL = "https://reststop.randomhouse.com/resources/titles"

        # "start", "max", and "expandlevel" are required parameters.
        query_params = {"start": 0, "max": 100, "expandlevel": 1, "theme": str(theme)}

        response = requests.get(
            BASE_URL, params=query_params, headers={"Accept": "application/json"}
        )

        # Whatever information you'd like to pull out goes down below.
        book_titles = []
        book_urls = []
        book_ISBNs = []
        already_selected_books = []

        # Chooses a random set of 6 books under a chosen theme. Already selected books are not chosen twice.
        for index in range(6):
            response_json = response.json()
            book_selection = int(random.randint(0, 99))
            while book_selection in already_selected_books:
                book_selection = int(random.randint(0, 99))

            book_title = response_json["title"][book_selection]["titleweb"]
            book_url = BASE_URL + "/" + response_json["title"][book_selection]["isbn"]
            bookISBN = response_json["title"][book_selection]["isbn"]

            book_titles.append(book_title)
            book_urls.append(book_url)
            book_ISBNs.append(bookISBN)
            already_selected_books.append(book_selection)

        return book_titles, book_urls, book_ISBNs

    except:
        sample_title = ["Sample Title"]
        sample_book_url = [
            "https://reststop.randomhouse.com/resources/titles/9781400079148"
        ]
        sample_book_ISBN = [9781400079148]
        return (sample_title, sample_book_url, sample_book_ISBN)
