from threading import Thread

from app import my_app_instance
from pub import broker_mosquitto, port, pub
from sub import Sub

replay_script = pub()
registration_script = Sub()


def main():
    my_app_instance.run()


def run_script():
    replay_script.run(broker_mosquitto, port)


def run_registration():
    registration_script.run()


# Creation des deux threads t1 et t2
t1 = Thread(target=run_script, args=[])
t2 = Thread(target=main, args=[])
t3 = Thread(target=run_registration, args=[])

# Lancement des deux threads
t2.start()
t1.start()
t3.start()

# Wait for threads to finish
t1.join()
t3.join()
t2.join()
