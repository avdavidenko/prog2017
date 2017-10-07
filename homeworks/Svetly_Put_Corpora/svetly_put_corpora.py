import urllib.request
import re
import os
import time
import csv

def clean_text (text):
    html_content = '<html>....</html>'
    regTag = re.compile('<.*?>', re.DOTALL)
    regScript = re.compile('<script>.*?</script>', re.DOTALL)
    regComment = re.compile('<!--.*?-->', re.DOTALL)
    regTitle = re.compile ('<td class="contentheading" width="100%">(.*?)</td>', re.DOTALL)
    regAdm = re.compile ('<span class="small">(.*?)</span>', re.DOTALL)
    regDate = re.compile ('<td valign="top" class="createdate">\n\t\t(.*?)\t</td>', re.DOTALL)
    regSpace = re.compile('\s+', re.DOTALL)
    clean_t = text.replace ('&nbsp;', '')
    clean_t = regDate.sub ("", clean_t)
    clean_t = regTitle.sub ("", clean_t)
    clean_t = regAdm.sub ("", clean_t)
    clean_t = regScript.sub("", clean_t)
    clean_t = regComment.sub("", clean_t)
    clean_t = regTag.sub("", clean_t)
    clean_t = regSpace.sub(' ', clean_t) 
    import html
    html.unescape(clean_t)
    clean_t.strip(clean_t[0])
    return clean_t

def clean_author (author):
    html_content = '<html>....</html>'
    regTag = re.compile('<.*?>', re.DOTALL)
    regScript = re.compile('<script>.*?</script>', re.DOTALL)
    regComment = re.compile('<!--.*?-->', re.DOTALL)
    regTitle = re.compile ('<td class="contentheading" width="100%">(.*?)</td>', re.DOTALL)
    regAdm = re.compile ('<span class="small">(.*?)</span>', re.DOTALL)
    regDate = re.compile ('<td valign="top" class="createdate">\n\t\t(.*?)\t</td>', re.DOTALL)
    regSpace = re.compile('\s+', re.DOTALL)
    author[0] = author[0].replace ('&nbsp;', '')
    author[0] = regDate.sub ("", author[0])
    author[0] = regTitle.sub ("", author[0])
    author[0] = regAdm.sub ("", author[0])
    author[0] = regScript.sub("", author[0])
    author[0] = regComment.sub("", author[0])
    author[0] = regTag.sub("", author[0])
    author[0] = regSpace.sub(' ', author[0]) 
    import html
    html.unescape(author[0])
    author[0].strip(author[0])
    return author

def clean_title (title):
    regSpace = re.compile('\s+', re.DOTALL)
    title[0] = regSpace.sub(' ', title[0])
    import html
    title[0] = html.unescape(title[0])
    title[0].strip(title[0])
    return title

def replace_by_table(title):
    converted = ""
    for ch in title[0]:
        converted += replacement_table.get(ch, ch)
    title[0] = converted
    
def tagging (date, filename, main_text, directory):
    new_directory = 'Svetly_Put\\mystem-plain\\' + date[0][6:10] + '\\' + date[0][3:5] + '\\'
    if os.path.exists(new_directory) == False:
        os.makedirs(new_directory)
    new_directory = new_directory + filename
    os.system(r"mystem.exe " + "-idc " + directory + " " + new_directory)
   
def tagging_xml (date, filename, main_text, directory):
    new_directory = 'Svetly_Put\\mystem-xml\\' + date[0][6:10] + '\\' + date[0][3:5] + '\\'
    if os.path.exists(new_directory) == False:
        os.makedirs(new_directory)
    new_directory = new_directory + filename
    os.system(r"mystem.exe " + "--format xml -id " + directory + " " + new_directory)

def writing_plain(about_text, title, date, main_text, author, pageUrl):
    directory = 'Svetly_Put\\plain\\' + date[0][6:10] + '\\' + date[0][3:5] + '\\'
    if os.path.exists(directory) == False:
        os.makedirs(directory)
    replace_by_table(title)
    filename =  title[0] + '.txt'
    directory = directory + filename
    with open(directory, 'w', encoding = 'utf-8') as f:
          if  len(main_text) > 0:
              f.write (clean_text(main_text[0]))
          else:
              print ('Main text = 0')
    csv_file = 'Svetly_Put\\metadata.csv'
    csv_info (csv_file, directory, author, title, date, pageUrl)
    tagging (date, filename, main_text, directory)
    tagging_xml (date, filename, main_text, directory)
    main_text[0] = clean_text(main_text[0])
    with open(directory, 'w', encoding = 'utf-8') as f:
          if  len(main_text) > 0:
              f.write (about_text)
              f.write ('\n')
              f.write (clean_text(main_text[0]))
          else:
              print ('Main text = 0')
    return

def csv_info (csv_file, directory, author, title, date, pageUrl):
    with open (csv_file, "a", newline = "") as file:
        writer = csv.writer(file, delimiter = '\t')
        writer.writerows([[directory, author[0], title[0], date[0][0:10], 'публицистика', '', '', '', '', 'нейтральный', 'н-возраст', 'н-уровень', 'районная', pageUrl, 'Светлый путь', date[0][6:10], 'газета', 'Россия', 'Игринский район Удмуртской Республики', 'ru']])

def info (text, pageUrl):
    author = re.findall('<p align="right"><strong>(.*?)</strong>', text)
    if author == []:
        author = ['Noname']
    author = clean_author (author)
    if author[0].count ('▼') > 0:
        author[0] = author[0].replace ('▼', '')
    title = re.findall('<meta name="title" content="(.*?)" />', text)
    clean_title (title)
    regDate = re.compile('<td valign="top" class="createdate">\n\t\t(.*?)\t</td>', re.DOTALL)
    date = regDate.findall(text)
    regMain = re.compile('<table class="contentpaneopen">(.*?)<!-- START of joscomment -->', re.DOTALL)
    main_text = regMain.findall (text)
    about_text = '@au ' + author[0] + '\n@ti ' + title[0] + '\n@da ' + date[0][:10] + '\n@url ' + pageUrl
    Udmurt = False
    if main_text[0].count ('Ӝ') > 0:
        Udmurt = True
    elif main_text[0].count('ӝ') > 0:
        Udmurt = True
    elif main_text[0].count('Ӟ') > 0:
        Udmurt = True
    elif main_text[0].count('ӟ') > 0:
        Udmurt = True
    elif main_text[0].count('Ӥ') > 0:
        Udmurt = True
    elif main_text[0].count('ӥ') > 0:
        Udmurt = True
    elif main_text[0].count('Ӧ') > 0:
        Udmurt = True
    elif main_text[0].count('ӧ') > 0:
        Udmurt = True
    elif main_text[0].count('Ӵ') > 0:
        Udmurt = True
    elif main_text[0].count('ӵ') > 0:
        Udmurt = True            
    if len(main_text) > 0 and Udmurt == False:
        writing_plain (about_text, title, date, main_text, author, pageUrl)
    return  

def download_page(commonUrl):
    for i in range(9,12): # 9 919
#        print ('article: ', i)
        pageUrl = commonUrl + str(i)
        tryNumber = 0
        succeed = False
        while succeed == False and tryNumber < 3:
            try:
                page = urllib.request.urlopen(pageUrl)
                text = page.read().decode('utf-8')
                info(text, pageUrl)
                succeed = True
            except urllib.error.HTTPError:
                tryNumber += 3
            except urllib.error.URLError:
                tryNumber += 1
                time.sleep (2)
            except:
                raise
                tryNumber += 1
                time.sleep(2)

        if succeed == False:
            print('Error at', pageUrl)
            
replacement_table = {' ':'_',
                     '"':'',
                     '«':'',
                     '»':'',
                     '?':'',
                     '*':'',
                     '+':'',
                     '№':'',
                     '\t':' ',
                     '\n':' ',
                     ':':'',
                     '|':'',
                     '\\':'',
                     '>':'',
                     '<':'',
                     '/':'',
                     "'":'',
                     '▼':'',
                     'а':'a',
                     'б':'b',
                     'в':'v',
                     'г':'g',
                     'д':'d',
                     'е':'e',
                     'ё':'yo',
                     'ж':'zh',
                     'з':'z',
                     'и':'i',
                     'й':'y',
                     'к':'k',
                     'л':'l',
                     'м':'m',
                     'н':'n',
                     'о':'o',
                     'п':'p',
                     'р':'r',
                     'с':'s',
                     'т':'t',
                     'у':'u',
                     'ф':'f',
                     'х':'h',
                     'ц':'c',
                     'ч':'ch',
                     'ш':'sh',
                     'щ':'shch',
                     'ъ':'y',
                     'ы':'y',
                     'ь':'',
                     'э':'e',
                     'ю':'yu',
                     'я':'ya',
                     'А':'A',
                     'Б':'B',
                     'В':'V',
                     'Г':'G',
                     'Д':'D',
                     'Е':'E',
                     'Ё':'Yo',
                     'Ж':'Zh',
                     'З':'Z',
                     'И':'I',
                     'Й':'Y',
                     'К':'K',
                     'Л':'L',
                     'М':'M',
                     'Н':'N',
                     'О':'O',
                     'П':'P',
                     'Р':'R',
                     'С':'S',
                     'Т':'T',
                     'У':'U',
                     'Ф':'F',
                     'Х':'H',
                     'Ц':'Ts',
                     'Ч':'Ch',
                     'Ш':'Sh',
                     'Щ':'Shch',
                     'Ъ':'Y',
                     'Ы':'Y',
                     'Ь':'',
                     'Э':'E',
                     'Ю':'Yu',
                     'Я':'Ya'}

commonUrl = 'http://svetly-put.ru/index.php?option=com_content&view=article&id='
download_page(commonUrl)
#print ('The end')


    
