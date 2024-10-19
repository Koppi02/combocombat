import pygame

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps):
        self.player = player
        self.size= data[0]
        self.image_scale = data[1]
        self.offset= data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0:áll 1:fut 2:ugrik 3:attack1 4:attack2 5:találat 6:halál
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180 ))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.blocking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True

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
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                #jump
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = - 30
                    self.jump = True

                #támadás
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(target)

                    #melyik támadást használod
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2

                #block
                if key[pygame.K_z]:
                    self.blocking = True
                else:
                    self.blocking = False

             # 2 játékos
            if self.player == 2:
                        # mozgás
                        if key[pygame.K_LEFT]:
                            dx = -SPEED
                            self.running = True
                        if key[pygame.K_RIGHT]:
                            dx = SPEED
                            self.running = True
                        # jump
                        if key[pygame.K_UP] and self.jump == False:
                            self.vel_y = - 30
                            self.jump = True

                        # támadás
                        if key[pygame.K_KP1] or key[pygame.K_KP2]:
                            self.attack(target)

                            # melyik támadást használod
                            if key[pygame.K_KP1]:
                                self.attack_type = 1
                            if key[pygame.K_KP2]:
                                self.attack_type = 2

                        #block
                        if key[pygame.K_KP3]:
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
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)#6: rip
        if self.hit == True:
            self.update_action(5) #5: eltaláltak
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)#3: attack típus 1
            elif self.attack_type == 2:
                self.update_action(4)#4: attack típus 2
        elif self.jump == True:
            self.update_action(2) #2:ugrik
        elif self.running == True:
            self.update_action(1) #1:fut
        else:
            self.update_action(0) #0:áll

        animation_cooldown = 60
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # check ha az animáció végzet
        if self.frame_index >= len(self.animation_list[self.action]):
            # nézze meg ha a játékos halott és akkor fejzze be az animációt
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action])-1
            else:
                self.frame_index = 0
                #nézze meg, hogy attacknak vége van e
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 50
                #nézze meg, hogy a hitnek vége van e
                if self.action == 5:
                    self.hit = False
                #miközben a játékos üt aközben megütnek, akkor megáll az ütés
                    self.attacking == False
                    self.attack_cooldown = 20


    def attack(self,  target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(self.rect.centerx - (2*self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect) and target.blocking == False:
                target.health -= 10
                target.hit = True 
            elif attacking_rect.colliderect(target.rect) and target.blocking == True:
                print("Blocked")
       # pygame.draw.rect(surface, (0,255,0), attacking_rect)

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