from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from .extensions import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question_text = db.Column(db.String(64))
    answer_text = db.Column(db.String(64))

    def __repr__(self):
        return f'Question : {self.question_text}'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    full_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(100))
    teacher = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return f'User[{self.id}] : {self.username}'

    def gen_hashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)