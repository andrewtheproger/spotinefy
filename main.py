import os
from re import S
from mutagen.mp3 import MP3
from data import db_session
from flask import Flask, render_template, request, url_for, redirect
from flask_login import current_user
from flask import Flask, render_template, session
from data.edit import EditForm
from data.register_form import RegisterForm
from data.songs import Song
from data.authors import Author
from data.links import Link
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import send_from_directory, abort
import xmltodict
from pprint import pprint
import json
import requests
from data.login_form import LoginForm
from flask_login import LoginManager, UserMixin,  login_required, login_user, current_user, logout_user

from data.users import User
from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

UPLOAD_FOLDER = "./static/img/"
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config["CLIENT_SONGS"] = "./songs/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"
user_email = ''
nic = ''

@app.route("/share-song/<id>")
def share_song(id):
    song = db_sess.query(Song).filter(Song.id == id).first()
    authors = ", ".join(map(lambda x: x.name, db_sess.query(Author).filter(Author.id.in_(json.loads(get_song_data(id))["authors"]))))
    print(song.clip.replace("watch?v=", "embed/"))
    return render_template("share.html", id=id, name=song.name, authors=authors, duration=song.duration, clip=song.clip.replace("watch?v=", "embed/"), text=get_song_text(id).split("\n"))

@app.route('/')
def start():
    return render_template("start.html")

@app.route('/reg', methods=['GET', 'POST'])
def reqister():
    global user_email, nic
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            nic=form.nic.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        print(user.set_password(form.password.data))
        db_sess.add(user)
        db_sess.commit()
        nic = form.nic.data
        user_email = form.email.data
        return redirect('/music')
    return render_template('register.html', title='Регистрация', form=form)



@app.route("/get-song-text/<id>")
def get_song_text(id):
    song = json.loads(get_song_data(id))["name"]
    author = (
        db_sess.query(Author)
        .filter(Author.id == json.loads(get_song_data(id))["authors"][-1])
        .first()
        .name
    )
    responce = requests.get(
        f"http://api.chartlyrics.com/apiv1.asmx/SearchLyric?artist={author}&song={song}"
    )
    data = json.loads(json.dumps(xmltodict.parse(responce.content)))[
        "ArrayOfSearchLyricResult"
    ]["SearchLyricResult"][0]
    responce = requests.get(
        f"http://api.chartlyrics.com/apiv1.asmx/GetLyric?lyricId={data['LyricId']}&lyricCheckSum={data['LyricChecksum']}"
    )
    return json.loads(json.dumps(xmltodict.parse(responce.content)))["GetLyricResult"][
        "Lyric"
    ]


@app.route("/music")
def index():
    return render_template("index.html", nic=nic)

@app.route("/artists")
def artists():
    auther = db_sess.query(Author).all()
    for user in db_sess.query(Author).all():
        print(user.name)
    return render_template("artists.html", auther=auther, nic=nic)

@app.route("/charts")
def charts_music():
    pass
    # responce = requests.get(
    #     f"http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country=Russia&api_key=cc197bad-dc9c-440d-a5b5-d52ba2e14234"
    # )
    # return json.loads(json.dumps(xmltodict.parse(responce.content)))


@app.route("/add-music", methods=["POST", "GET"])
def add_music():
    if request.method == "POST":
        file = request.files["file"]

        f = open(
            os.path.join(app.config["CLIENT_SONGS"], f"{request.form['name']}.mp3"),
            "wb+",
        )
        f.close()
        file.save(
            os.path.join(app.config["CLIENT_SONGS"], f"{request.form['name']}.mp3")
        )
        db_sess = db_session.create_session()
        song = Song()
        song.name = request.form["name"]
        song.clip = request.form["clip"]
        song.year = int(request.form["year"])
        for author in request.form["authors"].split(","):
            song.authors.append(
                db_sess.query(Author).filter(Author.name == author.strip()).first()
            )
        song.duration = int(
            MP3(
                os.path.join(app.config["CLIENT_SONGS"], f"{request.form['name']}.mp3")
            ).info.length
        )
        db_sess.add(song)
        db_sess.commit()
    return render_template("add_music.html", nic=nic)


@app.route("/get-song-file/<id>")
def get_song_file(id):
    try:
        return send_from_directory(
            app.config["CLIENT_SONGS"],
            db_sess.query(Song).filter(Song.id == id).first().name + ".mp3",
            as_attachment=True,
        )
    except FileNotFoundError:
        abort(404)


@app.route("/get-song-data/<id>")
def get_song_data(id):
    res = {}
    song = db_sess.query(Song).filter(Song.id == id).first()
    res["authors"] = list(
        map(lambda x: x.author_id, db_sess.query(Link).filter(Link.song_id == id))
    )
    res["year"] = song.year
    res["duration"] = song.duration
    res["name"] = song.name
    return json.dumps(res)


@app.route("/add-artist", methods=["POST", "GET"])
def add_artist():
    if request.method == "GET":
        return render_template("add_artist.html", nic=nic)

@login_required
@app.route('/setting', methods=['GET', 'POST'])
def edit_users():
    global user_email
    form = EditForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        users = db_sess.query(User).filter(User.email == user_email
                                          ).first()
        if users:
            form.name.data = users.name
            form.surname.data = users.surname
            form.nic.data = users.nic
            form.email.data = users.email
            form.password.data = users.password
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        users = db_sess.query(User).filter(User.email == user_email
                                          ).first()
        if users:
            if form.password.data == form.password_again.data:
                users.name = form.name.data
                users.surname = form.surname.data
                users.nic = form.nic.data
                users.email = form.email.data
                users.password = form.password.data
                db_sess.commit()
                return redirect('/music')
            else:
                return render_template('settings.html', title='Настройки',
                                       form=form,
                                       message="Пароли не совпадают", nic=nic)
        else:
            abort(404)
    return render_template('settings.html',
                           title='Настройки',
                           form=form, nic=nic
                           )

def check_user_authorised():
    """Перенаправляет пользователя на страницу входа с сообщением о причине редиректа"""
    if not current_user.is_authenticated:
        session['message'] = 'Зарегистрируйтесь или войдите, чтобы просматривать эту страницу'
        return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == login_form.email.data).first()
        if user and user.check_password(login_form.password.data):
            login_user(user)
            return redirect("/music")
        return render_template('login.html', form=login_form,
                               message='Неверный логин или пароль')
    try:
        message = session['message']
        session.pop('message', None)
        return render_template('login.html', form=login_form,
                               message=message)
    except Exception:
        return render_template('login.html', form=login_form)


@login_required
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    db_session.global_init("db/service.db")
    db_sess = db_session.create_session()
    db_sess.commit()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)