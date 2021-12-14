from flask import Blueprint, render_template, request, redirect, url_for 

from flask_quiz_app.extensions import db
from flask_quiz_app.models import Question
from flask_quiz_app.forms import QuestionForm

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def home():
    return render_template('base.html', navbar_title = 'Home')

@main_routes.route('/admin', methods = ['GET', 'POST'])
def admin():
    form = QuestionForm()
    if form.validate_on_submit():
        new_question = Question(question_text = form.question_text.data, answer_text = form.answer_text.data)

        db.session.add(new_question)
        db.session.commit()
        print('New Question Created')
    
        form.question_text.data, form.answer_text.data = "", ""

    return render_template('admin.html', title = 'Admin Page', form = form, navbar_title = 'Add Question')

@main_routes.route('/user', methods = ['GET', 'POST'])
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