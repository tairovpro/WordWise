from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load questions from a JSON file
def load_questions():
    with open('questions.json') as f:
        return json.load(f)

questions = load_questions()

@app.context_processor
def utility_processor():
    return dict(enumerate=enumerate)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html', questions=questions)

@app.route('/result', methods=['POST'])
def result():
    user_answers = request.form
    score = 0
    for i, question in enumerate(questions):
        if question['answer'] == user_answers.get(f'question_{i}'):
            score += 1
    return render_template('result.html', score=score, total=len(questions))

if __name__ == '__main__':
    app.run(debug=True)

