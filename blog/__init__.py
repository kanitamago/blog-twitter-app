from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#オブジェクトとしてconfigを登録
app.config.from_object("blog.config")

#アプリケーション用のデータベースを定義
db = SQLAlchemy(app)

from blog.views import views, entries, getImage
