# Factory Simulator For The Publisher

## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
- [Folder Structure](#folder-structure)
- [Frontend (HTML and JavaScript)](#frontend)
  - [Dependencies](#dependencies)
  - [Styles](#styles)
  - [Scripts](#scripts)
- [Backend (Flask Application)](#backend)
  - [Flask Routes](#flask-routes)
  - [Flask Application Structure](#flask-application-structure)
  - [Message Broadcasting](#message-broadcasting)
  - [Simulation Control](#simulation-control)
  - [Scenario Management](#scenario-management)
  - [Broker Configuration](#broker-configuration)
  - [WebSocket Communication](#websockets)
- [Running the Application](#running-the-application)
- [Simulator Modes](#simulator-modes)
- [Threading Implementation](#threading-implementation)
- [Conclusion](#conclusion)

---

## Overview

The Factory Simulator is a web application designed to simulate various scenarios within a factory environment. It utilizes HTML, JavaScript, Tailwind CSS, Flask, and WebSocket for real-time communication. The simulator includes features such as broker selection, scenario tree, simulation control buttons, and a console to display simulation messages.

## Getting Started

To get started with the Factory Simulator, follow these steps:

1. Clone the repository.
2. Install the necessary dependencies using `pip install ' flask , flask_cors ,paho.mqtt , flask_socketio and time
3. Run the Flask application using `python main.py`.
4. Open the application in a web browser at `http://127.0.0.1:5000`.

tips : Because this project is still being refined, it is not yet possible to run the registration and replay functions properly at the same time. In this case, please change the startup of the corresponding thread according to the function you want to test.

## Folder Structure

- **templates:** Contains the HTML template (`replay.html`).
- **scenarios:** Directory to store scenario files used in the simulation.
- **src:** Contains the back-end service

---

## Frontend

### Dependencies

- **Tailwind CSS:** A utility-first CSS framework used for styling.
- **jQuery:** A fast, small, and feature-rich JavaScript library.
- **jstree:** A JavaScript library for interactive tree views.
- **socketio** a library to communication by WebSocket

### Styles

The styling of the application is managed using Tailwind CSS and a custom stylesheet (`styles.css`). Key styles include sidebar layout, buttons, and the console appearance.

### Scripts

JavaScript is used to handle user interactions and communicate with the Flask backend. Key scripts include controlling the simulation state, updating scenarios dynamically, handling broker selection, and real-time WebSocket communication.

---

## Backend

The backend is implemented using Flask, a Python web framework. It handles various routes for fetching scenarios, managing broker data, topic and filename, simulation state, selected scenarios, and sending real-time messages through WebSocket.

### Flask Routes

- **/scen:** GET and POST routes for retrieving and updating available scenarios.
- **/broker:** POST route for updating broker information.
- **/state:** POST route for updating the simulation state.
- **/selected_scenario:** POST route for handling selected scenarios.
- **/message:** POST and GET routes for sending and fetching real-time messages.
- **/topic:** POST route for updating topic to receive information
- **/filename:** POST route for updating filename to save message information

Certainly! Let's add more details to the README specifically focusing on the backend.


### Flask Application Structure

The backend code is organized into a Flask application (`MyApp` class) with several routes and functionalities:

- **Routes:**
  - `/scen`: Handles both GET and POST requests to retrieve and update the list of available scenarios.
  - `/broker`: Receives POST requests with broker information and updates the backend.
  - `/state`: Manages POST requests to update the simulation state.
  - `/selected_scenario`: Handles POST requests related to selected scenarios.
  - `/message`: Manages both GET and POST requests for sending and fetching real-time messages using WebSocket.

- **SocketIO Integration:**
  - Utilizes the `SocketIO` extension to establish WebSocket communication with the frontend. This allows real-time updates and messaging during the simulation.

- **Multithreading:**
  - Implements multithreading to run the Flask application (`t2`) concurrently with the publish simulation script (`t1`) and the subscribe simulation script (`t2`). This ensures the responsiveness of the frontend while the simulation continues in the background.

### Message Broadcasting

Real-time messages are broadcasted to connected clients using WebSocket (`SocketIO`). The `/message` route emits the `message` event, carrying payload information such as the topic, payload, and timestamp. This event is then handled on the frontend to update the user interface dynamically.

### Simulation Control

- **Simulation State Handling:**
  - The `/state` route is responsible for receiving and updating the simulation state. It manages the state transitions such as 'start', 'pause', 'restart', and 'end'.
  - The frontend JavaScript sends state information to the backend, which is then broadcasted to all connected clients.

### Scenario Management

- **Scenario Selection:**
  - The `/scen` route handles scenario-related operations. It fetches the list of available scenarios from the server and dynamically updates the frontend.
  - The selected scenarios are sent to the backend, and the `/selected_scenario` route manages the corresponding logic.

### Broker Configuration

- **Broker Information:**
  - The `/broker` route handles broker-related operations. It receives broker information (selected broker, broker address, port) from the frontend and updates the backend accordingly.

### WebSocket Communication

- **SocketIO Event Handling:**
  - Listens for the `message` event from the frontend using `SocketIO.on('message', ...)`. When a message is received, it is processed and broadcasted to all connected clients.

---

## Running the Application

1. Run the Flask application by executing `main.py`.
2. Open your web browser and navigate to `http://127.0.0.1:5000`.
3. Explore different features such as scenario selection, broker configuration, and simulation control.
4. navigate to `http://127.0.0.1:5000/registration`. Explor a page similary as `replay` page

---

## Simulator Modes for replaying

The Factory Simulator offers three main modes:

1. **Send One Message:** Allows users to manually send a single message.
2. **Send Series of Messages:** Sends a predefined series of messages defined in `customized_messages.txt`.
3. **Replay Scenario:** Replays a scenario by reading messages from a JSON file under the `scenarios` folder.
But in our web application only mode three is activated by clicking on Start button (Using other modes in a web application is unnecessary. ) 
#### Mode 1: Send One Message

- **Description**: This mode allows the user to send a single message. The user can choose from a predefined list of messages.
- **Usage**: Select this mode if you need to send a specific, one-time message to an MQTT topic.

#### Mode 2: Send a Series of Messages Defined in `custom_messages.txt`

- **Description**: In this mode, the script sends a series of messages as defined in the `custom_messages.txt` file. This mode is useful for sending a batch of predetermined messages.
- **Usage**: Use this mode for automated sending of multiple messages, where each message and its corresponding topic are defined in the `custom_messages.txt` file.

#### Mode 3: Replay `_scenario.json` under the Folder `scenarios`

- **Description**: This mode is designed to replay scenarios from JSON files located in the `scenarios` folder. Each file should follow the `_scenario.json` naming convention. The script reads these files and replays the messaging sequence as per the data in the JSON file.
- **Usage**: Choose this mode to simulate real-world scenarios or to replay message sequences for testing or demonstration purposes.

#### Mode 4: Exit

- **Description**: This mode simply exits the script.
- **Usage**: Select this option to safely terminate the script.

---

## Threading Implementation

The application employs multithreading to run the Flask application and the simulator script concurrently. Three threads (`t1` and `t2`, `t3`) are created for running the script and the Flask application simultaneously.

- **Thread 1 (`t1`):** Runs the publish simulation script concurrently with the Flask application.
- **Thread 2 (`t2`):** Handles the Flask application, including route setup and WebSocket communication.
- **Thread 1 (`t3`):** Runs the subscribe simulation script concurrently with the Flask application.

...

## Conclusion

The Factory Simulator seamlessly integrates frontend and backend technologies to provide a dynamic simulation experience. By employing Flask for backend logic, WebSocket for real-time communication, and a multithreaded approach, the application ensures a responsive user interface while efficiently running complex simulations. Explore the various modes and features to simulate diverse factory scenarios and messaging patterns.
