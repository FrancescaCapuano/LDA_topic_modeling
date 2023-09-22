import pickle
import gensim
import pyLDAvis.gensim
import pyLDAvis



# reads back lda_model, corpus and dictionary with tags to prepare visualization:
with open ('lda_model_with_tags_19', 'rb') as dc:
    lda_model = pickle.load(dc)
with open ('corpus_with_tags_19', 'rb') as dc:
    corpus = pickle.load(dc)
with open ('dictionary_with_tags_19', 'rb') as dc:
    dictionary = pickle.load(dc)



# topic model visualisation with tags
lda_vis_data = pyLDAvis.gensim.prepare(lda_model,corpus,dictionary)
pyLDAvis.show(lda_vis_data)