import urllib.request
import re
import html
import os

def clean_text (text):
    html_content = '<html>....</html>'  # тут какой-то html
    regTag = re.compile('<.*?>', re.DOTALL)  # это рег. выражение находит все тэги
    regScript = re.compile('<script>.*?</script>', re.DOTALL) # все скрипты
    regComment = re.compile('<!--.*?-->', re.DOTALL)  # все комментарии
    # а дальше заменяем ненужные куски на пустую строку
    clean_t = regScript.sub("", text)
    clean_t = regComment.sub("", clean_t)
    clean_t = regTag.sub("", clean_t)
    clean_t = html.unescape(clean_t)
    return

def writing_plain(about_text, title, date, main_text):
    print (about_text)
    directory = 'Светлый путь\\plain\\' + date[0][6:10] + '\\' + date[0][3:5] + '\\'
    #print (directory)
    if os.path.exists(directory) == False:
        os.makedirs(directory)
    #print (title[0])
    filename =  title[0] + '.txt'
    #print (filename)
    directory = directory + filename
    print (directory)
    with open(directory, 'w', encoding = 'utf-8') as f:
          f.write (about_text)
          f.write ('\n')
          f.write (main_text[0])

def info (text, pageUrl):
    author = re.findall('<p align="right"><strong>(.*?)</strong>', text)
    if author == []:
        author = ['Noname']
    #print (author)
    title = re.findall('<meta name="title" content="(.*?)" />', text)
    #print (title)
    #topic на странице нет
    regDate = re.compile('<td valign="top" class="createdate">\n\t\t(.*?)\t</td>', re.DOTALL)
    date = regDate.findall(text)
    #print (date)
    #текст статьи находится не вeзде (см., например, 106)
    main_text = re.findall ('<p>(.*?)</p>', text)
    #print (main_text)
    about_text = '@au ' + author[0] + '\n@ti ' + title[0] + '\n@da ' + date[0][:10] + '\n@url ' + pageUrl
    #print (about_text)
    #print ('\n', main_text[0])
    #article = '@au ' + author[0] + '\n@ti ' + title[0] + '\n@da ' + date[0] + '\n@url ' + pageUrl + '\n' + main_text[0]
    #print (article)
    writing_plain (about_text, title, date, main_text)
    return  


#def tagging (text):
    #inp = "Светлый путь\plain"
    #lst = os.listdir(inp)
    #for fl in lst:
        #os.system(r"C:\mystem.exe " + inp + os.sep + fl + " mystem-plain" + os.sep + fl)


def download_page(commonUrl):
    links = []
    for i in range(9,919):
        pageUrl = commonUrl + str(i)
        try:
            page = urllib.request.urlopen(pageUrl)
            text = page.read().decode('utf-8')
            info(text, pageUrl)
            clean_text (text)
        except:
            print('Error at', pageUrl)
            return 
      
commonUrl = 'http://svetly-put.ru/index.php?option=com_content&view=article&id='
download_page(commonUrl)

    
