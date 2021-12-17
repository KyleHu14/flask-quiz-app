from flask import Blueprint, render_template, request, redirect, url_for 

from flask_quiz_app.extensions import db
from flask_quiz_app.models import Question
from flask_quiz_app.forms import QuestionForm

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def home():
    return render_template('home.html')

@main_routes.route('/question_manager', methods = ['GET', 'POST'])
def question_manager():

    questions = Question.query.all()

    form = QuestionForm()
    if form.validate_on_submit():
        new_question = Question(question_text = form.question_text.data, answer_text = form.answer_text.data)

        db.session.add(new_question)
        db.session.commit()
    
        form.question_text.data, form.answer_text.data = "", ""

        return render_template('question_manager.html', 
            title = 'Question manager', 
            form = form, 
            navbar_title = 'Question manager', 
            questions = Question.query.all()
        )

    return render_template('question_manager.html', 
        title = 'Question manager', 
        form = form, 
        navbar_title = 'Question manager', 
        questions = questions
    )

@main_routes.route('/user', methods = ['GET', 'POST'])
def user():
    all_questions = Question.query.all()

    if request.method == 'POST':
        user_correct = 0
        results_dict = {}

        for question in all_questions:
            user_answer = request.form.get(f'answer{question.id}')
            if user_answer == question.answer_text:
                user_correct += 1
            results_dict = {
                'num_correct' : user_correct,
                'percent_score' : f'{float(user_correct/len(all_questions))*100}%'
            }                

        return render_template('user.html', questions = all_questions, navbar_title = "Questions", results = results_dict)
    return render_template('user.html', questions = all_questions, navbar_title = "Questions")

@main_routes.route('/del_question/<int:question_id>')
def del_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    
    return redirect(url_for('main_routes.question_manager'))

@main_routes.route('/user_manager')
def user_manager():
    return render_template('user_manager.html')