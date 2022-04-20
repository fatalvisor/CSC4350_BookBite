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


def book_suggestions(theme, display_number):
    """Finds and returns the titles and cover image URLs of randomly selected books falling under a certain theme."""
    try:
        # "start", "max", and "expandlevel" are required parameters.
        BASE_URL = "https://reststop.randomhouse.com/resources/titles"
        query_params = {"start": 0, "max": 40, "expandlevel": 1, "theme": str(theme)}

        response = requests.get(
            BASE_URL, params=query_params, headers={"Accept": "application/json"}
        )

        # Whatever information you'd like to pull out goes down below.
        book_titles = []
        book_urls = []
        book_ISBNs = []
        already_selected_books = []

        # Chooses a random set of 6 books under a chosen theme. Already selected books are not chosen twice.
        for index in range(display_number):
            response_json = response.json()
            book_selection = int(random.randint(0, 39))
            while book_selection in already_selected_books:
                book_selection = int(random.randint(0, 39))

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
        sample_book_url = ["../static/sample_book_cover.jpg"]
        sample_book_ISBN = [9781400079148]
        return (sample_title, sample_book_url, sample_book_ISBN)


def title_search(title):
    """Finds and returns the ISBN of the top search result given a book title."""

    # "start", "max", and "expandlevel" are required parameters.
    BASE_URL = "https://reststop.randomhouse.com/resources/titles"
    query_params = {"start": 0, "max": 25, "expandlevel": 1, "search": str(title)}

    response = requests.get(
        BASE_URL, params=query_params, headers={"Accept": "application/json"}
    )
    response_json = response.json()
    book_index = int(random.randint(0, len(response_json["title"]) - 1))

    book_ISBN = response_json["title"][book_index]["isbn"]
    return book_ISBN


def basic_book_info(isbn):
    """Grabs the title and book cover URL of a single book using the provided ISBN number."""
    isbn = str(isbn)
    try:
        BASE_URL = "https://reststop.randomhouse.com/resources/titles/"
        book_titles = []
        book_urls = []
        url = BASE_URL + isbn
        response = requests.get(url, headers={"Accept": "application/json"})
        response_json = response.json()

        book_title = response_json["titleweb"]
        book_cover = response_json["@uri"]

        book_titles.append(book_title)
        book_urls.append(book_cover)
        return (book_title, book_cover)
    except:
        sample_title = ["Book Missing Information"]
        sample_book_url = ["../static/sample_book_cover.jpg"]
        return sample_title, sample_book_url


def all_book_info(isbn):
    """Grabs all the information about a single book using the provided ISBN number."""
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
        book_theme = get_themes(response_json["themes"])
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
        author = "Anonymous"
        flapcopy = (
            "This is what an example of a newly-discovered but broken book looks like."
        )
        author_bio = "This is an author who, for many years, has eluded the public eye. His origins are currently unknown."
        book_isbn = 123456789123
        page_num = 35
        book_theme = "None"
        book_cover = "../static/sample_book_cover.jpg"
        book_title = "Book Missing Information"
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


def get_single_book_theme(isbn):
    """Grabs all the information about a single book using the provided ISBN number."""
    isbn = str(isbn)
    try:
        BASE_URL = "https://reststop.randomhouse.com/resources/titles/"
        url = BASE_URL + isbn
        response = requests.get(url, headers={"Accept": "application/json"})
        response_json = response.json()

        try:
            book_theme = response_json["themes"]["theme"]
            single_theme = book_theme[0]
            return single_theme
        except:
            book_theme = response_json["themes"]["theme"]
            return book_theme
    except:
        book_theme = "None"
        return book_theme
