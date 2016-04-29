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

if __name__ == "__main__":      #считываем аргумент с путем к файлу с текстом при запуске программы из командной строки.
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

wordsused = dict()          #считываем сохраненные после обучения словари с лемматизированными формами слов.
os.chdir(os.path.join(os.getcwd(), "Dicts"))
for dictw in os.listdir(os.getcwd()):
    wordsused.update(pickle.load(open(dictw, "rb")))

file = open(namespace.path, 'r')         #открываем указанный пользователем файл для чтения.
text = file.read()
probability_dict = dict()      #создаем словарь с вероятностью использования юниграмм/биграмм
#регулярными выражениями чистим текст.
text = re.sub("[0-9a-zA-Z,.—;=\[\]@:?/!\'_\"<>•\(\)*]", " ", text)      #убираем все знаки, английские слова и буквы.
text = re.sub("[^а-яА-я]+[\-]+[^а-яА-я]+", " ", text)       #убираем все тире(те, которые являются частью слова - не трогаем. К примеру "что-нибудь").
text = re.sub(" ", "  ", text)          #удваиваем пробелы в тексте. Без этого последующее удаление стоп-слов происходит некорректно, т.к несколько слов сливаются в 1но.
text = re.sub("\s{1}[а-яА-Я\-]{1,3}\s{1}", "", text)        #убираем все слова размера 3 и меньше.
text = text.lower()

uni = nltk.word_tokenize(text)      #разбиваем текст на токены.
amount_uni = len(uni)       #считаем кол-во слов.
set_uni = set(uni)      #составляем множество неповторяющихся слов в тексте, чтобы далее не обрабатывать несколько одинаковых слов.

for word in set_uni:
    if (word not in wordsused):     #если программа не встречала такого слова при обучении, находим его нормальную форму с помощью библиотеки pymorphy2.
        wordsused[word] = pymorphy2.MorphAnalyzer().parse(word)[0].normal_form
    probability_dict[wordsused[word]] = probability_dict.get(wordsused[word], 0) + uni.count(word)      #запоминаем сколько раз каждое слово встречалось в тексте с помощью словаря.

for phrase in nltk.bigrams(uni):        #теперь посчитаем сколько раз встречалась каждая биграмма.
        probability_dict[(wordsused[phrase[0]], wordsused[phrase[1]])] = probability_dict.get((wordsused[phrase[0]], wordsused[phrase[1]]), 0) + 1

for pair in probability_dict.items():       #теперь словарь хранит вероятностную оценку использования юниграмм и биграмм.
    probability_dict[pair[0]] = pair[1] / amount_uni

file.close()
os.chdir(os.path.join(os.path.dirname(os.getcwd()), "Data"))        #переходим в папку с векторами текстов, на которых обучена программа.


#далее для каждого текста будем по методу cos считать "расстояние" между их векторами, составленными из вероятностных оценок.
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
        authors[text] = [((1 - (vect_sklr / (length1 * length2)))*100), author]         #для каждого текста из обучающей выборки храним его расстояние от проверяемого
                                                                                        #текста и автора.
sorted_authors = list(authors.items())      #сортируем все тексты по расстоянию.
sorted_authors.sort(key = lambda item: (item[1])[0])
answerdict = dict()
koeff = 1
for pair in sorted_authors[:50]:        #50 ближайших текстов запомним. Также, чем текст дальше от проверяемого, тем меньше его "вес".
    answerdict[pair[1][1]] = answerdict.get(pair[1][1], 0) + 1*koeff
    koeff = koeff - 0.02
    print(pair[0], " ", pair[1][0], " ", pair[1][1])

sorted_answer = list(answerdict.items())        #сортируем список авторов по их оценке.
sorted_answer.sort(key = lambda item: item[1], reverse = True)

for pair in sorted_answer:           #выводим значение близости для каждого автора. Чем оно выше, тем вероятнее, что автором данного текста является именно он.
    print(pair[0], " ", round(pair[1], 2))