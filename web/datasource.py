"""Provides the DataSource class to retrieve information about executions in the United States

Provides methods to retrieve executions information from a specified database

:author: Judi Bush, Luna Yee, Matt Stecklow
"""

import psycopg2


TEAM_CREDENTIALS = {
    "user": "yeec",
    "password": "field429carpet"
}


"""Must be formatted in the same order as the SQL table."""
DB_ENTRY_FIELDS = ["race", "age", "subdivision", "jurisdiction", "crime", "manner",
                   "year", "state", "county", "sex"]

DB_FIELD_ALIASES = { entry: entry.title() for entry in DB_ENTRY_FIELDS }
DB_FIELD_ALIASES.update({
    "subdivision": "Place of Execution",
    "crime": "Crime Committed",
    "manner": "Manner of Execution",
    "county": "County Code"
})


class DataSource:
    """DataSource executes all of the queries on a database of executions in the United States

    It will format the data it sends back to the frontend, usually as an ordered list of the data points.
    """

    def __init__(self, connection):
        """Creates a new DataSource from a psycopg2 connection

        Closing the provided connection will render the DataSource useless.

        PARAMETERS:
            connection - a psycopg2 connection on which to execute queries (see psycopg2 documentation)

        RETURN:
            a new DataSource that will utilize this connection
        """
        self.connection = connection

    def get_unique_values(self, field):
        """Retrieves unique values of a field in the dataset

        PARAMETERS:
            field - the field to search (string-like)

        RETURN:
            a list of all unique elements found for the field
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT DISTINCT " + field + " FROM executions")
            output = cursor.fetchall()
            # SELECT DISTINCT returns a list of 1-length tuples
            values = []
            for value in output:
                values.extend(value)
            values = list(filter(None, values))
            values.sort()

            return values

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def get_executions_by_field_exact(self, field, qualifier):
        """Returns a list of all the executions that exactly fit the qualifier for the field

        PARAMETERS:
            field - the column of the table the query searches
            qualifier - the specific data in the table the query searches for

        Return:
            a list of all the executions that fit the Query
        """
        query = "SELECT * FROM executions WHERE " + field + " = '" + qualifier + "' ORDER BY year DESC"
        return self.execute_query(query)

    def get_executions_by_field_lower_bound(self, field, start):
        """Returns a list of all the executions where the field value >= the start value

        PARAMETERS:
            field - the column of the table the query searches, must be quantifiable
            start - the start value of the range, inclusive

        Return:
            a list of all the executions that fit the Query
        """
        query = "SELECT * FROM executions WHERE " + field + " >= '" + start + "' ORDER BY " + field + " DESC"
        return self.execute_query(query)

    def get_executions_by_field_upper_bound(self, field, end):
        """Returns a list of all the executions where the field value <= the end value

        PARAMETERS:
            field - the column of the table the query searches, must be quantifiable
            end - the end value of the range, inclusive

        Return:
            a list of all the executions that fit the Query
        """
        query = "SELECT * FROM executions WHERE " + field + " <= '" + end + "' ORDER BY " + field + " DESC"
        return self.execute_query(query)

    def execute_query(self, query):
        """Attempts to execute a query on the database.

        PARAMETERS:
            query - the postgreSQL query to search the database with based off of user input

        RETURN:
            None if query fails or finds nothing; or a list of all the executions that fit the query

        NOTES:
            Prints an error report if query fails
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return Execution.convert_to_executions(result)

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None


class Execution:
    """Stores metadata about one execution for retrieval

    These metadata may be retrieved by referencing the instance variables.
    """

    @staticmethod
    def convert_to_executions(db_entry_list):
        """Converts a list of database-formatted tuples to Execution objects

        PARAMETERS:
            db_entry_list - list of tuples, as returned by the database

        RETURN:
            a list of Execution objects created from the above data
        """
        return [Execution(entry) for entry in db_entry_list]

    def __init__(self, db_entry):
        self.metadata = {field : value for field, value in zip(DB_ENTRY_FIELDS, db_entry)}

    def to_dict(self, alias=False):
        """Returns a dict representation of the Execution

        PARAMETERS:
            alias - whether to alias the fields per DB_FIELD_ALIASES

        RETURN:
            a dict of {field(aliased): value} pairs
        """
        execution_dict = self.metadata
        if alias:
            execution_dict = {DB_FIELD_ALIASES[field]: value for field, value in execution_dict.items()}
        return execution_dict

    def get_value_of(self, field):
        """Retrieves the stored value associated with the given field

        PARAMETERS:
            field - string matching one of Execution.DB_ENTRY_FORMAT

        RETURN:
            value for field provided; type may depend on field
        """
        return self.metadata[field]


def establish_connection(credentials, dbname=None):
    """Establishes a connection to the database

    PARAMETERS:
        credentials - dict-like with "user" and "password" properties for validating the connection
        dbname - the name of the db to access if not default (i.e. same as user in credentials)

    RETURN:
        a psycopg2 connection object
    """
    dbname = credentials["user"] if dbname is None else dbname

    try:
        connection = psycopg2.connect(dbname=credentials["user"], user=credentials["user"], password=credentials["password"])

    except Exception as e:
        print("Connection error: ", e)
        exit(1)

    return connection


def main():
    """FOR TESTING PURPOSES ONLY

    Attempts to connect to the database using our credentials, then execute the implemented methods
    and print the results.
    """
    connection = establish_connection(TEAM_CREDENTIALS)
    data_source = DataSource(connection)

    # Disconnect from database
    connection.close()

if __name__ == "__main__":
    main()
