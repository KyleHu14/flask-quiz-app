from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# [START Initialization]
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# [END Initialization]

# [START Views]
@app.route('/admin')
def admin():
    return render_template('admin.html')
# [END Views]

# [START Forms]
class QuestionForm(FlaskForm):
    question_text = StringField('Question', validators = [DataRequired()])
    answer_text = StringField('Answer', validators = [DataRequired()])
    submit = SubmitField('Create Question')
# [END Forms]

# [START Models]
class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question_text = db.Column(db.String(64))
    answer_text = db.Column(db.String(64))

    def __repr__(self):
        return f'Question : {self.question_text}'
# [END Models]

if __name__ == '__main__':
    app.run(debug=True)