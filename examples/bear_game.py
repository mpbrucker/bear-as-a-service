import logging
import os
import random
import string
import sys
import time

import click
from twilio.rest import Client
from profanityfilter import ProfanityFilter

sys.path.append(os.path.join(os.path.dirname(__file__), './../scripts'))
from send_mqtt_messages import publish
from receive_mqtt_messages import create_subscription_queue
from db_client import DatabaseClient

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('messages')

SEND_TOPIC = 'speak'

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

assert ACCOUNT_SID, 'Error: the TWILIO_ACCOUNT_SID is not set'
assert AUTH_TOKEN, 'Error: the TWILIO_AUTH_TOKEN is not set'
assert PHONE_NUMBER, 'Error: the TWILIO_PHONE_NUMBER is not set'

REPLY_TEXT = os.getenv('BEAR_REPLY_TEXT') or "The bear has received your message."
UNCLEAN_MESSAGE_REPLY_TEXT = "Hey! That's not very nice. Keep it clean, kids!"

CANNED_SPEECHES = [
    "Come to the Holiday Happening!", "Come take a photo with me at the Holiday Happening!",
    "Did you know that the Holiday Happening is this next Monday at 3PM in the library?",
    "I am very sad inside", "Nothing is real.", "Plus one good timing", "Love equals quantum entanglement",
    "Come to the Holiday Happening for cookies, crafts, friendship, and more",
    "Class of 2020 was a mistake", "Keenan Zucker is hot", "Every one of us is a lab rat but we are also the observer",
    "Numbers matter dates matter numbers are not all the same they are very unique",
    "Thanks everyone for coming I'll be here all week I also do birthday parties and bar mitzvahs",
    "Come give me a hug", "What is your name", "Long live poop monkey"]

pf = ProfanityFilter()

client = DatabaseClient("trivia")

def process_message(message, reply_text=None):
    print(message)
    from_number = message['From']
    message_body = message['Body']

    if pf.is_clean(message_body):
        response_text = parse_command(message_body, from_number)
        # if speech:
        #     publish(SEND_TOPIC, message=speech)
    else:
        response_text = UNCLEAN_MESSAGE_REPLY_TEXT
    if response_text:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        client.api.account.messages.create(
            to=from_number,  # sic
            from_=PHONE_NUMBER,
            body=response_text)


def parse_command(command, sent_number):
    print(command)
    command = ''.join(c for c in command
                      if ord(c) < 128 and c not in string.punctuation)

    words = command.lower().split(maxsplit=2)
    if words[0] in ('speak', 'say'):
        if words[1:]:
            return ' '.join(words[1:])
        else:
            return random.choice(CANNED_SPEECHES)
    # elif words[0] in ('name'):
    #     person_name = ' '.join(words[1:])
    #     names[sent_number] = person_name
    #     coins[sent_number] = 0
    #     return 'Hello ' + person_name
    elif words[0] == 'coins':
        coins_retrieved = 5
        client.update_user_points(sent_number, coins_retrieved)
        curr_coins = client.get_points(sent_number)
        return 'You now have ' + str(curr_coins) + ' coins.'
    else:
        return command.lower()


@click.command()
@click.option('--reply-text', default='Bear has spoken')
def main(reply_text=None):
    logger.setLevel(logging.INFO)
    topic = 'incoming-sms-' + PHONE_NUMBER.strip('+')
    logger.info('Waiting for messages on {}'.format(topic))
    for payload in create_subscription_queue(topic):
        process_message(payload, reply_text=reply_text)


if __name__ == '__main__':
    main()
