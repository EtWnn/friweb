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
        self.key_words = []

    def __clean_tokens(self):
        temp = filter(lambda t: t.isalpha(), self.tokens)  # non alpha words
        temp = filter(lambda t: not(t in STOPWORDS), temp)  # remove stopwords
        self.tokens = list(temp)
        self.n_tokens = len(self.tokens)

    def __construct_occurrences(self):
        self.occurrences = {}
        for token in self.tokens:
            try:
                self.occurrences[token] += 1
            except KeyError:
                self.occurrences[token] = 1

    def __construct_key_words(self):
        if len(self.occurrences) == 0:
            self.__construct_key_words()
        scores = [(value, word) for word, value in self.occurrences.items()]
        scores.sort(reverse=True)
        self.key_words = [s[1] for s in scores[:5]]

    def load_content(self, collection_path):
        file_path = os.path.join(collection_path, f"{self.parent_folder}/{self.name}")
        with open(file_path, "r") as file:
            for line in file.readlines():
                self.tokens.extend(line.rstrip("\n").split(" "))
        self.__clean_tokens()

    def get_occurrences(self):
        if len(self.occurrences) == 0:
            self.__construct_occurrences()
        return self.occurrences
    
    def lemmatize(self, lemmatizer):
        self.tokens = list(map(lemmatizer.lemmatize, self.tokens))

    def get_key_words(self):
        if len(self.key_words) == 0:
            self.__construct_key_words()
        return self.key_words

    def get_TF(self, token):
        try:
            return self.occurrences[token] / self.n_tokens
        except :
            return 0


if __name__ == "__main__":
    doc = Document(0, 0, "3dradiology.stanford.edu_")
    doc.load_content("data/cs276")
    doc.lemmatize(nltk.stem.WordNetLemmatizer())
    print(doc.get_occurrences())
    print(doc.get_key_words())
