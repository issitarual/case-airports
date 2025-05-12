from database import InMemoryDatabase

class UserRepository:
    def __init__(self):
        self.db = InMemoryDatabase()
        self.collection = self.db.get_collection("users")

    def insert(self, data: dict):
        self.collection.insert_one(data)

    def find_by_name(self, name: str):
        return self.collection.find_one({"name": name})

    def find_all(self):
        return [x for x in self.collection.find({}, {"_id": 0})]
