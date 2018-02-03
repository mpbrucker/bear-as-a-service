import requests
import json
from random import shuffle

class Game(object):

    def __init__(self):
        self.questions = []
        self.num_questions = 2
        self.counter = 0
        self.players = dict()

    def play_game(self):
        """
        Cycles through a round of questions
        """
        self.get_name()
        self.grab_questions()
        for n in range(self.num_questions):
            answers = self.ask_question()
            self.handle_answer('Isa', answers)
            self.counter += 1
            print('\n\n')
        self.end_game()

    def get_name(self):
        name = input('Hi! My name is Bear. What is yours? ')
        self.players[name] = 0
        print(self.players)

    def grab_questions(self):
        """
        Grabs trivia json from Open Trivia DB API tool
        """
        r = requests.get("https://opentdb.com/api.php?amount=%d&type=multiple" % self.num_questions)
        self.questions = r.json()['results']
        self.sort_questions()

    def sort_questions(self):
        """
        Sorts questions by difficulty
        """
        easy = [q for q in self.questions if q['difficulty'] == 'easy']
        medium = [q for q in self.questions if q['difficulty'] == 'medium']
        hard = [q for q in self.questions if q['difficulty'] == 'hard']
        self.questions = easy + medium + hard


    def ask_question(self):
        """
        Prints question out to command line
        """
        current_question = self.questions[self.counter]['question']
        answers = self.questions[self.counter]['incorrect_answers'] + [(self.questions[self.counter]['correct_answer'])]
        shuffle(answers)
        print(current_question)
        for i, ans in enumerate(answers):
            print("%d: %s" % (i+1, ans))
        return(answers)

    def handle_answer(self, user, answers):
        """
        Handles user input on the command line
        """
        user_answer = input('Type the number to the answer here: ')
        if user_answer not in ['1','2','3','4']:
            print('That is not a number between 1 and 4')
            self.handle_answer(user, answers)
        elif answers[int(user_answer)-1] == self.questions[self.counter]['correct_answer']:
            print('Yay!  That is correct!')
            self.add_point(user)
        else:
            print('Boooooo you suck! The correct answer was "%s"' % self.questions[self.counter]['correct_answer'])


    def add_point(self, user):
        """
        Add one point to a player's score
        """
        self.players[user] += 1
        print(self.players)

    def end_game(self):
        """
        Say thanks for playing and read off scores
        """
        print('Thanks for playing!')
        for name in self.players:
            print('%s, you scored %d points. Good job!' % (name, self.players[name]))


def main():
    g = Game()
    g.play_game()

if __name__ == '__main__':
    main()
