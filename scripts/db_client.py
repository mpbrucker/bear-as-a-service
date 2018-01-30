from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')


class DatabaseClient():

    def __init__(self, database_name):
        self.db = client[database_name]
        self.users = self.db['users']
        self.questions = self.db['questions']

    """
    Adds a single user to the database. Users are referenced by phone number, and optionally by name.
    """
    def add_user(self, phone, points=0, user_name=None):
        attributes = {
            'phone': phone,
            'points': points
        }
        if user_name:
            attributes['name'] = user_name
        res = self.users.insert_one(attributes)
        return 'Inserted user ID {0}'.format(res.inserted_id)

    """
    Gets the number of points a user has in the database.
    """
    def get_points(self, phone):
        user = self.users.find_one({'phone': phone})
        return user['points']
