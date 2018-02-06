import requests
import json
from random import shuffle
from db_client import DatabaseClient
import html

class Game(object):

    def __init__(self, database_password, database_name="trivia"):
        self.questions = []
        self.num_questions = 10
        self.counter = -1
        self.players = dict()
        self.answers = []
        self.db = DatabaseClient(database_name, database_password)

    def play_game(self):
        """
        Grabs and sorts questions
        """
        self.grab_questions()
        self.sort_questions()

    def add_player(self, number):
        """
        Adds a new player to the players dictionary and give them a score of 0
        """
        self.players[number] = 0

    def grab_questions(self):
        """
        Grabs trivia json from Open Trivia DB API tool
        """
        r = requests.get("https://opentdb.com/api.php?amount=%d&type=multiple" % self.num_questions)
        self.questions = r.json()['results']

    def sort_questions(self):
        """
        Sorts questions by difficulty
        """
        easy = [q for q in self.questions if q['difficulty'] == 'easy']
        medium = [q for q in self.questions if q['difficulty'] == 'medium']
        hard = [q for q in self.questions if q['difficulty'] == 'hard']
        self.questions = easy + medium + hard

    def get_next_question(self):
        """
        Returns current question and answers
        """
        self.counter += 1
        current_question = self.questions[self.counter]['question']
        self.answers = self.questions[self.counter]['incorrect_answers'] + [(self.questions[self.counter]['correct_answer'])]
        shuffle(self.answers)
        answers_string = ', '.join(["%d: %s" % (n+1, q) for n, q in enumerate(self.answers)])
        return html.unescape(current_question + ' ' + answers_string)

    def handle_answer(self, number, answer):
        """
        Returns string saying whether you were right or not

            Arguments:
            number: string, represents the user's phone number
            answer: string, the user's answer

        """
        is_correct = False
        response_message = ""

        if number not in list(self.players.keys()):
            self.add_player(number)
        if answer not in ['1','2','3','4']:
            response_message = 'That is not a number between 1 and 4'
        elif self.answers[int(answer)-1] == self.questions[self.counter]['correct_answer']:
            self.add_point(number)
            response_message = 'Yay! That is correct!'
            is_correct = True
        else:
            response_message = 'Aw that was wrong!'
        return (is_correct, response_message)

    def add_point(self, number):
        """
        Add one point to a player's score
        """
        self.players[number] += 1
        self.db.update_user_points(number, 1)

    def score_player(self, number):
        """
        Return a string telling a certain player their score
        """
        return('You scored %d points. Good job!' % (self.players[number]))

    def end_game(self):
        """
        Clear game and return thanks for playing
        """
        self.__init__()
        return('Thanks for playing!')
