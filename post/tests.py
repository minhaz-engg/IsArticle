from django.test import TestCase

# Create your tests here.
text = """ The intensity of the feeling makes up for the disproportion of the objects.  Things are equal to the imagination, which have the power of affecting the mind with an equal degree of terror, admiration, delight, or love.  When Lear calls upon the heavens to avenge his cause, "for they are old like him," there is nothing extravagant or impious in this sublime identification of his age with theirs; for there is no other image which could do justice to the agonising sense of his wrongs and his despair! """

BAD_CHARS = ".!?,\'\""

# transform text into a list words--removing punctuation and filtering small words
words = [ word.strip(BAD_CHARS) for word in text.strip().split() if len(word) > 4 ]

word_freq = {}

# generate a 'word histogram' for the text--ie, a list of the frequencies of each word
for word in words :
  word_freq[word] = word_freq.get(word, 0) + 1

# sort the word list by frequency 
# (just a DSU sort, there's a python built-in for this, but i can't remember it)
tx = [ (v, k) for (k, v) in word_freq.items()]
tx.sort(reverse=True)
word_freq_sorted = [ (k, v) for (v, k) in tx ]

# eg, what are the most common words in that text?
# returns: [('which', 4), ('other', 4), ('like', 4), ('what', 3), ('upon', 3)]
# obviously using a text larger than 50 or so words will give you more meaningful results

term_importance = lambda word : 1.0/word_freq[word]

# select document keywords from the words at/near the top of this list:
map(term_importance, word_freq.keys())

def getList(dict):
    list = []
    for key in dict.keys():
        list.append(key)
          
    return list

print(getList(word_freq))
