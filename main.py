import pygame
from fighter import Fighter
from import_characters import *
from settings import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Combocombat')

clock = pygame.time.Clock()

fighters = import_characters()

# Főmenü
def start_menu():
    pygame.mixer.music.load('./Music/menu_music.mp3')
    pygame.mixer.music.play(-1)
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
fighter_1 = Fighter(1, 200, 310, False, fighters[2].data, fighters[2].sprite_sheet, fighters[2].animation_steps)
fighter_2 = Fighter(2, 700, 310, True, fighters[1].data, fighters[1].sprite_sheet, fighters[1].animation_steps)

# Játék Loop
if start_menu():
    run = True
    while run:
        clock.tick(FPS)
        draw_bg(bg_image)  # Háttér kirajzolása

        # HP bar, játékosok, stb. kirajzolása
        draw_health_and_stamina_bar(fighter_1.health, fighter_1.max_health, fighter_1.stamina, fighter_1.max_stamina, 20, 20)
        draw_health_and_stamina_bar(fighter_2.health, fighter_2.max_health, fighter_2.stamina, fighter_2.max_stamina, 580, 20)
        draw_text(f"{fighter_1.name}: " + str(score[0]), SCORE_FONT, RED, 20, 80)
        draw_text(f"{fighter_2.name}: " + str(score[0]), SCORE_FONT, RED, 580, 80)

        # Visszaszámláló logika
        if intro_count <= 0:
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            draw_centered_text(str(intro_count), COUNT_FONT, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

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
        if round_over == False:
            winner = ''
            if fighter_1.alive == False:
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
            # screen.blit(victory_img, (360, 150))
            draw_centered_text(f'{winner} wins!', COUNT_FONT, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 3
                # Új harcosok inicializálása
                fighter_1 = Fighter(1, 200, 310, False, fighters[2].data, fighters[2].sprite_sheet, fighters[2].animation_steps)
                fighter_2 = Fighter(2, 700, 310, True, fighters[1].data, fighters[1].sprite_sheet, fighters[1].animation_steps)

        # Frissíti a képet
        pygame.display.update()


pygame.quit()
