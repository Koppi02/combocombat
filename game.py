import pygame
from settings import *
from import_characters import *
from charsel import CharacterSelection


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.fighters = import_characters()
        self.title_sound = pygame.mixer.Sound('./Sounds/title_sound.wav')
        self.ready_sound = pygame.mixer.Sound('./Sounds/ready.wav')
        self.fight_sound = pygame.mixer.Sound('./Sounds/fight.wav')

        # Intró
        self.last_count_update = pygame.time.get_ticks()
        self.score = [0, 0]  # score [P1,P2]
        self.round_over = False

        # háttér beállítás
        self.bg_image = pygame.image.load('./Maps/japan.png').convert_alpha()
        self.menu_image = pygame.image.load('./MenuArt.png').convert_alpha()

        self.health_image_width = 102
        self.health_image_height = 15
        self.health_image_scale = 3
        self.health_image = self.load_hud_sprite(
            './hpbar.png', self.health_image_width, self.health_image_height, 100, self.health_image_scale)

        self.stamina_image_width = 88
        self.stamina_image_height = 10
        self.stamina_image_scale = 3
        self.stamina_image = self.load_hud_sprite(
            './staminabar.png', self.stamina_image_width, self.stamina_image_height, 100, self.stamina_image_scale)

    pygame.display.set_caption('Combocombat')

    # Főmenü

    def start_menu(self):
        pygame.mixer.Sound.play(self.title_sound)
        menu_running = True
        while menu_running:

            self.draw_bg(self.menu_image)

            self.draw_centered_text('Combocombat', COUNT_FONT, BLACK,
                                    SCREEN_WIDTH / 2 + 5, SCREEN_HEIGHT / 3 + 5)
            self.draw_centered_text('Combocombat', COUNT_FONT, RED,
                                    SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            self.draw_centered_text('Press ENTER to Start', SCORE_FONT,
                                    BLACK, SCREEN_WIDTH / 2 + 2, SCREEN_HEIGHT / 2 + 2)
            self.draw_centered_text('Press ENTER to Start', SCORE_FONT,
                                    RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            self.draw_centered_text('Press ESC to Quit', SCORE_FONT,
                                    BLACK, SCREEN_WIDTH / 2 + 2, SCREEN_HEIGHT / 1.5 + 2)
            self.draw_centered_text('Press ESC to Quit', SCORE_FONT,
                                    RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.5)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        menu_running = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return False
            pygame.display.update()
        return True

    def winner_screen(self, winner):
        self.screen.fill(BLACK)
        self.draw_centered_text(f'{winner} wins the match', COUNT_FONT,
                                RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        self.draw_centered_text('Press ENTER to Play Again', SCORE_FONT,
                                WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.draw_centered_text('Press ESC to Return to Menu', SCORE_FONT,
                                WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.5)
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return 'restart'
                    elif event.key == pygame.K_ESCAPE:
                        return 'menu'

    # kiírja amit kell

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def draw_centered_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        text_rect = img.get_rect(center=(x, y))
        self.screen.blit(img, text_rect)

    # háttér kirajzolása

    def draw_bg(self, image):
        scaled_bg = pygame.transform.scale(
            image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(scaled_bg, (0, 0))

    # hp bar és stamina bar kirajzolása

    def load_hud_sprite(self, sprite_sheet, width, height, steps, scale):
        # extract képeket a sprite sheetből
        img = pygame.image.load(sprite_sheet).convert_alpha()
        progress_list = []
        for x in range(steps):
            frame = img.subsurface(0, x * height, width, height)
            progress_list.append(pygame.transform.scale(
                frame, (width * scale, height * scale)))
        return progress_list

    def draw_health_and_stamina_bar(self, health_image, health, max_health, stamina_image, stamina, max_stamina, x, y, flip):
        # hp bar
        health_ratio = int(health / max_health * 100) - \
            (int(health / max_health * 100) > 0)
        self.screen.blit(health_image[health_ratio], (x, y)) if flip == False else self.screen.blit(pygame.transform.flip(
            health_image[health_ratio], True, False), (x - self.health_image_width * self.health_image_scale, y))

        # stamina bar
        stamina_ratio = stamina / max_stamina
        stamina_y = y + self.health_image_height * self.health_image_scale
        stamina_ratio = int(stamina / max_stamina * 100) - \
            (int(stamina / max_stamina * 100) > 0)
        self.screen.blit(stamina_image[stamina_ratio], (x, stamina_y)) if flip == False else self.screen.blit(pygame.transform.flip(
            stamina_image[stamina_ratio], True, False), (x - self.stamina_image_width * self.stamina_image_scale, stamina_y))

    def set_fighters(self, selected_chars):
        fighter_1 = Fighter(1, SCREEN_WIDTH / 4, GROUND_LEVEL, False, self.fighters[selected_chars[0]].data, self.fighters[selected_chars[0]
                                                                                                                           ].sprite_sheet, self.fighters[selected_chars[0]].animation_steps, self.fighters[selected_chars[0]].thumbnail)
        fighter_2 = Fighter(2, SCREEN_WIDTH - SCREEN_WIDTH / 4 - 80 * width_scale, GROUND_LEVEL, True, self.fighters[selected_chars[1]].data, self.fighters[
                            selected_chars[1]].sprite_sheet, self.fighters[selected_chars[1]].animation_steps, self.fighters[selected_chars[1]].thumbnail)

        return fighter_1, fighter_2

    pygame.mixer.music.load("./Music/fight_music.wav")
