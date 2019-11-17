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
DB_ENTRY_FIELDS = ["race", "age", "place", "jurisdiction", "crime", "manner", "day", "month",
                   "year", "state", "county", "sex"]

DB_FIELD_ALIASES = { entry: entry.title() for entry in DB_ENTRY_FIELDS }
DB_FIELD_ALIASES.update({
    "age": "Age at Execution",
    "place": "Place of Execution",
    "jurisdiction": "Jurisdiction of Execution",
    "crime": "Crime Committed",
    "manner": "Manner of Execution",
    "state": "State of Execution",
    "county": "County of Conviction (Code)"
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

    def get_executions_by_race(self, race):
        """Returns a list of all of the executions on persons of the specified race.

        PARAMETERS:
            race - the race of the executee

        RETURN:
            a list of all of the executions where the person is of the specified race
        """
        race = race.title()
        query = "SELECT * FROM executions WHERE race = '" + race + "' ORDER BY year DESC"
        return self.execute_query(query)

    def get_executions_within_age_range(self, start_age, end_age):
        """Returns a list of all of the executions that occurred within the specified age range (inclusive)

        PARAMETERS:
            start_age - the lower end of the age range (inclusive)
            end_age - the upper end of the age range (inclusive)

        RETURN:
            a list of all of the executions that occurred within this age range
        """
        query = "SELECT * FROM executions WHERE age BETWEEN " + str(start_age) + " AND " + str(end_age) + " ORDER BY age DESC"
        return self.execute_query(query)

    def get_executions_within_year_range(self, start_year, end_year):
        """Returns a list of all of the executions that occurred within the specified year range (inclusive)

        PARAMETERS:
            start_year - the starting year of the range (inclusive)
            end_year - the ending year of the range (inclusive)

        RETURN:
            a list of all of the executions that occurred within this year range.
        """
        query = "SELECT * FROM executions WHERE year BETWEEN " + str(start_year) + " AND " + str(end_year) + " ORDER BY year DESC"
        return self.execute_query(query)

    def get_executions_by_state(self, state):
        """Returns a list of all of the executions that occurred in the specified state

        PARAMETERS:
            state - the state of the executions

        RETURN:
            a list of all of the executions that occurred in this state
        """
        state = state.title()
        query = "SELECT * FROM executions WHERE state = '" + state + "' ORDER BY year DESC"
        return self.execute_query(query)

    def get_executions_by_county_of_conviction(self, county_number):
        """Returns a list of all of the executions where conviction occurred in the specified county

        PARAMETERS:
            county_number - the FIPS code of the county of the executions

        RETURN:
            a list of all of the executions where conviction occurred in this county
        """
        query = "SELECT * FROM executions WHERE county = '" + str(county) + "' ORDER BY year DESC"
        return self.execute_query(query)

    def get_executions_by_crime_committed(self, crime):
        """Returns a list of all of the executions for the specified crime

        PARAMETERS:
            crime - the crime committed that resulted in execution

        RETURN:
            a list of all of the executions for this crime
        """
        crime = crime.title()
        query = "SELECT * FROM executions WHERE crime = '" + crime + "' ORDER BY year DESC"
        return self.execute_query(query)

    def get_executions_by_jurisdiction(self, jurisdiction):
        """Returns a list of all of the executions that occurred in the specified type of jurisdiction

           PARAMETERS:
               jurisdiction - the authority under which the execution occurred (state, federal, military, etc.)

           RETURN:
               a list of all of the executions that occurred in this type of jurisdiction
        """
        jurisdiction = jurisdiction.title()
        query = "SELECT * FROM executions WHERE jurisdiction = '" + jurisdiction + "' ORDER BY year DESC"
        return self.execute_query(query)

    def get_executions_by_manner_of_execution(self, manner):
        """Returns a list of all of the executions that used the specified method

        PARAMETERS:
            manner - the method of execution

        RETURN:
            a list of all of the executions that used this method
        """
        manner = manner.title()
        query = "SELECT * FROM executions WHERE manner = '" + manner + "' ORDER BY year DESC"
        return self.execute_query(query)

    def get_executions_by_sex(self, sex):
        """Returns a list of all executions of people of the specified gender

        PARAMETERS:
            sex - the sex of the executee, i.e. 'male' or 'female'

        RETURN:
            a list of all the executions of people of this gender
        """
        sex = sex.title()
        query = "SELECT * FROM executions WHERE sex = '" + sex + "' ORDER BY year DESC"
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
