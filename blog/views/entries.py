#Loading app instance created at __init__.py
from blog import app
#Loading should need library in flask
from flask import request, redirect, url_for, render_template, flash, session
#Loading myDatabase for posting articles
from blog.models.entries import Entry
from blog.models.comments import Comment
import random
from blog import db
import easygui
from blog.views.views import login_required

#Default at templates folder
@app.route("/")
def index():
    q = random.sample(range(1, 9999), 1)[0]
    #現在存在しているデータベース内のデータを取得する
    entries = Entry.query.order_by(Entry.id.desc()).all()
    return render_template("entries/index.html", entries=entries, q=q)

@app.route("/post/create", methods=["GET"])
@login_required
def post_menu():
    q = random.sample(range(1, 9999), 1)[0]
    return render_template("entries/post.html", q=q)

@app.route("/post", methods=["POST"])
@login_required
def post():
    entry = Entry(title=request.form["title"], text=request.form["text"], category=request.form["category"])
    db.session.add(entry)
    db.session.commit()
    flash("新しく記事が作成されました")
    return redirect(url_for("index"))

@app.route("/post/<int:id>", methods=["GET"])
def show_entry(id):
    q = random.sample(range(1, 9999), 1)[0]
    entry = Entry.query.get(id)
    comments = Comment.query.order_by(Comment.article_id.desc()).all()
    return render_template("entries/show.html", entry=entry, comments=comments, q=q)

#paging to edit
@app.route("/post/<int:id>/edit", methods=["GET"])
@login_required
def edit(id):
    q = random.sample(range(1, 9999), 1)[0]
    entry = Entry.query.get(id)
    return render_template("entries/edit.html", entry=entry, q=q)

#clicking to edit complete
@app.route("/post/<int:id>/update", methods=["POST"])
@login_required
def update(id):
    entry = Entry.query.get(id)
    entry.title = request.form["title"]
    entry.text = request.form["text"]
    entry.category = request.form["category"]
    entry.update_time()
    db.session.merge(entry)
    db.session.commit()
    flash("記事が更新されました")
    return redirect(url_for("index"))

#clicking to delete button
@app.route("/post/<int:id>/delete", methods=["POST"])
@login_required
def delete(id):
    entry = Entry.query.get(id)
    comments = Comment.query.filter(Comment.article_id == id).all()
    result = easygui.ynbox("本当に記事を削除してよろしいですか？", "確認", ("問題ない", "やっぱやめる"))
    if result:
        for comment in comments:
            db.session.delete(comment)
        db.session.delete(entry)
        db.session.commit()
        flash("記事が削除されました")
        return redirect(url_for('index'))
    else:
        return redirect(url_for('show_entry', id=entry.id))

@app.route("/post/<int:id>/comment", methods=["POST"])
def post_comment(id):
    if request.form["name"] != "":
        comment = Comment(name=request.form["name"], text=request.form["comment"], article_id=id)
        db.session.add(comment)
        db.session.commit()
        flash("コメントが投稿されました")
        return redirect(url_for('show_entry', id=id))
    else:
        comment = Comment(text=request.form["comment"], article_id=id)
        db.session.add(comment)
        db.session.commit()
        flash("名無しとしてコメントが投稿されました")
        return redirect(url_for("show_entry", id=id))

@app.route("/post/<int:id>/comment<int:ci>/delete", methods=["POST"])
@login_required
def delete_comment(id, ci):
    comment = Comment.query.get(ci)
    db.session.delete(comment)
    db.session.commit()
    flash("コメントが削除されました")
    return redirect(url_for("show_entry", id=id))
