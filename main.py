import os
from re import S
from mutagen.mp3 import MP3
from data import db_session
from flask import Flask, render_template, request, url_for, redirect
from flask_login import current_user
from flask import Flask, render_template, session
from data.edit import EditForm
from data.songs import Song
from data.authors import Author
from data.links import Link
from flask import send_from_directory, abort
import xmltodict
from pprint import pprint
import json
import requests
from flask_login import LoginManager, UserMixin,  login_required, login_user, current_user, logout_user

from data.users import User

UPLOAD_FOLDER = "./static/img/"
app = Flask(__name__)
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


@app.route('/', methods=['GET', 'POST'])
def reqister():
    if request.method == "POST":
        global user_email, nic
        if request.form["password"] != request.form["passwordagain"]:
            return render_template('register.html', title='Регистрация',
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == request.form["email"]).first():
            return render_template('register.html', title='Регистрация',
                                   message="Такой пользователь уже есть")
        users = User()
        users.name = request.form["name"]
        users.surname = request.form["surname"]
        users.nic = request.form["nic"]
        users.email = request.form["email"]
        users.password = request.form["password"]
        user_email = request.form["email"]
        nic = request.form["nic"]
        users.set_password(request.form["password"])
        db_sess.add(users)
        db_sess.commit()
        return redirect('/music')
    return render_template("register.html")


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
    global nic
    return render_template("index.html", nic=nic)


@app.route("/add-music", methods=["POST", "GET"])
def add_music():
    global nic
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
    global nic
    if request.method == "GET":
        return render_template("add_artist.html", nic=nic)

# global user_email
#     form = EditForm()
#     if request.method == "GET":
#         db_sess = db_session.create_session()
#         users = db_sess.query(User).filter(User.email == user_email
#                                           ).first()
#         if users:
#             form.name.data = users.name
#             form.surname.data = users.surname
#             form.nic.data = users.nic
#             form.email.data = users.email
#             form.password.data = users.password
#         else:
#             abort(404)
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         users = db_sess.query(User).filter(User.email == user_email
#                                           ).first()
#         if users:
#             if form.password.data == form.password_again.data:
#                 users.name = form.name.data
#                 users.surname = form.surname.data
#                 users.nic = form.nic.data
#                 users.email = form.email.data
#                 users.password = form.password.data
#                 db_sess.commit()
#                 return redirect('/music')
#             else:
#                 return render_template('settings.html', title='Настройки',
#                                        form=form,
#                                        message="Пароли не совпадают")
#         else:
#             abort(404)
#     return render_template('settings.html',
#                            title='Настройки',
#                            form=form
#                            )

@app.route('/setting', methods=['GET', 'POST'])
def edit_news():
    global user_email
    # if request.method == "POST":
    #     db_sess = db_session.create_session()
    #     users = db_sess.query(User).filter(User.email == user_email
    #                                        ).first()
    #     if users:
    #         if request.form["password"] == request.form["passwordagain"]:
    #             users.name = request.form["name"]
    #             users.surname = request.form["surname"]
    #             users.nic = request.form["nic"]
    #             users.email = request.form["email"]
    #             users.password = request.form["email"]
    #             db_sess.commit()
    #             return redirect('/music')
    #         else:
    #             return render_template('settings.html', title='Настройки',
    #                                    message="Пароли не совпадают")
    #     else:
    #         abort(404)
    return render_template('settings.html',
                           title='Настройки', name=request.form["name"], surname=request.form["surname"],
                           nic=request.form["nic"], email=request.form["email"],
                           password=request.form["password"]
                           )

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