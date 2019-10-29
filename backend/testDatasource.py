import unittest
from datasource import *


class DataSourceTester(unittest.TestCase):

    def setUp(self):
        connection = establish_connection(TEAM_CREDENTIALS)
        self.data_source = DataSource(connection)

    def test_race_expected(self):
        race_expected_results = self.data_source.get_executions_by_race("White")
        # 173 is the number of those with race: "White" in the database
        self.assertEqual(len(race_expected_results), 173)

    def test_race_native_american(self):
        race_native_american_results = self.data_source.get_executions_by_race("Native American")
        # 52 is the number of those with race: "Native American" in the database
        self.assertEqual(len(race_native_american_results), 52)

    def test_race_capitalization(self):
        race_lowercase_results = self.data_source.get_executions_by_race("wHiTe")
        # 173 is the number of those with race: "White" in the database
        self.assertEqual(len(race_lowercase_results), 173)

    def test_race_invalid_string(self):
        race_invalid_string_results = self.data_source.get_executions_by_race("banana")
        self.assertIsNone(race_invalid_string_results)

    def test_race_not_string(self):
        race_not_string_results = self.data_source.get_executions_by_race("22")
        self.assertIsNone(race_not_string_results)


if __name__ == '__main__':
    unittest.main()
