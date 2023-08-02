from pymongo import MongoClient


class MongoDriver:
    def __init__(self, port=27017, db="academicworld"):
        self.client = MongoClient("localhost", port)
        self.db = self.client[db]

    def get_faculty(self, name):
        pipeline = [
            {"$match": {"name": name}},
            {"$project": {"_id": 0, "name": 1, "affiliation.name": 1, "position": 1, "photoUrl": 1}},
            {"$limit": 1}
        ]
        return list(self.db.faculty.aggregate(pipeline))[0]

    def close(self):
        self.client.close()
