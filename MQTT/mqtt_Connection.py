import json
import ssl
import paho.mqtt.client as mqtt


class GameMQTT:
    """
    This class handles all MQTT communication for the Pacman game.

    What this class does:
    - Connects to the HiveMQ broker
    - Subscribes to MQTT topics for one game room
    - Receives messages from other players / host
    - Sends player input (for example: left, right, up, down)
    - Sends the current game state (usually done by the host)

    Important idea:
    - Every player connects to the same broker
    - Players in the same room use the same room name
    - Topics are based on that room name
    """

    def __init__(self, player_id, room):
        """
        Create a new MQTT game client.

        Parameters:
        player_id (str): Unique name/id for this player
        room (str): Name/code of the game room
        """

        # Store the player name and room name
        self.player_id = player_id
        self.room = room

        # This dictionary will contain all players received from the 'state' topic
        # Example:
        # {
        #     "stephan": {"x": 5, "y": 7},
        #     "anna": {"x": 10, "y": 3}
        # }
        self.players = {}

        # This list will store received input messages if needed later
        # Example:
        # [{"player_id": "stephan", "direction": "left"}]
        self.received_inputs = []

        # ------------------------------------------------------------
        # MQTT broker connection settings
        # Replace these with your own HiveMQ credentials
        # ------------------------------------------------------------
        self.broker_host = "4abaa784a435421ba0190c9884dd2b89.s1.eu.hivemq.cloud"
        self.broker_port = 8883
        self.username = "YOUR_USERNAME"
        self.password = "YOUR_PASSWORD"

        # ------------------------------------------------------------
        # MQTT topics for one room
        # Example room = "room1"
        # state topic = pacman/room1/state
        # input topic = pacman/room1/input
        # ------------------------------------------------------------
        self.state_topic = f"pacman/{self.room}/state"
        self.input_topic = f"pacman/{self.room}/input"
        self.join_topic = f"pacman/{self.room}/join"
        self.leave_topic = f"pacman/{self.room}/leave"

        # ------------------------------------------------------------
        # Create MQTT client
        # ------------------------------------------------------------
        self.client = mqtt.Client()

        # Set username and password for HiveMQ Cloud authentication
        self.client.username_pw_set(self.username, self.password)

        # Enable TLS because HiveMQ Cloud on port 8883 requires a secure connection
        self.client.tls_set(cert_reqs=ssl.CERT_REQUIRED)

        # Link MQTT events to methods in this class
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        # Connect to the MQTT broker
        self.client.connect(self.broker_host, self.broker_port)

        # Start the MQTT network loop in the background
        # This is necessary so the client can receive messages continuously
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        """
        This method is called automatically when the client connects to the broker.

        Parameters:
        client: The MQTT client instance
        userdata: Optional user data
        flags: Response flags from the broker
        rc: Result code (0 means success)
        """

        print(f"[MQTT] Connected with result code: {rc}")

        if rc == 0:
            print("[MQTT] Connection successful.")

            # Subscribe to the room's topics
            # 'state' is usually published by the host
            # 'input' is published by the players
            client.subscribe(self.state_topic)
            client.subscribe(self.input_topic)

            print(f"[MQTT] Subscribed to: {self.state_topic}")
            print(f"[MQTT] Subscribed to: {self.input_topic}")

            # Let the room know this player has joined
            self.send_join_message()
        else:
            print("[MQTT] Connection failed.")

    def on_message(self, client, userdata, msg):
        """
        This method is called automatically when a subscribed message is received.

        Parameters:
        client: The MQTT client instance
        userdata: Optional user data
        msg: The received MQTT message object
        """

        try:
            # Convert the received JSON string back into a Python dictionary
            data = json.loads(msg.payload.decode())

            print(f"[MQTT] Message received on topic: {msg.topic}")
            print(f"[MQTT] Data: {data}")

            # If the message comes from the state topic,
            # it usually contains all player positions from the host
            if msg.topic == self.state_topic:
                self.players = data

            # If the message comes from the input topic,
            # it contains a movement command from one player
            elif msg.topic == self.input_topic:
                self.received_inputs.append(data)

        except json.JSONDecodeError:
            print("[MQTT] Error: received message is not valid JSON.")

    def on_disconnect(self, client, userdata, rc):
        """
        This method is called automatically when the client disconnects.

        Parameters:
        client: The MQTT client instance
        userdata: Optional user data
        rc: Result code
        """

        print(f"[MQTT] Disconnected with result code: {rc}")

    def send_join_message(self):
        """
        Send a message to let other clients know this player joined the room.
        """

        data = {
            "player_id": self.player_id,
            "message": "joined the room"
        }

        self.client.publish(self.join_topic, json.dumps(data))
        print(f"[MQTT] Sent join message: {data}")

    def send_leave_message(self):
        """
        Send a message to let other clients know this player left the room.
        """

        data = {
            "player_id": self.player_id,
            "message": "left the room"
        }

        self.client.publish(self.leave_topic, json.dumps(data))
        print(f"[MQTT] Sent leave message: {data}")

    def send_input(self, direction):
        """
        Send a movement command for this player.

        Parameters:
        direction (str): Example values: 'left', 'right', 'up', 'down'
        """

        data = {
            "player_id": self.player_id,
            "direction": direction
        }

        self.client.publish(self.input_topic, json.dumps(data))
        print(f"[MQTT] Sent input: {data}")

    def send_state(self, state):
        """
        Send the current game state.
        Usually only the host should do this.

        Parameters:
        state (dict): Example:
        {
            "stephan": {"x": 5, "y": 7},
            "anna": {"x": 10, "y": 3}
        }
        """

        self.client.publish(self.state_topic, json.dumps(state))
        print(f"[MQTT] Sent state: {state}")

    def disconnect(self):
        """
        Disconnect the MQTT client cleanly.
        Call this when closing the game.
        """

        self.send_leave_message()
        self.client.loop_stop()
        self.client.disconnect()
        print("[MQTT] Client disconnected cleanly.")