import os
from data import db_session
from flask import Flask, render_template
from data.songs import Song
from data.authors import Author
UPLOAD_FOLDER = './static/img/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    db_session.global_init('db/service.db')
    db_sess = db_session.create_session()
    db_sess.commit()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
