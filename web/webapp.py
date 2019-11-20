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
    display_fields = ds.DB_ENTRY_FIELDS
    search_terms = {field: request.args.get(field) for field in ds.DB_ENTRY_FIELDS}
    field_aliases = ds.DB_FIELD_ALIASES
    unique_values = get_all_unique_values()
    select_fields = []
    input_fields = []
    for field in ds.DB_ENTRY_FIELDS:
        if are_numeric_values(unique_values[field]):
            input_fields.append(field)
        else:
            select_fields.append(field)
    results = get_results(search_terms)
    return render_template('interactor.html', field_aliases=field_aliases,
                           display_fields=display_fields, results=results,
                           input_fields=input_fields, select_fields=select_fields,
                           unique_values=unique_values, search_terms=search_terms)

def get_results(search_terms):
    connection = ds.establish_connection(ds.TEAM_CREDENTIALS)
    data_source = ds.DataSource(connection)
    # TODO: clean this
    results = None
    for field, value in search_terms.items():
        if value is not None and value is not "":
            field_results = data_source.get_executions_by_field(field, value)
            field_results = [result.to_dict() for result in field_results]
            if results is None:
                results = field_results
            else:
                results = [result for result in results if result in field_results]
    connection.close()

    return results if results is not None else []

def get_all_unique_values():
    connection = ds.establish_connection(ds.TEAM_CREDENTIALS)
    data_source = ds.DataSource(connection)
    unique_values = {field: data_source.get_unique_values(field) for field in ds.DB_ENTRY_FIELDS}

    return unique_values

def are_numeric_values(values):
    for value in values:
        if not str(value).isnumeric():
            return False

    return True

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
