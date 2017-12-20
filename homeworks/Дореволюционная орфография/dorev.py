from flask import Flask
from flask import render_template,request
import urllib.request
import re
import os

app = Flask(__name__)

def create_dictionary():
    dictionary = {}
    file = open('dict1.csv', 'r', encoding = 'utf-8')
    for line in file:
#        print(line)
        line2 = line.split('\t')
#        print(line2)
        if len(line2) > 1:
            line2[1] = line2[1].replace('\n', '')
            dictionary[line2[0]]=line2[1]
#    print (dictionary)
    return dictionary

def one_word(word, dictionary):
    new_word = dictionary.get(word, 'No key')
    if new_word == 'No key':
        new_word = positions(word)
    return new_word

def lemmatize():
    mystem()
    file = open('output.txt', 'r', encoding = 'utf-8')
    text = file.read()
    text = text.replace ('{', ' ')
    text = text.replace ('}', ' ')    
    text = text.replace ('?', '')
    text = text.split()
    new_text = ''
    for i in range(1, len(text), 2):
        new_word = one_word(text[i], dictionary)
        new_text = new_text + new_word + ' '
    return new_text

def positions(word):
    new_word = ''
    target = {'И', 'и', 'Й', 'й'}
    vowels = {'у', 'е', 'ы', 'а', 'о', 'э', 'я', 'и', 'ю', 'й', 'У', 'Е', 'Ы', 'А', 'О', 'Э', 'Я', 'И', 'Ю', 'ь', 'ъ'}    
    if len(word) > 1:
        for i in range(0,len(word)-1):
            if word[i] in target and word[i+1] in vowels:
                new_word += 'i'
            else:
                new_word += word[i]
        new_word += word[-1]
        if new_word[-1] not in vowels:
            new_word += 'ъ'
        if new_word.startswith('бес'):
            base = new_word[3:]
            new_word = 'без' + base
        if new_word.startswith('черес'):
            base = new_word[5:]
            new_word = 'через' + base
        if new_word.startswith('чрес'):
            base = new_word[4:]
            new_word = 'чрез' + base
    else:
        new_word = word
    return new_word
    
def mystem():
    os.system(r"mystem.exe " + "-d -e utf-8 " + 'input.txt' + " " + 'output.txt')
    return

def find_weather():
    url = 'https://yandex.ru/pogoda/10463'
    page = urllib.request.urlopen(url)
    text = page.read().decode('utf-8')
    regTag = re.compile('<.*?>', re.DOTALL)
    regSpace = re.compile('\s\s*', re.DOTALL)
    weather1 = re.search('<time class="time fact__time"(.*?)<dl class="term fact__water">', text)
    clean_weather = regTag.sub ('\n', weather1.group())
    clean_weather = regSpace.sub (' ', clean_weather)
    clean_weather = clean_weather.replace (' °', '°')
    return clean_weather

def download_html(url):
    page = urllib.request.urlopen(url)
    text = page.read().decode('utf-8')
    return text

def clean_html(text):
    html_content = '<html>....</html>'
    regTag = re.compile('<.*?>', re.DOTALL)
    regScript = re.compile('<script>.*?</script>', re.DOTALL)
    regComment = re.compile('<!--.*?-->', re.DOTALL)
    regTitle = re.compile ('<td class="contentheading" width="100%">(.*?)</td>', re.DOTALL)
    regAdm = re.compile ('<span class="small">(.*?)</span>', re.DOTALL)
    regDate = re.compile ('<td valign="top" class="createdate">\n\t\t(.*?)\t</td>', re.DOTALL)
    regSpace = re.compile('\s+', re.DOTALL)
    clean_t = text.replace ('&nbsp;', '')
    clean_t = regDate.sub ("  ", clean_t)
    clean_t = regTitle.sub (" ", clean_t)
    clean_t = regAdm.sub (" ", clean_t)
    clean_t = regScript.sub(" ", clean_t)
    clean_t = regComment.sub(" ", clean_t)
    clean_t = regTag.sub(" ", clean_t)
    clean_t = regSpace.sub(' ', clean_t) 
    import html
    html.unescape(clean_t)
    print (clean_t)
    clean_t.strip(clean_t[0])
    return clean_t

def find_text(text):
    lines = re.findall('[А-Яа-яЁё\s.,!?:;\\-0-9]+', text)
    new_text = ''
    for line in lines:
        print (line)
        new_text = ' ' + new_text + line + ' '
    print (new_text)
    return new_text

dictionary = create_dictionary()

@app.route('/')
def index():
    weather = find_weather()
    return render_template('index.html', weather = weather)

@app.route('/result')
def resultword():
    if request.args:
        word = request.args['word']
        new_word = one_word(word, dictionary)
        return render_template('result.html', new_word = new_word)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/testresult')
def testresult():
    score = 0
    if request.args:
        answers = ['answer1', 'answer2', 'answer3', 'answer4', 'answer5', 'answer6', 'answer7', 'answer8', 'answer9', 'answer10']
        for answer in answers:
            verified = request.args[answer]
            score += amswer.value
    return render_template('testresult.html', score = score)

@app.route('/news')
def news():
    text = download_html('https://news.yandex.ru/')
    file = open('input.txt','w', encoding = 'utf-8')
    text = clean_html(text)
    clean_text = find_text(text)
    file.write(clean_text)
    file.close()
    clean_text = lemmatize()
    return render_template('news.html', clean_text = clean_text)
    
if __name__ == '__main__':
   app.run(debug=True)
   
#create_dictionary()
#dictionary = create_dictionary()
#lemmatize()
