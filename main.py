import nltk

from models.search_engine import SearchEngine
from models.query import Query


def main():
    stopwords = nltk.corpus.stopwords.words("english")
    lemmatizer = nltk.stem.WordNetLemmatizer()
    search_engine = SearchEngine("cs276", [], lemmatizer)
    while True:
        str_query = input("enter your query: ")
        query = Query(str_query.lower(), [], lemmatizer)
        if query.length:
            results = search_engine.search(query)
            for result in results:
                print(result)
            if "n" in input("retry? (y/n)").lower():
                break
        else:
            print("empty query, please retry")


if __name__ == "__main__":
    main()
