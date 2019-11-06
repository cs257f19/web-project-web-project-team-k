"""Provides the DataSource class to retrieve information about executions in the United States

Provides methods to retrieve executions information from a specified database

:author: Judi Bush, Luna Yee, Matt Stecklow
"""

import psycopg2


TEAM_CREDENTIALS = {
    "user": "yeec",
    "password": "field429carpet"
}


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

    def get_executions_by_race(self, race):
        """Returns a list of all of the executions on persons of the specified race.

        PARAMETERS:
            race - the race of the executee

        RETURN:
            a list of all of the executions where the person is of the specified race
        """
        race = race.title()
        query = "SELECT * FROM executions WHERE race = '" + race + "' ORDER BY race DESC"
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
            if len(result) == 0:
                return None
            return result

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None


    def get_executions_within_age_range(self, start_age, end_age):
        """Returns a list of all of the executions that occurred within the specified age range (inclusive)

        PARAMETERS:
            start_age - the lower end of the age range (inclusive)
            end_age - the upper end of the age range (inclusive)

        RETURN:
            a list of all of the executions that occurred within this age range
        """
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM executions WHERE age BETWEEN " + str(start_age) + " AND " + str(end_age) + " ORDER BY age DESC"
            cursor.execute(query)
            return cursor.fetchall()

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def get_executions_within_year_range(self, start_year, end_year):
        """Returns a list of all of the executions that occurred within the specified year range (inclusive)

        PARAMETERS:
            start_year - the starting year of the range (inclusive)
            end_year - the ending year of the range (inclusive)

        RETURN:
            a list of all of the executions that occurred within this year range.
        """
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM executions WHERE year BETWEEN " + str(start_year) + " AND " + str(end_year) + " ORDER BY year DESC"
            cursor.execute(query)
            return cursor.fetchall()

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def get_executions_by_state(self, state):
        """Returns a list of all of the executions that occurred in the specified state

        PARAMETERS:
            state - the state of the executions

        RETURN:
            a list of all of the executions that occurred in this state
        """
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM executions WHERE state = '" + state + "' ORDER BY state DESC"
            cursor.execute(query)
            return cursor.fetchall()

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def get_executions_by_county_of_conviction(self, county_number):
        """Returns a list of all of the executions where conviction occurred in the specified county

        PARAMETERS:
            county_number - the FIPS code of the county of the executions

        RETURN:
            a list of all of the executions where conviction occurred in this county
        """
        pass

    def get_executions_by_crime_committed(self, crime):
        """Returns a list of all of the executions for the specified crime

        PARAMETERS:
            crime - the crime committed that resulted in execution

        RETURN:
            a list of all of the executions for this crime
        """
        pass

    def get_executions_by_jurisdiction(self, jurisdiction):
        """Returns a list of all of the executions that occurred in the specified type of jurisdiction

           PARAMETERS:
               jurisdiction - the authority under which the execution occurred (state, federal, military, etc.)

           RETURN:
               a list of all of the executions that occurred in this type of jurisdiction
        """
        pass

    def get_executions_by_manner_of_execution(self, manner):
        """Returns a list of all of the executions that used the specified method

        PARAMETERS:
            manner - the method of execution

        RETURN:
            a list of all of the executions that used this method
        """
        pass

    def get_executions_by_sex(self, sex):
        """Returns a list of all executions of people of the specified gender

        PARAMETERS:
            sex - the sex of the executee, i.e. 'male' or 'female'

        RETURN:
            a list of all the executions of people of this gender
        """
        pass


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

    # Execute implemented queries, then print successful retrievals (up to 10 items per query)

    results_year = data_source.get_executions_within_year_range(1899, 1900)
    results_state = data_source.get_executions_by_state("Maine")
    results_age = data_source.get_executions_within_age_range(50, 55)

    if results_year is not None:
        print("Query year results: ")
        print(len(results_year))
        print(type(results_year))
        for item in results_year[:10]:
            print(item)

    if results_state is not None:
        print("Query state results: ")
        print(len(results_state))
        print(type(results_age))
        for item in results_state[:10]:
            print(item)

    if results_age is not None:
        print("Query age results: ")
        print(len(results_age))
        print(type(results_age))
        for item in results_age[:10]:
            print(item)

    # Disconnect from database
    connection.close()


if __name__ == "__main__":
    main()
