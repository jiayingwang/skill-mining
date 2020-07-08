import os
from dblp import DBLP
import pickle
from rake import Rake
from nltk.corpus import stopwords

class Basic:
    
    def __init__(self, Dataset=DBLP, path=None):
        self.dataset = Dataset()
        self.dataset.load(path)
        self.path = self.dataset.default_path
        if path:
            self.path = path
        self.keywords = []
        
    def load_keywords(self):
        self.keywords.clear()
        print('load keywords...', end='', flush=True)
        keyword_path = os.path.join(self.path, 'keyword.dat')
        self.keywords = pickle.load(open(keyword_path, 'rb'))
        print('done.')
        
    def generate_keywords(self):
        ger_stop_words = stopwords.words('german')
        stop_words = stopwords.words('english')
        stop_words.extend(ger_stop_words)
        stop_words.extend(['via','using','fr'])
        r = Rake(stop_words)
        r.extract_keywords_from_sentences(self.dataset.titles)
        keyword_path = os.path.join(self.path, 'keyword.dat')
        print('generate keywords', end='', flush=True)
        with open(keyword_path, 'wb') as f:
            i = 0
            for title in self.dataset.titles:
                i += 1
                if i % 100000 == 0:
                    print('.', end='', flush=True)
                phrases = r._generate_phrases(title)
                phrases_scores = []
                for phrase in phrases:
                    true_phrase = '_'.join(phrase)
                    score = r.phrase_score[true_phrase]
                    phrases_scores.append((true_phrase, score))
                self.keywords.append(phrases_scores)
            pickle.dump(self.keywords, f)
        print('done')
    
    def search_skills(self, author_name):
        skills = {}
        if author_name not in self.dataset.authors:
            return skills
        for idx, order in self.dataset.authors[author_name]:
            for keyword, weight in self.keywords[idx]:
                score = weight * (0.5 ** order)
                skills[keyword] = skills.setdefault(keyword, 0) + score
        return skills