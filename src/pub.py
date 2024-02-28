import datetime
import os
import time

from paho.mqtt import client as mqtt_client

from app import my_app_instance
from sub import Sub
from utils.json_service import read_json_file
from utils.mqtt_service import connect_mqtt, publish

# from threading import Thread


broker_mosquitto = "test.mosquitto.org"
port = 1883


class pub:
    def __init__(self):
        self.customized_messages = None
        self.client = None

    def load_customized_messages(self) -> dict[str, str]:
        config = {}
        with open("customized_messages.txt", "r") as file:
            for line in file:
                topic, message = line.strip().split(maxsplit=1)
                config[message] = topic
        return config

    def replay_json_file(self, file_name: str) -> None:
        messages = read_json_file(file_name)
        for message in messages:
            test = True
            # if my_app_instance.state == "end":
            #     print("end relay")
            #     return
            if my_app_instance.state != "end":
                print_time = datetime.datetime.now()
                print(
                    f"Sent message {message['topic']} with payload {message['payload']} at {print_time}"
                )
                my_app_instance.message = message
                my_app_instance.print_time = print_time
                my_app_instance.send_message()
                time.sleep(1)
                while (
                    my_app_instance.state == "pause"
                    and my_app_instance.state != "restart"
                ):
                    if test == True:
                        print("Pause")
                        test = False
                    time.sleep(1)
            elif my_app_instance.state == "end":
                break

    def mode_one(self) -> None:
        while True:
            print("\nAvailable Messages:")
            for idx, (message, topic) in enumerate(self.customized_messages.items(), 1):
                print(f"{idx}. Message: {message} (Topic: {topic})")
            print(f"{len(self.customized_messages) + 1}. Go Back")

            selection_idx = input("Enter your message selection or go back: ")
            try:
                selection_idx = int(selection_idx)
                if selection_idx == len(self.customized_messages) + 1:
                    break
                selected_message = list(self.customized_messages.keys())[
                    selection_idx - 1
                ]
                if selected_message in self.customized_messages:
                    publish(
                        self.client,
                        self.customized_messages[selected_message],
                        selected_message,
                    )
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def mode_two(self) -> None:
        for message, topic in self.customized_messages.items():
            publish(self.client, topic, message)
            time.sleep(0.5)

    def mode_three(self) -> None:
        current_directory = os.getcwd()
        parent_directory = os.path.dirname(current_directory)
        scenarios_dir = os.path.join(parent_directory, "scenarios")
        while my_app_instance.state == "start":
            try:
                print("******************mode three with start ****************")
                file_name = my_app_instance.selected_scenario[0]
                file_to_read = os.path.join(scenarios_dir, file_name)
                self.replay_json_file(file_to_read)
                # if my_app_instance.state == "end":
                #     print("end mode three")
                #     return
            except ValueError:
                print("Please enter a valid number.")
            time.sleep(1)

    def run(self, broker_mosquitto, port) -> None:
        self.client = connect_mqtt(broker_mosquitto, port)
        self.client.loop_start()
        choice = "0"
        choice_prompt = (
            "\nChoose mode:"
            "\n 1: Send one message"
            "\n 2: Send a series of messages defined in custom_messages.txt"
            "\n 3: Replay _scenario.json under the folder scenarios"
            "\n 4: Exit"
            "\n Enter your choice: "
        )
        self.customized_messages = self.load_customized_messages()
        strategies = {
            "1": lambda: self.mode_one(),
            "2": lambda: self.mode_two(),
            "3": lambda: self.mode_three(),
        }

        while 1:
            if (
                broker_mosquitto != my_app_instance.broker
                and my_app_instance.broker != None
            ):
                print("changement de broker_mosquitto ")
                try:
                    print("changement de broker_mosquitto to another one ")
                    broker_mosquitto = str(my_app_instance.broker)
                    self.client = connect_mqtt(broker_mosquitto, port)
                except Exception as e:
                    print("keeping the test.mosquitto.org by exception")
                    self.client = connect_mqtt("test.mosquitto.org", 1883)
            if port != my_app_instance.port and my_app_instance.port != None:
                port = int(my_app_instance.port)
                print("changement de port ")

            if my_app_instance.state == "start":
                choice = "3"
                action = strategies.get(choice)
                if action:
                    action()
                    # if my_app_instance.state == "end":
                    #     print(
                    #         "**********************end of simulation****************************"
                    #     )
                    #     break
            else:
                print("Invalid choice. Please enter Start '1, 2, 3, or 4.' ")
            time.sleep(1)
        self.client.loop_stop()
