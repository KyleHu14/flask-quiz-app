from flask import Flask, render_template, request
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
@app.route('/')
def home():
    return render_template('base.html', navbar_title = 'Home')

@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    form = QuestionForm()
    if form.validate_on_submit():
        new_question = Question(question_text = form.question_text.data, answer_text = form.answer_text.data)

        db.session.add(new_question)
        db.session.commit()
        print('New Question Created')
    
        form.question_text.data, form.answer_text.data = "", ""

    return render_template('admin.html', title = 'Admin Page', form = form, navbar_title = 'Add Question')

@app.route('/user', methods = ['GET', 'POST'])
def user():
    all_questions = Question.query.all()
    if request.method == 'POST':
        user_correct = 0
        for index_id in range(1,len(all_questions)+1):
            user_answer = request.form.get(f'answer{index_id}')
            if user_answer == Question.query.filter_by(id = index_id).first().answer_text:
                user_correct += 1
            results_dict = {
                'num_correct' : user_correct,
                'percent_score' : float(user_correct/len(all_questions))*100
            }
        return render_template('user.html', questions = all_questions, navbar_title = "Questions", results = results_dict)
    return render_template('user.html', questions = all_questions, navbar_title = "Questions")
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