from flask import Flask, request, render_template
import json
import sys
import datasource as ds

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/interactor')
def interactor():
    display_fields = ['race', 'age', 'year', 'manner', 'state']
    display_fields = [ds.DB_FIELD_ALIASES[field] for field in display_fields]
    race = request.args.get('race')
    all_fields = ds.DB_ENTRY_FIELDS
    unique_values = get_all_unique_values()
    results = get_results_from_race(race) if race is not None else []
    return render_template('interactor.html',
                           display_fields=display_fields, results=results,
                           all_fields=all_fields, unique_values=unique_values)

def get_results_from_race(race):
    connection = ds.establish_connection(ds.TEAM_CREDENTIALS)
    data_source = ds.DataSource(connection)
    results = data_source.get_executions_by_race(race)
    results = [result.to_dict() for result in results]
    connection.close()

    return results

def get_all_unique_values():
    connection = ds.establish_connection(ds.TEAM_CREDENTIALS)
    data_source = ds.DataSource(connection)
    unique_values = {field: data_source.get_unique_values(field) for field in ds.DB_ENTRY_FIELDS}
    return unique_values

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
