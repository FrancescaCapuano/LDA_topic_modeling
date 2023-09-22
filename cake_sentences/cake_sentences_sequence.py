import zipfile
import pickle
import itertools
from itertools import islice

# reads back lda_model, corpus, dictionary and doc_complete
with open ('lda_model', 'rb') as dc:
    lda_model = pickle.load(dc)
with open ('corpus', 'rb') as dc:
    corpus = pickle.load(dc)
with open ('dictionary', 'rb') as dc:
    dictionary = pickle.load(dc)
with open ('doc_complete', 'rb') as dc:
    doc_complete = pickle.load(dc)
with open ('sents_per_doc', 'rb') as dc:
    sents_per_doc = pickle.load(dc)


# a list of the best topic per sentence in the corpus
best_topics=list()


# topic_sentences is a dict that stores, for each topic, a list of tuples
# of the 10 best sentences associated with the topic, with the probability of association
num_topics=19
topic_sentences={topic: [] for topic in range(num_topics)}

for i in range(len(corpus)):
    best_topic=lda_model.get_document_topics(corpus[i])[0][0]
    prob=lda_model.get_document_topics(corpus[i])[0][1]
    topic_sentences[best_topic].append((doc_complete[i],prob))
    best_topics.append(best_topic)




for topic in topic_sentences:
    topic_sentences[topic]=sorted(topic_sentences[topic], key=lambda x: x[1],reverse=True)[:10]


# a function that, given a seq list and a num list, splits the seq list into sublists
# of lengths num.
# ex: split_by_lengths([1,2,3],[2,1]) returns [[1,2],[3]]
def split_by_lengths(seq, num):
    it = iter(seq)
    out =  [x for x in (list(islice(it, n)) for n in num) if x]
    remain = list(it)
    return out if not remain else out + [remain]

# a list of lists, where each sublist represents a document,
# and contains, in order, the best topic for each sentence of the document
best_topics_per_doc = split_by_lengths(best_topics,sents_per_doc)


# A_before_B_counts is a dict that stores the counts of the times that 
# topic A mostly precedes another topic B in a document
# (we take a decision per document on whether topic a precedes topic b.
# if this is the case, we increase A_before_B_counts[a][b] by one)
# initialize dict
A_before_B_counts =dict()
for topic_A in range(num_topics):
    A_before_B_counts[topic_A]={topic_B: 0 for topic_B in range(num_topics)}


# for each document
for doc in best_topics_per_doc:
    # create a set of the best topics it contains
    doc_topics=set(doc)
    # a_before_a_counts is a dict that stores the counts of the times that 
    # topic a precedes another topic b in a single document
    a_before_b_doc=dict()
    # initialize dict
    for topic_a in doc_topics:
        a_before_b_doc[topic_a]={topic_b: 0 for topic_b in doc_topics}

    # increase count every time that a precedes b
    for a in range(len(doc)-1):
        for b in range(a+1,len(doc)):
            if doc[a]!=doc[b]:
                a_before_b_doc[doc[a]][doc[b]]+=1
    
    # for all possible couples of topics in the document - order is irrelevant:
    # ex. itertools.combinations([3,4,5], 2) returns iter((3,4),(3,5),(4,5))
    for pair in itertools.combinations(doc_topics, 2):
        a=pair[0]
        b=pair[1]
        # we take a decision per document:
        # if the number of times topic a precedes topic b in a document
        # is higher than the number of times topic b precedes topic a:
        # increase count of A_before_B_counts[a][b] by one
        if a_before_b_doc[a][b]>a_before_b_doc[b][a]:
            A_before_B_counts[a][b]+=1
        elif a_before_b_doc[a][b]<a_before_b_doc[b][a]:
            A_before_B_counts[b][a]+=1
        # if they precede each other the same number of time: ignore
        else:
            continue



# our approximation of the best sequence of topics
# according to the model
# initialize sequence with the last topic
best_sequence=[num_topics-1]

# until the length of the sequence is equal to the number of topics
while len(best_sequence)!=num_topics:
    # for each topic left (b)
    for b in range(num_topics-1):
        # check from right to left in best sequence
        for index_a in reversed(range(len(best_sequence))):
            a=best_sequence[index_a]
            # if a topic a in best_sequence precedes b 
            if A_before_B_counts[a][b]>=A_before_B_counts[b][a]:
                # if so, insert b to best sequence after a
                best_sequence.insert(index_a+1,b)
                break
            else:
                # if we reached the beginning of best_sequence and a doesn't precede b, 
                if index_a==0:
                    # insert b at the beginning of the list
                    best_sequence.insert(index_a,b)
                    break
                # if a topic a in best_sequence doesn't precede b 
                else:
                    # check with previous topic a in best_sequence
                    continue

print(best_sequence)
# save topic_sentences in the best_sequence order to file
with open('cake_sentences_sequence_results.txt','w') as s:
    for topic in best_sequence:
        s.write(str(topic)+'\n')
        for tupl in topic_sentences[topic]:
            s.write(str(tupl)+'\n')

