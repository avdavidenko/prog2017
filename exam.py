##1. (5 баллов) Скачать отсюда архив страниц интернет-сайта с тайско-английским
##словарём. Извлечь с каждой страницы пары "тайское слово -- английское слово"
##и поместить их в питоновскую структуру данных типа "словарь", где ключом будет
##тайское слово, а значением - английское.
##
##2. (8 балла) Использовать структуру данных из предыдущего задания, записать
##её в файл формата json на диск, а также создать ещё одну структуру данных, где
##будет наоборот: английское слово ключ, а массив тайских слов - значение. Её
##тоже записать на диск в формате json.
##
##3. (10 баллов) Создать на фласке веб-приложение "Англо-тайский словарь", где
##можно было бы в текстовом поле ввести английское слово и получить в качестве
##результата запроса - его перевод на тайский.


import os
import re

def clean_text (text):   
    import html
#    lines = re.findall ("<td class=th><a href='/id/228985'>(.+?)</a></td><td>(.+?)td class=pos></td><td>&#34;(.+?)&#34;</td>", text, re.DOTALL)
#    print (lines)
    regTag = re.compile('<.*?>', re.DOTALL)
    clean_t = regTag.sub(" ", text)
    html.unescape(clean_t)
    return clean_t

def open_html ():
#    for i in range (187, 206):
#        for j in range (1, 80):
    for i in range (187, 188):
        for j in range (31, 32):
            name = 'thai_pages\\' + str(i) + '.' + str(j) + '.html'
            print (name)
            file = open(name, 'r', encoding = 'utf8')
            text = file.read()
#            print (text)
            new_text = clean_text(text)
#            print (new_text)
            splitted = new_text.split ()
#            print (splitted)
            thai = []
            for i in range (1, len(splitted)):
                if (re.search ('[ก-๛]', splitted[i]) != None):
                    thai.append (splitted[i])
            print (thai)
    return

def dictionary(clean_text):
    return

open_html()
