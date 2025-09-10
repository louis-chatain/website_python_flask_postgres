from flask import Flask, redirect, render_template, request, url_for
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timezone
from donnees import donnees
from bdd_articles import liste_articles
from bdd_projets import liste_projets
import os

NB_PROJETS = 3
NB_ARTICLES = 3
IMG_UPLOAD = "static/images/"

app = Flask(__name__)

# ---------------------- DATABASE -------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_51.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(150))
    slug = db.Column(db.String(150))
    contenu = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc))


class Projet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(150))
    slug = db.Column(db.String(150))
    img_url = db.Column(db.String(100))
    contenu = db.Column(db.Text)
# ------------------------ END DATABASE --------------------------

@app.errorhandler(404)
def page_404(error):
    # print(error)
    return render_template("page_404.html"), 404


@app.route("/")
def home():
    return render_template(
        "index.html",
        liste_projets=Projet.query.all()[:NB_PROJETS],
        liste_articles=Article.query.all()[:NB_ARTICLES]
    )


@app.route("/projets/")
@app.route("/projets/<string:slug>")
def projets(slug=""):
    if slug:
        projet = Projet.query.filter_by(slug=slug).first_or_404()
        return render_template("projet.html", projet=projet)
    projets = Projet.query.all()
    return render_template("projets.html", liste_projets=projets)


@app.route("/projets/creer", methods=["GET", "POST"])
def add_projet():
    if request.method == "POST":
        titre = request.form["titre"]
        slug = request.form["slug"]
        img_url = request.files["image"]
        contenu = request.form["contenu"]

        image_url = "/static/images/DOROHEDORO.png"
        if img_url.filename != "":
            image_url = f"/static/images/{img_url.filename}"
            img_url.save(os.path.join(IMG_UPLOAD, img_url.filename))
        # verifie que user est connecte
        projet = Projet(titre=titre, slug=slug, img_url=image_url, contenu=contenu)
        db.session.add(projet)
        db.session.commit()
        return redirect(url_for("projets"))
    return render_template("projet_creation.html")


@app.route("/articles/")
@app.route("/articles/<string:slug>")
def articles(slug=""):
    if slug:
        article = Article.query.filter_by(slug=slug).first_or_404()
        return render_template("article.html", article=article)       
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("articles.html", liste_articles=articles)


@app.route("/articles/creer", methods=["GET", "POST"])
def creation_article():
    if request.method == "POST":
        titre = request.form["titre"]
        slug = request.form["slug"]
        contenu = request.form["contenu"]
        # verifie que user est connecte
        article = Article(titre=titre, slug=slug, contenu=contenu)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("articles"))
    return render_template("creation_article.html")


@app.route("/celebrites")
def celebrites():
    return render_template("celeb.html", donnees=donnees)


@app.route("/celebrites/api/<string:slug>")
def celebrite(slug):
    slug = escape(slug)
    if slug in donnees:
        return donnees[slug]
    else:
        return {"erreur": "non existant"}, 404


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username, password)
        return redirect(url_for("home"))
    else:
        return render_template("login.html")


@app.route("/jinja")
def jinja():
    return render_template(
        "jinja.html",
        name="louis",
        show=True,
        users=["patate", "momo", "mina", "dilcu", "ochako"],
    )
