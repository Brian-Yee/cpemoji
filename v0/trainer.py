"""
Analyze wikipedia descriptions of emojis.
"""
import argparse
import collections
import glob
import json
import os
import pickle

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize

from lxml import etree
import sklearn.feature_extraction.text


def preprocess(text, min_words=2):
    stops = set(stopwords.words("english"))
    stemmer = SnowballStemmer("english")

    words = []
    for word in word_tokenize(text):
        if (  # pylint: disable=bad-continuation
            word in stops
            or sum(map(word.count, ":/-")) > 1
            or sum(x.isalpha() for x in word) == 0
        ):
            continue

        stemmed = stemmer.stem(word)
        if stemmed in stops:
            continue

        words.append(stemmed)

    counts = collections.Counter(words)
    words = [
        " ".join(k for _ in range(v)) for k, v in counts.most_common() if v >= min_words
    ]

    return " ".join(words)


def main(fpath, html_dir):
    """
    Download emojis and correspondign Wikipedia pages.

    Arguments:
        fpath: str
            File path to read emoji corresponding wikipedia pages from.
        html_dir: str
            Directory to read Wikipedia html results from.
    """
    with open(fpath, "r") as fptr:
        pageid_emojis = {os.path.split(k)[-1]: v for k, v in json.load(fptr).items()}

    print("Loading emoji corpus. This may take a while...")
    index, corpus = [], []
    for html_fpath in glob.glob(os.path.join(html_dir, "*")):
        with open(html_fpath, "r") as fptr:
            html = fptr.read()

        tree = etree.fromstring(html)
        text = "".join(tree.xpath(".//text()"))
        corpus.append(text)

        pageid = os.path.splitext(os.path.split(html_fpath)[-1])[0]
        index.append(pageid_emojis[pageid])

    vectorizer = sklearn.feature_extraction.text.TfidfVectorizer(
        max_features=10000, min_df=1, preprocessor=preprocess
    )

    print("Fitting Model. This may take a while...")
    weights = vectorizer.fit_transform(corpus)

    model = {
        "weights": weights,
        "columns": vectorizer.get_feature_names(),
        "index": index,
    }

    with open("build/model.pckl", "wb") as fptr:
        pickle.dump(model, fptr)


if __name__ == "__main__":
    # fmt: off
    PARSER = argparse.ArgumentParser(
        "Analyze wikipedia descriptions of emojis."
    )

    PARSER.add_argument(
        "fpath",
        type=str,
        help="Filepath to read emoji corresponding wikipedia pages from.",
    )

    PARSER.add_argument(
        "html_dir",
        type=str,
        help="Directory to read emoji htmls from",
    )

    ARGS = PARSER.parse_args()

    main(ARGS.fpath, ARGS.html_dir)
