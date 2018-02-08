import requests
from random import shuffle
from db_client import DatabaseClient
import html


class Game(object):

<<<<<<< HEAD
    def __init__(self, database_password, database_name="trivia"):
        """
        :param database_password: password found in bear-secrets.txt
        :param database_name: name of database
        """

        self.counter = -1  # Current round number, -1 means game has not started
        self.db = DatabaseClient(database_name, database_password)  # Setup database
=======
    def __init__(self, database_password, database_name="trivia", **kwargs):
        self.counter = -1 # Current round number, -1 means game has not started
        self.db = DatabaseClient(database_name, database_password, *kwargs) # Setup database
>>>>>>> 9d77ef7354a3fc0ee2be95e1fb7e5c26901124d7

    def play_game(self):
        """
        Calls functions needed to prep game
        """

        self.questions = []
        self.num_questions = 10
        self.players = dict()  # Keys = players' numbers, values = points
        self.answers = []  # List of answers to the current question
        self.answered = []  # List of players that have answered in the current round
        self.grab_questions()
        self.sort_questions()

    def add_player(self, number):
        """
        Adds a new player to dictionary and give them a score of 0

        :param number: player id
        """

        self.players[number] = 0

    def grab_questions(self):
        """
        Grabs trivia json from Open Trivia DB API tool
        """

        r = requests.get("https://opentdb.com/api.php?amount=%d&category=9&type=multiple" % self.num_questions)
        self.questions = r.json()['results']

    def sort_questions(self):
        """
        Sorts questions by difficulty
        """

        easy = [q for q in self.questions if q['difficulty'] == 'easy']
        medium = [q for q in self.questions if q['difficulty'] == 'medium']
        hard = [q for q in self.questions if q['difficulty'] == 'hard']
        self.questions = easy + medium + hard

    @property
    def get_next_question(self):
        """
        Returns current question and answers

        :return: the current question and its answers
        :rtype: str
        """

        self.answered = []  # Reset the list of who has answered
        self.counter += 1  # Increase counter to next question
        if self.counter >= self.num_questions:  # If we are at the end of the questions
            return self.end_game
        current_question = self.questions[self.counter]['question']
        self.answers = self.questions[self.counter]['incorrect_answers'] + \
            [(self.questions[self.counter]['correct_answer'])]
        shuffle(self.answers)
        answers_string = ', '.join(["%d: %s" % (n+1, q) for n, q in enumerate(self.answers)])
        return html.unescape("question " + str(self.counter+1) + '. ' + current_question + ' ' + answers_string)

    @property
    def get_correct_answer(self):
        """
        Formats a string that gives the current question's correct answer

        :return: correct answer string
        :rtype: str
        """

        return "The correct answer is {}".format(self.questions[self.counter]['correct_answer'])

    def handle_answer(self, number, answer):
        """
        Check a player's answer and respond

        :param number: string, represents the user's phone number
        :param answer: string, the user's answer
        :return: Message saying whether the player was right
        :rtype: bool, str
        """

        is_correct = False
        response_message = ""

        if number in self.answered:
            return False, "Your answer has already been recorded for this round"

        self.answered.append(number)
        if number not in list(self.players.keys()):
            self.add_player(number)
        if answer not in ['1', '2', '3', '4']:
            response_message = 'That is not a number between 1 and 4'
        elif self.answers[int(answer)-1] == self.questions[self.counter]['correct_answer']:
            self.add_point(number)
            response_message = 'Yay! That is correct!'
            is_correct = True
        else:
            response_message = 'Aw that was wrong!'
        return is_correct, response_message

    def add_point(self, number):
        """
        Add one point to a player's score

        :param number: player id
        """

        self.players[number] += 1
        self.db.update_user_points(number, 1)

    def score_player(self, number):
        """
        Update a player's score

        :param number: player id
        :return: Number of points the user has
        :rtype: str
        """

        cur_points = self.db.get_points(number)
        if cur_points != 1:
            return 'You have {} points.'.format(cur_points)
        else:
            return 'You have 1 point.'

    @property
    def is_running(self):
        """
        Checks if the game is running

        :return: whether game is running
        :rtype: bool
        """
        return self.counter != -1

    @property
    def end_game(self):
        """
        Clear game and thank players.

        :return: thanks message
        :rtype: str
        """

        self.counter = -1  # Current round number, -1 means game has not started
        return 'And that does it for trivia! Thanks for playing!'
