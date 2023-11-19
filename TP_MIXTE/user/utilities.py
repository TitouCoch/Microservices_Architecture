import json
from datetime import datetime


class UserRepository:

    def __init__(self):
        with open('./data/users.json', "r") as jsf:
            self.users = json.load(jsf)["users"]

    def get_users(self):
        return self.users

    def get_user_by_id(self, userid):
        user = next((user for user in self.users if user["id"] == userid), None)
        return user

    def add_user(self, user):
        user["id"] = user["name"].replace(' ', '_').replace('-', '_').lower()
        user["last_active"] = int(datetime.now().timestamp())
        if self.get_user_by_id(user["id"]) is not None:
            return None
        self.users.append(user)
        self.save()
        return user

    def update_user_name(self, userid, name):
        for user in self.users:
            if str(user["id"]) == str(userid):
                user["name"] = name
                self.save()
                return user
        return None

    def delete_user(self, userid):
        for user in self.users:
            if user["id"] == userid:
                self.users.remove(user)
                self.save()
                return True
        return None

    def save(self):
        with open('./data/users.json', "w") as jsf:
            json.dump({"users": self.users}, jsf)
