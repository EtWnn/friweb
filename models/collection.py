from os import path, listdir
from math import log
from typing import List, Dict
from models.document import Document
from tqdm import tqdm
from helpers.helpers import load_pickle_file, save_pickle_file


class Collection:
    def __init__(self, name, path_to_data="./data/cs276"):
        self.name = name
        self.documents: List[Document] = []
        self.inverted_index: Dict[str, Dict[int, int]] = {}
        self.path_to_data = path_to_data
        self.nb_docs = 0
        self.average_document_length = 0

        self.__load_data()

    def __load_data(self):
        try:
            self.documents = load_pickle_file(self.name, "preprocessed_documents")
            self.inverted_index = load_pickle_file(self.name, "inverted_index")
        except FileNotFoundError:
            nb_document_loaded = 0
            document_id = 1
            for directory_index in range(10):
                path_directory = path.join(self.path_to_data, str(directory_index))
                for filename in tqdm(listdir(path_directory)):
                    document = Document(
                        document_id=document_id,
                        parent_folder=str(directory_index),
                        name=filename,
                    )
                    document.load_content(self.path_to_data)
                    occurrences = document.get_occurrences()
                    self.documents.append(document)
                    self.average_document_length += document.length
                    for token, occurrence in occurrences.items():
                        if token not in self.inverted_index:
                            self.inverted_index[token] = {document_id: occurrence}
                        else:
                            self.inverted_index[token][document_id] = occurrence
                    self.documents.append(document)
                    nb_document_loaded += 1
                    document_id = +1
            save_pickle_file(self.name, "preprocessed_documents", self.documents)
            save_pickle_file(self.name, "inverted_index", self.inverted_index)
        self.nb_docs = len(self.documents)
        self.average_document_length /= self.nb_docs

    def __get_term_frequency(self, target_term, target_doc_id):
        try:
            term_frequency = self.inverted_index[target_term][target_doc_id]
            return term_frequency
        except KeyError:
            return 0

    def __get_pivoted_normalizer(self, target_doc_id, b):
        pivoted_normalizer = (
            1
            - b
            + (b * self.documents[target_doc_id].length / self.average_document_length)
        )
        return pivoted_normalizer

    def __get_pivoted_and_concave_ln_tf(self, target_term, target_doc_id, b):
        term_frequency = self.__get_term_frequency(target_term, target_doc_id)
        if term_frequency == 0:
            return 0
        concave_tf = 1 + log(1 + log(term_frequency))
        return concave_tf / self.__get_pivoted_normalizer(target_doc_id, b)

    def get_idf(self, target_term):
        try:
            df = len(self.inverted_index[target_term].keys())
        except KeyError:
            return 0
        return log((self.nb_docs + 1) / df)

    def get_tf_idf(self, target_term, target_doc_id, b):
        normalized_tf = self.__get_pivoted_and_concave_ln_tf(
            target_term, target_doc_id, b
        )
        if normalized_tf == 0:
            return 0
        else:
            return (normalized_tf + 1) * self.get_idf(target_term)

    def get_posting_list(self, target_term):
        try:
            doc_list = list(self.inverted_index[target_term].keys())
        except KeyError:
            return []
        return doc_list
