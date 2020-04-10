from math import sqrt
import time
from models.corpus import Corpus
from models.query import Query
from models.result import Result
from helpers.helpers import merge_appearance_lists


class SearchEngine:
    def __init__(self, corpus_name: str, stopwords, lemmatizer):
        self.stopwords = stopwords
        self.lemmatizer = lemmatizer
        print("Loading Corpus")
        self.corpus = Corpus(corpus_name, self.stopwords, self.lemmatizer)
        print("Corpus Loaded Successfully!")
        print("Computing documents norms")
        self.corpus.load_documents_norms()
        print("Norms Computed Successfully!")
        print("Corpus ready")

    def search(self, query, n_results=10):
        t0 = time.time()
        appearance_list = self.__get_appearance_list(query)
        doc_scores = self.__get_scores(appearance_list, query)
        print(f"found {len(doc_scores)} documents in {time.time() - t0 :.3f}s")
        n_results = min(n_results, len(doc_scores))
        selected_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[
            :n_results
        ]
        results = []
        for i, (doc_id, score) in enumerate(selected_docs):
            doc_infos = self.corpus.get_doc_infos(doc_id)
            results.append(
                Result(
                    i,
                    doc_id,
                    doc_infos["parent_folder"],
                    doc_infos["name"],
                    score,
                    doc_infos["key_words"],
                )
            )
        return results

    def __get_appearance_list(self, query: Query):
        vocabulary = query.get_vocabulary()
        appearance_list = self.corpus.get_appearance_list(vocabulary[0])
        for token in vocabulary[1:]:
            temp_appearance_list = self.corpus.get_appearance_list(token)
            appearance_list = merge_appearance_lists(
                temp_appearance_list, appearance_list, "intersection"
            )
        return appearance_list

    def __get_scores(self, appearance_list, query):
        query_tf_idf = {}
        norm_query_vector = 0
        query_vocabulary = query.get_vocabulary()
        for token in query_vocabulary:
            tf_idf = query.get_tf(token) * self.corpus.get_idf(token)
            query_tf_idf[token] = tf_idf
            norm_query_vector += tf_idf ** 2
        norm_query_vector = sqrt(norm_query_vector)
        doc_scores = {}
        for doc_id in appearance_list:
            score = 0
            for token in query_vocabulary:
                weight = self.corpus.get_tf_idf(
                    target_term=token, target_doc_id=doc_id, b=0.2
                )
                score += query_tf_idf[token] * weight
            score /= self.corpus.documents_norms[doc_id] * norm_query_vector
            doc_scores[doc_id] = score
        return doc_scores
