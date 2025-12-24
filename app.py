from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
import random

app = Flask(__name__)
app.secret_key = "twoo:3er_uwu_123"
app.permanent_session_lifetime = timedelta(days=7)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
db = SQLAlchemy(app)


class Twoot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(32), nullable=False)
    content = db.Column(db.String(320), nullable=False)
    is_edited = db.Column(db.Boolean, default=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


@app.route("/", methods=["GET"])
def index():
    if "user" in session:
        user = session["user"]
        twoots = Twoot.query.order_by(Twoot.date_created.desc()).all()
        return render_template("index.html", user=user, twoots=twoots)
    else:
        return redirect(url_for("login"))


@app.route("/twoot", methods=["GET", "POST"])
def twoot():
    if request.method == "POST":
        twoot_contents = request.form["content"]
        new_twoot = Twoot(
            content=twoot_contents,
            user=session["user"]
        )
        db.session.add(new_twoot)
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return render_template("twoot.html", user=session["user"])


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    twoot_to_edit = Twoot.query.get_or_404(id)
    if request.method == "POST":
        twoot_to_edit.content = request.form["content"]
        twoot_to_edit.is_edited = True
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", twoot=twoot_to_edit)


@app.route("/delete/<int:id>")
def delete(id):
    twoot_to_del = Twoot.query.get_or_404(id)
    try:
        db.session.delete(twoot_to_del)
        db.session.commit()
        if session["user"] == "fumafuamuf2101":
            return redirect(url_for("admin"))
        return redirect(url_for("index"))
    except:
        return "Failed to delete"


@app.route("/login", methods=["GET", "POST"])
def login():
    suggestion_nm_li = [
        "Goonlord65",
        "xXx_HxNTER K!LLER_xXx",
        "Ladiesman217",
        "Masterbaiter69",
        "Dudeman",
        "Femboy_Slayer_666",
        "Freddy Fazbear"
    ]
    suggestion_nm = random.choice(suggestion_nm_li)
    if request.method == "POST":
        session.permanent = True
        user = request.form["username"]
        session["user"] = user
        return redirect(url_for("index"))
    else:
        if "user" in session:
            return redirect(url_for("index"))
        return render_template("login.html", nm_suggestion=suggestion_nm)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "user" in session:
        if session["user"] == "fumafuamuf2101":
            twoots = Twoot.query.order_by(Twoot.date_created.desc()).all()
            return render_template("admin.html", twoots=twoots)
    return redirect(url_for("index"))


@app.route("/secret", methods=["GET"])
def secret():
    return render_template("secret.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
