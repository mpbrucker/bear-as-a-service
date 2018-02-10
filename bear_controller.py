import logging
import os
import string
import time
import threading
import urllib.parse as urlparse

import click
from trivia_game import Game
from twilio.rest import Client
import mqtt_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('messages')

SEND_TOPIC = 'speak'

ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', None)
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', None)
PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', None)
DB_PASSWORD = os.environ.get('POSTGRES_KEY', None)
IS_REMOTE = os.environ.get('DATABASE_URL', None)

assert ACCOUNT_SID, 'Error: the TWILIO_ACCOUNT_SID is not set'
assert AUTH_TOKEN, 'Error: the TWILIO_AUTH_TOKEN is not set'
assert PHONE_NUMBER, 'Error: the TWILIO_PHONE_NUMBER is not set'

topic = 'incoming-sms-' + PHONE_NUMBER.strip('+')
if IS_REMOTE:  # If we are deployed to heroku, use remote credentials
    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port
    game = Game(password, database_name=dbname, username=user, port=int(port), hostname=host)
else:
    assert DB_PASSWORD, 'Error: the POSTGRES_KEY is not set'
    game = Game(DB_PASSWORD)
lock = threading.Lock()
mqtt_client = mqtt_json.Client(topic, game.get_question)


def parse_command(number, command, question=0):
    """
    Takes in a command input and takes action based on the command. Returns the text response message.
    """
    # We need to parse the command
    response_message = "I don\'t recognize that command. 🐻"

    translator = str.maketrans('', '', string.punctuation)
    sanitized_command = command.translate(translator)  # Remove punctuation to avoid injection attacks
    command_words = sanitized_command.lower().split(maxsplit=1)
    if command_words[0] == 'trivia' and not game.is_running:  # Start a new game
        game.play_game()
        respond_bear("welcome to bear trivia tm")
        response_message = "Let's play trivia! 🐻"
        next_question()
    elif command_words[0] == 'score':
        response_message = game.score_player(number)
    elif game.is_running and game.get_question() == question: # If the game is running, AND the answer is for the current question:
        answer = command_words[0]
        is_correct, response_message = game.handle_answer(number, answer)
        if is_correct:
            logging.info("Correct answer, moving to next question")
            respond_bear("correct")
            next_question()

    return response_message


def check_timeout(orig_time, timeout=30):
    """
    Checks whether the timeout period for a question has occurred.
    """
    if time.time() - orig_time > timeout:
        return True


def respond_bear(speech):
    """
    Send a message to the bear.
    """
    mqtt_client.publish(SEND_TOPIC, message=speech)


def respond_text(phone, message):
    """
    Respond to a user via text.
    """
    logging.info("Responding to number {}".format(phone))
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    client.api.account.messages.create(
        to=phone,  # sic
        from_=PHONE_NUMBER,
        body=message)


def time_up(timeout, counter):
    """
    A timer function that detects whether the time limit for a given question has passed.
    """
    lock.acquire()
    if game.is_running and game.counter == counter:
        #  If we're still on the same question as when the timer was created:
        respond_bear("Time's up!")
        next_question(timeout)
    else:
        logging.info("Ending timer for question {}".format(counter+1))
    lock.release()


def next_question(timeout=30):
    """
    Moves on to the next question. Handles the resetting of the timer and the processing of the next question.
    """
    respond_bear(game.get_correct_answer) # Say the correct answer
    response_bear_text = game.get_next_question
    respond_bear(response_bear_text)
    timeout_watcher = threading.Timer(timeout, time_up, [timeout, game.counter])
    timeout_watcher.start()



@click.command()
@click.option('--reply-text', default='Bear has spoken')
@click.option('--remote-db', is_flag=True)
def main(reply_text=None, remote_db=False):
    """
    Handles the main control loop of bear interaction.
    """
    logger.setLevel(logging.INFO)
    logger.info('Starting bear trivia client on {}'.format(topic))
    while True:
        payload = mqtt_client.get_messages()
        if payload is not None:  # If there are new messages
            cur_number = payload['From'][-4:] # Store users by last 4 digits of number

            text_response = parse_command(cur_number, payload['Body'], question=payload['QuestionNum'])
            response_number = payload['From']
            respond_text(response_number, text_response)


if __name__ == '__main__':
    main()
