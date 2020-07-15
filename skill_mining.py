import os
from dblp import DBLP
from keyword_extraction import KeywordExtraction
from collections import defaultdict
from text_rank import TextRank

class Basic:
    
    def __init__(self):
        self.authors = None
        self.keywords = None
        self.rake_score = None
        self.node_weights = None
    
    def load_dataset(self, dataset, path):
        dataset = dataset(path)
        dataset.load_authors()
        self.authors = dataset.authors
        
    def load_keyword(self):
        ke = KeywordExtraction()
        ke.generate_rake_keywords()
        self.keywords = ke.keywords
        self.rake_scores = ke.rake_scores
        
    def load_text_rank(self):
        tr = TextRank()
        tr.generate_ranks()
        self.node_weights = tr.node_weights
        
    def get_skills(self, author_name, dataset=DBLP, path=None, method='rake'):
        if self.authors is None:
            self.load_dataset(dataset, path)
        skills = defaultdict(int)
        if author_name not in self.authors:
            return skills
        if self.keywords is None:
            self.load_keyword()    
        for idx, order in self.authors[author_name]:
            for keyword in self.keywords[idx]:
                score = 0
                if method == 'rake':
                    score = self.rake_scores[keyword] * (0.5 ** order)
                elif method == 'text rank':
                    if self.node_weights is None:
                        self.load_text_rank()
                    score = self.node_weights[keyword] * (0.5 ** order)
                elif method == 'combined':
                    if self.node_weights is None:
                        self.load_text_rank()
                    score = self.node_weights[keyword] * self.rake_scores[keyword] * (0.5 ** order)
                skills[keyword] += score
        return skills