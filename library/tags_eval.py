#import numpy as np
import pickle
import gensim
from gensim import corpora


# saves the 3 tags with the highest counts per topic (ordered from the most to the least frequent)
def save_tags_eval(lda_filename,num_topics,results_filename):

    # reads back lda_model
    with open (lda_filename, 'rb') as dc:
        lda_model = pickle.load(dc)


    # reads back the 2 files created by the script ../library/tags-word_best_tag.py
    # tags is a list of all tags used for the CAKE scenario in the InScript corpus
    # word_best_tag is a dictionary that stores the best tag associated with each word (if any, because not all words were tagged)
    with open ('../library/tags', 'rb') as dc:
        tags = pickle.load(dc)
    with open ('../library/word_best_tag', 'rb') as dc:
        word_best_tag = pickle.load(dc)
    #word_best_tag = np.load('../library/word_best_tag.npy').item()
    #tags = np.load('../library/tags.npy').item()


    # a dict where the keys are the topics, the values are a dict where 
    # the keys are the tags, the values are the number of the words among 
    # the 30 words with the highest prob for each topic, that were associated with a specific tag
    # topics_tag_distr = {0:{'ScrEv_get_ingredients':3,'ScrEv_take_out_oven':7,...},...}
    topics_tags_distr=dict()
    # initialize dict
    for topic in range(num_topics):
        topics_tags_distr[topic]={tag: 0 for tag in tags}


    # a dict where the keys are the topics, the values are ordered lists of the 3 best tags
    # associated with each topic (the 3 tags with the highest counts per topic in topics_tags_distr)
    # topics_best_tags = {0:['ScrEv_get_ingredients','ScrEv_take_out_oven','ScrPart_utensil'],...}
    topics_best_tags =dict()


    for topic in range(num_topics):
        # best_words is a list of tuples (word, probability) of the 30 words with the highest probability for each topic
        best_words=lda_model.show_topic(topic, topn=30)
        for word_prob in best_words:
            best_word=word_prob[0]
            # some words were not tagged:
            if best_word not in word_best_tag.keys():
                continue
            # best_tag is the tag most often associated with the word
            best_tag=word_best_tag[best_word]
            topics_tags_distr[topic][best_tag]+=1
        # the 3 tags with the highest counts per topic (ordered from the most to the least frequent)
        topics_best_tags[topic]=sorted(topics_tags_distr[topic], key=topics_tags_distr[topic].get, reverse=True)[:3]


    # a dict that stores the number of different tags per position
    # i.e. the number of all different first, second and third best tags
    tags_per_position={position:{} for position in range(3)}
    for topic in range(num_topics):
        for position in range(3):
            best_tag=topics_best_tags[topic][position]
            if best_tag in tags_per_position[position].keys():
                tags_per_position[position][best_tag]+=1
            else:
                tags_per_position[position][best_tag]=1


    # save topics_best_tags and tags_per_position to file
    with open(results_filename,'w') as s:
        for topic in range(num_topics):
            s.write(str(topic)+str(topics_best_tags[topic])+'\n')
        for position in range(3):
            s.write(str(position)+'\n'+str(tags_per_position[position])+'\n')