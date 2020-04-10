from time import time
from os.path import isfile
import nltk
import math

from helpers.helpers import merge_appearance_lists
from models.search_engine import SearchEngine
from models.query import Query


def show_accuracy():
    """
    This function compares the results from the dev predictions and dev output to evaluate the
    performance of a model
    :return:
    """
    print("\n accuracy by query:")
    if not isfile("tests_data/predictions/9.out".format()):
        compute_dev_predictions()
    for i in range(1, 9):
        dev_output = []
        search_engine_output = []
        with open("tests_data/output/{}.out".format(i), "r") as file:
            reader = file.readlines()
            for line in reader:
                dev_output.append(line.rstrip("\n"))
        with open("tests_data/predictions/{}.out".format(i), "r") as file:
            reader = file.readlines()
            for line in reader:
                parsed_line = line.rstrip("\n").split(" ")
                search_engine_output.append(parsed_line[0])
        with open("tests_data/queries/query.{}".format(i), "r") as file:
            query_content = next(file).rstrip("\n")
        if len(search_engine_output) == 0:
            print("Search Engine has failed on Query {}".format(i))
        else:
            search_engine_output = search_engine_output[: len(dev_output)]

            posting_term1 = sorted(dev_output)
            posting_term2 = sorted(search_engine_output)

            final_list = merge_appearance_lists(
                posting_term1, posting_term2, "intersection"
            )
            score = len(final_list) / len(dev_output)

            print(
                'For Query {} : "{}" the accuracy score is {}%'.format(
                    i, query_content, "{0:.2f}".format(score * 100)
                )
            )


def compute_dev_predictions():
    stopwords = nltk.corpus.stopwords.words("english")
    lemmatizer = nltk.stem.WordNetLemmatizer()
    search_engine = SearchEngine(
        corpus_name="cs276", stopwords=[], lemmatizer=lemmatizer,
    )

    for i in range(1, 9):
        start = time()
        with (open("tests_data/queries/query.{}".format(str(i)), "r")) as query_file:
            query_content = next(query_file).rstrip("\n")
        print(query_content)
        query = Query(query_content, [], lemmatizer)
        results = search_engine.search(query, math.inf)
        with open("tests_data/predictions/{}.out".format(str(i)), "w") as result_file:
            for result in results:
                line = "{}/{} {}".format(
                    result.parent_folder, result.doc_name, result.score,
                )
                result_file.write(line + "\n")
        # print("Query{} duration : {} seconds".format(str(i), time() - start))


if __name__ == "__main__":
    show_accuracy()
