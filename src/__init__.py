import paho.mqtt.client as mqttClient
from flask import Flask, escape, request

from video_controller import video_controller_sender, image_controller_sender, video_camera_live

PORT = 1883

queue = None

app = Flask(__name__)


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@app.route('/health')
def check_health():
    return 'App is running!'


@app.route('/start-image')
def start_image_recognition():
    print('Sending image...')
    return image_controller_sender(queue)


@app.route('/start-video')
def start_video_recognition():
    print('Sending video frames...')
    return video_controller_sender(queue)


@app.route('/start-video-live')
def start_live_video_recognition():
    print('Sending video frames live...')
    return video_camera_live(queue)


def create_connection():
    client = mqttClient.Client('image_recognition')
    client.connect('0.0.0.0', PORT)
    return client


if __name__ == "__main__":
    queue = create_connection()
    app.run(debug=True)
