import base64
import os
import time
from datetime import datetime
import cv2
import paho.mqtt.client as mqttClient

from publisher import publish

CAMERA_ID = 'da7dtbqniuejiq9'
PORT = 1883


def video_controller_sender(queue) -> str:
    print('Sending video frames')
    video = cv2.VideoCapture('assets/iphonevideo.mp4')
    if video is None:
        print("\n### Error: image not found ### \n\n")
        os.system("pause")
        return 'Video not found'

    i = 1

    while video.isOpened():

        # Capture frame-by-frame
        ret, frame = video.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if i % 30 == 0:
            print('Frame: ' + str(i))
            print('Envío frame')
            timestamp = time.time()
            date_str = datetime.fromtimestamp(timestamp)
            print(date_str)
            id = CAMERA_ID + '@' + str(timestamp)
            frame_base64 = str(base64.b64encode(gray))
            result = publish(frame_base64, id, queue)

        i = i + 1

        # Display the resulting frame
        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    video.release()
    cv2.destroyAllWindows()

    return 'ok'


def image_controller_sender(queue) -> str:
    img = cv2.imread("assets/plateToyota.jpg")

    if img is None:
        print("\n### Error: image not found ### \n\n")
        os.system("pause")
        return 'Image not found'

    img_base64 = str(base64.b64encode(img))

    print(img_base64)

    timestamp = time.time()
    id = CAMERA_ID + '@' + str(timestamp)

    result = publish(img_base64, id, queue)

    print(result)


def video_loop():
    video = cv2.VideoCapture('assets/iphonevideo.mp4')
    fps = video.get(cv2.CAP_PROP_FPS)
    print(fps)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print(total_frames)

    x = [i for i in range(1, total_frames) if divmod(i, int(30))[1] == 0]
    print(x)

    for myFrameNumber in x:
        # set which frame to read
        video.set(cv2.CAP_PROP_POS_FRAMES, myFrameNumber)
        # read frame
        ret, frame = video.read()
        # display frame
        cv2.imshow("video" + str(myFrameNumber), frame)

    cv2.waitKey(30)


def video_camera_live(queue):
    cap = cv2.VideoCapture(0)
    i = 1

    while True:

        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if i % 15 == 0:
            print('Frame: ' + str(i))
            print('Envío frame')
            timestamp = time.time()
            id = CAMERA_ID + '@' + str(timestamp)
            frame_base64 = str(base64.b64encode(gray))
            result = publish(frame_base64, id, queue)

        i = i + 1

        # Display the resulting frame
        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def create_connection():
    client = mqttClient.Client('image_recognition')
    client.connect('0.0.0.0', PORT)
    return client


if __name__ == "__main__":
    queue = create_connection()
    video_controller_sender(queue)
