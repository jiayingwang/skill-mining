import os
from dblp import DBLP
import pickle
from rake import Rake
from nltk.corpus import stopwords

class KeywordExtraction:
    
    def __init__(self, dataset=DBLP, path=None):
        self.dataset = dataset(path)
        self.path = self.dataset.path
        self.keyword_file = os.path.join(self.path, 'keyword.dat')
        self.rake_score_file = os.path.join(self.path, 'rake_score.dat')
        self.keywords = []
        self.rake_scores = []
        
    def load(self):
        if not os.path.exists(self.path):
            print('Failed to find path ' + path)
            return
        self.load_keywords()
        self.load_rake_scores() 
        
        
    def load_keywords(self):
        path = self.keyword_file
        if not os.path.exists(path):
            print('Failed to find file', path)
            return
        self.keywords.clear()
        print('load keywords...', end='', flush=True)
        self.keywords = pickle.load(open(path, 'rb'))
        print('done')
        
    def load_rake_scores(self):
        path = self.rake_score_file
        if not os.path.exists(path):
            print('Failed to find file', path)
            return
        self.rake_scores.clear()
        print('load rake scores...', end='', flush=True)
        self.rake_scores = pickle.load(open(path, 'rb'))
        print('done')
        
    def generate_rake_keywords(self):
        if os.path.exists(self.keyword_file) and os.path.exists(self.rake_score_file):
            print('Already have the files ['+ self.keyword_file + ', ' + self.rake_score_file +']', ', directly load them.')
            self.load()
            return
        self.dataset.load()
        if self.path is None:
            self.path = self.dataset.default_path
        ger_stop_words = stopwords.words('german')
        stop_words = stopwords.words('english')
        stop_words.extend(ger_stop_words)
        stop_words.extend(['via','using','fr'])
        r = Rake(stop_words)
        r.extract_keywords_from_sentences(self.dataset.titles)
        path = os.path.join(self.path, 'keyword.dat')
        print('generate keywords', end='', flush=True)
        with open(path, 'wb') as f:
            i = 0
            for title in self.dataset.titles:
                i += 1
                if i % 100000 == 0:
                    print('.', end='', flush=True)
                phrases = r.generate_phrases(title)
                phrases = [' '.join(phrase) for phrase in phrases]
                self.keywords.append(phrases)
            pickle.dump(self.keywords, f)
        self.rake_scores = r.phrase_score
        path = os.path.join(self.path, 'rake_score.dat')
        with open(path, 'wb') as f:
            pickle.dump(self.rake_scores, f)         
        print('done')