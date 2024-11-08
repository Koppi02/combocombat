import pygame
from settings import *


class CharacterSelection:
    def __init__(self, screen, fighters, font):
        self.screen = screen
        self.fighters = fighters
        self.selected_characters = [None, None]
        self.current_indices = [0, 0]  # Két játékos indexei
        self.font = font
        self.screen_height = self.screen.get_height()  # Képernyő magasságának beállítása

    def run(self):
        selecting = True
        while selecting:
            self.draw()  # Draw the selection screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

                if event.type == pygame.KEYDOWN:
                    # Player 1 controls (A, D, R)
                    if event.key == P1_LEFT and self.selected_characters[0] is None:
                        self.current_indices[0] = (
                            self.current_indices[0] - 1) % len(self.fighters)
                    elif event.key == P1_RIGHT and self.selected_characters[0] is None:
                        self.current_indices[0] = (
                            self.current_indices[0] + 1) % len(self.fighters)
                    elif event.key == P1_ATK1 and self.selected_characters[0] is None:
                        if self.selected_characters[0] is None:
                            self.selected_characters[0] = self.current_indices[0]
                            print(f"Player 1 selected fighter {
                                  self.current_indices[0]}")

                    # Player 2 controls (Arrow keys, Comma)
                    if event.key == P2_LEFT and self.selected_characters[1] is None:
                        self.current_indices[1] = (
                            self.current_indices[1] - 1) % len(self.fighters)
                    elif event.key == P2_RIGHT and self.selected_characters[1] is None:
                        self.current_indices[1] = (
                            self.current_indices[1] + 1) % len(self.fighters)
                    elif event.key == P2_ATK1 and self.selected_characters[1] is None:
                        if self.selected_characters[1] is None:
                            self.selected_characters[1] = self.current_indices[1]
                            print(f"Player 2 selected fighter {
                                  self.current_indices[1]}")

                    # Check if both players have selected their fighters
                    if all(character is not None for character in self.selected_characters):
                        self.draw()  # Egy utolsó képfrissítés
                        # Wait for a moment before proceeding
                        # Várakozás 1000 ms (1 másodperc)
                        pygame.time.delay(1000)
                        selecting = False

            pygame.display.update()

        return self.selected_characters

    def draw(self):
        self.screen.fill((0, 0, 0))  # tiszta háttér

        # Player 1 képének megjelenítése
        fighter_1 = self.fighters[self.current_indices[0]]
        image_surface_1 = fighter_1.thumbnail  # Kép betöltése
        # Kép átméretezése, hogy a magassága megegyezzen a képernyő magasságával
        image_surface_1 = pygame.transform.scale(image_surface_1, (int(image_surface_1.get_width(
        ) * (self.screen_height / image_surface_1.get_height())), self.screen_height))
        # Kép elhelyezése a bal oldalon
        self.screen.blit(image_surface_1, (0, 0))

        # Player 2 képének megjelenítése
        fighter_2 = self.fighters[self.current_indices[1]]
        image_surface_2 = pygame.transform.flip(
            fighter_2.thumbnail, True, False)  # Kép betöltése
        # Kép átméretezése, hogy a magassága megegyezzen a képernyő magasságával
        image_surface_2 = pygame.transform.scale(image_surface_2, (int(image_surface_2.get_width(
        ) * (self.screen_height / image_surface_2.get_height())), self.screen_height))
        self.screen.blit(image_surface_2, (self.screen.get_width(
        ) - image_surface_2.get_width(), 0))  # Kép elhelyezése a jobb oldalon

        # Keretek rajzolása, ha a karaktert kiválasztották
        # Ha az 1. játékos választott
        if self.selected_characters[0] is not None:
            pygame.draw.rect(self.screen, RED, (0, 0, image_surface_1.get_width(
            ), self.screen_height), 3)  # Sárga keret
        # Ha a 2. játékos választott
        if self.selected_characters[1] is not None:
            pygame.draw.rect(self.screen, BLUE, (self.screen.get_width(
                # Zöld keret
            ) - image_surface_2.get_width(), 0, image_surface_2.get_width(), self.screen_height), 3)

        # Indikátorok megjelenítése
        indicator_surface = self.font.render(fighter_1.name, True, RED)
        self.screen.blit(indicator_surface, (0, 0))

        indicator_surface = self.font.render(fighter_2.name, True, BLUE)
        self.screen.blit(indicator_surface, (self.screen.get_width(
        ) - self.font.size(fighter_2.name)[0], 0))

        pygame.display.flip()
