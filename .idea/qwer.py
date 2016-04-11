import re
import pymorphy2
import os
import pickle
import nltk
quantity = 0;
#print(os.getcwd())
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
        z = file.read()
        if (len(z) > 5000):
            y = z[:5000]
        else:
            y = z
        timedict = dict()
        y = re.sub("[0-9a-zA-Z,.—;=&\[\]@`:?/!\'_\"<>•\(\)*]", " ", y)
        y = re.sub("[^а-яА-я]+[\-]+[^а-яА-я]+", " ", y)
        y = re.sub(" ", "  ", y)
        y = re.sub("\s{1}[а-яА-Я\-]{1,3}\s{1}", "", y)
        y = y.lower()
        listy = nltk.word_tokenize(y)
        leny = len(listy)
        sety = set(listy)
        quantity += len(sety)
        print(len(sety))
        print(quantity)
        for word in sety:
            print(word, " ", end='')
            normword = pymorphy2.MorphAnalyzer().parse(word)[0].normal_form
            timedict[normword] = timedict.get(normword, 0) + listy.count(word)
            print(normword)
        for pair in timedict.items():
            print(pair[0], " ", pair[1])
            timedict[pair[0]] = pair[1]/leny
            print(pair[0], ' ', timedict[pair[0]])
        os.chdir(os.path.join("C:\\Users\\User\\PycharmProjects\\untitled7\\Data", author))
        vector = open(text, "wb+")
        pickle.dump(timedict, vector)
        vector.close()
        file.close()
        os.chdir(p)