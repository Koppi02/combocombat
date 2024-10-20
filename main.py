import pygame
from fighter import Fighter

pygame.init()
#ablak kreálás
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Combocombat')

#fps
clock = pygame.time.Clock()
FPS = 60

#színek megadása
YELLOW = (255,255,0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

#intro
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#score [P1,P2]
round_over = False
ROUND_OVER_COOLDOWN = 5000

#a harcosok változója
WARRIOR_SIZE = 128
WARRIOR_SCALE = 1.5
WARRIOR_OFFSET = [40, 20]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 128
WIZARD_SCALE = 1.5
WIZARD_OFFSET = [40, 20]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# importCharacters.import()

#háttér beállítás
bg_image = pygame.image.load('./Sprites/japan.png').convert_alpha()

#spritesheets
warrior_sheet = pygame.image.load('./Sprites/BSS.png').convert_alpha()
wizard_sheet = pygame.image.load('./Sprites/BSS.png').convert_alpha()

#victory
victory_img = pygame.image.load('./Sprites/victory.png').convert_alpha()

#megszámolni a lépéseket minden egyes animációban
WARRIOR_ANIMATION_STEPS = [53, 12, 16 , 15 , 15 , 12, 54, 1]
WIZARD_ANIMATION_STEPS = [53, 12, 16 , 15 , 15 , 12, 54, 1]

#font
count_font = pygame.font.Font('./turok.ttf', 80)
score_font = pygame.font.Font('./turok.ttf', 30)

#kiírja amit kell
def draw_text(text, font,text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#háttér kirajzolása
def draw_bg():
    scaled_bg =  pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#hp bar
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x-2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y , 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400*ratio, 30))


# TODO: karakter választó

# 2 db fighter
fighter_1 = Fighter(1,200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)
fighter_2 = Fighter(2,700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)



# játék loop
run = True
while run:

    clock.tick(FPS)

#háttér megrajzolása
    draw_bg()
# játékosnak mutassa a hp
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)


    #update visszaszámláló
    if intro_count <= 0:
        # fighter mozgatása
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
            print(intro_count)



#update fighter
    fighter_1.update()
    fighter_2.update()

#fighter rajzolása
    fighter_1.draw(screen)
    fighter_2.draw(screen)

#néze meg ha valaki vesztett
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        screen.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)
            fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)
    #event használó
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #frissíti a képet
    pygame.display.update()

pygame.quit()