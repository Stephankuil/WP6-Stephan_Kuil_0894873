import json
import ssl
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional

import paho.mqtt.client as mqtt


@dataclass(frozen=True)
class MQTTConfig:
    broker_host: str
    broker_port: int
    username: str
    password: str


@dataclass(frozen=True)
class RoomTopics:
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
    players: List[str] = field(default_factory=list)
    host_player: Optional[str] = None
    game_started: bool = False

    def add_player(self, player_id: str) -> None:
        if player_id not in self.players:
            self.players.append(player_id)

    def remove_player(self, player_id: str) -> None:
        if player_id in self.players:
            self.players.remove(player_id)

    def set_host_if_missing(self, player_id: str) -> None:
        if self.host_player is None:
            self.host_player = player_id


@dataclass
class PlayerState:
    player_id: str
    x: int
    y: int
    direction: str = "stop"
    score: int = 0
    lives: int = 3

    def to_dict(self) -> Dict:
        return asdict(self)


class MQTTMessageFactory:
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
    def create_game_state_message(players_state: Dict[str, Dict]) -> Dict:
        return {
            "players": players_state
        }


class GameMQTT:
    def __init__(self, config: MQTTConfig, player_id: str, room_code: str, is_host: bool):
        self.config = config
        self.player_id = player_id
        self.room_code = room_code
        self.is_host = is_host

        self.topics = RoomTopics(room_code)
        self.lobby_state = LobbyState()

        # Alleen host gebruikt deze queue echt actief
        self.received_inputs: List[Dict] = []

        # Deze state bevat alle spelers in de game
        # host: bron van waarheid
        # client: laatst ontvangen state van host
        self.players_state: Dict[str, Dict] = {}

        self.start_game_received = False

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
        self.client.connect(self.config.broker_host, self.config.broker_port)
        self.client.loop_start()

    def disconnect(self) -> None:
        self.send_leave()
        self.client.loop_stop()
        self.client.disconnect()

    # ---------------------------------------------------------
    # MQTT CALLBACKS
    # ---------------------------------------------------------

    def on_connect(self, client, userdata, flags, rc) -> None:
        print(f"[MQTT] Connected with result code: {rc}")

        if rc != 0:
            print("[MQTT] Connection failed.")
            return

        print("[MQTT] Connection successful.")

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
        print(f"[MQTT] Disconnected with result code: {rc}")

    def on_message(self, client, userdata, msg) -> None:
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
        player_id = data.get("player_id")
        is_host = data.get("is_host", False)

        if not player_id:
            return

        self.lobby_state.add_player(player_id)

        if is_host:
            self.lobby_state.host_player = player_id
        else:
            self.lobby_state.set_host_if_missing(player_id)

        if self.is_host:
            self.add_player_to_game(player_id)
            self.send_lobby_state()

        print(f"[MQTT] Player joined lobby: {player_id}")
        print(f"[MQTT] Players now: {self.lobby_state.players}")
        print(f"[MQTT] Host: {self.lobby_state.host_player}")

    def _handle_leave_message(self, data: Dict) -> None:
        player_id = data.get("player_id")

        if not player_id:
            return

        self.lobby_state.remove_player(player_id)

        if self.is_host:
            self.remove_player_from_game(player_id)
            self.send_lobby_state()

        print(f"[MQTT] Player left lobby: {player_id}")
        print(f"[MQTT] Players now: {self.lobby_state.players}")

    def _handle_lobby_state_message(self, data: Dict) -> None:
        players = data.get("players", [])
        host_player = data.get("host_player")

        self.lobby_state.players = players
        self.lobby_state.host_player = host_player

        print(f"[MQTT] Lobby state updated: {self.lobby_state.players}")
        print(f"[MQTT] Host player: {self.lobby_state.host_player}")

    def _handle_start_game_message(self, data: Dict) -> None:
        self.lobby_state.game_started = True
        self.start_game_received = True

        started_by = data.get("started_by", "unknown")
        print(f"[MQTT] Start game received from: {started_by}")

    def _handle_input_message(self, data: Dict) -> None:
        # Alleen host hoeft input op te slaan om te verwerken
        if self.is_host:
            self.received_inputs.append(data)

    def _handle_game_state_message(self, data: Dict) -> None:
        self.players_state = data.get("players", {})
        print(f"[MQTT] Players state updated: {self.players_state}")

    # ---------------------------------------------------------
    # GAME STATE HELPERS
    # ---------------------------------------------------------

    def add_player_to_game(self, player_id: str) -> None:
        if player_id in self.players_state:
            return

        spawn_positions = [
            (5, 5),
            (7, 5),
            (9, 5),
            (11, 5)
        ]

        index = len(self.players_state)
        if index < len(spawn_positions):
            spawn_x, spawn_y = spawn_positions[index]
        else:
            spawn_x = 5 + (index * 2)
            spawn_y = 5

        player = PlayerState(
            player_id=player_id,
            x=spawn_x,
            y=spawn_y
        )

        self.players_state[player_id] = player.to_dict()

    def remove_player_from_game(self, player_id: str) -> None:
        if player_id in self.players_state:
            del self.players_state[player_id]

    def pop_received_inputs(self) -> List[Dict]:
        inputs = self.received_inputs[:]
        self.received_inputs.clear()
        return inputs

    def set_player_direction(self, player_id: str, direction: str) -> None:
        if player_id not in self.players_state:
            return

        self.players_state[player_id]["direction"] = direction

    def move_player(self, player_id: str, dx: int, dy: int) -> None:
        if player_id not in self.players_state:
            return

        self.players_state[player_id]["x"] += dx
        self.players_state[player_id]["y"] += dy

    def get_local_player(self) -> Optional[Dict]:
        return self.players_state.get(self.player_id)

    def get_remote_players(self) -> Dict[str, Dict]:
        return {
            pid: pdata
            for pid, pdata in self.players_state.items()
            if pid != self.player_id
        }

    def build_game_state(self) -> Dict:
        return MQTTMessageFactory.create_game_state_message(self.players_state)

    # ---------------------------------------------------------
    # PUBLIC SEND METHODS
    # ---------------------------------------------------------

    def send_join(self) -> None:
        payload = MQTTMessageFactory.create_join_message(
            player_id=self.player_id,
            is_host=self.is_host
        )

        self.client.publish(self.topics.join, json.dumps(payload))
        print(f"[MQTT] Sent join message: {payload}")

    def send_leave(self) -> None:
        payload = MQTTMessageFactory.create_leave_message(self.player_id)

        self.client.publish(self.topics.leave, json.dumps(payload))
        print(f"[MQTT] Sent leave message: {payload}")

    def send_lobby_state(self) -> None:
        payload = MQTTMessageFactory.create_lobby_state_message(
            players=self.lobby_state.players,
            host_player=self.lobby_state.host_player
        )

        self.client.publish(self.topics.lobby_state, json.dumps(payload))
        print(f"[MQTT] Sent lobby state: {payload}")

    def send_start_game(self) -> None:
        payload = MQTTMessageFactory.create_start_game_message(self.player_id)

        self.client.publish(self.topics.start_game, json.dumps(payload))
        print(f"[MQTT] Sent start game message: {payload}")

    def send_input(self, direction: str) -> None:
        payload = MQTTMessageFactory.create_input_message(
            player_id=self.player_id,
            direction=direction
        )

        self.client.publish(self.topics.input, json.dumps(payload))
        print(f"[MQTT] Sent input: {payload}")

    def send_game_state(self) -> None:
        payload = self.build_game_state()

        self.client.publish(self.topics.state, json.dumps(payload))
        print(f"[MQTT] Sent game state: {payload}")