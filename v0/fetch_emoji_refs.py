"""
Download emojis and correspondign Wikipedia pages.
"""
import argparse
import collections
import json

from bs4 import BeautifulSoup

from utils import wiki  # pylint: disable=no-name-in-module


def main(fpath):
    """
    Download emojis and correspondign Wikipedia pages.

    Arguments:
        fpath: str
            Filepath to save wikipedia emoji data to.
    """
    html = wiki.html("Emoji")

    soup = BeautifulSoup(html, "lxml")
    tables = soup.find_all("table", {"class": "wikitable nounderlines"})

    print("Fetching emoji reference pages. This may take a while ...")
    page_emojis = collections.defaultdict(list)
    for table in tables:
        for td in table.find_all("td"):  # pylint: disable=invalid-name
            link = td.find("a", {"class": "mw-redirect"})
            if link is None:
                continue

            emoji = link.text.strip()
            redirect = wiki.resolve_redirects(link["href"])

            page_emojis[redirect].append(emoji)

    with open(fpath, "w") as fptr:
        json.dump(page_emojis, fptr)


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
