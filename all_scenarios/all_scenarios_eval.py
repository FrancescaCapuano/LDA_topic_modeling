import pickle
import copy


# reads back corpus, lda_model and doc_scenarios (ordered list of scenarios corresponding to each doc):
with open ('corpus', 'rb') as dc:
    corpus = pickle.load(dc)
with open ('lda_model', 'rb') as dc:
    lda_model = pickle.load(dc)
with open ('doc_scenarios', 'rb') as dc:
    doc_scenarios = pickle.load(dc)

scenarios = ['bath','bicycle','bus','cake','flight','grocery','haircut','library','train','tree']
num_topics=10


# a dict where the keys are the 10 topics, the values are dictionaries where the keys are the 
# scenarios, the values are the number of times the model classifies a doc belonging to the scenario
# as being mostly about that topic
# topics_doc_distr = {0:{'bath':3, 'bicycle':27,...},...}
topics_doc_distr=dict()
for topic in range(num_topics):
	topics_doc_distr[topic]={scenario: 0 for scenario in scenarios}

for i in range(len(corpus)):
	# best topic is the topic with the highest probability for each document
	best_topic=lda_model.get_document_topics(corpus[i])[0][0]
	# doc_scenario is the scenario the document originally corresponds to
	doc_scenario=doc_scenarios[i]
	topics_doc_distr[best_topic][doc_scenario]+=1


# dict that stores number of documents per scenario
documents_per_scenario={scenario: doc_scenarios.count(scenario) for scenario in scenarios}

# a deepcopy of topics_doc_distr normalized by documents per scenario
# ex. normalize_per_scenario[topic][scenario] = 
# number of documents from the scenario assigned to the topic/total number of documents in the scenario
normalize_per_scenario = copy.deepcopy(topics_doc_distr)

for topic in range(num_topics):
	for scenario in scenarios:
			normalize_per_scenario[topic][scenario]=normalize_per_scenario[topic][scenario]/documents_per_scenario[scenario]



# save topics_doc_distr to file, together with a visualization of the 15 words 
# with the highest prob per topic as found by the model,
# and normalize_per_scenario
with open('all_scenarios_results.txt','w') as s:
	for topic in range(num_topics):
		s.write(str(topic)+'\t'+str(topics_doc_distr[topic])+'\n')
	for topic_best_words in lda_model.print_topics(num_topics=num_topics, num_words=15):
		s.write(str(topic_best_words)+'\n')
	for topic in range(num_topics):
		s.write(str(topic)+'\n')
		for scenario in scenarios:
			s.write(str(scenario)+'\t'+str(normalize_per_scenario[topic][scenario])+'\n')