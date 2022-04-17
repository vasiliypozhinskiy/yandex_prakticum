from app.core import db


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    testfield = db.Column(db.Text)

    __table_args__ = {"schema": "auth"}
