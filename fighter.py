import pygame
from settings import *
import math

class Fighter():
    # Dinamikus skálázási tényezők
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, thumbnail):
        self.player = player
        self.data = data
        self.name = data[0]
        self.thumbnail = thumbnail
        self.size = SPRITE_SIZE
        self.image_scale = SPRITE_SCALE
        self.offset = SPRITE_OFFSET
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  # 0: idle, 1: run, 2: jump, 3: attack1, 4: attack2, 5: hit, 6: death, 7: block
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        # Karakter téglalapja
        self.rect = pygame.Rect((x, y - COL_RECT_HEIGHT * height_scale, COL_RECT_WIDTH * width_scale, COL_RECT_HEIGHT * height_scale))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attacking_completed = False
        self.blocking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.max_health = data[1]
        self.health = self.max_health
        self.max_stamina = data[2]
        self.stamina = self.max_stamina
        self.stamina_regen_rate = 0.2
        self.dmg1 = data[3]
        self.dmg2 = data[4]
        self.alive = True
        self.sprite_sheet = sprite_sheet
        self.animation_steps = animation_steps

    def load_images(self, sprite_sheet, animation_steps):
        width_scale, height_scale = calculate_scaling_factor()
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                scaled_img = pygame.transform.scale(temp_img, (int(self.size * self.image_scale * width_scale),
                                                               int(self.size * self.image_scale * height_scale)))
                temp_img_list.append(scaled_img)
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        dx, dy = 0, 0
        self.running = False
        self.attack_type = 0

        # Billentyűk kezelése
        key = pygame.key.get_pressed()

        if self.attacking == False and self.alive == True and round_over == False:
            # 1. játékos mozgása
            if self.player == 1:
                if key[P1_LEFT] and not self.hit and not self.blocking:
                    dx = -SPEED
                    self.running = True
                if key[P1_RIGHT] and not self.hit and not self.blocking:
                    dx = SPEED
                    self.running = True
                if key[P1_JUMP] and not self.jump and not self.blocking:
                    self.vel_y = -40 * height_scale
                    self.jump = True
                if key[P1_ATK1] or key[P1_ATK2] and not self.hit:
                    self.attack(target)
                    if key[P1_ATK1]:
                        self.attack_type = 1
                    if key[P1_ATK2]:
                        self.attack_type = 2
                if key[P1_BLOCK] and self.stamina >= (self.dmg1 if self.attack_type == 1 else self.dmg2):
                    self.blocking = True
                else:
                    self.blocking = False

            # 2. játékos mozgása
            if self.player == 2:
                if key[P2_LEFT] and not self.hit and not self.blocking:
                    dx = -SPEED
                    self.running = True
                if key[P2_RIGHT] and not self.hit and not self.blocking:
                    dx = SPEED
                    self.running = True
                if key[P2_JUMP] and not self.jump and not self.blocking:
                    self.vel_y = -40 * height_scale
                    self.jump = True
                if (key[P2_ATK1] or key[P2_ATK2]) and not self.hit:
                    self.attack(target)
                    if key[P2_ATK1]:
                        self.attack_type = 1
                    if key[P2_ATK2]:
                        self.attack_type = 2
                if key[P2_BLOCK] and self.stamina >= (target.dmg1 if target.attack_type == 1 else target.dmg2):
                    self.blocking = True
                else:
                    self.blocking = False

        # Gravitáció alkalmazása
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Játékos a pályán belül marad
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right
        if self.rect.bottom + dy > GROUND_LEVEL:
            self.vel_y = 0
            self.jump = False
            dy = GROUND_LEVEL - self.rect.bottom


        # Egymás felé néznek
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # Collision másik játékossal
        if self.rect.colliderect(target.rect):
            dx = (-10*width_scale if self.flip == False else 10*width_scale) if self.jump else (-1*width_scale if self.flip == False else 1*width_scale)

        # Támadás visszaszámláló
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Játékos pozíciójának frissítése
        self.rect.x += dx
        self.rect.y += dy
    #animáció kezelése
    def update(self):
        # Ellenőrizd, hogy a játékos halott-e
        if not self.alive:
            self.update_action(6)  # Halott állapot
        elif self.health <= 0:
            self.health = 0
            self.alive = False
        elif self.hit and self.alive:  # Csak ha él, és eltalálták
            self.update_action(5)  # Találat animáció
            self.attacking = False  # Ha eltalálták, állítsd le a támadást
        elif self.attacking:
            if self.attack_type == 1:
                self.update_action(3)  # Támadás 1
            elif self.attack_type == 2:
                self.update_action(4)  # Támadás 2
        elif self.jump:
            self.update_action(2)  # Ugrás
        elif self.running:
            self.update_action(1)  # Futás
        elif self.blocking:
            self.update_action(7)  # Blokkolás
        else:
            self.update_action(0)  # Állás

        # Frissítjük a jelenlegi képet az animációs listából
        try: 
            self.image = self.animation_list[self.action][self.frame_index]
        except:
            print("Sprite index out of range.")
        
        # Animációs időzítés
        if pygame.time.get_ticks() - self.update_time > ANIMATION_SPEED:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # Ellenőrizzük, hogy az animáció végére értünk-e
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 5:  # Találat animáció
                self.hit = False  # Reseteljük a hit állapotot
            elif self.action in [3, 4]:  # Támadás animáció
                self.attacking = False  # Támadás befejezése
                self.attack_cooldown = 1  # Támadási időzítő
            elif self.action == 6:  # Halál animáció
                self.frame_index = len(self.animation_list[self.action]) - 1  # Maradjunk az utolsó frame-nél
            else:
                self.frame_index = 0  # Visszaállítjuk az indexet

    def attack(self, target):
        if self.attack_cooldown == 0 and self.stamina > (self.dmg1 if self.attack_type == 1 else self.dmg2):
            self.attacking = True
            self.stamina -= self.dmg1 if self.attack_type == 1 else self.dmg2
            attacking_rect = pygame.Rect(self.rect.centerx - (1.2 * self.rect.width * self.flip), self.rect.y, 1.2 * self.rect.width, self.rect.height)

            # Ellenőrizzük, hogy a támadás eltalálta-e a célt
            if attacking_rect.colliderect(target.rect):
                if target.blocking:
                    target.stamina -= self.dmg1 if self.attack_type == 1 else self.dmg2
                    print("Blocked")
                else:
                    if not target.hit:  # Csak akkor sebez, ha a target még nem kapott sebzést
                        target.health -= self.dmg1 if self.attack_type == 1 else self.dmg2
                        target.hit = True  # Beállítjuk a hit flaget a célnak


       # pygame.draw.rect(surface, (0,255,0), attacking_rect)

    def regen(self):
        # Stamina regenerálás a maximális stamina határáig
        if self.stamina < self.max_stamina and not self.attacking and not self.blocking:
            self.stamina += self.stamina_regen_rate

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        # pygame.draw.rect(surface, RED, self.rect)
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))