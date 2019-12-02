PORT = 1883
TOPIC = "images"


def publish(img, id, queue):
    payload = '{"id": "' + id + '", "image": "' + img + '"}'
    print(payload)
    queue.publish(TOPIC, payload)
