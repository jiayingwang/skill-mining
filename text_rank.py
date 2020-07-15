import os
import pickle
from dblp import DBLP
from keyword_extraction import KeywordExtraction
from collections import defaultdict

class TextRank:
    
    def __init__(self, dataset=DBLP, path=None):
        self.graph = defaultdict(lambda: defaultdict(int))
        self.dataset = dataset(path)
        self.path = self.dataset.path
        self.weight_file = os.path.join(self.path, 'text_rank.dat')
        self.d = 0.85
        self.node_weights = defaultdict(float)
        
    def add_edge(self, u, v):
        self.graph[u][v] += 1
        self.graph[v][u] = self.graph[u][v]
        
    def compute_ranks(self):
        total_weights = defaultdict(float)
        default_weight = 1.0 / len(self.graph or 1.0)
        for node, out in self.graph.items():
            self.node_weights[node] = default_weight
            total_weights[node] = sum(out.values())
        
        while(True):
            total_weight_diff = 0
            for u in self.graph.keys():
                new_weight = 0
                for v, weight in self.graph[u].items():
                    new_weight += weight/total_weights[v] * self.node_weights[v]
                new_weight = (1-self.d) + self.d * new_weight
                total_weight_diff += abs(self.node_weights[u] - new_weight)
                self.node_weights[u] = new_weight
            if total_weight_diff < 1:
                break
            print(total_weight_diff)
    
    def load_weights(self):
        if not os.path.exists(self.weight_file):
            print('Failed to find path ' + self.weight_file)
            return
        self.node_weights.clear()
        print('load weights...', end='', flush=True)
        self.node_weights = pickle.load(open(self.weight_file, 'rb'))
        print('done')
        
    def generate_ranks(self, path=None):
        if os.path.exists(self.weight_file):
            print('already have weight file ['+ self.weight_file +'], directly load it')
            self.load_weights()
            return
        keyword_extraction = KeywordExtraction()
        keyword_extraction.load()
        keywords_list = keyword_extraction.keywords
        print('build graph...', end='', flush=True)
        for keywords in keywords_list:
            for i in range(len(keywords)):
                for j in range(i+1, len(keywords)):
                    self.add_edge(keywords[i], keywords[j])
        print('done')
        print('compute text rank...', end='', flush=True)
        self.compute_ranks()
        print('done', flush=True)
        print('save text rank...', end='', flush=True)
        with open(self.weight_file, 'wb') as f:
            pickle.dump(self.node_weights, f)         
        print('done')
        
        
        