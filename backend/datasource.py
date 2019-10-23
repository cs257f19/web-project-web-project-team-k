import psycopg2
import getpass

class DataSource:
	"""DataSource executes all of the queries on the database.

	It also formats the data to send back to the frontend, typically in a list
	or some other collection or object.
	"""

    def __init__(self, connection):
		self.connection = connection

    def get_executions_by_race(self, race):
        """Returns a list of all of the executions on persons of the specified race.

        PARAMETERS:
            race - the race of the executee

        RETURN:
            a list of all of the executions where the person is of the specified race
        """
        return []

    def get_executions_by_age(self, startAge, endAge):
        """Returns a list of all of the executions that occurred within the specified age range (inclusive).

        PARAMETERS:
            startAge - the lower end of the age range
			endAge - the upper end of the age range

        RETURN:
            a list of all of the executions that occurred within the given age range
        """
        try:
			cursor = connection.cursor()
			query = "SELECT	* FROM executions WHERE age > " + str(startAge) + "AND age < " + str(endAge) + " ORDER BY age DESC"
			cursor.execute(query)
			return cursor.fetchall()

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return None

    def get_executions_by_date(self, startDate, endDate):
        """Returns a list of all of the executions that occurred within the range of specified dates.

        PARAMETERS:
            startDate - the starting date of the range
            endDate - the ending date of the range

        RETURN:
            a list of all of the executions that occurred within this date range.
        """
        try:
			cursor = connection.cursor()
			query = "SELECT	* FROM executions WHERE date > " + str(startDate) + "AND date < " + str(endDate) + " ORDER BY date DESC"
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
			cursor = connection.cursor()
			query = "SELECT	* FROM executions WHERE state = " + str(state) + " ORDER BY state DESC"
			cursor.execute(query)
			return cursor.fetchall()

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return None

	def get_executions_by_county(self, state):
		"""Returns a list of all of the executions that occurred in the specified county

        PARAMETERS:
            county - the county of the executions

        RETURN:
            a list of all of the executions that occurred in this county
        """
        return []

	def get_executions_by_crime(self, crime):
		"""Returns a list of all of the executions for the specified crime

        PARAMETERS:
            crime - the crime committed that resulted in execution

        RETURN:
            a list of all of the executions for the crime
        """
        return []

	def get_executions_by_jurisdiction(self, jurisdiction):
		"""Returns a list of all of the executions that occurred in the specified type of jurisdiction

	       PARAMETERS:
	           jurisdiction - the authority under which the execution occurred (state, federal, military, etc.)

	       RETURN:
	           a list of all of the executions that occurred in this type of jurisdiction
       """
       return []

	def get_executions_by_method_of_execution(self, method):
		"""Returns a list of all of the executions that used the spefified method

        PARAMETERS:
            method - the method of execution

        RETURN:
            a list of all of the executions that used this method
        """
        return []

	def get_executions_by_gender(self, gender):
		"""Returns a list of all executions of people of the specified get_executions_by_gender

		PARAMETERS:
			gender - the gender of the executee

		RETURN:
			a list of all the executions of people of the specified gender
		"""
		return []


def establish_connection(user, password, dbname):
	"""Establishes a connection to the database.

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


def main():
	"""FOR TESTING PURPOSES ONLY

	Attempts to connect to the database using our credentials, then execute the implemented methods
	and print the results.
	"""
	# Our credentials
	user = 'yeec'
	password = getpass.getpass()
	port = 5128

	connection = establish_connection(user, password, dbname=user, port=port) # dbname=user assumes default database name
	data_source = DataSource(connection)

	# Execute a simple query: how many earthquakes above the specified magnitude are there in the data?
	results_date = data_source.get_executions_by_date("1800-01-01", "1900-01-01")
	resultsState = data_source.get_executions_by_state(Maine)
	resultsAge = data_source.get_executions_by_age(45, 55)

	if resultDate is not None:
		print("Query date results: ")
		for item in resultsDate:
			print(item)

	if resultsState is not None:
		print("Query state results: ")
		for item in resultsState:
			print(item)

	if resultsAge is not None:
		print("Query age results: ")
		for item in results:
			print(item)

	# Disconnect from database
	connection.close()

main()
