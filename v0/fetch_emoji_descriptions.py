"""
Download emojis and corresponding Wikipedia page text.
"""
import argparse
import json
import os

from utils import wiki  # pylint: disable=no-name-in-module


def main(fpath, outdir):
    """
    Download emojis and correspondign Wikipedia pages.

    Arguments:
        fpath: str
            File path to read emoji corresponding wikipedia pages from.
        outdir: str
            Directory to save Wikipedia html results to.
    """
    with open(fpath, "r") as fptr:
        page_emojis = json.load(fptr)

    print("Saving html of pages descrbing emojis. This may take a while...")
    for page, _ in page_emojis.items():
        *_, pageid = os.path.split(page)

        savepath = os.path.join(outdir, "{pageid}.html".format(pageid=pageid))
        if os.path.exists(savepath):
            continue

        try:
            html = wiki.html(pageid)
        except KeyError:
            print("Unable to fetch html for {pageid}.")

        with open(savepath, "w") as fptr:
            fptr.write(html)


if __name__ == "__main__":
    # fmt: off
    PARSER = argparse.ArgumentParser(
        "Download emoji wikipedia page descriptions."
    )

    PARSER.add_argument(
        "fpath",
        type=str,
        help="File path to read emoji corresponding wikipedia pages from.",
    )

    PARSER.add_argument(
        "outdir",
        type=str,
        help="Directory to save html results to.",
    )
    # fmt: on

    ARGS = PARSER.parse_args()

    main(ARGS.fpath, ARGS.outdir)
