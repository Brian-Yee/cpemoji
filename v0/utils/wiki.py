"""
Wikipedia utility functions.
"""
import os
import requests

SESSION = requests.Session()


def html(page):
    """
    Fetch html from wikipedia page

    Arguments:
        session: requests.Session
            Requets session to use GET request with.
        page: str
            Name of page to search for songs on.

    Returns:
        html: str
            HTML on Wikipedia page.
    """
    data = SESSION.get(
        url="https://en.wikipedia.org/w/api.php",
        params={"action": "parse", "page": page, "format": "json"},
    ).json()

    return data["parse"]["text"]["*"]


def resolve_redirects(href):
    """
    Wrapper for resolve Wikimedia API href redirects.

    Arguments:
        href: str
            Wikipedia href or page name.

    Returns:
        str
            Final url after redirections.
    """
    if href.startswith("/wiki/"):
        href = href[6:]

    return SESSION.get(
        os.path.join("https://en.wikipedia.org/api/rest_v1/page/summary", href),
        allow_redirects=True,
    ).url
