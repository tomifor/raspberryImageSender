PORT = 1883


def publish(img, id, queue):
    payload = '{"id": "' + id + '", "image": "' + img + '"}'
    queue.publish("image", payload)
