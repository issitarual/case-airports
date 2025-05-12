from repositories.user import UserRepository

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def insert_user(self, data: dict):
        self.repo.insert(data)
        return {"status": "ok"}

    def get_user(self, name: str):
        return {"status": "ok", "user": self.repo.find_by_name(name)}

    def list_users(self):
        return {"status": "ok", "users": self.repo.find_all()}
