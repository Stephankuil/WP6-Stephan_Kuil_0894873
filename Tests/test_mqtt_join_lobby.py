import os
import time
import uuid

from MQTT.gamemqtt import MQTTConfig, GameMQTT
import os
from dotenv import load_dotenv

load_dotenv()

def create_config():
    """
    Create MQTT configuration from environment variables.

    This keeps secrets out of the source code.
    """
    return MQTTConfig(
        broker_host=os.getenv("MQTT_BROKER_HOST"),
        broker_port=int(os.getenv("MQTT_BROKER_PORT", "8883")),
        username=os.getenv("MQTT_USERNAME"),
        password=os.getenv("MQTT_PASSWORD"),
    )


def test_4_players_can_join_real_broker():
    """
    Integration test:
    Check if 4 players can join the same lobby using the real MQTT broker.

    What this test does:
    - creates 4 MQTT clients
    - connects them to the real HiveMQ broker
    - all clients join the same room
    - checks whether the host sees all 4 players in the lobby

    Important:
    This test depends on real network timing, so we wait briefly after messages.
    """

    config = create_config()

    # Use a unique room code every test run so old broker messages do not interfere
    room_code = f"test-room-{uuid.uuid4().hex[:8]}"

    host = GameMQTT(
        config=config,
        player_id="host_player",
        room_code=room_code,
        is_host=True
    )

    player_2 = GameMQTT(
        config=config,
        player_id="player_2",
        room_code=room_code,
        is_host=False
    )

    player_3 = GameMQTT(
        config=config,
        player_id="player_3",
        room_code=room_code,
        is_host=False
    )

    player_4 = GameMQTT(
        config=config,
        player_id="player_4",
        room_code=room_code,
        is_host=False
    )

    clients = [host, player_2, player_3, player_4]

    try:
        # Connect all clients
        for client in clients:
            client.connect()

        # Give the broker a moment to finish connections/subscriptions
        time.sleep(2)

        # Send join messages one by one
        for client in clients:
            client.send_join()
            time.sleep(0.5)

        # Give time for all messages to propagate
        time.sleep(3)

        # Check if host sees all 4 players
        expected_players = {"host_player", "player_2", "player_3", "player_4"}
        actual_players = set(host.lobby_state.players)

        assert expected_players.issubset(actual_players), (
            f"Expected players {expected_players}, but host sees {actual_players}"
        )

        assert len(actual_players.intersection(expected_players)) == 4

    finally:
        # Always disconnect cleanly, even if the test fails
        for client in clients:
            try:
                client.disconnect()
            except Exception:
                pass