#-*- coding=utf-8 -*-
import os
from flask import Flask, render_template, request, Markup
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_title = db.Column(db.String())
    article_content = db.Column(db.String())
    article_time = db.Column(db.DateTime())
    article_from = db.Column(db.String(64))
    article_readed = db.Column(db.String())
    article_wait = db.Column(db.String())

    def __init__(self, article_title, article_content, article_time,
                 article_from, article_readed, article_wait):
        self.article_title = article_title
        self.article_content = article_content
        self.article_time = article_time
        self.article_from = article_from
        self.article_readed = article_readed
        self.article_wait = article_wait

    def __repr__(self):
        return '<Article %r>' % self.article_title


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
    return render_template('article.html', content=Markup(request.form['editorValue']), publish_data=u'2017-10-23 11:34', link=u'新闻')


if __name__ == '__main__':
    app.run(debug=True)
