import psycopg2


class DataSource:
    """DataSource executes all of the queries on the database

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
        pass

    def get_executions_within_age_range(self, startAge, endAge):
        """Returns a list of all of the executions that occurred within the specified age range (inclusive)

        PARAMETERS:
            startAge - the lower end of the age range (inclusive)
            endAge - the upper end of the age range (inclusive)

        RETURN:
            a list of all of the executions that occurred within this age range
        """
        try:
            cursor = self.connection.cursor()
            query = "SELECT	* FROM executions WHERE age BETWEEN " + str(startAge) + " AND " + str(endAge) + " ORDER BY age DESC"
            cursor.execute(query)
            return cursor.fetchall()

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def get_executions_within_year_range(self, startYear, endYear):
        """Returns a list of all of the executions that occurred within the specified year range (inclusive)

        PARAMETERS:
            startYear - the starting year of the range (inclusive)
            endYear - the ending year of the range (inclusive)

        RETURN:
            a list of all of the executions that occurred within this year range.
        """
        try:
            cursor = self.connection.cursor()
            query = "SELECT	* FROM executions WHERE year BETWEEN " + str(startYear) + " AND " + str(endYear) + " ORDER BY year DESC"
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
            query = "SELECT	* FROM executions WHERE state = '" + state + "' ORDER BY state DESC"
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

    def get_executions_by_method_of_execution(self, method):
        """Returns a list of all of the executions that used the specified method

        PARAMETERS:
            method - the method of execution

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


def main():
    """FOR TESTING PURPOSES ONLY

    Attempts to connect to the database using our credentials, then execute the implemented methods
    and print the results.
    """
    # Team credentials
    user = "yeec"
    password = "field429carpet"

    connection = establish_connection(user, password, dbname=user) # dbname=user assumes default database name
    data_source = DataSource(connection)

    # Execute implemented queries, then print successful retrievals (up to 10 items per query)

    results_year = data_source.get_executions_within_year_range(1899, 1900)
    results_state = data_source.get_executions_by_state("Maine")
    results_age = data_source.get_executions_within_age_range(50, 55)

    if results_year is not None:
        print("Query year results: ")
        for item in results_year[:10]:
            print(item)

    if results_state is not None:
        print("Query state results: ")
        for item in results_state[:10]:
            print(item)

    if results_age is not None:
        print("Query age results: ")
        for item in results_age[:10]:
            print(item)

    # Disconnect from database
    connection.close()


def establish_connection(user, password, dbname):
    """Establishes a connection to the database

    PARAMETERS:
        user - username credential for db access
        password - associated password for db access
        dbname - the name of the db to access

    RETURN:
        a psycopg2 connection object
    """
    try:
        connection = psycopg2.connect(dbname=dbname, user=user, password=password)

    except Exception as e:
        print("Connection error: ", e)
        exit(1)

    return connection


main()
