from flask import Flask, render_template, request

app = Flask(__name__)


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
    return render_template('article.html', content=request.form['editorValue'])


if __name__ == '__main__':
    app.run(debug=True)
