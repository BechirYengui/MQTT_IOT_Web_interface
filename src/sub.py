import datetime
import time

from flask import jsonify

from app import my_app_instance
from utils.json_service import write_to_json
from utils.mqtt_service import connect_mqtt

# TODO: if the json file is to large, stop registerment

# User input for topic and filename
# topic = input("Enter the MQTT topic to subscribe: ")
# filename = input("Enter the filename to store messages: ") + "_scenario.json"
# print_to_terminal_input = input("Print messages to terminal? (yes/no): ").strip().lower()
# print_to_terminal = print_to_terminal_input == 'yes'


class Sub:
    def __init__(self):
        self.client = None

    def run(self):
        while True:
            print("app state:", my_app_instance.state)
            if my_app_instance.state != "end_registration":
                if my_app_instance.state == "start_registration":
                    print("current client:", self.client)
                    if self.client is None:
                        broker = str(my_app_instance.broker)
                        print(broker)
                        port = int(my_app_instance.port)
                        self.client = connect_mqtt(broker, port)
                        self.client.loop_start()

                    self.client.on_message = self.on_message
                    self.client.subscribe(my_app_instance.topic)

                    # if my_app_instance.state == "end_registration":
                    #     print(
                    #         "**********************end of simulation****************************"
                    #     )
                    #     break
                else:
                    print("waiting for start")
                time.sleep(1)
            else:
                if self.client is not None:
                    self.client.loop_stop()
                    self.client.disconnect()
                    self.client = None

    def on_message(self, client, userdata, msg):
        current_time = datetime.datetime.now().isoformat()
        message_data = {
            "topic": msg.topic,
            "payload": msg.payload.decode(),
            "receiving_time": current_time,
        }

        write_to_json(message_data, my_app_instance.filename, print_to_terminal=True)
        print("send to client")
        try:
            with my_app_instance.app.app_context():
                my_app_instance.message = message_data
                my_app_instance.send_message_registration()
                print("Message sent to clients.")
                return jsonify({"status": "ok", "message": "Message sent to clients"})
        except Exception as e:
            print("Error sending message:", str(e))
            return jsonify({"status": "error", "message": "Error sending message"}), 500


# if __name__ == '__main__':
#     print("Starting MQTT client. Press Ctrl+C to stop.")
#     run()
