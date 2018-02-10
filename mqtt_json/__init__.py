import json
import logging
import socket
import sys
import queue

import paho.mqtt.client as mqtt
from .mqtt_config import config
import paho.mqtt.publish as mqtt_publish


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('messages')


class Client():
    def __init__(self, topic, counter):
        self.messages = queue.Queue()
        self.client = self.create_client(topic, counter)

    def create_client(self, topic, counter):
        """
        Builds an MQTT client. Subscribes the MQTT client to a given topic, and directs messages to self.messages
        """
        def on_connect(client, userdata, flags, rc):
            logger.info('connected result code=%s', str(rc))
            logger.info('subscribe topic=%s', topic)
            client.subscribe(topic, 0)

        def on_log(client, userdata, level, string):
            logger.info('log %s %s', level, string)

        def on_message(client, userdata, msg):
            logger.info('message topic=%s timestamp=%s payload=%s', msg.topic, msg.timestamp, msg.payload)
            self.messages.put((msg, counter())) # Record the current question when the message waas received

        def on_publish(client, userdata, rc):
            logger.info('published result code=%s', rc)

        def on_disconnect(client, userdata, other):
            logger.info('disconnected result code=%s', other)

        client = mqtt.Client(topic, clean_session=False)
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect
        client.on_publish = on_publish

        if config.hostname:
            if config.username:
                client.username_pw_set(config.username, config.password)
            try:
                client.connect(config.hostname, 1883, 60)
                client.loop_start()
                logger.info('subscribed to %s', config.hostname)
            except socket.error as err:
                print('MQTT:', err, file=sys.stderr)
                print('Continuing without subscriptions', file=sys.stderr)

        self.messages.queue.clear()

    def get_messages(self):
        """
        Retrieves the messages from the queue. If there are no messages, returns None.
        """
        try:
            (msg, counter) = self.messages.get(block=False)
            payload = json.loads(msg.payload.decode('utf-8'))
            payload = {k: v[0] if isinstance(v, list) and len(v) == 1 else v
                       for k, v in payload.items()}
            payload['QuestionNum'] = counter
            return payload
        except queue.Empty:
            return None

    def publish(self, topic, **payload):
        """
        Publishes on the given topic.
        """
        logger.info('publish topic=%s payload=%s', topic, payload)
        mqtt_publish.single(topic,
                            payload=json.dumps(payload),
                            qos=1,
                            retain=True,
                            hostname=config.hostname,
                            auth=config.auth,
                            port=config.port,
                            client_id='')

    def repl(self, topic):
        while True:
            try:
                message = input('> ')
            except EOFError:
                break
            self.publish(topic, message=message)
