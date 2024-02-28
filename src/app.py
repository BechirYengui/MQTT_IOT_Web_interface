import os

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_socketio import SocketIO


class MyApp:
    def __init__(self, message, print_time):
        self.template_folder = os.path.join(os.environ["PYTHONPATH"], "templates")
        self.selected_broker = None
        self.broker = None
        self.port = None
        self.topic = None
        self.state = None
        self.selected_scenario = None
        self.message = message
        self.print_time = print_time
        self.filename = None
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.parent_dir = os.path.abspath(os.path.join(self.current_dir, os.pardir))
        self.app = Flask(__name__, template_folder=self.template_folder)
        self.socketio = SocketIO(self.app)
        self.setup_routes()

    def setup_routes(self):
        self.app.route("/scen", methods=["GET", "POST"])(self.get_scenarios)
        self.app.route("/broker", methods=["GET", "POST"])(self.handle_broker_data)
        self.app.route("/state", methods=["GET", "POST"])(self.handle_state_data)
        self.app.route("/selected_scenario", methods=["GET", "POST"])(
            self.handle_selected_scenario
        )
        self.app.route("/filename", methods=["GET", "POST"])(self.handle_filename_data)
        self.app.route("/topic", methods=["GET", "POST"])(self.handle_topic_data)
        self.app.route("/message", methods=["POST", "GET"])(self.send_message)
        self.app.route("/")(self.replay)
        self.app.route("/registration")(self.registration)

    def send_message(self):
        data = {
            "topic": str(self.message["topic"]),
            "payload": str(self.message["payload"]),
            "timestamp": str(self.print_time),
        }

        try:
            with self.app.app_context():
                # Emit a WebSocket event to send the message
                self.socketio.emit("message", data)

                print("Message sent to clients.")
                return jsonify({"status": "ok", "message": "Message sent to clients"})
        except Exception as e:
            print("Error sending message:", str(e))
            return jsonify({"status": "error", "message": "Error sending message"}), 500

    def get_scenarios(self):
        scenarios_dir = os.path.join(self.parent_dir, "scenarios")
        scenarios = os.listdir(scenarios_dir)
        print(scenarios)
        return jsonify(scenarios=scenarios)

    def handle_broker_data(self):
        try:
            # Récupérer les données JSON envoyées depuis le frontend
            data = request.get_json()

            # Extraire les valeurs
            self.selected_broker = data.get("selectedBroker")
            self.broker = data.get("broker")
            self.port = data.get("port")

            # Faire ce que vous avez besoin de faire avec les valeurs
            print(f"Broker sélectionné : {self.selected_broker}")
            print(f"Broker : {self.broker}")
            print(f"Port : {self.port}")

            # Vous pouvez également renvoyer une réponse au frontend si nécessaire
            return jsonify({"status": "ok"}), 200
        except Exception as e:
            # Gérer les erreurs ici, par exemple, si les données JSON ne sont pas valides
            print(f"Erreur lors de la gestion des données du broker : {str(e)}")
            return (
                jsonify({"error": "Erreur lors du traitement des données du broker"}),
                500,
            )

    def handle_state_data(self):
        try:
            # Récupérer les données JSON envoyées depuis le frontend
            data = request.get_json()

            # Extraire la valeur de l'état
            self.state = data.get("state")

            # Faire ce que vous avez besoin de faire avec la valeur de l'état
            print(f"État reçu du frontend : {self.state}")

            # Vous pouvez également renvoyer une réponse au frontend si nécessaire
            return jsonify({"status": "ok"}), 200
        except Exception as e:
            # Gérer les erreurs ici, par exemple, si les données JSON ne sont pas valides
            print(f"Erreur lors de la gestion de l'état : {str(e)}")
            return jsonify({"error": "Erreur lors du traitement de l'état"}), 500

    def handle_selected_scenario(self):
        try:
            # Récupérer les données JSON envoyées depuis le frontend
            data = request.get_json()

            if data is None or "selectedScenario" not in data:
                print("Invalid data received for selected_scenario.")
                return jsonify({"error": "Invalid data"}), 400

            # Extraire le scénario sélectionné
            self.selected_scenario = data.get("selectedScenario")

            if self.selected_scenario is None:
                print("No selected scenario received.")
                return jsonify({"error": "No selected scenario received"}), 400

            # Faire ce que vous avez besoin de faire avec le scénario sélectionné
            print(f"Scénario sélectionné :", self.selected_scenario[0])

            # Vous pouvez également renvoyer une réponse au frontend si nécessaire
            return jsonify({"status": "ok"}), 200
        except Exception as e:
            # Gérer les erreurs ici, par exemple, si les données JSON ne sont pas valides
            print(f"Erreur lors de la gestion du scénario sélectionné : {str(e)}")
            return (
                jsonify({"error": "Erreur lors du traitement du scénario sélectionné"}),
                500,
            )

    def send_message_registration(self):
        try:
            with self.app.app_context():
                # Emit a WebSocket event to send the message
                self.socketio.emit("message", {"data": self.message})

                print("Message sent to clients.")
                return jsonify({"status": "ok", "message": "Message sent to clients"})
        except Exception as e:
            print("Error sending message:", str(e))
            return jsonify({"status": "error", "message": "Error sending message"}), 500

    def handle_topic_data(self):
        try:
            # Récupérer les données JSON envoyées depuis le frontend
            data = request.get_json()

            # Extraire les valeurs
            self.topic = data.get("topic")

            # Faire ce que vous avez besoin de faire avec les valeurs
            print(f"Topic : {self.topic}")

            # Vous pouvez également renvoyer une réponse au frontend si nécessaire
            return jsonify({"status": "ok"}), 200
        except Exception as e:
            # Gérer les erreurs ici, par exemple, si les données JSON ne sont pas valides
            print(f"Erreur lors de la gestion des données du broker : {str(e)}")
            return (
                jsonify({"error": "Erreur lors du traitement des données du broker"}),
                500,
            )

    def handle_filename_data(self):
        try:
            # Récupérer les données JSON envoyées depuis le frontend
            data = request.get_json()

            # Extraire les valeurs
            self.filename = data.get("filename")

            # Faire ce que vous avez besoin de faire avec les valeurs
            print(f"filename : {self.filename}")

            # Vous pouvez également renvoyer une réponse au frontend si nécessaire
            return jsonify({"status": "ok"}), 200
        except Exception as e:
            # Gérer les erreurs ici, par exemple, si les données JSON ne sont pas valides
            print(f"Erreur lors de la gestion des données du broker : {str(e)}")
            return (
                jsonify({"error": "Erreur lors du traitement des données du broker"}),
                500,
            )

    def replay(self):
        return render_template("replay.html")

    def registration(self):
        return render_template("registration.html")

    def run(self):
        CORS(self.app, origins="*", supports_credentials=True)
        self.socketio.run(self.app, debug=False, host="127.0.0.1", port=5000)


mess = {"topic": "First", "payload": "First", "First": "First"}
print_t = None
my_app_instance = MyApp(mess, print_t)

# if __name__ == "__main__":
#     socketio.run(app, debug=True)
