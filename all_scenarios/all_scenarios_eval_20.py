import pickle
import operator


# reads back corpus, lda_model and doc_scenarios (ordered list of scenarios corresponding to each doc):
with open ('corpus_20', 'rb') as dc:
    corpus = pickle.load(dc)
with open ('lda_model_20', 'rb') as dc:
    lda_model = pickle.load(dc)

num_topics=20

# total number of documents in the corpus
num_docs=len(corpus)

# docs_per_topic is a dict that stores, for each topic,
# the number of documents classified as mostly about that topic 
docs_per_topic={topic:0 for topic in range(num_topics)}
for i in range(len(corpus)):
	# best topic is the topic with the highest probability for each document
	best_topic=lda_model.get_document_topics(corpus[i])[0][0]
	docs_per_topic[best_topic]+=1

# same as docs_per_topic, but only with the 10 topics with the highest number of documents
docs_per_10_best_topic = dict(sorted(docs_per_topic.items(), key=operator.itemgetter(1), reverse=True)[:10])
# number of documents captured by the 10 best topics
num_docs_in_10_best_topic = sum(docs_per_10_best_topic.values())

# proportion of documents captured by the 10 best topics
print(num_docs_in_10_best_topic/num_docs)