from clean import *
from clean_with_tags import *
import pickle
import gensim
from gensim import corpora


def __create_lda(doc_clean,n_topics):
	
	# creates the term dictionary of our courpus, where every unique term is assigned an index. 
	dictionary = corpora.Dictionary(doc_clean)

	# converts list of documents into Document Term Matrix (corpus) using dictionary prepared above.
	corpus = [dictionary.doc2bow(doc) for doc in doc_clean]

	# creates the object for LDA model using gensim library
	Lda = gensim.models.ldamodel.LdaModel

	# runs and trains LDA model on the document term matrix.
	lda_model = Lda(corpus, num_topics=n_topics, id2word = dictionary, passes=50, iterations=100)

	return(dictionary,corpus,lda_model)



def save_lda(doc_complete,n_topics):

	# removes punctuation, stopwords and lemmatizes the corpus.
	doc_clean = [clean(doc).split() for doc in doc_complete]  

	dictionary,corpus,lda_model=__create_lda(doc_clean,n_topics)

	# saves dictionary, corpus and lda_model to file
	with open('dictionary', 'wb') as dc:
	    pickle.dump(dictionary, dc)

	with open('corpus', 'wb') as dc:
	    pickle.dump(corpus, dc)

	with open('lda_model', 'wb') as dc:
	    pickle.dump(lda_model, dc)




def save_lda_with_tags(doc_complete,n_topics):

	# remove punctuation, stopwords, lemmatize the corpus and concatenate best tag to lemmas
	doc_clean_with_tags = [clean_with_tags(doc) for doc in doc_complete]

	dictionary,corpus,lda_model=__create_lda(doc_clean_with_tags,n_topics)

	# save dictionary, corpus and lda_model to file
	with open('dictionary_with_tags', 'wb') as dc:
	    pickle.dump(dictionary, dc)

	with open('corpus_with_tags', 'wb') as dc:
	    pickle.dump(corpus, dc)

	with open('lda_model_with_tags', 'wb') as dc:
	    pickle.dump(lda_model, dc)
