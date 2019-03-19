from blog import db
from datetime import datetime

class Entry(db.Model):
    #Created Table(表)
    __tablename__ = "entries_table"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    text = db.Column(db.Text)
    created_at = db.Column(db.String(15))
    update_at = db.Column(db.String(15))
    category = db.Column(db.String(20))

    def __init__(self, title=None, text=None, category="カテゴリなし", update_at=None):
        self.title = title
        self.text = text
        self.created_at = "{0:%Y/%m/%d/ %H:%M:%S}".format(datetime.now())
        self.category = category
        self.update_at = update_at

    def update_time(self):
        self.update_at = "{0:%Y/%m/%d/ %H:%M:%S}".format(datetime.now())

    def __repr__(self):
        return "<Entry id: {} title: {} text: {} created_at: {} category: {}>".format(self.id, self.title, self.text, self.created_at, self.category)
