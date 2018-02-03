import sqlalchemy
import logging

class DatabaseClient():

    def __init__(self, database_name, password, username="bearclient", port="5432", hostname="localhost"):
        db_uri = "postgresql://{}:{}@{}:{}/{}".format(username, password, hostname, port, database_name)
        self.db = sqlalchemy.create_engine(db_uri)
        self.db.execute("CREATE TABLE IF NOT EXISTS users (phone text, score smallint)")
    def add_user(self, phone, points=0):
        """
        Adds a single user to the database. Users are referenced by phone number, and optionally by name.
        """
        db_command = "INSERT INTO users (phone, score) VALUES (\'{}\', {})".format(phone, points)
        res = self.db.execute(db_command)
        return res

    def get_points(self, phone):
        """
        Gets the number of points a user has in the database.
        """
        db_command = "SELECT points FROM users WHERE phone=\'{}\'".format(phone)
        result_set = self.db.execute(db_command)
        list_results = [res for res in result_set]
        if len(list_results) == 0:
            raise TypeError("No user found.")
        else:
            return list_results[0][0]

    # def update_user_name(self, phone, name):
    #     """
    #     Updates the name corresponding to a certain user.
    #     """
    #     user = self.users.find_one({"phone": phone})
    #     if user is not None:
    #         self.users.update_one(
    #             {"phone": phone},
    #             {
    #                 "$set": {"name": name}
    #             }
    #         )
    #     else:
    #         self.add_user(phone, user_name=name)

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
