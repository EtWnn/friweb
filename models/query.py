from nltk.stem import WordNetLemmatizer


class Query:
    def __init__(self, content, stopwords, lemmatizer):
        self.content = content
        self.stopwords = stopwords
        self.lemmatizer = lemmatizer
        self.tokens = content.split(" ")
        self._length = len(self.tokens)
        self.term_frequencies = {}
        self.__process_query()

    def __remove_stopwords(self):
        self.tokens = [token for token in self.tokens if token not in self.stopwords]

    def __lemmatize(self):
        self.tokens = [self.lemmatizer.lemmatize(token) for token in self.tokens]

    def __compute_term_frequencies(self):
        for token in self.tokens:
            if token in self.term_frequencies:
                self.term_frequencies[token] += 1
            else:
                self.term_frequencies[token] = 1

    def __process_query(self):
        self.__remove_stopwords()
        self.__lemmatize()
        self.__compute_term_frequencies()
        self.__length = len(self.tokens)

    def get_tf(self, term):
        target_term = self.lemmatizer.lemmatize(term)
        try:
            tf = self.term_frequencies[target_term]
        except KeyError:
            return 0
        return tf

    def get_vocabulary(self):
        return list(self.term_frequencies.keys())


word_net_lemmatizer = WordNetLemmatizer()
string_query = "cat dog, the coucou hello ici feet foot help hi good better"
query = Query(string_query.lower(), ["the"], word_net_lemmatizer)

print(query.get_tf("feet"))
