import pygame
from settings import *

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps):
        self.player = player
        self.data = data
        self.size= data[0]
        self.image_scale = data[1]
        self.offset= data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0:áll 1:fut 2:ugrik 3:attack1 4:attack2 5:találat 6:halál 7:blokk
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180 ))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attacking_completed = False
        self.blocking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.health = 100
        self.stamina = 100
        self.max_stamina = 100
        self.stamina_regen_rate = 0.2
        self.block_uses = 3
        self.max_block_uses = 3
        self.block_regen_time = 1000
        self.last_block_time = 0
        self.block_stamina_cost = 10
        self.alive = True
        self.sprite_sheet = sprite_sheet
        self.animation_steps = animation_steps

    def load_images(self, sprite_sheet, animation_steps):
        #extract képeket a sprite sheetből
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list
#1.08.21

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # billenytű használat
        key = pygame.key.get_pressed()

        #csak akkor tudsz mést csinálni ha nem támadsz
        if self.attacking == False and self.alive == True and round_over == False:
            # 1 játékos
            if self.player == 1:
                #mozgás
                if key[P1_LEFT] and self.hit == False and self.blocking == False:
                    dx = -SPEED
                    self.running = True
                if key[P1_RIGHT] and self.hit == False and self.blocking == False:
                    dx = SPEED
                    self.running = True
                #jump
                if key[P1_JUMP] and self.jump == False and self.blocking == False:
                    self.vel_y = - 30
                    self.jump = True

                #támadás
                if key[P1_ATK1] or key[P1_ATK2]:
                    self.attack(target)

                    #melyik támadást használod
                    if key[P1_ATK1]:
                        self.attack_type = 1
                    if key[P1_ATK2]:
                        self.attack_type = 2

                #block
                if key[P1_BLOCK] and self.stamina >= 20:
                    self.blocking = True
                else:
                    self.blocking = False

             # 2 játékos
            if self.player == 2:
                        # mozgás
                        if key[P2_LEFT] and self.hit == False and self.blocking == False:
                            dx = -SPEED
                            self.running = True
                        if key[P2_RIGHT] and self.hit == False and self.blocking == False:
                            dx = SPEED
                            self.running = True
                        # jump
                        if key[P2_JUMP] and self.jump == False and self.blocking == False:
                            self.vel_y = - 30
                            self.jump = True

                        # támadás
                        if key[P2_ATK1] or key[P2_ATK2]:
                            self.attack(target)

                            # melyik támadást használod
                            if key[P2_ATK1]:
                                self.attack_type = 1
                            if key[P2_ATK2]:
                                self.attack_type = 2

                        #block
                        if key[P2_BLOCK] and self.stamina >= 20:
                            self.blocking = True
                        else:
                            self.blocking = False

        #gravitáció használata
        self.vel_y += GRAVITY
        dy += self.vel_y


        #a játékos maradjon a pályán
        if self.rect.left + dx < 0:
            dx = - self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height -110 -self.rect.bottom

        #egymás felé néznek
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # attack visszaszámláló
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1


        #frissit a játékos pozicióját
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
        self.image = self.animation_list[self.action][self.frame_index]
        
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
        if self.attack_cooldown == 0 and self.stamina > 20:
            self.attacking = True
            self.stamina -= 20
            attacking_rect = pygame.Rect(self.rect.centerx - (1.2 * self.rect.width * self.flip), self.rect.y, 1.2 * self.rect.width, self.rect.height)

            # Ellenőrizzük, hogy a támadás eltalálta-e a célt
            if attacking_rect.colliderect(target.rect):
                if target.blocking:
                    target.stamina -= 20
                    print("Blocked")
                else:
                    if not target.hit:  # Csak akkor sebez, ha a target még nem kapott sebzést
                        target.health -= 10
                        target.hit = True  # Beállítjuk a hit flaget a célnak
                
                # Támadó játékos sebzése (ha a target is támad)
                if target.attacking and not self.hit:
                    self.health -= 10  # Támadó játékos sebzése
                    self.hit = True  # Beállítjuk a hit flaget a támadónak
            
            self.attack_cooldown = 0  # Beállítjuk a támadási időzítőt


       # pygame.draw.rect(surface, (0,255,0), attacking_rect)
    #def attack_anim_end(self):
     #   self.attacking = False

    def regen(self):
        if self.stamina < self.max_stamina and not self.attacking and not self.blocking:
            self.stamina += self.stamina_regen_rate

        if pygame.time.get_ticks() - self.last_block_time > self.block_regen_time and self.block_uses < self.max_block_uses:
            self.block_uses = self.max_block_uses

    def update_action(self, new_action):
    #nézze meg hogy más e az action
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
       # pygame.draw.rect(surface, (250, 0, 0), self.rect)
        surface.blit(img, (self.rect.x -  (self.offset[0]*self.image_scale), self.rect.y - (self.offset[1]*self.image_scale)))