import pickle
import nltk
import re


class spamClassifier:
    def  __init__(self):
        pkl_filename = "spamClassifier.pkl"
        self.stop_words = nltk.corpus.stopwords.words('english')
        self.porter = nltk.PorterStemmer()
        with open(pkl_filename, 'rb') as file:  
            self.clf = pickle.load(file)

    def preprocess_text(self, messy_string):
        cleaned = re.sub(r'\b[\w\-.]+?@\w+?\.\w{2,4}\b', 'emailaddr', messy_string)
        cleaned = re.sub(r'(http[s]?\S+)|(\w+\.[A-Za-z]{2,4}\S*)', 'httpaddr', cleaned)
        cleaned = re.sub(r'£|\$', 'moneysymb', cleaned)
        cleaned = re.sub(r'\b(\+\d{1,2}\s)?\d?[\-(.]?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b','phonenumbr', cleaned)
        cleaned = re.sub(r'\d+(\.\d+)?', 'numbr', cleaned)
        cleaned = re.sub(r'[^\w\d\s]', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = re.sub(r'^\s+|\s+?$', '', cleaned.lower())
        return ' '.join(
            self.porter.stem(term) 
            for term in cleaned.split()
            if term not in set(self.stop_words)
        )
    #1 = spam,
    #0 = ham
    def classify(self, email):
        email = self.preprocess_text(email)
        return self.clf.predict([email])


