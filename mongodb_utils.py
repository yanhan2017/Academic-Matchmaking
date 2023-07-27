from pymongo import MongoClient


class MongoDriver:
    def __init__(self, port=27017, db="academicworld"):
        self.client = MongoClient("localhost", port)
        self.db = self.client[db]

    def close(self):
        self.client.close()