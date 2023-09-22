import zipfile
import os
#import numpy as np
import xml.etree.ElementTree as ET
from clean import *
import pickle


# check if InScript folder is already extracted, otherwise extract it
if os.path.isdir("../InScript")==False:
	myzip=zipfile.ZipFile('.../InScript_LREC2016.zip')
	myzip.extractall()
	myzip.close()


# tags is a list of all tags used for the CAKE scenario in the InScript corpus
tags=set()

# word_tags is a dictionary that stores the counts of the tags associated with each word (if any, because not all words were tagged)
word_tags=dict()

# open each xml file from the CAKE corpus 
path = '../InScript/corpus/cake'


for filename in os.listdir(path):
	tree = ET.parse(path+'/'+filename)
	root = tree.getroot()
	# retrieve the labels 'label' (the annotations)
	for label in root.iter('label'):
		# retrieve and clean the text under the inner label 'text' (the text that was annotated with one tag)
		text=clean(label.attrib['text'])
		# retrieve the corresponding tag
		tag=label.attrib['name']
		# add tag to the set of tags
		tags.add(tag)
		# for each word in the text annotated with a tag, increase count in words_tags[word][tag] by one
		for word in text.split():
			if word in word_tags.keys():
				if tag in word_tags[word].keys():
					word_tags[word][tag]+=1
				else:
					word_tags[word][tag]=1
			else:
				word_tags[word]=dict()
				word_tags[word][tag]=1


# save tags to file
#np.save('tags.npy', tags) 
with open('tags', 'wb') as dc:
    pickle.dump(tags, dc)


# word_best_tag is a dictionary that stores the best tag associated with each word
word_best_tag=dict()
for word in word_tags.keys():
	best_tag=max(word_tags[word], key=word_tags[word].get)
	word_best_tag[word]=best_tag

# save word_best_tag to file
#np.save('word_best_tag.npy', word_best_tag) 
with open('word_best_tag', 'wb') as dc:
    pickle.dump(word_best_tag, dc)
