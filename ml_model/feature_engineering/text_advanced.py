from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

class TFIDF:
    def __init__(self):
        self.vec = TfidfVectorizer(max_features=3000, ngram_range=(1,2))

    def fit_transform(self, text):
        return self.vec.fit_transform(text).toarray()

    def transform(self, text):
        return self.vec.transform(text).toarray()

    def save(self, path):
        pickle.dump(self.vec, open(path, "wb"))

    def load(self, path):
        self.vec = pickle.load(open(path, "rb"))