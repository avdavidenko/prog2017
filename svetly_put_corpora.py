import urllib.request
import re
import html
import os
import time

def clean_text (text):
    html_content = '<html>....</html>'  # тут какой-то html
    regTag = re.compile('<.*?>', re.DOTALL)  # это рег. выражение находит все тэги
    regScript = re.compile('<script>.*?</script>', re.DOTALL) # все скрипты
    regComment = re.compile('<!--.*?-->', re.DOTALL)  # все комментарии
    regTitle = re.compile ('<td class="contentheading" width="100%">(.*?)</td>', re.DOTALL)
    regAdm = re.compile ('<span class="small">(.*?)</span>', re.DOTALL)
    regDate = re.compile ('<td valign="top" class="createdate">\n\t\t(.*?)\t</td>', re.DOTALL)
    regSpace = re.compile('\s+', re.DOTALL)
#     заменяем ненужные куски на пустую строку
    clean_t = text.replace ('&nbsp;', '')
    clean_t = regDate.sub ("", clean_t)
    clean_t = regTitle.sub ("", clean_t)
    clean_t = regAdm.sub ("", clean_t)
    clean_t = regScript.sub("", clean_t)
    clean_t = regComment.sub("", clean_t)
    clean_t = regTag.sub("", clean_t)
    clean_t = regSpace.sub(' ', clean_t) 
#    print (clean_t)
#    print(html.unescape(clean_t))
    return clean_t

#def tagging (date, filename, main_text):
#    new_directory = 'Светлый путь\\mystem-plain\\' + date[0][6:10] + '\\' + date[0][3:5] + '\\'
#    if os.path.exists(new_directory) == False:
#        os.makedirs(new_directory)
#    new_directory = new_directory + filename
#    print (new_directory)
#    сложить необработанный текст в файл и дать его майстему на вход. Иначе паймайстем, но это сложно
#    print ("mystem.exe " + 'Светлый путь\\plain\\' + date[0][6:10] + '\\' + date[0][3:5] + '\\' + filename + " " + new_directory)
#    os.system("mystem.exe " + filename + " " + new_directory)
    
#def tagging_xml (date, filename, main_text):
#    new_directory = 'Светлый путь\\mystem-xml\\' + date[0][6:10] + '\\' + date[0][3:5] + '\\'
#    if os.path.exists(new_directory) == False:
#        os.makedirs(new_directory)
#    new_directory = new_directory + filename
#    print (new_directory)
#    print ("mystem.exe " + "--format xml " + directory + " " + new_directory)
#    os.system("mystem.exe " + "--format xml " + main_text[0] + " " + new_directory)

def writing_plain(about_text, title, date, main_text):
#    print (about_text[0])
    directory = 'Светлый путь\\plain\\' + date[0][6:10] + '\\' + date[0][3:5] + '\\'
#    print (directory)
    if os.path.exists(directory) == False:
        os.makedirs(directory)
#    print (title[0])
    filename =  title[0] + '.txt'
#    print (filename)
    directory = directory + filename
#    print (directory)
    with open(directory, 'w', encoding = 'utf-8') as f:
          f.write (about_text)
          f.write ('\n')
          if  len(main_text) > 0:
              f.write (clean_text(main_text[0]))
          else:
              print ('Main text = 0')
#    tagging (date, filename, main_text)
#    tagging_xml (date, filename, main_text)
    return

def csv_info (directory, author, title, date, pageUrl):
    row = '%s\t%s\t\t\t%s\t%s\tпублицистика\t\t\t\t\tнейтральный\tн-возраст\tн-уровень\tрайонная\t%s\tСветлый путь\t\t%s\tгазета\tРоссия\tИгринский район Удмуртской Республики\tru'
    print(row(directory, author[0], title[0], date[0][:10], pageUrl, date[0][6:10]))
    
def info (text, pageUrl):
    author = re.findall('<p align="right"><strong>(.*?)</strong>', text)
    if author == []:
        author = ['Noname']
#    print (author)
    title = re.findall('<meta name="title" content="(.*?)" />', text)
#    print (title[0])
    if title[0].count ('"') > 0:
        title[0] = title[0].replace('"', '')
    if title[0].count ('«') > 0:
        title[0] = title[0].replace('«', '')
    if title[0].count ('»') > 0:
        title[0] = title[0].replace('»', '')
    if title[0].count ('?') > 0:
        title[0] = title[0].replace ('?', '_')
    if title[0].count ('*') > 0:
        title[0] = title[0].replace ('*', '_')
    if title[0].count ('+') > 0:
        title[0] = title[0].replace ('+', '_')
    if title[0].count ('№') > 0:
        title[0] = title[0].replace ('№', '_')
    if title[0].count ('?') > 0:
        title[0] = title[0].replace ('?', '_')
    if title[0].count ('\t') > 0:
        title[0] = title[0].replace ('\t', ' ')
    if title[0].count ('\n') > 0:
        title[0] = title[0].replace ('\n', ' ')
    if title[0].count (':') > 0:
        title[0] = title[0].replace (':', '_')
    if title[0].count ('|') > 0:
        title[0] = title[0].replace ('|', '_')
    if title[0].count ('\\') > 0:
        title[0] = title[0].replace ('\\', '_')
    if title[0].count ('>') > 0:
        title[0] = title[0].replace ('>', '_')                                
    if title[0].count ('<') > 0:
        title[0] = title[0].replace ('<', '_')
    if title[0].count ('/') > 0:
        title[0] = title[0].replace ('/', '_')
    if title[0].count ("'") > 0:
        title[0] = title[0].replace ("'", "_")
    regSpace = re.compile('\s+', re.DOTALL)
    title[0] = regSpace.sub(' ', title[0])
#    title[0] = html.unescape(title[0])
    print (pageUrl)
    print (title[0])
#    topic на странице нет
    regDate = re.compile('<td valign="top" class="createdate">\n\t\t(.*?)\t</td>', re.DOTALL)
    date = regDate.findall(text)
#    print (date)
    regMain = re.compile('<table class="contentpaneopen">(.*?)<!-- START of joscomment -->', re.DOTALL)
    main_text = regMain.findall (text)
#    print (main_text)
#    main_text[0] = clean_text (main_text[0])
#    print (main_text[0])
    about_text = '@au ' + author[0] + '\n@ti ' + title[0] + '\n@da ' + date[0][:10] + '\n@url ' + pageUrl
#    print (about_text)
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
        writing_plain (about_text, title, date, main_text)
    return  

#def tagging (text):
#    inp = "Светлый путь\plain"
#    lst = os.listdir(inp)
#    for fl in lst:
#        os.system(r"C:\mystem.exe " + inp + os.sep + fl + " mystem-plain" + os.sep + fl)


def download_page(commonUrl):
    for i in range(9,919): # 9 919
        pageUrl = commonUrl + str(i)
        tryNumber = 0
        succeed = False
        while succeed == False and tryNumber < 5:
            try:
                page = urllib.request.urlopen(pageUrl)
                text = page.read().decode('utf-8')
#                print (text)
                info(text, pageUrl)
#                clean_text (text)
                succeed = True
            except urllib.error.HTTPError:
                tryNumber += 3
#                time.sleep(2)
            except urllib.error.URLError:
                tryNumber += 1
                time.sleep (2)
            except:
                raise
                tryNumber += 1
                time.sleep(2)

        if succeed == False:
            print('Error at', pageUrl)
      
commonUrl = 'http://svetly-put.ru/index.php?option=com_content&view=article&id='
download_page(commonUrl)
print ('The end')
