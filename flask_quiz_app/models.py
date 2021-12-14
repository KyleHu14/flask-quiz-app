from .extensions import db
class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question_text = db.Column(db.String(64))
    answer_text = db.Column(db.String(64))

    def __repr__(self):
        return f'Question : {self.question_text}'