from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_questions(category):
    with open(f'{category}_questions.json') as f:
        return json.load(f)

@app.route('/')
def home():
    return render_template('title.html')

@app.route('/start/<category>')
def start(category):
    session['score'] = 0
    session['question_index'] = 0
    session['category'] = category
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    category = session.get('category')
    questions = load_questions(category)
    question_index = session.get('question_index', 0)
    score = session.get('score', 0)

    if request.method == 'POST':
        selected_answer = request.form.get('answer')
        correct_answer = questions[question_index - 1]['answer']

        if selected_answer == correct_answer:
            session['score'] = score + 1

    if question_index >= len(questions):
        return redirect(url_for('result'))

    question = questions[question_index]
    session['question_index'] = question_index + 1

    return render_template('quiz.html', question=question, question_index=question_index + 1, total_questions=len(questions))

@app.route('/result')
def result():
    score = session.get('score', 0)
    total_questions = len(load_questions(session.get('category')))
    return render_template('result.html', score=score, total_questions=total_questions)

if __name__ == '__main__':
    app.run(debug=True)
