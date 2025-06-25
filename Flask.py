from flask import Flask, request, render_template
from openai import OpenAI
import os
from config import api_key

# Initialize Flask app and OpenAI client
app = Flask(__name__)
client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
max_tokens = 60

@app.route('/')
def intro():
    return render_template('index.html')

@app.route('/2nd_grade_summary')
def second_grade_summary():
    return render_template('main.html', kind="2nd Grade Summary")

@app.route('/2nd_grade_summary', methods=['POST'])
def second_grade_summary_post():
    user_input = request.form['text']
    prompt = (
        "I rephrased this for my daughter, in plain language a second grader can understand:\n"
        f"{user_input}"
    )
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful text simplifier."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=max_tokens
    )
    
    output = response.choices[0].message.content
    return render_template('main.html', output=output, kind="2nd Grade Summary")

@app.route('/TLDR')
def tldr():
    return render_template('main.html', kind="TL;DR")

@app.route('/TLDR', methods=['POST'])
def tldr_post():
    user_input = request.form['text']
    prompt = f"tl;dr:\n{user_input}"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful text summarizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=max_tokens
    )
    
    output = response.choices[0].message.content
    return render_template('main.html', output=output, kind="TL;DR")

@app.route('/One_Line_Summary')
def one_line():
    return render_template('main.html', kind="One Line Summary")

@app.route('/One_Line_Summary', methods=['POST'])
def one_line_post():
    user_input = request.form['text']
    prompt = f"One-sentence summary:\n{user_input}"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a concise summarizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=max_tokens
    )
    
    output = response.choices[0].message.content
    return render_template('main.html', output=output, kind="One Line Summary")

@app.route('/sheesh', methods=['POST'])
def my_form_post():
    text = request.form['text']
    return text.upper()

@app.route('/experiment')
def experiment():
    return render_template('experiment.html')

@app.route('/experiment', methods=['POST'])
def experiment_post():
    text = request.form['text']
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an experimental AI."},
            {"role": "user", "content": text}
        ],
        temperature=0.7,
        max_tokens=120
    )
    
    experiment_output = response.choices[0].message.content
    return render_template('experiment.html', experiment_output=experiment_output)

if __name__ == '__main__':
    app.run(debug=False)