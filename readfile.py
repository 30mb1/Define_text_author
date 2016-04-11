import re
import pymorphy2
import os
import math
import pickle
import nltk
import argparse
import sys

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-path')
    return parser

if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

file = open(namespace.path, 'r')
text = file.read()[:7000]
probability_dict = dict()

text = re.sub("[0-9a-zA-Z,.—;=\[\]@:?/!\'_\"<>•\(\)*]", " ", text)
text = re.sub("[^а-яА-я]+[\-]+[^а-яА-я]+", " ", text)
text = re.sub(" ", "  ", text)
text = re.sub("\s{1}[а-яА-Я\-]{1,3}\s{1}", "", text)
text = text.lower()

uni = nltk.word_tokenize(text)
amount_uni = len(uni)
set_uni = set(uni)

for word in set_uni:
    print(word, " ", end='')
    norm_word = pymorphy2.MorphAnalyzer().parse(word)[0].normal_form
    probability_dict[norm_word] = probability_dict.get(norm_word, 0) + uni.count(word)
    print(norm_word)

for pair in probability_dict.items():
    print(pair[0], " ", pair[1])
    probability_dict[pair[0]] = pair[1] / amount_uni
    print(pair[0], ' ', probability_dict[pair[0]])

file.close()
os.chdir(os.path.join(os.getcwd(), "Data"))
authors = dict()

for (p, d, f) in os.walk(os.getcwd()):
    author = os.path.basename(p)
    os.chdir(p)
    authors[author] = 0
    for text in f:
        vector = open(text, "rb")
        text_freq = pickle.load(vector)

        vect_sklr = 0
        for pair in probability_dict.items():
            vect_sklr += probability_dict[pair[0]] * text_freq.get(pair[0], 0)

        length1 = 0
        for value in probability_dict.values():
            length1 += value**2
        length1 = math.sqrt(length1)

        length2 = 0
        for value in text_freq.values():
            length2 += value**2
        length2 = math.sqrt(length2)

        distance = (1 - (vect_sklr / (length1 * length2)))*100 + 0.000000001
        authors[author] += 1/(distance**2)
    print(author, " ", authors[author])