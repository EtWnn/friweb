import os
import nltk

STOPWORDS = nltk.corpus.stopwords.words("english")


class Document:
    def __init__(self, document_id: int, parent_folder: int, name: str):
        self.document_id = document_id
        self.parent_folder = parent_folder
        self.name = name
        self.tokens = []
        self.n_tokens = 0
        self.occurrences = {}

    def load_content(self, collection_path):
        file_path = os.path.join(collection_path, f"{self.parent_folder}/{self.name}")
        with open(file_path, "r") as file:
            for line in file.readlines():
                self.tokens.extend(line.rstrip("\n").split(" "))
        self.__clean_tokens()

    def __clean_tokens(self):
        temp = filter(lambda t: t.isalpha(), self.tokens)  # non alpha words
        temp = filter(lambda t: not (t in STOPWORDS), temp)  # remove stopwords
        self.tokens = list(temp)
        self.n_tokens = len(self.tokens)

    def __construct_occurrences(self):
        self.occurrences = {}
        for token in self.tokens:
            try:
                self.occurrences[token] += 1
            except KeyError:
                self.occurrences[token] = 1

    def get_occurrences(self):
        if len(self.occurrences) == 0:
            self.__construct_occurrences()
        return self.occurrences


if __name__ == "__main__":
    # doc = Document(0, 0, "3dradiology.stanford.edu_")
    # doc.load_content("data/cs276")
    # print(doc.tokens)
    # print(doc.n_tokens)
    pass
