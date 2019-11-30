"""
Download emojis and correspondign Wikipedia pages.
"""
import argparse
import csv
import os
import requests

from bs4 import BeautifulSoup

SESSION = requests.Session()


def wiki_html(page):
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

    html = data["parse"]["text"]["*"]

    return html


def resolve_redirect(href):
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


def main(fpath):
    """
    Download emojis and correspondign Wikipedia pages.

    Arguments:
        fpath: str
            Filepath to save wikipedia emoji data to.
    """
    html = wiki_html("Emoji")

    soup = BeautifulSoup(html, "lxml")
    tables = soup.find_all("table", {"class": "wikitable nounderlines"})

    emoji_pages = []
    print("Fetching emoji reference pages. This may take a while ...")
    for table in tables:
        for td in table.find_all("td"):  # pylint: disable=invalid-name
            link = td.find("a", {"class": "mw-redirect"})
            if link is None:
                continue

            emoji = link.text.strip()
            redirect = resolve_redirect(link["href"])

            emoji_pages.append([emoji, redirect])

    with open(fpath, "w") as fptr:
        writer = csv.writer(fptr)
        writer.writerows(emoji_pages)


if __name__ == "__main__":
    # fmt: off
    PARSER = argparse.ArgumentParser(
        "Download emoji wikipedia page references."
    )

    PARSER.add_argument(
        "fpath",
        type=str,
        help="Where to save csv output.",
    )
    # fmt: on

    ARGS = PARSER.parse_args()

    main(ARGS.fpath)
