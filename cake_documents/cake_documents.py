import zipfile
import os,sys
import xml.etree.ElementTree as ET
import pickle
sys.path.append('../library')
from lda_model import *
import gensim
from gensim import corpora



# check if InScript folder is already extracted, otherwise extract it
if os.path.isdir("../InScript")==False:
	myzip=zipfile.ZipFile('../InScript_LREC2016.zip')
	myzip.extractall('..')
	myzip.close()



# compile documents: doc_complete = [doc1, doc2, doc3, ... , docn]
# the docs are all the stories from the CAKE scenario in the InScript corpus
doc_complete=list()
path = '../InScript/corpus/cake'

# open each xml file from the CAKE corpus 
for filename in os.listdir(path):
	tree = ET.parse(path+'/'+filename)
	root = tree.getroot()
	# retrieve the text under the label 'content' (a full story)
	for content in root.iter('content'):
		# append each full story to doc_complete
		doc_complete.append(content.text)

# save dictionary, corpus and lda_model trained with 37 topics to current folder
# using the lda_model module under ../library
num_topics=37
save_lda(doc_complete,num_topics)

# save dictionary, corpus and lda_model with tags trained with 37 topics to current folder
# using the lda_model module under ../library
save_lda_with_tags(doc_complete,num_topics)