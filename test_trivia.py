import unittest
from trivia_game import Game

class TestTrivia(unittest.TestCase):

    def setUp(self):
        self.g = Game(database_password)

    def test_play_game(self):
