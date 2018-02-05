import logging
import os
import random
import string
import sys
import time

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

mqtt_client = mqtt_json.Client()
is_game_running = False


def parse_command(phone, command):
    """
    Takes in a command input and takes action based on the command. Returns the response message and the bear message.
    """
    ## We need to parse the command
    response_text, bear_message = None

    sanitized_command = command.translate(None, string.punctuation) # Remove punctuation to avoid injection attacks
    command_words = sanitized_command.lower().split(maxplit=2)
    if command_words[0] == 'trivia' and game.counter == -1:
        game.start_game()
        respond_bear("welcome to bear trivia tm")
        response_message = "Let's play trivia!"
    elif game.counter != -1:
        answer = command_words[1:]
        response_message = game.handle_answer(answer)
    return response_message


def check_timeout(orig_time, timeout=45):
    if time.time() - orig_time > timeout:
        return True


def respond_bear(speech):
    mqtt_client.publish(SEND_TOPIC, message=speech)

def respond_text(phone, message):
    """
    Respond to a user via text.
    """
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    client.api.account.messages.create(
        to=phone,  # sic
        from_=PHONE_NUMBER,
        body=message)

@click.command()
@click.option('--reply-text', default='Bear has spoken')
def main(reply_text=None):
    game = Game(DB_PASSWORD)
    timeout_time = time.time()
    logger.setLevel(logging.INFO)
    topic = 'incoming-sms-' + PHONE_NUMBER.strip('+')
    logger.info('Waiting for messages on {}'.format(topic))

    # Essentially functions as a while loop
    for payload in mqtt_client.create_subscription_queue(topic):

        if check_timeout(timeout_time) and game.counter != -1:  # If we hit the timeout for the current question, move to the new one
            respond_bear("Time's up!")
            game.get_next_question()
            timeout_time = time.time()
        if payload is not None:
            text_response = process_message(payload)
            response_number = payload['From']
            respond_text(response_number, text_response)


if __name__ == '__main__':
    main()
