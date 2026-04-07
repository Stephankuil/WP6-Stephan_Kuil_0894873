import pygame
import sys


class HomeScreen:
    def __init__(self, window, breedte, hoogte):
        self.window = window
        self.breedte = breedte
        self.hoogte = hoogte

        self.titel_font = pygame.font.SysFont(None, 80)
        self.knop_font = pygame.font.SysFont(None, 40)

        self.start_knop = pygame.Rect(breedte // 2 - 100, 250, 200, 60)
        self.stop_knop = pygame.Rect(breedte // 2 - 100, 340, 200, 60)

    def teken(self):
        self.window.fill((0, 0, 0))

        titel = self.titel_font.render("PACMAN", True, (255, 255, 0))
        titel_rect = titel.get_rect(center=(self.breedte // 2, 150))
        self.window.blit(titel, titel_rect)

        pygame.draw.rect(self.window, (255, 255, 0), self.start_knop)
        pygame.draw.rect(self.window, (200, 0, 0), self.stop_knop)

        start_text = self.knop_font.render("START", True, (0, 0, 0))
        stop_text = self.knop_font.render("AFSLUITEN", True, (255, 255, 255))

        self.window.blit(start_text, start_text.get_rect(center=self.start_knop.center))
        self.window.blit(stop_text, stop_text.get_rect(center=self.stop_knop.center))

        pygame.display.update()

    def run(self):
        while True:
            self.teken()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_knop.collidepoint(event.pos):
                        return "start"

                    if self.stop_knop.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()