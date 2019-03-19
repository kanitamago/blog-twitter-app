from blog import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = "comments_table"
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer)
    name = db.Column(db.String(15))
    text = db.Column(db.Text)
    created_at = db.Column(db.String(15))

    def __init__(self, name="名無しさん", text=None, article_id=None):
        self.name = name
        self.text = text
        self.created_at = "{0:%Y/%m/%d/ %H:%M:%S}".format(datetime.now())
        self.article_id = article_id
