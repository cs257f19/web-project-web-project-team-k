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
    ordinal_fields = ['year', 'age', 'state']
    # Protect from unexpected search terms
    search_terms = request.args
    field_aliases = ds.DB_FIELD_ALIASES
    unique_values = get_all_unique_values()
    select_fields = []
    input_fields = []
    range_fields = []
    for field in ds.DB_ENTRY_FIELDS:
        if are_numeric_values(unique_values[field]):
            input_fields.append(field) if field not in ordinal_fields else range_fields.append(field)
        else:
            select_fields.append(field)
    results = get_results(search_terms)
    return render_template('interactor.html', search_terms=search_terms,
                           field_aliases=field_aliases, display_fields=display_fields,
                           results=results, input_fields=input_fields,
                           select_fields=select_fields, range_fields=range_fields,
                           ordinal_fields=ordinal_fields,
                           unique_values=unique_values)


def get_results(search_terms):
    connection = ds.establish_connection(ds.TEAM_CREDENTIALS)
    data_source = ds.DataSource(connection)
    results = None

    order_by = search_terms.get('order')
    # Protect from unexpected query terms
    search_terms = {field: value for field, value in search_terms.items() if is_valid_field(field)}
    for search_term in search_terms.items():
        field_results = get_field_results(data_source, search_term)
        if field_results is None:
            continue
        # If multiple search terms, get intersection
        if results is None:
            results = field_results
        else:
            results = [result for result in results if result in field_results]

    connection.close()

    if results is None:
        return []
    elif order_by is not None:
        sort_results_by_field(results, order_by)

    return results




def get_field_results(data_source, search_term):
    field, value = search_term
    if value is None or value == "":
        return None

    if field.find("!") != -1:
        # Allow start and end terms
        field, bound = field.split("!", 1)
        if bound.lower() == "start":
            field_results = data_source.get_executions_by_field_lower_bound(field, value)
        elif bound.lower() == "end":
            field_results = data_source.get_executions_by_field_upper_bound(field, value)
        else:
            return None
    else:
        field_results = data_source.get_executions_by_field_exact(field, value)

    return [field_result.to_dict() for field_result in field_results]


def get_all_unique_values():
    connection = ds.establish_connection(ds.TEAM_CREDENTIALS)
    data_source = ds.DataSource(connection)
    unique_values = {field: data_source.get_unique_values(field) for field in ds.DB_ENTRY_FIELDS}
    connection.close()

    return unique_values


def is_valid_field(field):
    # Get field name (before bang delim)
    field = field.split("!", 1)[0]
    return field in ds.DB_ENTRY_FIELDS


def are_numeric_values(values):
    for value in values:
        if not str(value).isnumeric():
            return False

    return True


def sort_results_by_field(results, field):
    results.sort(key=lambda result: result[field])


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
