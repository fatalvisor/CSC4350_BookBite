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


def book_search(theme):
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


def book_info(isbn):
    """Get all the information about the book using the ISBN number"""
    isbn = str(isbn)
    try:
        BASE_URL = "https://reststop.randomhouse.com/resources/titles/"
        url = BASE_URL + isbn
        response = requests.get(url, headers={"Accept": "application/json"})
        response_json = response.json()
        # Get author name
        name = response_json["author"]
        author = " ".join(reversed(name.split(",")))
        # Get Flap Copy which is like a summary for the book
        flapcopy_html = response_json["flapcopy"]
        flapcopy = tag_remove(flapcopy_html)
        # Get author bio
        author_bio_html = response_json["authorbio"]
        author_bio = tag_remove(author_bio_html)
        # Get ISBN number
        book_isbn = response_json["isbn"]
        # Get page number
        page_num = response_json["pages"]
        # Get the theme
        themes = response_json["themes"]
        book_theme = get_themes(themes)
        # Get book cover
        book_cover = response_json["@uri"]
        # Get book title
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
        return "Nothing"  # This is just place holder
