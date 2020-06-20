from rake import Rake
from nltk.corpus import stopwords

starttime = datetime.datetime.now()
ger_stop_words = stopwords.words('german')
stop_words = stopwords.words('english')
stop_words.extend(ger_stop_words)
stop_words.extend(['via','using','fr'])
r = Rake(stop_words)
with open(r'dblp_index/title.dat', encoding='utf-8') as f_title:
    titles = []
    for line in f_title:
        titles.append(line)
r.extract_keywords_from_sentences(titles)
print('generate keywords', end='', flush=True)
with open(r'dblp_index/keywords.dat', 'a', encoding='utf-8') as keywords:
    with open(r'dblp_index/title.dat', encoding='utf-8') as titles:
        i = 0
        for line in titles:
            i += 1
            if i % 10000 == 0:
                print('.', end='', flush=True)
            phrases = r._generate_phrases(line)
            phrases_scores = []
            for phrase in phrases:
                true_phrase = '_'.join(phrase)
                score = r.phrase_score[true_phrase]
                phrases_scores.append(true_phrase + ":" + str(score))
            keywords.write(','.join(phrases_scores)+'\n')
print('done')

