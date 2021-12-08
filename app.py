from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

@app.route('/')
def survey_start():
    return render_template('base.html', title=survey.title, instructions=survey.instructions)

@app.route('/begin', methods=["POST"])
def begin_survey():
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')

@app.route('/questions/<int:qid>')
def show_questions(qid):
    responses = session.get(RESPONSES_KEY)

    question = survey.questions[qid]

    if (responses is None):
        return redirect('/')
    
    if (len(responses) == len(survey.questions)):
        return redirect('/thankyou')
    
    if (len(responses) != qid):
        flash(f"Invalid Question ID: {qid}")
        return redirect(f'/questions/{len(responses)}')

    return render_template('questions.html', question_num=qid, question=question)

@app.route('/answer', methods=["POST"])
def collect_answer():
    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if len(responses) == len(survey.questions):
        return redirect('/thankyou')

    return redirect(f"/questions/{len(responses)}")

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')
