#!/usr/bin/env python
import argparse
import pickle
import numpy as np
from trainer import preprocess


def find_best_emojis(model, query):
    """
    Raises
        NameError.
    """
    words = preprocess(query, min_words=0)

    indices = []
    for word in words.split():
        try:
            idx = model["columns"].index(word)
        except ValueError:
            continue

        indices.append(idx)

    if not indices:
        return []

    sorted_args = (-model["weights"][:, indices].toarray().sum(axis=1)).argsort()

    emojis = []
    for arg in sorted_args:
        if np.isclose(model["weights"][arg, idx], 0):
            break
        emojis.append(model["index"][arg])

    return [a for b in emojis for a in b][:5]


def main(fpath):
    """
    Download emojis and correspondign Wikipedia pages.

    Arguments:
        fpath: str
            File path to read model from.
    """
    with open(fpath, "rb") as fptr:
        model = pickle.load(fptr)

    queries = [
        "ice cream",
        "irish cream",
        "bad apple",
        "the fuzz",
        "cycling",
        "drinking",
        "street racing"
        # "asdf",
        # "canada",
        # "cat",
        # "japan",
        # "burger",
        # "drugs",
        # "rock",
        # "ham",
        # "meat",
        # "panda",
        # "dragon",
        # "chinese",
        # "american",
        # "bike",
        # "football",
        # "hamtaro",
        # "motown",
        # "colombia",
        # "students",
        # "phone",
        # "beer",
        # "watch",
        # "samurai",
        # "cartoon",
        # "computer",
        # "christmas",
        # "jesus",
        # "magic",
        # "existentialism",
        # "philosophy",
        # "religion",
        # "ramen",
        # "avocado",
        # "tamago",
        # "sashimi",
        # "physics",
    ]

    for query in queries:
        try:
            emojis = find_best_emojis(model, query)
        except ValueError:
            emojis = []

        print(query, emojis)


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
