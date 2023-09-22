import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import pickle

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
with open ('../library/word_best_tag', 'rb') as dc:
    word_best_tag = pickle.load(dc)


# given a string, removes punctuation and stopwords, lemmatizes the words,
# concatenates to the lemma the best tag as found in word_best_tag,
# returns the string
def clean_with_tags(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    tagged=[]
    for word in punc_free.split():
        lem_word=lemma.lemmatize(word)
        if lem_word in word_best_tag.keys():
            lem_word=lem_word+'_'+word_best_tag[lem_word]
        tagged.append(lem_word)
    return tagged