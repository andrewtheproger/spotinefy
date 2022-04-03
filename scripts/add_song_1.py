import os
from data import db_session
from flask import Flask, render_template, request, url_for, redirect
from data.songs import Song
from data.authors import Author
from flask import send_file, send_from_directory, safe_join, abort
import xmltodict
from pprint import pprint
import json
import requests

UPLOAD_FOLDER = "./static/img/"
app = Flask(__name__)

if __name__ == "__main__":
    db_session.global_init('db/service.db')
    db_sess = db_session.create_session()
    author1 = Author()
    author1.name = "2pac"
    author1.photo = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fnote-store.com%2" \
                    "Fupload%2Fresize_cache%2Fiblock%2F037%2F325_380_2%2F2Pac.png&f=1&nofb=1"
    db_sess.add(author1)
    author2 = Author()
    author2.name = "Roger Troutman"
    author2.photo = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fd4q8jbdc3dbnf.clo" \
                    "udfront.net%2Fartist%2F34ef1d8808fe6119188aceb029d0b423.jpg&f=1&nofb=1"
    db_sess.add(author2)
    author3 = Author()
    author3.name = "Dr. Dre"
    author3.photo = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimg.europapress.e" \
                    "s%2Ffotoweb%2Ffotonoticia_20160215180004_1280.jpg&f=1&nofb=1"
    db_sess.add(author3)
    db_sess.commit()
    db_session.global_init('db/service.db')
    db_sess = db_session.create_session()
    song = Song()
    song.name = "California love"
    song.duration = 285
    song.clip = "https://www.youtube.com/watch?v=mwgZalAFNhM"
    song.year = 1995
    song.authors.append(author1)
    song.authors.append(author2)
    song.authors.append(author3)
    db_sess.add(song)
    db_sess.commit()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
