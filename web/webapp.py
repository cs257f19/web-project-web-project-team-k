from flask import Flask, request, render_template
import json
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text

@app.route('/interactor/')
def interactor():
    results = [
        (30, "Texas", "Murder", "Black", "January"),
        (55, "Florida", "Arson", "White", "January")
    ]
    return render_template('interactor.html', results=results)

@app.route('/about/data/')
def about_data():
    return render_template('about-data.html')

@app.route('/about/project/')
def about_project():
    return render_template('about-project.html')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
