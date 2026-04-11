import pygame
from Home_screen import HomeScreen
from Game_window import GameWindow
from level import Levelmap
from Pacman import Pacman
from Game import Game1
from lobby_screen import LobbyScreen
from MQTT.gamemqtt import MQTTConfig, GameMQTT


def main():
    pygame.init()

    breedte = 850
    hoogte = 600

    window = pygame.display.set_mode((breedte, hoogte))
    pygame.display.set_caption("Pacman")

    home_screen = HomeScreen(window, breedte, hoogte)
    keuze = home_screen.run()

    if keuze != "start":
        pygame.quit()
        return

    lobby_screen = LobbyScreen(window, breedte, hoogte)
    lobby_result = lobby_screen.run()

    if lobby_result == "back":
        main()
        return

    mode, player_name, room_code = lobby_result

    print("Lobby result:")
    print("Mode:", mode)
    print("Player Name:", player_name)
    print("Room Code:", room_code)

    config = MQTTConfig(
        broker_host="4abaa784a435421ba0190c9884dd2b89.s1.eu.hivemq.cloud",
        broker_port=8883,
        username="Stephan",
        password="Geheimwachtwoord1"
    )

    mqtt_handler = GameMQTT(
        config=config,
        player_id=player_name,
        room_code=room_code,
        is_host=(mode == "host")
    )

    mqtt_handler.connect()
    mqtt_handler.send_join()

    waiting = True
    clock = pygame.time.Clock()

    while waiting:
        window.fill((0, 0, 0))

        font = pygame.font.SysFont(None, 50)
        small_font = pygame.font.SysFont(None, 35)

        title = font.render("WAITING LOBBY", True, (255, 255, 0))
        info1 = small_font.render(f"Mode: {mode}", True, (255, 255, 255))
        info2 = small_font.render(f"Player: {player_name}", True, (255, 255, 255))
        info3 = small_font.render(f"Room: {room_code}", True, (255, 255, 255))

        window.blit(title, title.get_rect(center=(breedte // 2, 120)))
        window.blit(info1, (250, 180))
        window.blit(info2, (250, 220))
        window.blit(info3, (250, 260))

        players_title = small_font.render("Players in room:", True, (0, 255, 255))
        window.blit(players_title, (250, 320))

        y_offset = 360
        for player in mqtt_handler.lobby_state.players:
            player_text = small_font.render(f"- {player}", True, (255, 255, 255))
            window.blit(player_text, (280, y_offset))
            y_offset += 35

        if mode == "host":
            info4 = small_font.render("Press ENTER to start game", True, (0, 255, 0))
        else:
            info4 = small_font.render("Waiting for host to start...", True, (0, 255, 0))

        info5 = small_font.render("Press ESC to go back", True, (255, 0, 0))

        window.blit(info4, (250, 500))
        window.blit(info5, (250, 540))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mqtt_handler.disconnect()
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mqtt_handler.disconnect()
                    main()
                    return

                if mode == "host" and event.key == pygame.K_RETURN:
                    mqtt_handler.send_start_game()
                    waiting = False

        if mode != "host" and mqtt_handler.start_game_received:
            waiting = False

        clock.tick(30)

    levelmap = Levelmap()

    pacman = Pacman(
        levens=3,
        Xcoordinaat=1,
        Ycoordinaat=1,
        score=0,
        kleur=(255, 255, 0),
        naam=player_name
    )

    game = Game1.Game(levelmap, pacman, mqtt_handler)
    game_window = GameWindow(window, breedte, hoogte, mqtt_handler)

    game_window.run(game)

    mqtt_handler.disconnect()
    pygame.quit()


if __name__ == "__main__":
    main()