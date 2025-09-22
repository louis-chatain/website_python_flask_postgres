from datetime import datetime, timezone
from flask_login import UserMixin
from config import db

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


class Celebrity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    age = db.Column(db.SmallInteger)  # would use unsigned TINYINT but sqlite does not support either (0 - 256)
    profession = db.Column(db.String(500))
    taille = db.Column(db.Numeric(5, 2), nullable=False)
    Description = db.Column(db.String(550), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
