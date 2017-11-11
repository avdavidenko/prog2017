from flask import Flask
from flask import url_for, render_template, request, redirect
import csv

langs = {}
with open('lang_codes.csv', 'r', encoding = 'utf-8')as csvfile:
    lang_codes = csv.reader(csvfile)
    for row in lang_codes:
        ##print (row[0], row[1])
        langs[row[1]] = row[0]
##print(langs)
    
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', langs=langs)

@app.route('/codes')
@app.route('/codes/<name>')
def codes(name=None):
    if name is None:
        return 'Error'
    else:
        return render_template('codes.html', langs=langs, name=name)

if __name__ == '__main__':
    app.run()




