from os import path, listdir
from math import log, sqrt
from typing import List, Dict
from models.document import Document
from tqdm import tqdm
from helpers.helpers import load_pickle_file, save_pickle_file


class Corpus:
    def __init__(self, name, stopwords, lemmatizer, path_to_data="./data/"):
        self.name = name
        self.documents = []
        self.inverted_index = {}
        self.documents_norms = {}
        self.path_to_data = path_to_data + name
        self.stopwords = stopwords
        self.lemmatizer = lemmatizer
        self.nb_docs = 0
        self.average_document_length = 0

        self.generate_documents_index()

    def generate_documents_index(self):
        try:
            self.documents = load_pickle_file(self.name, "documents")
            self.inverted_index = load_pickle_file(self.name, "index")
        except FileNotFoundError:
            nb_document_loaded = 0
            document_id = 0
            subfolders = listdir(self.path_to_data)
            for sub_directory in subfolders:
                path_directory = path.join(self.path_to_data, sub_directory)
                files = listdir(path_directory)
                for filename in tqdm(files):
                    document = Document(
                        document_id=document_id,
                        parent_folder=sub_directory,
                        name=filename,
                    )
                    document.load_content(
                        self.path_to_data, self.stopwords, self.lemmatizer
                    )
                    occurrences = document.get_occurrences()
                    self.average_document_length += document.length
                    for token, occurrence in occurrences.items():
                        if token not in self.inverted_index:
                            self.inverted_index[token] = {document_id: occurrence}
                        else:
                            self.inverted_index[token][document_id] = occurrence
                    self.documents.append(document)
                    nb_document_loaded += 1
                    document_id += 1
            save_pickle_file(self.name, "documents", self.documents)
            save_pickle_file(self.name, "index", self.inverted_index)
        finally:
            for document in self.documents:
                self.average_document_length += document.length
            self.nb_docs = len(self.documents)
            self.average_document_length /= self.nb_docs

    def load_documents_norms(self):
        try:
            self.documents_norms = load_pickle_file(self.name, "tf-idf-norm")
        except FileNotFoundError:
            nb_norms_calculated = 0
            for document in tqdm(self.documents):
                doc_vocabulary = document.get_vocabulary()
                norm = 0
                for token in doc_vocabulary:
                    norm += self.get_tf_idf(token, document.id, 0.2) ** 2
                norm = sqrt(norm)
                self.documents_norms[document.id] = norm
                nb_norms_calculated += 1
            save_pickle_file(self.name, "tf-idf-norm", self.documents_norms)

    def __get_term_frequency(self, target_term, target_doc_id):
        try:
            term_frequency = self.inverted_index[target_term][target_doc_id]
            return term_frequency
        except KeyError:
            return 0

    def __compute_normalizer(self, target_doc_id, b):
        normalizer = (
            1
            - b
            + (b * self.documents[target_doc_id].length / self.average_document_length)
        )
        return normalizer

    def __compute_ln_tf(self, target_term, target_doc_id, b):
        term_frequency = self.__get_term_frequency(target_term, target_doc_id)
        if term_frequency == 0:
            return 0
        concave_tf = 1 + log(1 + log(term_frequency))
        return concave_tf / self.__compute_normalizer(target_doc_id, b)

    def get_idf(self, target_term):
        try:
            df = len(self.inverted_index[target_term].keys())
        except KeyError:
            return 0
        return log((self.nb_docs + 1) / df)

    def get_tf_idf(self, target_term, target_doc_id, b):
        normalized_tf = self.__compute_ln_tf(target_term, target_doc_id, b)
        if normalized_tf == 0:
            return 0
        else:
            return (normalized_tf + 1) * self.get_idf(target_term)

    def get_appearance_list(self, target_term):
        try:
            appearance_list = list(self.inverted_index[target_term].keys())
        except KeyError:
            return []
        return appearance_list

    def get_doc_infos(self, doc_id):
        try:
            document = self.documents[doc_id]
            return {
                "doc_id": doc_id,
                "name": document.name,
                "parent_folder": document.parent_folder,
                "key_words": document.key_words,
            }
        except:
            return {}
