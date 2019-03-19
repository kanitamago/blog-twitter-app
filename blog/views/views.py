#Loading app instance created at __init__.py
from blog import app
#Loading should need library in flask
from flask import request, redirect, url_for, render_template, flash, session
from functools import wraps
import random

def login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return inner

@app.route("/login", methods=["GET", "POST"])
def login():
    q = random.sample(range(1, 9999), 1)[0]
    error = None
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"]:
            flash("ログイン失敗")
            return render_template("login.html", error_username="ユーザー名が異なります", error_password="もう一度入力してください", q=q)
        elif request.form["password"] != app.config["PASSWORD"]:
            flash("ログイン失敗")
            return render_template("login.html", correct_username=request.form["username"], error_password="パスワードが異なります", q=q)
        else:
            session["logged_in"] = True
            flash("ログインしました")
            return redirect(url_for("index"))

    return render_template("login.html", q=q)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("ログアウトしました")
    return redirect(url_for("index"))
