import zipfile
import sys,os
import xml.etree.ElementTree as ET
import nltk
from nltk.tokenize import sent_tokenize
sys.path.append('../library')
from lda_model import *
import gensim
from gensim import corpora



# check if InScript folder is already extracted, otherwise extract it
if os.path.isdir("../InScript")==False:
	myzip=zipfile.ZipFile('../InScript_LREC2016.zip')
	myzip.extractall('..')
	myzip.close()


# compile documents: doc_complete = [doc1, doc2, doc3, ..., docn]
# the docs are all the sentences from all the stories from the CAKE scenario in the InScript corpus
doc_complete=list()


# a list that stores, in the same order as the corpus, the number of sentences contained in each full story
sents_per_doc = list()

# open each xml file from the CAKE corpus
path = '/home/francesca/Documents/Computational Linguistics 2/InScript/corpus/cake'
for filename in os.listdir(path):
    tree = ET.parse(path+'/'+filename)
    root = tree.getroot()
    # retrieve the text under the label 'content' (a full story)
    for content in root.iter('content'):
        # divide each full story in sentences with sent_tokenize 
        sents=nltk.sent_tokenize(content.text)
        # append number of sentences per story in sents_per_doc
        sents_per_doc.append(len(sents))
        # append each sentence to doc_complete
        for sentence in sents:
            doc_complete.append(sentence)


# save doc_complete and sents_per_doc to file, to be used in the evaluation
with open('doc_complete', 'wb') as dc:
    pickle.dump(doc_complete, dc)
with open('sents_per_doc', 'wb') as dc:
    pickle.dump(sents_per_doc, dc)



# save dictionary, corpus and lda_model trained with 20 topics to current folder
# using the lda_model module under ../library
num_topics=19
save_lda(doc_complete,num_topics)


# save dictionary, corpus and lda_model with tags trained with 20 topics to current folder
# using the lda_model module under ../library
save_lda_with_tags(doc_complete,num_topics)