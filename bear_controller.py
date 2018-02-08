import logging
import os
import string
import time
import threading

import click
from trivia_game import Game
from twilio.rest import Client
import mqtt_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('messages')

SEND_TOPIC = 'speak'

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
DB_PASSWORD = os.getenv('POSTGRES_KEY')

assert ACCOUNT_SID, 'Error: the TWILIO_ACCOUNT_SID is not set'
assert AUTH_TOKEN, 'Error: the TWILIO_AUTH_TOKEN is not set'
assert PHONE_NUMBER, 'Error: the TWILIO_PHONE_NUMBER is not set'
assert DB_PASSWORD, 'Error: the POSTGRES_KEY is not set'

topic = 'incoming-sms-' + PHONE_NUMBER.strip('+')
mqtt_client = mqtt_json.Client(topic)
game = Game(DB_PASSWORD)
lock = threading.Lock()



def parse_command(number, command):
    """
    Takes in a command input and takes action based on the command. Returns the text response message.
    """
    ## We need to parse the command
    response_message = "bear has spoken"

    translator = str.maketrans('', '', string.punctuation)
    sanitized_command = command.translate(translator) # Remove punctuation to avoid injection attacks
    command_words = sanitized_command.lower().split(maxsplit=1)
    if command_words[0] == 'trivia' and not game.is_running(): # Start a new game
        game.play_game()
        respond_bear("welcome to bear trivia tm")
        response_message = "Let's play trivia!"
        next_question()
    elif game.is_running():
        answer = command_words[0]
        is_correct, response_message = game.handle_answer(number, answer)
        if is_correct:
            logging.info("Correct answer, moving to next question")
            respond_bear("correct")
            next_question()

    return response_message


def check_timeout(orig_time, timeout=45):
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
    if game.is_running() and game.counter == counter: # If we're still on the same question as when the timer was created:
        respond_bear("Time's up!")
        next_question(timeout)
    else:
        logging.info("Ending timer for question {}".format(counter+1))
    lock.release()


def next_question(timeout=30):
    """
    Moves on to the next question. Handles the resetting of the timer and the processing of the next question.
    """
    response_bear_text = game.get_next_question()
    respond_bear(response_bear_text)
    timeout_watcher = threading.Timer(timeout, time_up, [timeout, game.counter])
    timeout_watcher.start()




@click.command()
@click.option('--reply-text', default='Bear has spoken')
def main(reply_text=None):
    """
    Handles the main control loop of bear interaction.
    """
    logger.setLevel(logging.INFO)
    logger.info('Starting bear trivia client on {}'.format(topic))
    while True:
        payload = mqtt_client.get_messages()
        if payload is not None: # If there are new messages
            text_response = parse_command(payload['From'], payload['Body'])
            response_number = payload['From']
            respond_text(response_number, text_response)




if __name__ == '__main__':
    main()
