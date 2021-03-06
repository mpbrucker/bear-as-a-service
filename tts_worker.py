#!/usr/bin/env python3
import logging
import os
import platform
import subprocess
import sys

import click

sys.path.append(os.path.join(os.path.dirname(__file__), './..'))
import mqtt_json

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('speaker')
logger.setLevel(logging.INFO)


SPEECH_COMMAND = 'say' if platform.system() == 'Darwin' else 'espeak'


@click.command()
@click.option('--topic', default='speak')
def main(topic):
    mqtt_client = mqtt_json.Client(topic)
    while True:
        msg = mqtt_client.get_messages()
        if msg:
            message = msg['message']
            logger.info(msg)
            res = subprocess.run([SPEECH_COMMAND, message],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res.returncode != 0:
                logger.error(res.stderr.decode().strip())


if __name__ == '__main__':
    main()
