import random
import requests
from bs4 import BeautifulSoup  # Please run sudo pip3 install beautifulsoup4 to run this


def tag_remove(text):
    """Using BeautifulSoup to remove HTML tags"""
    soup = BeautifulSoup(text, "html.parser")
    result = soup.get_text()
    return result


def get_themes(themes):
    """Get the book themes if exist"""
    book_themes = []
    if themes is not None:
        for theme in themes["theme"]:
            book_themes.append(theme)
        return "Themes: " + ", ".join(book_themes)
    return "None"


def book_suggestions(theme):
    """Finds and returns the titles and cover image URLs of randomly selected books falling under a certain theme."""
    try:
        # "start", "max", and "expandlevel" are required parameters.
        BASE_URL = "https://reststop.randomhouse.com/resources/titles"
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


def title_search(title):
    """Finds and returns the ISBN of the top search result given a book title."""
    try:
        # "start", "max", and "expandlevel" are required parameters.
        BASE_URL = "https://reststop.randomhouse.com/resources/titles"
        query_params = {"start": 0, "max": 1, "expandlevel": 1, "keyword": str(title)}

        response = requests.get(
            BASE_URL, params=query_params, headers={"Accept": "application/json"}
        )
        response_json = response.json()

        book_ISBN = response_json["title"][0]["isbn"]
        return book_ISBN

    except:
        sample_book_ISBN = 9781400079148
        return sample_book_ISBN


def basic_book_info(isbn):
    """Grabs the titles and book cover URLs of a set of books using the provided ISBN number."""
    isbn = str(isbn)
    try:
        BASE_URL = "https://reststop.randomhouse.com/resources/titles/"
        book_titles = []
        book_urls = []
        for index in range(len(isbn)):
            url = BASE_URL + isbn
            response = requests.get(url, headers={"Accept": "application/json"})
            response_json = response.json()

            book_title = response_json["titleweb"]
            book_cover = response_json["@uri"]

            book_titles.append(book_title)
            book_urls.append(book_cover)
            return (book_title, book_cover)
    except:
        # This is just a place holder value for now until proper dummy return values are added later.
        return "Nothing"


def all_book_info(isbn):
    """Get all the information about the book using the provided ISBN number."""
    isbn = str(isbn)
    try:
        BASE_URL = "https://reststop.randomhouse.com/resources/titles/"
        url = BASE_URL + isbn
        response = requests.get(url, headers={"Accept": "application/json"})
        response_json = response.json()

        # The name of the author is found below.
        name = response_json["author"]
        author = " ".join(reversed(name.split(",")))

        # flapcopy is the summary for the book. HTML tags are removed from this attribute.
        flapcopy_html = response_json["flapcopy"]
        flapcopy = tag_remove(flapcopy_html)

        # Provides brief info about the author. HTML tags are removed from this attribute.
        author_bio_html = response_json["authorbio"]
        author_bio = tag_remove(author_bio_html)

        # Grabs various other useful pieces of information about the book.
        book_isbn = response_json["isbn"]
        page_num = response_json["pages"]
        themes = response_json["themes"]
        book_theme = get_themes(themes)
        book_cover = response_json["@uri"]
        book_title = response_json["titleweb"]
        return (
            author,
            flapcopy,
            author_bio,
            book_isbn,
            page_num,
            book_theme,
            book_cover,
            book_title,
        )
    except:
        # This is just a place holder value for now until proper dummy return values are added later.
        return "Nothing"
