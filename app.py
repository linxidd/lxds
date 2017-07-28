# -*- coding=utf-8 -*-
import os
import re
from datetime import datetime
import json
from flask import Flask, render_template, request, Markup
from flask_sqlalchemy import SQLAlchemy
from upload import Uploader

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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/article')
def article():
    return render_template('article.html')


@app.route('/editor')
def editor():
    return render_template('ueditor.html')


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    result = {}
    action = request.args.get('action')
    with open(os.path.join(os.getcwd(), 'static', 'ueditor', 'php',
                           'config.json')) as fp:
        try:
            CONFIG = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
        except:
            CONFIG = {}
    if action == 'config':
        result = json.dumps(CONFIG)
        return result
    elif action in ('uploadimage', 'uploadvideo', 'uploadfile'):
        if action == "uploadimage":
            fieldName = CONFIG.get('imageFieldName')
            config = {
                'pathFormat': CONFIG['imagePathFormat'],
                'maxSize':CONFIG['imageMaxSize'],
                'allowFiles':CONFIG['imageAllowFiles']
            }
        else:
            fieldName = CONFIG.get('fileFieldName')
            config = {
                'pathFormat': CONFIG['filePathFormat'],
                'maxSize':CONFIG['fileMaxSize'],
                'allowFiles':CONFIG['fileAllowFiles']
            }
        if fieldName in request.files:
            field = request.files[fieldName]
            uploader = Uploader(field,config,app.static_folder)
            result = uploader.getFileInfo()
        return json.dumps(result)

    else:
        now = datetime.now()
        article = Article(article_title=request.form['title'],
                          article_content=request.form['editorValue'],
                          article_time=now,
                          article_from=request.form['publisher'],
                          article_readed='',
                          article_wait='')
        db.session.add(article)
        db.session.commit()
        return render_template('article.html',
                               title=request.form['title'],
                               article_content=Markup(
                                   request.form['editorValue']),
                               publish_date=now.strftime('%Y-%m-%d %H:%M:%S'),
                               publisher=request.form['publisher'],
                               link=u'新闻')


if __name__ == '__main__':
    app.run(debug=True)
