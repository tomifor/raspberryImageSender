import json
import os
import enviroment

import paho.mqtt.client as mqtt


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    print(payload['id'])


def start_subscriber():
    client = mqtt.Client(os.environ['QUEUE_CLIENT'])
    client.connect( os.environ['QUEUE_IP'], int(os.environ['QUEUE_PORT']))
    client.subscribe("image")
    client.on_message = on_message
    print("Waiting for messages .....")
    client.loop_forever()


if __name__ == "__main__":
    start_subscriber()
