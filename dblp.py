import os
import sys
import pickle
from xml.sax.handler import ContentHandler
from xml.sax import parse

paper_tag = ('article','inproceedings','proceedings','book',
                   'incollection','phdthesis','mastersthesis')

class ResolveHandler(ContentHandler):
    
    def __init__(self, author_dict, titles):
        super().__init__()
        self.author_dict = author_dict
        self.titles = titles
        self.authors = ''
        self.title =''
        self.count = 0
        self.author_flag = False
        self.title_flag = False
        self.paper_flag = False
        
    def startElement(self, name, attrs):
        if self.paper_flag:
            if name == 'author':
                self.author_flag = True
            elif name == 'title':
                self.title_flag = True      
        elif name in paper_tag:
            self.paper_flag = True
                
    def endElement(self, name):
        if self.paper_flag:
            if name == 'author':
                self.authors += ','
                self.author_flag = False
            if name =='title':
                self.title_flag = False
            if name in paper_tag:
                i = 1            #位序
                for author in self.authors.split(','):
                    if author != '':
                        self.author_dict.setdefault(author.lower(), []).append((self.count, i))#索引 位序
                        i = i + 1
                self.titles.append(self.title)
                if self.count % 100000 == 0:
                    print('.', end='', flush=True)
                self.count += 1
                self.authors = ''
                self.title = ''
                self.paper_flag = False
        
    def characters(self, s):
        if self.paper_flag:
            if self.author_flag:
                self.authors += s
            elif self.title_flag:
                self.title += s

class DBLP:
    def __init__(self):
        self.authors = {}
        self.titles = []
        self.default_path = 'dblp_index'
        
    def load(self, path=None):
        if not path:
            path = self.default_path
        if not os.path.exists(path):
            print('Failed to find path ' + path)
            return
        self.authors.clear()
        self.titles.clear()
        author_path = os.path.join(path, 'author.dat')
        title_path = os.path.join(path, 'title.dat')
        print('load index...', end='', flush=True)
        self.authors = pickle.load(open(author_path, 'rb'))
        self.titles = pickle.load(open(title_path, 'rb'))
        print('done.')
            
    def search(self, author_name):
        titles_and_orders = []
        if author_name in self.authors:
            for idx in self.authors[author_name]:
                titles_and_orders.append((self.titles[idx[0]], idx[1]))
        return titles_and_orders
        
    def creat_index(self, raw_file='dblp.xml', path=None):
        if not os.path.exists(raw_file):
            print(raw_file, 'is not found')
            return
        if not path:
            path = self.default_path
        if not os.path.exists(path):
            os.makedirs(path)
        author_path = os.path.join(path, 'author.dat')
        title_path = os.path.join(path, 'title.dat')
        print('parsing dblp.xml', end='', flush=True)
        self.authors.clear()
        self.titles.clear()
        parse(raw_file, ResolveHandler(self.authors, self.titles))
        print('done.')
        print('create index ...', end='', flush=True)
        
        f = open(author_path, 'wb')
        pickle.dump(self.authors, f)
        
        f = open(title_path, 'wb')
        pickle.dump(self.titles, f)
        print('done.')

if __name__ == "__main__":
    dblp = DBLP()
    dblp.creat_index()

    dblp.load()
    name = input('please enter a name: ')
    titles_and_orders = dblp.search(name.strip().lower())    #函数返回一个放入所查作者的title的列表
    print('-'*50)
    for title, order in titles_and_orders:
        print(title, order)
    print('-'*50)
    print(str(len(titles_and_orders)) + ' papers were found.')