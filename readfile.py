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
wordsused = dict()
os.chdir(os.path.join(os.getcwd(), "Dicts"))
for dictw in os.listdir(os.getcwd()):
    wordsused.update(pickle.load(open(dictw, "rb")))

file = open(namespace.path, 'r')
text = file.read()
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
    if (word not in wordsused):
        wordsused[word] = pymorphy2.MorphAnalyzer().parse(word)[0].normal_form
    probability_dict[wordsused[word]] = probability_dict.get(wordsused[word], 0) + uni.count(word)

for phrase in nltk.bigrams(uni):
        probability_dict[(wordsused[phrase[0]], wordsused[phrase[1]])] = probability_dict.get((wordsused[phrase[0]], wordsused[phrase[1]]), 0) + 1

for pair in probability_dict.items():
    probability_dict[pair[0]] = pair[1] / amount_uni

file.close()
os.chdir(os.path.join(os.path.dirname(os.getcwd()), "Data"))

length1 = 0
for value in probability_dict.values():
    length1 += value**2
length1 = math.sqrt(length1)

authors = dict()
for (p, d, f) in os.walk(os.getcwd()):
    author = os.path.basename(p)
    os.chdir(p)
    for text in f:
        print(text)
        vector = open(text, "rb")
        text_freq = pickle.load(vector)

        vect_sklr = 0
        for pair in probability_dict.items():
            vect_sklr += probability_dict[pair[0]] * text_freq.get(pair[0], 0)

        length2 = 0
        for value1 in text_freq.values():
            length2 += value1**2
        length2 = math.sqrt(length2)
        authors[text] = [((1 - (vect_sklr / (length1 * length2)))*100), author]

sorted_authors = list(authors.items())
sorted_authors.sort(key = lambda item: (item[1])[0])
answerdict = dict()
koeff = 1
for pair in sorted_authors[:50]:
    answerdict[pair[1][1]] = answerdict.get(pair[1][1], 0) + 1*koeff
    koeff = koeff - 0.02
    print(pair[0], " ", pair[1][0], " ", pair[1][1])

sorted_answer = list(answerdict.items())
sorted_answer.sort(key = lambda item: item[1], reverse = True)

for pair in sorted_answer:
    print(pair[0], " ", round(pair[1], 2))