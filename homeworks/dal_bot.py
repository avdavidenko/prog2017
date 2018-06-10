import urllib.request
import time
import re
import os
import random
import tweepy
from credentials import *

def download_page(commonUrl):
    for i in range(1, 179):
        print ('page: ', i)
        pageUrl = commonUrl + str(i) + '.php'
        tryNumber = 0
        succeed = False
        while succeed == False and tryNumber < 3:
            try:
                page = urllib.request.urlopen(pageUrl)
                text = page.read().decode('utf-8')
##                print (text)
                clean_text (text)
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

def clean_text (text):
    import re
    html_content = '<html>....</html>'
    regTheme = re.compile ('<h1 class="post-title entry-title">(.*?)</h1>')
    theme = regTheme.findall (text)
    regText = re.compile('<a href="http://hobbitaniya.ru/dal/dal.php">Даль В.И. Пословицы русского народа</a><br /></p><ul>(.*?)</ul><p><a href="http://hobbitaniya.ru/">Хранители сказок</a>', re.DOTALL)
    t = regText.findall (text)
    regTag = re.compile ('<.*?>', re.DOTALL)
    t = regTag.sub ('/', t[0])
    t = t.replace ('//', '\n')
    t = t.replace ('/', '')
    t = t.replace ('  ', ' ')
    import html
    t = html.unescape(t)
    theme = html.unescape(theme[0])
##    print (theme)
##    print (t)
    writing_text (theme, t)

def writing_text(theme, text):
    directory = 'pages\\'
    if os.path.exists(directory) == False:
        os.makedirs(directory)
    filename =  theme + '.txt'
    directory = directory + filename
    directories.append (directory)
    with open(directory, 'w', encoding = 'utf-8') as f:
          if  len(text) > 0:
              writing = theme + '\n\n' + text
              f.write (writing)
          else:
              print ('Main text = 0')

def choose(directories):
    directory = random.choice(directories)
    with open (directory, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        number = random.randint(2, len (lines)-1)
        tweet = lines[number] + 'Раздел: ' + lines[0]
##        print (tweet)
    return (tweet, directory)

commonUrl = 'http://hobbitaniya.ru/dal/dal'
directories = []
previous = ''
download_page(commonUrl)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
while 0 == 0:
    directory = previous
    while previous == directory:
        (tweet, directory) = choose (directories)

    try:   
        api.update_status(tweet)
    except tweepy.error.TweepError as err:
        print(err)
        continue
    except:
        print('Unknown error')
        continue
        
    my_last_tweet = api.user_timeline(count=1)[0]
    print(my_last_tweet.id, my_last_tweet.user.screen_name, my_last_tweet.text)

    previous = directory
    time.sleep(60*60*2)
