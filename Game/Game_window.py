import pygame
from sys import exit

game_breedte = 800
game_hoogte = 600
pygame.init()

window = pygame.display.set_mode((game_breedte, game_hoogte))

pygame.display.set_caption("Pacman")
klok = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    klok.tick(60)



