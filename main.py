import pygame
from fighter import Fighter
from import_characters import *
from settings import *
from settings import intro_count

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Combocombat')

clock = pygame.time.Clock()

fighters = import_characters()

title_sound = pygame.mixer.Sound('./Sounds/title_sound.wav')
ready_sound = pygame.mixer.Sound('./Sounds/ready.wav')
fight_sound = pygame.mixer.Sound('./Sounds/fight.wav')

# Főmenü
def start_menu():
    pygame.mixer.Sound.play(title_sound)
    menu_running = True
    while menu_running:

        draw_bg(menu_image)


        draw_centered_text('Combocombat', COUNT_FONT, BLACK, SCREEN_WIDTH / 2 + 5, SCREEN_HEIGHT / 3 + 5)
        draw_centered_text('Combocombat', COUNT_FONT, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        draw_centered_text('Press ENTER to Start', SCORE_FONT, BLACK, SCREEN_WIDTH / 2 + 2, SCREEN_HEIGHT / 2 + 2)
        draw_centered_text('Press ENTER to Start', SCORE_FONT, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        draw_centered_text('Press ESC to Quit', SCORE_FONT, BLACK, SCREEN_WIDTH / 2 + 2, SCREEN_HEIGHT / 1.5 + 2)
        draw_centered_text('Press ESC to Quit', SCORE_FONT, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.5)

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
                        self.current_indices[0] = (self.current_indices[0] - 1) % len(self.fighters)
                    elif event.key == P1_RIGHT and self.selected_characters[0] is None:
                        self.current_indices[0] = (self.current_indices[0] + 1) % len(self.fighters)
                    elif event.key == P1_ATK1 and self.selected_characters[0] is None:
                        if self.selected_characters[0] is None:
                            self.selected_characters[0] = self.current_indices[0]
                            print(f"Player 1 selected fighter {self.current_indices[0]}")

                    # Player 2 controls (Arrow keys, Comma)
                    if event.key == P2_LEFT and self.selected_characters[1] is None:
                        self.current_indices[1] = (self.current_indices[1] - 1) % len(self.fighters)
                    elif event.key == P2_RIGHT and self.selected_characters[1] is None:
                        self.current_indices[1] = (self.current_indices[1] + 1) % len(self.fighters)
                    elif event.key == P2_ATK1 and self.selected_characters[1] is None:
                        if self.selected_characters[1] is None:
                            self.selected_characters[1] = self.current_indices[1]
                            print(f"Player 2 selected fighter {self.current_indices[1]}")

                    # Check if both players have selected their fighters
                    if all(character is not None for character in self.selected_characters):
                        self.draw() # Egy utolsó képfrissítés
                        # Wait for a moment before proceeding
                        pygame.time.delay(1000)  # Várakozás 1000 ms (1 másodperc)
                        selecting = False

            pygame.display.update()

        return self.selected_characters


    def draw(self):
        self.screen.fill((0, 0, 0))  # tiszta háttér

        # Player 1 képének megjelenítése
        fighter_1 = self.fighters[self.current_indices[0]]
        image_surface_1 = fighter_1.thumbnail  # Kép betöltése
        # Kép átméretezése, hogy a magassága megegyezzen a képernyő magasságával
        image_surface_1 = pygame.transform.scale(image_surface_1, (int(image_surface_1.get_width() * (self.screen_height / image_surface_1.get_height())), self.screen_height))
        self.screen.blit(image_surface_1, (0, 0))  # Kép elhelyezése a bal oldalon

        # Player 2 képének megjelenítése
        fighter_2 = self.fighters[self.current_indices[1]]
        image_surface_2 = pygame.transform.flip(fighter_2.thumbnail, True, False)  # Kép betöltése
        # Kép átméretezése, hogy a magassága megegyezzen a képernyő magasságával
        image_surface_2 = pygame.transform.scale(image_surface_2, (int(image_surface_2.get_width() * (self.screen_height / image_surface_2.get_height())), self.screen_height))
        self.screen.blit(image_surface_2, (self.screen.get_width() - image_surface_2.get_width(), 0))  # Kép elhelyezése a jobb oldalon

        # Keretek rajzolása, ha a karaktert kiválasztották
        if self.selected_characters[0] is not None:  # Ha az 1. játékos választott
            pygame.draw.rect(self.screen, (255, 255, 0), (0, 0, image_surface_1.get_width(), self.screen_height), 3)  # Sárga keret
        if self.selected_characters[1] is not None:  # Ha a 2. játékos választott
            pygame.draw.rect(self.screen, (0, 255, 0), (self.screen.get_width() - image_surface_2.get_width(), 0, image_surface_2.get_width(), self.screen_height), 3)  # Zöld keret

        # Indikátorok megjelenítése
        indicator_surface = self.font.render(fighter_1.name, True, (255, 255, 0))
        self.screen.blit(indicator_surface, (0, 0))
        
        indicator_surface = self.font.render(fighter_2.name, True, (0, 255, 0))
        self.screen.blit(indicator_surface, (self.screen.get_width() - self.font.size(fighter_2.name)[0], 0))

        pygame.display.flip()








def winner_screen(winner):
    screen.fill(BLACK)
    draw_centered_text(f'{winner} wins the match', COUNT_FONT, RED, SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 3 )
    draw_centered_text('Press ENTER to Play Again', SCORE_FONT, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    draw_centered_text('Press ESC to Return to Menu', SCORE_FONT, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.5)
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

# Intró
last_count_update = pygame.time.get_ticks()
score = [0, 0]#score [P1,P2]
round_over = False

#háttér beállítás
bg_image = pygame.image.load('./Maps/japan.png').convert_alpha()
menu_image = pygame.image.load('./MenuArt.png').convert_alpha()

#kiírja amit kell
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_centered_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    text_rect = img.get_rect(center=(x, y))
    screen.blit(img, text_rect)

#háttér kirajzolása
def draw_bg(image):
    scaled_bg = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#hp bar és stamina bar kirajzolása
def load_hud_sprite(sprite_sheet, width, height, steps, scale):
    #extract képeket a sprite sheetből
        img = pygame.image.load(sprite_sheet).convert_alpha()
        progress_list = []
        for x in range(steps):
            frame = img.subsurface(0, x * height, width, height)
            progress_list.append(pygame.transform.scale(frame, (width * scale, height * scale)))
        return progress_list

health_image_width = 102
health_image_height = 15
health_image_scale = 3
health_image = load_hud_sprite('./hpbar.png', health_image_width, health_image_height, 100, health_image_scale)

stamina_image_width = 88
stamina_image_height = 10
stamina_image_scale = 3
stamina_image = load_hud_sprite('./staminabar.png', stamina_image_width, stamina_image_height, 100, stamina_image_scale)

def draw_health_and_stamina_bar(health_image, health, max_health, stamina_image, stamina, max_stamina, x, y, flip):
    # hp bar
    health_ratio = int(health / max_health * 100) - (int(health / max_health * 100) > 0)
    screen.blit(health_image[health_ratio], (x, y)) if flip == False else screen.blit(pygame.transform.flip(health_image[health_ratio], True, False), (x - health_image_width * health_image_scale, y))

    #stamina bar
    stamina_ratio = stamina / max_stamina
    stamina_y = y + health_image_height * health_image_scale
    stamina_ratio = int(stamina / max_stamina * 100) - (int(stamina / max_stamina * 100) > 0)
    screen.blit(stamina_image[stamina_ratio], (x, stamina_y)) if flip == False else screen.blit(pygame.transform.flip(stamina_image[stamina_ratio], True, False), (x - stamina_image_width * stamina_image_scale, stamina_y))



def set_fighters():
    global fighter_1 
    global fighter_2
    fighter_1 = Fighter(1, SCREEN_WIDTH / 4, GROUND_LEVEL, False, fighters[selected_fighter_indices[0]].data, fighters[selected_fighter_indices[0]].sprite_sheet, fighters[selected_fighter_indices[0]].animation_steps, fighters[selected_fighter_indices[0]].thumbnail)
    fighter_2 = Fighter(2, SCREEN_WIDTH - SCREEN_WIDTH / 4 - 80 * width_scale, GROUND_LEVEL, True, fighters[selected_fighter_indices[1]].data, fighters[selected_fighter_indices[1]].sprite_sheet, fighters[selected_fighter_indices[1]].animation_steps, fighters[selected_fighter_indices[1]].thumbnail)

pygame.mixer.music.load("./Music/fight_music.wav")

# Játék Loop
while True:
    if start_menu():

        char_selection = CharacterSelection(screen, fighters, pygame.font.Font('./DoubleHomicide.ttf', 48))
        selected_fighter_indices = char_selection.run()

        if selected_fighter_indices is None:
            break

        set_fighters()

        score = [0, 0]
        intro_count = 4
        say_ready = True
        say_fight = True
        round_over = False

        run = True
        while run:
            clock.tick(FPS)
            draw_bg(bg_image)  # Háttér kirajzolása

            # Fighter frissítés és kirajzolás
            fighter_1.update()
            fighter_2.update()
            fighter_1.draw(screen)
            fighter_2.draw(screen)
            fighter_1.regen()
            fighter_2.regen()

            # HP bar, játékosok, stb. kirajzolása
            draw_health_and_stamina_bar(health_image, fighter_1.health, fighter_1.max_health, stamina_image, fighter_1.stamina, fighter_1.max_stamina, SCREEN_WIDTH / 50, SCREEN_HEIGHT / 30, False)
            draw_health_and_stamina_bar(health_image, fighter_2.health, fighter_2.max_health, stamina_image, fighter_2.stamina, fighter_2.max_stamina, SCREEN_WIDTH - SCREEN_WIDTH / 50, SCREEN_HEIGHT / 30, True)
            draw_text(f"{fighter_1.name}: " + str(score[0]), SCORE_FONT, RED, SCREEN_WIDTH / 50, SCREEN_HEIGHT / 30 + 75)
            draw_text(f"{fighter_2.name}: " + str(score[1]), SCORE_FONT, RED, SCREEN_WIDTH - SCREEN_WIDTH / 50 - SCORE_FONT.size(f"{fighter_2.name}: " + str(score[1]))[0], SCREEN_HEIGHT / 30 + 75)

            # Visszaszámláló logika
            if intro_count <= 0:
                fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
                fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
            else:
                if intro_count == 2:
                    draw_centered_text("READY", COUNT_FONT, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                    if say_ready:
                        pygame.mixer.Sound.play(ready_sound)
                        say_ready = False
                if intro_count == 1:
                    draw_centered_text("Fight", COUNT_FONT, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                    if say_fight:
                        pygame.mixer.Sound.play(fight_sound)
                        say_fight = False
                        pygame.mixer.music.set_volume(1)
                if (pygame.time.get_ticks() - last_count_update) >= 1000:
                    intro_count -= 1
                    last_count_update = pygame.time.get_ticks()
                if intro_count == 0:
                    pygame.mixer.music.play(-1)
                


            # Eseménykezelés
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Nézze meg ha valaki vesztett
            if not round_over:
                winner = ''
                if  fighter_1.alive == False or fighter_2.alive == False:
                    winner = fighter_2.name if fighter_1. alive == False else fighter_1.name
                    score[1 if fighter_1. alive == False else 0] += 1
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
                    pygame.mixer.music.fadeout(1000)

                else:

                    if score[0] >= WINNING_SCORE or score[1] >= WINNING_SCORE:
                        pygame.mixer.music.fadeout(1000)
                        result = winner_screen(fighter_1.name if score[0] > score[1] else fighter_2.name)
                        if result == 'restart':
                            score = [0, 0]
                            set_fighters()
                        elif result == 'menu':
                            score = [0, 0]
                            run = start_menu()
                        else:
                            run = False
                        continue
            else:
                draw_centered_text(f'{winner} wins!', COUNT_FONT, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                    round_over = False
                    intro_count = 4
                    say_ready = True
                    say_fight = True
                    set_fighters()

            # Frissíti a képet
            pygame.display.update()
    pygame.quit()