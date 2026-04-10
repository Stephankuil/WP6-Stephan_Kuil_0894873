import json
import ssl
from dataclasses import dataclass, field
from typing import List, Dict, Optional

import paho.mqtt.client as mqtt


@dataclass(frozen=True)
class MQTTConfig:
    """
    Stores all broker connection settings in one place.

    Why this is useful:
    - Single Responsibility: this class only stores configuration
    - Easy to replace later if you want to load from .env or settings.py
    """
    broker_host: str
    broker_port: int
    username: str
    password: str


@dataclass(frozen=True)
class RoomTopics:
    """
    Builds all MQTT topics for one room.

    Why this is useful:
    - No repeated hardcoded topic strings everywhere
    - Easy to add more topics later
    """
    room_code: str

    @property
    def join(self) -> str:
        return f"pacman/{self.room_code}/join"

    @property
    def leave(self) -> str:
        return f"pacman/{self.room_code}/leave"

    @property
    def lobby_state(self) -> str:
        return f"pacman/{self.room_code}/lobby_state"

    @property
    def start_game(self) -> str:
        return f"pacman/{self.room_code}/start_game"

    @property
    def input(self) -> str:
        return f"pacman/{self.room_code}/input"

    @property
    def state(self) -> str:
        return f"pacman/{self.room_code}/state"


@dataclass
class LobbyState:
    """
    Stores the current lobby state.

    Why this is useful:
    - Keeps lobby-related state together
    - Easy to understand and inspect
    """
    players: List[str] = field(default_factory=list)
    host_player: Optional[str] = None
    game_started: bool = False

    def add_player(self, player_id: str) -> None:
        """
        Add a player only if they are not already in the lobby list.
        """
        if player_id not in self.players:
            self.players.append(player_id)

    def remove_player(self, player_id: str) -> None:
        """
        Remove a player if present.
        """
        if player_id in self.players:
            self.players.remove(player_id)

    def set_host_if_missing(self, player_id: str) -> None:
        """
        Set host only if no host is known yet.
        """
        if self.host_player is None:
            self.host_player = player_id


class MQTTMessageFactory:
    """
    Creates outgoing MQTT message payloads.

    Why this is useful:
    - Single Responsibility: only builds message dictionaries
    - Keeps GameMQTT cleaner
    """

    @staticmethod
    def create_join_message(player_id: str, is_host: bool) -> Dict:
        return {
            "player_id": player_id,
            "is_host": is_host
        }

    @staticmethod
    def create_leave_message(player_id: str) -> Dict:
        return {
            "player_id": player_id
        }

    @staticmethod
    def create_lobby_state_message(players: List[str], host_player: Optional[str]) -> Dict:
        return {
            "players": players,
            "host_player": host_player
        }

    @staticmethod
    def create_start_game_message(started_by: str) -> Dict:
        return {
            "started_by": started_by
        }

    @staticmethod
    def create_input_message(player_id: str, direction: str) -> Dict:
        return {
            "player_id": player_id,
            "direction": direction
        }

    @staticmethod
    def create_game_state_message(state: Dict) -> Dict:
        return state


class GameMQTT:
    """
    Main class that handles MQTT communication for the multiplayer Pacman game.

    Main responsibilities:
    - connect to the broker
    - subscribe to room topics
    - send and receive lobby messages
    - send and receive gameplay messages
    - expose simple properties that the rest of the game can use

    Design note:
    This class acts as the communication layer between your game and MQTT.
    """

    def __init__(self, config: MQTTConfig, player_id: str, room_code: str, is_host: bool):
        """
        Parameters:
        - config: MQTT connection settings
        - player_id: unique player name/id
        - room_code: room/lobby identifier
        - is_host: True if this player hosts the room
        """

        self.config = config
        self.player_id = player_id
        self.room_code = room_code
        self.is_host = is_host

        self.topics = RoomTopics(room_code)
        self.lobby_state = LobbyState()
        self.received_inputs: List[Dict] = []
        self.players_state: Dict = {}

        # This flag becomes True when a start_game message is received
        self.start_game_received = False

        # MQTT client setup
        self.client = mqtt.Client()
        self.client.username_pw_set(self.config.username, self.config.password)
        self.client.tls_set(cert_reqs=ssl.CERT_REQUIRED)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    # ---------------------------------------------------------
    # CONNECTION METHODS
    # ---------------------------------------------------------

    def connect(self) -> None:
        """
        Connect to the MQTT broker and start the background loop.
        """
        self.client.connect(self.config.broker_host, self.config.broker_port)
        self.client.loop_start()

    def disconnect(self) -> None:
        """
        Disconnect cleanly from the MQTT broker.
        """
        self.send_leave()

        self.client.loop_stop()
        self.client.disconnect()

    # ---------------------------------------------------------
    # MQTT CALLBACKS
    # ---------------------------------------------------------

    def on_connect(self, client, userdata, flags, rc) -> None:
        """
        Called automatically when the client connects to the broker.
        """
        print(f"[MQTT] Connected with result code: {rc}")

        if rc != 0:
            print("[MQTT] Connection failed.")
            return

        print("[MQTT] Connection successful.")

        # Subscribe to all topics needed for lobby + gameplay
        client.subscribe(self.topics.join)
        client.subscribe(self.topics.leave)
        client.subscribe(self.topics.lobby_state)
        client.subscribe(self.topics.start_game)
        client.subscribe(self.topics.input)
        client.subscribe(self.topics.state)

        print(f"[MQTT] Subscribed to: {self.topics.join}")
        print(f"[MQTT] Subscribed to: {self.topics.leave}")
        print(f"[MQTT] Subscribed to: {self.topics.lobby_state}")
        print(f"[MQTT] Subscribed to: {self.topics.start_game}")
        print(f"[MQTT] Subscribed to: {self.topics.input}")
        print(f"[MQTT] Subscribed to: {self.topics.state}")

    def on_disconnect(self, client, userdata, rc) -> None:
        """
        Called automatically when the client disconnects.
        """
        print(f"[MQTT] Disconnected with result code: {rc}")

    def on_message(self, client, userdata, msg) -> None:
        """
        Called automatically when a subscribed message is received.

        This method routes the message to the correct internal handler.
        """
        try:
            data = json.loads(msg.payload.decode())

            print(f"[MQTT] Message received on topic: {msg.topic}")
            print(f"[MQTT] Data: {data}")

            if msg.topic == self.topics.join:
                self._handle_join_message(data)

            elif msg.topic == self.topics.leave:
                self._handle_leave_message(data)

            elif msg.topic == self.topics.lobby_state:
                self._handle_lobby_state_message(data)

            elif msg.topic == self.topics.start_game:
                self._handle_start_game_message(data)

            elif msg.topic == self.topics.input:
                self._handle_input_message(data)

            elif msg.topic == self.topics.state:
                self._handle_game_state_message(data)

        except json.JSONDecodeError:
            print("[MQTT] Error: received message is not valid JSON.")

    # ---------------------------------------------------------
    # INTERNAL MESSAGE HANDLERS
    # ---------------------------------------------------------

    def _handle_join_message(self, data: Dict) -> None:
        """
        Process a player joining the room.
        """
        player_id = data.get("player_id")
        is_host = data.get("is_host", False)

        if not player_id:
            return

        self.lobby_state.add_player(player_id)

        if is_host:
            self.lobby_state.host_player = player_id
        else:
            self.lobby_state.set_host_if_missing(player_id)

        print(f"[MQTT] Player joined lobby: {player_id}")
        print(f"[MQTT] Players now: {self.lobby_state.players}")
        print(f"[MQTT] Host: {self.lobby_state.host_player}")

        # If this client is the host, it becomes the source of truth for lobby state
        if self.is_host:
            self.send_lobby_state()

    def _handle_leave_message(self, data: Dict) -> None:
        """
        Process a player leaving the room.
        """
        player_id = data.get("player_id")

        if not player_id:
            return

        self.lobby_state.remove_player(player_id)

        # If the host leaves, host stays unchanged for now.
        # Later you could implement host migration here.
        print(f"[MQTT] Player left lobby: {player_id}")
        print(f"[MQTT] Players now: {self.lobby_state.players}")

        if self.is_host:
            self.send_lobby_state()

    def _handle_lobby_state_message(self, data: Dict) -> None:
        """
        Process the full lobby state.

        This is very important because it solves the problem where a new player
        joins later and still needs to know the full list of players.
        """
        players = data.get("players", [])
        host_player = data.get("host_player")

        self.lobby_state.players = players
        self.lobby_state.host_player = host_player

        print(f"[MQTT] Lobby state updated: {self.lobby_state.players}")
        print(f"[MQTT] Host player: {self.lobby_state.host_player}")

    def _handle_start_game_message(self, data: Dict) -> None:
        """
        Process the message that tells all players to start the game.
        """
        self.lobby_state.game_started = True
        self.start_game_received = True

        started_by = data.get("started_by", "unknown")
        print(f"[MQTT] Start game received from: {started_by}")

    def _handle_input_message(self, data: Dict) -> None:
        """
        Process a player input message.

        Usually the host will read these inputs and update the real game state.
        """
        self.received_inputs.append(data)

    def _handle_game_state_message(self, data: Dict) -> None:
        """
        Process the full game state from the host.
        """
        self.players_state = data

    # ---------------------------------------------------------
    # PUBLIC SEND METHODS
    # ---------------------------------------------------------

    def send_join(self) -> None:
        """
        Tell the room that this player has joined.
        """
        payload = MQTTMessageFactory.create_join_message(
            player_id=self.player_id,
            is_host=self.is_host
        )

        self.client.publish(self.topics.join, json.dumps(payload))
        print(f"[MQTT] Sent join message: {payload}")

    def send_leave(self) -> None:
        """
        Tell the room that this player has left.
        """
        payload = MQTTMessageFactory.create_leave_message(self.player_id)

        self.client.publish(self.topics.leave, json.dumps(payload))
        print(f"[MQTT] Sent leave message: {payload}")

    def send_lobby_state(self) -> None:
        """
        Host sends the full lobby state to everyone.
        """
        payload = MQTTMessageFactory.create_lobby_state_message(
            players=self.lobby_state.players,
            host_player=self.lobby_state.host_player
        )

        self.client.publish(self.topics.lobby_state, json.dumps(payload))
        print(f"[MQTT] Sent lobby state: {payload}")

    def send_start_game(self) -> None:
        """
        Host tells every client in the room to start the game.
        """
        payload = MQTTMessageFactory.create_start_game_message(self.player_id)

        self.client.publish(self.topics.start_game, json.dumps(payload))
        print(f"[MQTT] Sent start game message: {payload}")

    def send_input(self, direction: str) -> None:
        """
        Send player movement input.
        """
        payload = MQTTMessageFactory.create_input_message(
            player_id=self.player_id,
            direction=direction
        )

        self.client.publish(self.topics.input, json.dumps(payload))
        print(f"[MQTT] Sent input: {payload}")

    def send_game_state(self, state: Dict) -> None:
        """
        Host sends the full game state to all clients.
        """
        payload = MQTTMessageFactory.create_game_state_message(state)

        self.client.publish(self.topics.state, json.dumps(payload))
        print(f"[MQTT] Sent game state: {payload}")