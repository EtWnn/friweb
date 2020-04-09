import nltk

from models.search_engine import SearchEngine
from models.query import Query


def main():
    stopwords = nltk.corpus.stopwords.words("english")
    lemmatizer = nltk.stem.WordNetLemmatizer()
    search_engine = SearchEngine('cs276', stopwords, lemmatizer)
    while True:
        str_query = input("enter your query")
        query = Query(str_query.lower(), stopwords, lemmatizer)
        if query.length:
            doc_scores = search_engine.search(query)
            print(doc_scores[:10])
            if 'n' in input("retry? (y/n)").lower():
                break
        else:
            print("empty query, please retry")


if __name__ == "__main__":
    main()
