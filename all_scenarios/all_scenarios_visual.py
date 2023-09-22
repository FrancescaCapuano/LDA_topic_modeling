import pickle
import gensim
from gensim import corpora
import pyLDAvis.gensim
import pyLDAvis



# reads back lda_model, corpus and dictionary to prepare visualization:
with open ('lda_model_10', 'rb') as dc:
    lda_model = pickle.load(dc)
with open ('corpus_10', 'rb') as dc:
    corpus = pickle.load(dc)
with open ('dictionary_10', 'rb') as dc:
    dictionary = pickle.load(dc)



# topic model visualisation
lda_vis_data = pyLDAvis.gensim.prepare(lda_model,corpus,dictionary)
pyLDAvis.show(lda_vis_data)