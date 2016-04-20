import re
import pymorphy2
import os
import pickle
import nltk
print(os.getcwd())
os.chdir("C:\\Users\\User\\PycharmProjects\\untitled7\\Dicts")
wordsused = dict()
wordsusedfile = open("Dict1", "wb+")
# print(os.path.split(os.getcwd()))
for (p, d, f) in os.walk("C:\\Users\\User\\Downloads\\Books"):
    author = os.path.basename(p)
    os.chdir("C:\\Users\\User\\PycharmProjects\\untitled7\\Data")
    os.mkdir(author)
    os.chdir(p)
    print(author)
    print(p)
    print(f)
    for text in f:
        print(text)
        file = open(text, 'r')
        y = file.read()
        timedict = dict()
        y = re.sub("[0-9a-zA-Z,.—;=&\[\]@`:?/!\'_\"<>•\(\)*]", " ", y)
        y = re.sub("[^а-яА-я]+[\-]+[^а-яА-я]+", " ", y)
        y = re.sub(" ", "  ", y)
        y = re.sub("\s{1}[а-яА-Я\-]{1,3}\s{1}", "", y)
        y = y.lower()
        listy = nltk.word_tokenize(y)
        sety = set(listy)
        leny = len(listy)

        for word in sety:
            print(word, " ", end='')
            if (word in wordsused):
                print("BIIIIIIIIIIIIIIILOOOOOOOOOOOOOOO", end=' ')
            else:
                wordsused[word] = pymorphy2.MorphAnalyzer().parse(word)[0].normal_form
            timedict[wordsused[word]] = timedict.get(wordsused[word], 0) + listy.count(word)
            print(wordsused[word])
        for phrase in nltk.bigrams(listy):
            timedict[(wordsused[phrase[0]], wordsused[phrase[1]])] = timedict.get((wordsused[phrase[0]], wordsused[phrase[1]]), 0) + 1
        for pair in timedict.items():
            timedict[pair[0]] = pair[1]/leny
        os.chdir(os.path.join("C:\\Users\\User\\PycharmProjects\\untitled7\\Data", author))
        vector = open(text, "wb+")
        pickle.dump(timedict, vector)
        vector.close()
        file.close()
        os.chdir(p)
pickle.dump(wordsused, wordsusedfile)
wordsusedfile.close()