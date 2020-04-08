from os import path, listdir
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

        self.__load_documents()

    def __load_documents(self):
        try:
            self.documents = load_pickle_file(self.name, "preprocessed_documents")
        except FileNotFoundError:
            nb_document_loaded = 0
            document_id = 1
            for directory_index in range(10):
                path_directory = path.join(self.path_to_data, str(directory_index))
                for filename in tqdm(listdir(path_directory)):
                    document = Document(
                        document_id=document_id,
                        parent_folder=directory_index,
                        name=filename,
                    )
                    document.load_content(self.path_to_data)
                    occurrences = document.get_occurrences()
                    for token, occurrence in occurrences.items():
                        if token not in self.inverted_index:
                            self.inverted_index[token] = {document_id: occurrence}
                        else:
                            self.inverted_index[token][document_id] = occurrence
                    self.documents.append(document)
                    nb_document_loaded += 1
                    document_id = +1
            save_pickle_file(self.name, "preprocessed_documents", self.documents)