from flask import Flask
from flask import url_for, render_template, request, redirect
import sqlite3
import json
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import Required


app = Flask(__name__)

conn = sqlite3.connect('results.db')
c = conn.cursor()
c.execute('''CREATE TABLE results
            (language, word1, word2, word3, word4, word5, word6, word7, word8, word9, word10)''')

class Questions(Form):
    lang = TextField('lang', validators = [Required()])
    word1 = TextField('word1', validators = [Required()])
    word2 = TextField('word2', validators = [Required()])
    word3 = TextField('word3', validators = [Required()])
    word4 = TextField('word4', validators = [Required()])
    word5 = TextField('word5', validators = [Required()])
    word6 = TextField('word6', validators = [Required()])
    word7 = TextField('word7', validators = [Required()])
    word8 = TextField('word8', validators = [Required()])
    word9 = TextField('word9', validators = [Required()])
    word10 = TextField('word10', validators = [Required()])

class SearchFormLang(Form):
    inp_lang = TextField('inp_lang')

class SearchFormId(Form):
    inp_id = TextField ('inp_id')

@app.route('/')
def index():
    urls = {'статистика': url_for('stats'),
        'вывод всех данных в json': url_for('json'),
        'страница поиска': url_for('search')}
    form = Questions()
    render_template ('index.html', urls = urls, form = form)
    if form.validate_on_submit():
        lang = request.args['lang']
        word1 = request.args['word1']
        word2 = request.args['word2']
        word3 = request.args['word3']
        word4 = request.args['word4']
        word5 = request.args['word5']
        word6 = request.args['word6']
        word7 = request.args['word7']
        word8 = request.args['word8']
        word9 = request.args['word9']
        word10 = request.args['word10']
        db_input(lang, word1, word2, word3, word4, word5, word6, word7, word8, word9, word10)    
        return redirect('thanks', urls = urls)
    else:
        return render_template ('index.html', urls = urls, form = form)

def db_input(lang, word1, word2, word3, word4, word5, word6, word7, word8, word9, word10):
    c.execute("INSERT INTO results VALUES (lang, word1, word2, word3, word4, word5, word6, word7, word8, word9, word10)")
    conn.commit()
    return

@app.route('/thanks2')
def thanks2():
    urls = {'главная': url_for('index'),
        'статистика': url_for('stats'),
        'вывод всех данных в json': url_for('json'),
        'страница поиска': url_for('search')}
    return render_template('thanks.html', urls = urls)

@app.route('/error')
def error():
    urls = {'главная (эта страница)': url_for('index'),
        'статистика': url_for('stats'),
        'вывод всех данных в json': url_for('json'),
        'страница поиска': url_for('search')}
    return render_template('error.html', urls = urls)

@app.route('/stats')
def stats():
    urls = {'главная (эта страница)': url_for('index'),
        'вывод всех данных в json': url_for('json'),
        'страница поиска': url_for('search')}
    return render_template ('stats.html', urls = urls)

@app.route('/json')
def json():
    urls = {'главная (эта страница)': url_for('index'),
        'статистика': url_for('stats'),
        'страница поиска': url_for('search')}
    c.execute('SELECT * FROM results')
    all_res = c.fetchall()
    json_out = json.dumps (all_res)
    return render_template ('json.html', urls = urls, json_out = json_out)

@app.route('/search')
def search():
    urls = {'главная (эта страница)': url_for('index'),
        'статистика': url_for('stats'),
        'вывод всех данных в json': url_for('json')}
    form_lang = SearchFormLang()
    form_id = SearchFormId()
    render_template ('search.html', urls = urls, form_lang = form_lang, form_id = form_id)
    if form_lang.validate_on_submit():
        inp_lang = request.args['inp_lang']
        c.execute ('SELECT * FROM results WHERE language = inp_lang')
        search_res = c.fetchall()
    if form_id.validate_on_submit():
        inp_id = request.args['inp_id']
        c.execute ('SELECT * FROM results WHERE rowid = inp_id')
        search_res = c.fetchall()
    return render_template ('results.html', search_res = search_res)

if __name__ == '__main__':
    app.run(debug=True)
