import mysql.connector
import pandas as pd


class SQLDriver:

    def __init__(self, user='root', passwd='test_root', database='academicworld'):
        self.cnx = mysql.connector.connect(user=user, passwd=passwd, database=database)
        self.create_publication_year_index()

    def execute_command(self, command, params=None):
        cursor = self.cnx.cursor()
        cursor.execute(command, params)
        return cursor

    def query_to_df(self, query_str, params=None):
        cursor = self.execute_command(query_str, params)
        df = pd.DataFrame(cursor.fetchall(), columns=[x[0] for x in cursor.description])
        return df

    def create_publication_year_index(self):
        command = (
            "SELECT 1 "
            "FROM INFORMATION_SCHEMA.STATISTICS "
            "WHERE INDEX_NAME = 'publication_year'"
        )
        cursor = self.execute_command(command)
        # create index if it doesn't exist
        if not cursor.fetchone():
            command = ("CREATE INDEX publication_year "
                       "ON publication (year)")
            self.execute_command(command)

    def get_popular_keywords(self, n=300):
        query = (
            "SELECT name FROM keyword, publication_keyword "
            "WHERE publication_keyword.keyword_id = id "
            "GROUP BY id "
            "ORDER BY COUNT(*) DESC "
            "LIMIT %s"
        )
        cursor = self.execute_command(query, [n])
        return [x[0] for x in cursor.fetchall()]

    def get_top_n_publications(self, keyword, year_lower, year_upper, n=5):
        create_view = (
            "CREATE OR REPLACE VIEW publication_score AS "
            "SELECT publication.id, publication.title, publication.year, SUM(score*num_citations) AS KRC "
            "FROM publication, publication_keyword AS pk, keyword "
            "WHERE publication.id = pk.publication_Id "
            "AND publication.year <= %s "
            "AND publication.year >= %s "
            "AND keyword.id = pk.keyword_id "
            "AND keyword.name = %s "
            "GROUP BY publication.id ")
        self.execute_command(create_view, [year_upper, year_lower, keyword])

        query = ("SELECT title AS Title, year AS Year, KRC AS Score "
                 "FROM publication_score "
                 "ORDER BY KRC DESC "
                 "LIMIT %s")

        return self.query_to_df(query, [n])

    def get_top_n_faculties(self, n=5):
        create_view = (
            "CREATE OR REPLACE VIEW faculty_score AS "
            "SELECT faculty.id, faculty.name, faculty.university_id, SUM(publication_score.KRC) AS KRC "
            "FROM publication_score, faculty, faculty_publication AS fp "
            "WHERE faculty.id = fp.faculty_Id "
            "AND publication_score.id = fp.publication_Id "
            "GROUP BY faculty.id ")
        self.execute_command(create_view)
        query = ("SELECT faculty_score.name AS Name, university.name AS University, KRC AS Score "
                 "FROM faculty_score, university "
                 "WHERE university.id = faculty_score.university_id "
                 "ORDER BY KRC DESC "
                 "LIMIT %s")
        return self.query_to_df(query, [n])

    def get_top_n_universities(self, n=5):
        create_view = (
            "CREATE OR REPLACE VIEW university_score AS "
            "SELECT university.id, university.name, university.photo_url, SUM(faculty_score.KRC) AS KRC "
            "FROM faculty_score, university "
            "WHERE university.id = faculty_score.university_id "
            "GROUP BY university.id ")
        self.execute_command(create_view)

        query = ("SELECT name AS University, KRC AS Score "
                 "FROM university_score "
                 "ORDER BY KRC DESC "
                 "LIMIT %s")
        return self.query_to_df(query, [n])

