#-*- coding=utf-8 -*-
from flask import Flask, render_template, request, Markup
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////database.db'
db = SQLAlchemy(app)


'''
@app.route('/')
def index():
    return render_template('index.html')
'''


@app.route('/article')
def article():
    return render_template('article.html')


@app.route('/editor')
def editor():
    return render_template('ueditor.html')


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    return render_template('article.html', content=Markup(request.form['editorValue']),publish_data=u'2017-10-23 11:34',link=u'新闻')


if __name__ == '__main__':
    app.run(debug=True)
