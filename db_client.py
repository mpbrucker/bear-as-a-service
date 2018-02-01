from pymongo import MongoClient
import logging

client = MongoClient("mongodb://localhost:27017")


class DatabaseClient():

    def __init__(self, database_name):
        self.db = client[database_name]
        self.users = self.db["users"]
        self.questions = self.db["questions"]

    def add_user(self, phone, points=0, user_name=None):
        """
        Adds a single user to the database. Users are referenced by phone number, and optionally by name.
        """
        attributes = {
            "phone": phone,
            "points": points
        }
        if user_name:
            attributes["name"] = user_name
        res = self.users.insert_one(attributes)
        return "Inserted user ID {0}".format(res.inserted_id)

    def get_points(self, phone):
        """
        Gets the number of points a user has in the database.
        """
        user = self.users.find_one({"phone": phone})
        if user is not None:
            return user["points"]
        else:
            raise TypeError("No user found.")

    def update_user_name(self, phone, name):
        """
        Updates the name corresponding to a certain user.
        """
        user = self.users.find_one({"phone": phone})
        if user is not None:
            self.users.update_one(
                {"phone": phone},
                {
                    "$set": {"name": name}
                }
            )
        else:
            self.add_user(phone, user_name=name)

    def update_user_points(self, phone, points):
        """
        Updates the points of a single user in the database.
        """
        try:
            user_points = self.get_points(phone)
            new_points = user_points + points
        except TypeError:
            self.add_user(phone)
            new_points = points
        try:
            self.users.update_one(
                {"phone": phone},
                {
                    "$set": {"points": new_points}
                })
        except Exception as e:
            logging.info(str(e))
