from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class QuestionForm(FlaskForm):
    question_text = StringField('Question', validators = [DataRequired()])
    answer_text = StringField('Answer', validators = [DataRequired()])
    submit = SubmitField('Create Question')