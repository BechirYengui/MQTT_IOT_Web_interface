"""
This file contains the MQTT service. It is used to connect to the MQTT broker and publish messages. 
"""
import random

from paho.mqtt import client as mqtt_client

BROKER_ADDR_12 = "192.168.0.12"
BROKER_ADDR_13 = "192.168.0.13"
BROKER_MOSQUITTO = "test.mosquitto.org"

client_id = f"subscribe-{random.randint(0, 100)}"

MQTT_PORT = 1883


def connect_mqtt(broker, port, filename=None) -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id, userdata={"filename": filename})
    client.on_connect = on_connect
    try:
        print(f"Try to connect to {broker}")
        client.connect(broker, port)
        return client
    except Exception as e:
        print(f"Connection to {broker} failed: {e}")
    # try:
    #     print(f"Try to connect to {BROKER_ADDR_12}")
    #     client.connect(BROKER_ADDR_12, port)
    #     return client
    # except Exception as e:
    #     print(f"Connection to {BROKER_ADDR_12} failed: {e}")
    #     try:
    #         print(f"Try to connect to {BROKER_ADDR_13}")
    #         client.connect(BROKER_ADDR_13, port)
    #         return client
    #     except Exception as e:
    #         print(f"Connection to {BROKER_ADDR_13} failed: {e}")
    #         print(f"Try to connect to {BROKER_MOSQUITTO}")
    #         client.connect(BROKER_MOSQUITTO)
    return client


def publish(client, topic, message) -> None:
    result = client.publish(topic, message)
    status = result[0]
    if status == 0:
        print(f"Send `{message}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
