#!/usr/bin/env python
import argparse
import pickle
import numpy as np


def main(fpath):
    """
    Download emojis and correspondign Wikipedia pages.

    Arguments:
        fpath: str
            File path to read model from.
    """
    with open(fpath, "rb") as fptr:
        model = pickle.load(fptr)

    try:
        query = 'japan'
        idx = model['columns'].index(query)
        for arg in np.argsort(-model['weights'][:, idx].toarray().ravel())[:5]:
            print(model["index"][arg])
    except NameError:
        print("Word not found")
        raise SystemExit

if __name__ == "__main__":
    # fmt: off
    PARSER = argparse.ArgumentParser(
        "Analyze emoji model."
    )

    PARSER.add_argument(
        "fpath",
        type=str,
        help="Filepath to read model from.",
    )

    ARGS = PARSER.parse_args()

    main(ARGS.fpath)
