from flask import redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import escape
from config import login_manager, app, db
from models import User, Projet, Article, Celebrity
import os


NB_PROJETS = 3
NB_ARTICLES = 3


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.errorhandler(404)
def page_404(error):
    return render_template("page_404.html"), 404


@app.route("/")
def home():
    return render_template(
        "index.html",
        liste_projets=Projet.query.all()[:NB_PROJETS],
        liste_articles=Article.query.all()[:NB_ARTICLES],
    )


@app.route("/projets/")
@app.route("/projets/<string:slug>")
def projets(slug=""):
    slug = escape(slug)
    if slug:
        projet = Projet.query.filter_by(slug=slug).first_or_404()
        return render_template("projet.html", projet=projet)
    projets = Projet.query.all()
    return render_template("projets.html", liste_projets=projets)


@app.route("/projets/creer", methods=["GET", "POST"])
@login_required
def add_projet():
    if request.method == "POST":
        titre = request.form["titre"]
        slug = request.form["slug"]
        image = request.files["image"]
        contenu = request.form["contenu"]

        image_name = "DOROHEDORO.png"
        if image.filename != "":
            image_name = image.filename
            backend_path = os.path.dirname(os.path.abspath(__file__))
            images_folder_path = os.path.join(
                backend_path, "../frontend/static/images", image_name
            )
            image.save(images_folder_path)

        img_url = f"../static/images/{image_name}"  # only this is send to the database
        # verifie que user est connecte
        projet = Projet(titre=titre, slug=slug, img_url=img_url, contenu=contenu)
        db.session.add(projet)
        db.session.commit()
        return redirect(url_for("projets"))
    return render_template("projet_creation.html")


@app.route("/articles/")
@app.route("/articles/<string:slug>")
def articles(slug=""):
    slug = escape(slug)
    if slug:
        article = Article.query.filter_by(slug=slug).first_or_404()
        return render_template("article.html", article=article)
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("articles.html", liste_articles=articles)


@app.route("/articles/creer", methods=["GET", "POST"])
@login_required
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
@app.route("/celebrites/<string:slug>")
def celebrites(slug=""):
    slug = escape(slug)
    
    if slug:
        celeb = Celebrity.query.filter_by(nom=slug).first_or_404()
        return render_template("celeb.html", celeb=celeb)
    liste_celeb = Celebrity.query.all()
    return render_template("celebs.html", liste_celeb=liste_celeb)


@app.route("/celebrites/creer", methods=["GET", "POST"])
@login_required
def add_celeb():
    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        age = request.form["age"]
        profession = request.form["profession"]
        taille = request.form["taille"]
        Description = request.form["Description"]
        user_id = current_user.id

        # verifie que user est connecte
        celeb = Celebrity(
            nom=nom,
            prenom=prenom,
            age=age,
            profession=profession,
            taille=taille,
            Description=Description,
            user_id = user_id
        )
        db.session.add(celeb)
        db.session.commit()
        return redirect(url_for("celebrites"))
    return render_template("celeb_creation.html")

@app.route("/user")
@login_required
def user():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    return render_template("user.html", user=user)



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))
        return render_template(
            "login.html", message="Your email or password is incorect."
        )
    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method == "POST":
        logout_user()
        return redirect(url_for("home"))


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(
            password, method="pbkdf2:sha1", salt_length=8
        )

        new_user = User(email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/unregister", methods=["POST", "GET"])
@login_required
def unregister():
    if request.method == "POST":
        db.session.delete(current_user)
        db.session.commit()
        logout_user()
        return redirect(url_for("home"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=8000)
