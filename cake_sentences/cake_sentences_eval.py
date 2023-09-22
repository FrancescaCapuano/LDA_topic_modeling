import sys
sys.path.append('../library')
from tags_eval import *


# it stores, in order, the 3 tags most often associated with each topic 
# using the tags_eval module under ../library
save_tags_eval('lda_model',19,'cake_sentences_results.txt')