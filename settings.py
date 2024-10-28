import pygame
pygame.init()
# Beállítások

# Alap felbontás beállítása
BASE_SCREEN_WIDTH = 1024
BASE_SCREEN_HEIGHT = 576

# Aktuális felbontás
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 576

def calculate_scaling_factor():
    width_scale = SCREEN_WIDTH / BASE_SCREEN_WIDTH
    height_scale = SCREEN_HEIGHT / BASE_SCREEN_HEIGHT
    return width_scale, height_scale

    # FPS
FPS = 60
    # Színek
YELLOW = (255,255,0)
RED = (150, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 40, 190)
BLACK = (0, 0, 0)
    # Betűtípusok
COUNT_FONT = pygame.font.Font('./DoubleHomicide.ttf', 80)
SCORE_FONT = pygame.font.Font('./DoubleHomicide.ttf', 30)
    # Játék Beállítások
intro_count = 3
ROUND_OVER_COOLDOWN = 5000
WINNING_SCORE = 3
    # Sprite Beállítások - Mostmár egységesnek kell lennie mindegyik karakternek (Mert miért lenne nem egységes?)
SPRITE_SIZE = 128
SPRITE_SCALE = 1.7
SPRITE_OFFSET = [40 * calculate_scaling_factor()[0], 20 * calculate_scaling_factor()[1]]
ANIMATION_SPEED = 75
    # Irányítás
P1_LEFT = pygame.K_a
P1_RIGHT = pygame.K_d
P1_JUMP = pygame.K_w
P1_ATK1 = pygame.K_r
P1_ATK2 = pygame.K_t
P1_BLOCK = pygame.K_z

P2_LEFT = pygame.K_LEFT
P2_RIGHT = pygame.K_RIGHT
P2_JUMP = pygame.K_UP
P2_ATK1 = pygame.K_COMMA
P2_ATK2 = pygame.K_PERIOD
P2_BLOCK = pygame.K_MINUS