import logging
import os
import random
import string
import sys

import click
from twilio.rest import Client
import mqtt_json

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('messages')

SEND_TOPIC = 'speak'

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

assert ACCOUNT_SID, 'Error: the TWILIO_ACCOUNT_SID is not set'
assert AUTH_TOKEN, 'Error: the TWILIO_AUTH_TOKEN is not set'
assert PHONE_NUMBER, 'Error: the TWILIO_PHONE_NUMBER is not set'

mqtt_client = mqtt_json.Client()
is_game_running = False



def process_message(message):



def parse_command(command):
    """
    Takes in a command input and takes action based on the command. Returns the response message and the bear message.
    """

    ## We need to parse the command
    response_text, bear_message = None

    command_words = command.lower().split(maxplit=2)
    if words[0] == 'trivia':
        is_game_running = True
        bear_message = "welcome to bear trivia tm"





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
