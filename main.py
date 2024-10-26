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
        self.current_player = 0
        self.font = font
        self.done = False
        self.current_index = 0
        self.character_count = len(fighters)



    def run(self):
        selecting = True
        while selecting:
            self.draw()  # Draw the selection screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.current_index = (self.current_index - 1) % self.character_count
                    elif event.key == pygame.K_DOWN:
                        self.current_index = (self.current_index + 1) % self.character_count
                    elif event.key == pygame.K_RETURN:
                        if self.selected_characters[self.current_player] is None:
                            # választás
                            self.selected_characters[self.current_player] = self.current_index
                            print(f"Player {self.current_player + 1} selected fighter {self.current_index}")
                            if self.current_player == 0:
                                self.current_player = 1  # Switch P2
                            else:
                                selecting = False  # mind a 2 választot
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return None

            pygame.display.update()

        return self.selected_characters

    def draw(self):
        self.screen.fill((0, 0, 0))  # tiszta háttér

        # kiírja a karaktereket és, hogy állnak
        for idx, fighter in enumerate(self.fighters):
            # milyen színe legyen a választotnak
            if idx == self.current_index:
                color = (255, 255, 0)  # citrom
                # egy négyzetet rajzol a választot mögé
                pygame.draw.rect(self.screen, (50, 50, 50), (80, 95 + idx * 40, 320, 50))  # szürke háttér
                # a választottat felnagyítja
                text_surface = self.font.render(f"{fighter.name}", True, color)
                text_surface = pygame.transform.scale(text_surface, (
                    int(text_surface.get_width() * 1.2), int(text_surface.get_height() * 1.2)))  # felnagyítás
            else:
                color = (255, 255, 255)  # fehér háttér
                text_surface = self.font.render(f"{fighter.name}", True, color)

            # nevek elhelyezése
            self.screen.blit(text_surface,(100, 90 + idx * 40))

        indicator_surface = self.font.render("Current Selection:", True, (255, 255, 0))
        self.screen.blit(indicator_surface, (100, 50))

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
bg_image = pygame.image.load('./Maps/testMap.png').convert_alpha()
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
def draw_health_and_stamina_bar(health, max_health, stamina, max_stamina, x, y):
    # hp bar
    health_ratio = health / max_health
    pygame.draw.rect(screen, WHITE, (x-2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y , 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400*health_ratio, 30))

    #stamina bar
    stamina_ratio = stamina / max_stamina
    pygame.draw.rect(screen, WHITE, (x-2, y + 40, 404, 20))
    pygame.draw.rect(screen, BLUE, (x, y + 40, 400*stamina_ratio, 20))

# Karakterek Kiválasztása
fighter_1 = Fighter(1, 200, 310, False, fighters[0].data, fighters[0].sprite_sheet, fighters[0].animation_steps)
fighter_2 = Fighter(2, 700, 310, True, fighters[1].data, fighters[1].sprite_sheet, fighters[1].animation_steps)

pygame.mixer.music.load("./Music/fight_music.wav")

# Játék Loop
while True:
    if start_menu():

        char_selection = CharacterSelection(screen, fighters, pygame.font.Font('./DoubleHomicide.ttf', 48))
        selected_fighter_indices = char_selection.run()

        if selected_fighter_indices is None:
            break

        fighter_1 = Fighter(1, 200, 310, False, fighters[selected_fighter_indices[0]].data,
                            fighters[selected_fighter_indices[0]].sprite_sheet,
                            fighters[selected_fighter_indices[0]].animation_steps)
        fighter_2 = Fighter(2, 700, 310, True, fighters[selected_fighter_indices[1]].data,
                            fighters[selected_fighter_indices[1]].sprite_sheet,
                            fighters[selected_fighter_indices[1]].animation_steps)

        score = [0, 0]
        intro_count = 4
        say_ready = True
        say_fight = True
        round_over = False

        run = True
        while run:
            clock.tick(FPS)
            draw_bg(bg_image)  # Háttér kirajzolása

            # HP bar, játékosok, stb. kirajzolása
            draw_health_and_stamina_bar(fighter_1.health, fighter_1.max_health, fighter_1.stamina, fighter_1.max_stamina, 20, 20)
            draw_health_and_stamina_bar(fighter_2.health, fighter_2.max_health, fighter_2.stamina, fighter_2.max_stamina, 580, 20)
            draw_text(f"{fighter_1.name}: " + str(score[0]), SCORE_FONT, RED, 20, 80)
            draw_text(f"{fighter_2.name}: " + str(score[1]), SCORE_FONT, RED, 580, 80)

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
                        # pygame.mixer.music.play(-1)
                if (pygame.time.get_ticks() - last_count_update) >= 1000:
                    intro_count -= 1
                    last_count_update = pygame.time.get_ticks()
                if intro_count == 0:
                    pygame.mixer.music.play(-1)
                

            # Fighter frissítés és kirajzolás
            fighter_1.update()
            fighter_2.update()
            fighter_1.draw(screen)
            fighter_2.draw(screen)
            fighter_1.regen()
            fighter_2.regen()

            # Eseménykezelés
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Nézze meg ha valaki vesztett
            if not round_over:
                winner = ''
                if  fighter_1.alive == False:
                    winner = fighter_2.name
                    score[1] += 1
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
                elif fighter_2.alive == False:
                    winner = fighter_1.name
                    score[0] += 1
                    round_over = True
                    round_over_time = pygame.time.get_ticks()

                else:

                    if score[0] >= WINNING_SCORE or score[1] >= WINNING_SCORE:
                        pygame.mixer.music.fadeout(1000)
                        result = winner_screen(fighter_1.name if score[0] > score[1] else fighter_2.name)
                        if result == 'restart':
                            score = [0, 0]
                            fighter_1 = Fighter(1, 200, 310, False, fighters[selected_fighter_indices[0]].data,
                                fighters[selected_fighter_indices[0]].sprite_sheet,
                                fighters[selected_fighter_indices[0]].animation_steps)
                            fighter_2 = Fighter(2, 700, 310, True, fighters[selected_fighter_indices[1]].data,
                                fighters[selected_fighter_indices[1]].sprite_sheet,
                                fighters[selected_fighter_indices[1]].animation_steps)
                        elif result == 'menu':
                            score = [0, 0]
                            run = start_menu()
                        else:
                            run = False
                        continue
            else:
                # screen.blit(victory_img, (360, 150))
                draw_centered_text(f'{winner} wins!', COUNT_FONT, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                    round_over = False
                    intro_count = 4
                    say_ready = True
                    say_fight = True
                    # Új harcosok inicializálása
                    fighter_1 = Fighter(1, 200, 310, False, fighters[selected_fighter_indices[0]].data,
                            fighters[selected_fighter_indices[0]].sprite_sheet,
                            fighters[selected_fighter_indices[0]].animation_steps)
                    fighter_2 = Fighter(2, 700, 310, True, fighters[selected_fighter_indices[1]].data,
                            fighters[selected_fighter_indices[1]].sprite_sheet,
                            fighters[selected_fighter_indices[1]].animation_steps)

            # Frissíti a képet
            pygame.display.update()
    pygame.quit()