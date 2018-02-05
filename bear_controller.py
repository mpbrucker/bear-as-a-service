import logging
import os
import random
import string
import sys

import click
from twilio.rest import Client
from trivia_game import Game
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

mqtt_client = mqtt_json.Client()
is_game_running = False

class TriviaController():

def process_message(message):
    sent_num = message['From'] # The phone number the message was sent from


def parse_command(phone, command):
    """
    Takes in a command input and takes action based on the command. Returns the response message and the bear message.
    """

    ## We need to parse the command
    response_text, bear_message = None

    sanitized_command = command.translate(None, string.punctuation) # Remove punctuation to avoid injection attacks
    command_words = sanitized_command.lower().split(maxplit=2)
    if command_words[0] == 'trivia' and not is_game_running:
        is_game_running = True
        bear_message = "welcome to bear trivia tm"
        response_message = "Let's play trivia!"
    elif is_game_running and is_answerable:
        answer = command_words[1:]
        response_text = game.handle_answer(answer)




def run_game():
    while True:
        if is_game_running:
            game = Game()

@click.command()
@click.option('--reply-text', default='Bear has spoken')
def main(reply_text=None):
    logger.setLevel(logging.INFO)
    topic = 'incoming-sms-' + PHONE_NUMBER.strip('+')
    logger.info('Waiting for messages on {}'.format(topic))
    for payload in mqtt_client.create_subscription_queue(topic):
        process_message(payload, reply_text=reply_text)


if __name__ == '__main__':
    main()
