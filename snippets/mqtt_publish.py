"""This need the module umqttsimple which comes from
https://raw.githubusercontent.com/micropython/micropython-lib/master/umqtt.simple/umqtt/simple.py
"""
import machine
import ubinascii
from umqttsimple import MQTTClient, MQTTException

HOST = "<#your_broker_ip#>"
USER = "<#your_user#>"
PASSWORD = "<#your_password#>"


def publish_message(topic, msg):
    """Publish a message to a broker.

    If connection is not possible it will not publish any message.
    """
    broker = MQTTClient(
        ubinascii.hexlify(machine.unique_id()),
        server=HOST,
        user=USER,
        password=PASSWORD)
    try:
        broker.connect()
    except (MQTTException, OSError):
        print("Error occurred connecting to broker.")
        broker = None

    if broker is not None:
        broker.publish(topic.encode(), msg.encode())
        broker.disconnect()
