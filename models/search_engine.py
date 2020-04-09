from math import sqrt
from models.collection import Collection
from models.query import Query
from helpers.helpers import merge_posting_lists


class SearchEngine:

    def __init__(self, collection_name: str, stopwords, lemmatizer):
        self.stopwords = stopwords
        self.lemmatizer = lemmatizer
        print("loading collection")
        self.collection = Collection(collection_name, self.stopwords, self.lemmatizer)
        print("collection ready")

        self.__run()

    def search(self, query):
        posting_list = self.__get_posting_list(query)
        doc_scores = self.__get_scores(posting_list, query)
        return doc_scores


    def __get_posting_list(self, query: Query):
        vocabulary = query.get_vocabulary()
        posting_list = self.collection.get_posting_list(vocabulary[0])
        for token in vocabulary[1:]:
            temp_posting_list = self.collection.get_posting_list(token)
            posting_list = merge_posting_lists(temp_posting_list, posting_list, "intersection")
        return posting_list

    def __get_scores(self, posting_list, query):
        query_tf_idf = {}
        norm_query_vector = 0
        query_vocabulary = query.get_vocabulary()
        for token in query_vocabulary:
            tf_idf = query.get_tf(token) * self.collection.get_idf(token)
            query_tf_idf[token] = tf_idf
            norm_query_vector += tf_idf ** 2
        norm_query_vector = sqrt(norm_query_vector)
        doc_scores = {}
        for doc_id in posting_list:
            score = 0
            for token in query_vocabulary:
                weight = self.collection.get_tw_idf(target_term=token, target_doc_id=doc_id, b=0.003)
                score += query_tf_idf[token] * weight
            score /= self.collection.documents_norms[doc_id] * norm_query_vector
            doc_scores[doc_id] = score
        return doc_scores
