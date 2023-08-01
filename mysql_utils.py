import mysql.connector
import pandas as pd


class SQLDriver:

    def __init__(self, user='root', passwd='test_root', database='academicworld'):
        self.cnx = mysql.connector.connect(user=user, passwd=passwd, database=database)

    def execute_command(self, command, params=None):
        cursor = self.cnx.cursor()
        cursor.execute(command, params)
        return cursor
    def query_to_df(self, query_str, params=None):
        cursor = self.execute_command(query_str, params)
        df = pd.DataFrame(cursor.fetchall(), columns=[x[0] for x in cursor.description])
        return df
