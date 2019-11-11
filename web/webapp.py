from flask import Flask, request, render_template
import json
import sys
import datasource as ds

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text

@app.route('/interactor')
def interactor():
    display_fields = ['race', 'age', 'year', 'manner', 'state']
    display_fields = [ds.DB_ENTRY_ALIASES[field] for field in display_fields]
    # display_fields = request.args.get('display')
    # if display_fields is not None:
    #     display_fields = [ds.DB_ENTRY_ALIASES[field] for field in display_fields.split(',')]
    results = []
    race = request.args.get('race')
    if race is not None:
        connection = ds.establish_connection(ds.TEAM_CREDENTIALS)
        data_source = ds.DataSource(connection)
        results = data_source.get_executions_by_race(race)
        results = [result.to_dict() for result in results]
        connection.close()
    return render_template('interactor.html',
                           display_fields=display_fields, results=results)

# @app.route('/interactor', methods = ['POST', 'GET'])
# def interactor():
#     if request.method == 'POST':
#         display_fields = request.form.get('display')
#         print(display_fields)
#         results = []
#         # ds = datasource.DataSource()
#         # description = "Showing all names beginning with " + result.get("Letter") + " sorted alphabetically"
#         # result = ds.getLetter(result.get("Letter"))
#         return render_template('interactor.html', display_fields=display_fields, results=results)
#
#     else:
#         return render_template('interactor.html', display_fields=None, results=[])

@app.route('/about/data')
def about_data():
    return render_template('about-data.html')

@app.route('/about/project')
def about_project():
    return render_template('about-project.html')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
