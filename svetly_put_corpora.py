import urllib.request
import re
import html
import os
import time

#def clean_text (text):
    #html_content = '<html>....</html>'  # тут какой-то html
    #regTag = re.compile('<.*?>', re.DOTALL)  # это рег. выражение находит все тэги
    #regScript = re.compile('<script>.*?</script>', re.DOTALL) # все скрипты
    #regComment = re.compile('<!--.*?-->', re.DOTALL)  # все комментарии
    # заменяем ненужные куски на пустую строку
    #clean_t = regScript.sub("", text)
    #clean_t = regComment.sub("", clean_t)
    #clean_t = regTag.sub("", clean_t)
    #clean_t = html.unescape(clean_t)
    #return clean_t

def tagging (directory, date, filename, main_text):
    new_directory = 'Светлый путь\\mystem-plain\\' + date[0][6:10] + '\\' + date[0][3:5] + '\\'
    if os.path.exists(new_directory) == False:
        os.makedirs(new_directory)
    new_directory = new_directory + filename
#    print (new_directory)
    print ("mystem.exe " + directory + " " + new_directory)
    os.system("mystem.exe " + directory + " " + new_directory)
    
def tagging_xml (directory, date, filename, main_text):
    new_directory = 'Светлый путь\\mystem-xml\\' + date[0][6:10] + '\\' + date[0][3:5] + '\\'
    if os.path.exists(new_directory) == False:
        os.makedirs(new_directory)
    new_directory = new_directory + filename
#    print (new_directory)
    print ("mystem.exe " + "--format xml " + directory + " " + new_directory)
    os.system("mystem.exe " + "--format xml " + directory + " " + new_directory)

def writing_plain(about_text, title, date, main_text):
    # print (about_text[0])
    directory = 'Светлый путь\\plain\\' + date[0][6:10] + '\\' + date[0][3:5] + '\\'
    # print (directory)
    if os.path.exists(directory) == False:
        os.makedirs(directory)
    # print (title[0])
    filename =  title[0] + '.txt'
    # print (filename)
    directory = directory + filename
    #print (directory)
    with open(directory, 'w', encoding = 'utf-8') as f:
          f.write (about_text)
          f.write ('\n')
          if  len(main_text) > 0:
              f.write (main_text[0])
          else:
              print ('Main text = 0')
    tagging (directory, date, filename, main_text)
    tagging_xml (directory, date, filename, main_text)
    return

def csv_info (directory, author, title, date, pageUrl):
    row = '%s\t%s\t\t\t%s\t%s\tпублицистика\t\t\t\t\tнейтральный\tн-возраст\tн-уровень\tрайонная\t%s\tСветлый путь\t\t%s\tгазета\tРоссия\tИгринский район Удмуртской Республики\tru'
    print(row(directory, author[0], title[0], date[0][:10], pageUrl, date[0][6:10]))
    
def info (text, pageUrl):
    author = re.findall('<p align="right"><strong>(.*?)</strong>', text)
    if author == []:
        author = ['Noname']
    # print (author)
    title = re.findall('<meta name="title" content="(.*?)" />', text)
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
    title[0] = html.unescape(title[0])
    # print (title)
    # topic на странице нет
    regDate = re.compile('<td valign="top" class="createdate">\n\t\t(.*?)\t</td>', re.DOTALL)
    date = regDate.findall(text)
    # print (date)
    # текст статьи находится не вeзде (см., например, 106)
    main_text = re.findall ('<p>(.*?)</p>', text)
    # print (main_text)
    about_text = '@au ' + author[0] + '\n@ti ' + title[0] + '\n@da ' + date[0][:10] + '\n@url ' + pageUrl
    # print (about_text)
    # print ('\n', main_text[0])
    # article = '@au ' + author[0] + '\n@ti ' + title[0] + '\n@da ' + date[0] + '\n@url ' + pageUrl + '\n' + main_text[0]
    # print (article)
    if len(main_text) > 0:
        main_text[0] = html.unescape(main_text[0])
        writing_plain (about_text, title, date, main_text)
    return  

# def tagging (text):
    # inp = "Светлый путь\plain"
    # lst = os.listdir(inp)
    # for fl in lst:
        # os.system(r"C:\mystem.exe " + inp + os.sep + fl + " mystem-plain" + os.sep + fl)


def download_page(commonUrl):
    for i in range(9,12): # 9 919
        pageUrl = commonUrl + str(i)
        tryNumber = 0
        succeed = False
        while succeed == False and tryNumber < 1:
            try:
                page = urllib.request.urlopen(pageUrl)
                text = page.read().decode('utf-8')
                # print (text)
                info(text, pageUrl)
                # clean_text (text)
                succeed = True
            except urllib.error.HTTPError:
                tryNumber += 1
                time.sleep(1)
            except:
                raise
                tryNumber += 1
                time.sleep(1)

        if succeed == False:
            print('Error at', pageUrl)
      
commonUrl = 'http://svetly-put.ru/index.php?option=com_content&view=article&id='
download_page(commonUrl)

    
