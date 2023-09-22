import zipfile
import os,sys
sys.path.append('../library')
import xml.etree.ElementTree as ET
from lda_model import *
import pickle
import gensim
from gensim import corpora




# check if InScript folder is already extracted, otherwise extract it
if os.path.isdir("../InScript")==False:
	myzip=zipfile.ZipFile('../InScript_LREC2016.zip')
	myzip.extractall('..')
	myzip.close()



# compile documents: doc_complete = [doc1, doc2, doc3, ... , docn]
# the docs are all the stories from all scenarios in the InScript corpus
doc_complete=list()


# an ordered list of the documents scenarios, to be used in the evaluation to retrieve the scenario corresponding to a document: 
# doc_scenarios = ['bath', 'bath', 'bath', ... , 'tree']
doc_scenarios=list()


# the InScript corpus contains 10 folders (one for each scenario)
path = '../InScript/corpus'
scenarios = ['bath','bicycle','bus','cake','flight','grocery','haircut','library','train','tree']
# each scenario folder contains on average 91 xml files (one for each story)
# open each xml file from the corpus
for scenario in scenarios:
	for filename in os.listdir(path+'/'+scenario):
		tree = ET.parse(path+'/'+scenario+'/'+filename)
		root = tree.getroot()
		# retrieve the text under the label 'content' (a full story)
		for content in root.iter('content'):
			# append each full story to doc_complete	
			doc_complete.append(content.text)
		# append the corresponding scenario to doc_scenarios	
		doc_scenarios.append(scenario)


# save doc_scenarios for later use
with open('doc_scenarios', 'wb') as dc:
    pickle.dump(doc_scenarios, dc)


# save dictionary, corpus and lda_model trained with num_topics to current folder
# using the lda_model module under ../library
num_topics=10
save_lda(doc_complete,num_topics)
