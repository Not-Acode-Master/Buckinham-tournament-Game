import pygame
import os
import random
import csv

pygame.init()

clock = pygame.time.Clock()
fps = 60



SCREEN_WIDTH = 766
SCREEN_HEIGHT = 576 #608

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Plataformer')

#define game variables

GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 12 #19
COLS = 26 #75
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 23 #49
MAX_LEVELS = 2
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
game_paused = False
menu_state = "main"
main_m_state = "principal"
clicked = False
shield_active = False

shooting = True

# define player action variables
moving_left = False
moving_right = False
shoot = False
crouch = False
grenade = False
grenade_thrown = False

gun1_active = True
gun2_active = False
change_gun = False

#Load images
#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tilesets/Tile_img/sprite_{x}.png')
    #img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
#hearts
heart_img = pygame.image.load('img/icons/0.png').convert_alpha()
#shield
shield_img1 = pygame.image.load('img/icons/shield.png').convert_alpha()
shield_img = pygame.transform.scale(shield_img1, (32, 32))
#bullet
bullet_img = pygame.image.load('img/icons/bullett.png').convert_alpha()
bullet_imgg = pygame.image.load('img/icons/bullett.png').convert_alpha()

bullet2_img = pygame.image.load('img/icons/bullet2.png').convert_alpha()
#grenade
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()
#Keybinding images
W_key = pygame.transform.scale(pygame.image.load('img/Key_icons/KEYS/W.png').convert_alpha(), (75,75))
A_key = pygame.transform.scale(pygame.image.load('img/Key_icons/KEYS/A.png').convert_alpha(), (75,75))
S_key = pygame.transform.scale(pygame.image.load('img/Key_icons/KEYS/S.png').convert_alpha(), (75,75))
D_key = pygame.transform.scale(pygame.image.load('img/Key_icons/KEYS/D.png').convert_alpha(), (75,75))
P_key = pygame.transform.scale(pygame.image.load('img/Key_icons/KEYS/P.png').convert_alpha(), (75,75))
SPACE_key = pygame.transform.scale(pygame.image.load('img/Key_icons/KEYS/SPACE.png').convert_alpha(), (118,75))
ESC_key = pygame.transform.scale(pygame.image.load('img/Key_icons/KEYS/ESC.png').convert_alpha(), (75,75))  



#Button Images
play_img = pygame.image.load('img//Buttons/play_button.png').convert_alpha()
exit_img = pygame.image.load('img//Buttons/exit_button.png').convert_alpha()
replay_img = pygame.image.load('img/Buttons/replay_button.png').convert_alpha()
resume_img = pygame.image.load('img//Buttons/resume_button.png').convert_alpha()
options_img = pygame.image.load('img//Buttons/options_button.png').convert_alpha()
menu_img = pygame.image.load('img//Buttons/menu_button.png').convert_alpha()
keys_img = pygame.image.load('img//Buttons/keys_button.png').convert_alpha()
video_img = pygame.image.load('img//Buttons/video_button.png').convert_alpha()
audio_img = pygame.image.load('img//Buttons/audio_button.png').convert_alpha()
back_img = pygame.image.load('img//Buttons/back_button.png').convert_alpha()
mainmenu_img = pygame.image.load('img//Buttons/mainmenu_button.png').convert_alpha()
instructions_img = pygame.image.load('img//Buttons/instructions_button.png').convert_alpha()
history_img = pygame.image.load('img//Buttons/history_button.png').convert_alpha()

#backround
bcimg = pygame.image.load('img/Backround/backgrounds/background.png').convert_alpha()

#pickup boxes

health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
#item_boxes = {
#    'Health'    : health_box_img,
#    'Ammo'      : ammo_box_img
#}

#Define colors
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (102, 205, 0)
BLACK = (0, 0, 0)
BLUE = (52, 21, 252)
BG2 = (125,38,205)

#define font

font = pygame.font.SysFont('Futura', 30) #Cambiar después la fuente
font2 = pygame.font.SysFont('Grand 9k Pixel Regular', 20) #Cambiar después la fuente

##Define History
history = '''The world as we know it has become unstable. The laws of physics have 
been distorted and strange anomalies are appearing everywhere. It is discovered that a man named Dr. Marcus,a brilliant but reclusive 
scientist,he has been conducting experiments that have caused this disruption.\n \nYou are an special agent
 with the purpose of infiltrating in Dr.Marcus's Lab to figure out what is he planning and end his misterious experiments'''
history_imglab =  pygame.transform.scale(pygame.image.load('img/Aditional_imgs/lab.png').convert_alpha(), (350,250))
##

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def display_history(surface, history, pos, font, color):
    collection = [word.split(' ')for word in history.splitlines()]
    space = font2.size(' ')[0]
    x,y = pos
    for lines in collection:
        for words in lines:
            word_surface = font.render(words, True, color)
            word_with, word_height = word_surface.get_size()
            if x + word_with >= 800:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x,y))
            x += word_with + space
        x = pos[0]
        y += word_height

def draw_bg():
    screen.fill(BG)
    width = bcimg.get_width()
    for x in range(5):
        screen.blit(bcimg, ((x * width) - bg_scroll, 0))
        
#func to reset level
def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    portal_group.empty()
    boss_group.empty()
    
    #create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    
    return data


class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, an_col, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.original_speed = speed
        self.speed = speed
        self.ammo = ammo
        self.grenades = grenades
        self.an_col = an_col
        self.start_ammo =ammo
        self.shoot_cooldown = 0
        self.health = 100 #check min 27 from video 4 (maybe may enemies will need less health)x
        self.max_health = self.health
        self.shield = 100
        self.max_shield = self.shield
        self.shield_can_use = True
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0

        #load all images for the players
        animation_types = ['Idle', 'Run', 'Jump', 'Death', 'Shield', 'Crouch', 'Idle2', 'Run2', 'Jump2', 'Death2', 'Shield2', 'Crouch2']
        for animation in animation_types:
            #reset temporary list of images
            temp_list = []
            #count the number of files in the folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    
    def update(self):
        self.update_animation()
        self.check_alive()
        self.check_paused()
        self.check_shield()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if crouch == True:
            player.speed = 0
        #if shield_active == True:
            #print('a')
    
    
    def move(self, moving_left, moving_right):
        #reset movement variable
        screen_scroll = 0
        
        dx = 0
        dy = 0
        
        #assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        
        #jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        
        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y
        
        #check for collision
        for tile in world.obstacle_list:
            #check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground i.e jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
        
        #check for collision with portal
        
        level_complete = False
        if pygame.sprite.spritecollide(self, portal_group, False):
            level_complete = True
        
        
        #check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0
        
        #check if going off the edges of the screen
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0
            
            
        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy
        
        #update scroll based on players position
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_lenght * TILE_SIZE) - SCREEN_WIDTH)\
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx
                
        return screen_scroll, level_complete
        
    def shoot(self): # revisar aproximadamente minuto 15 en adelante ya que probablemnte no se necesite para mis sprites
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.75 * player.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            #reduce ammo
            self.ammo -= 1
    def shoot2(self): # revisar aproximadamente minuto 15 en adelante ya que probablemnte no se necesite para mis sprites
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet2(self.rect.centerx + (0.75 * player.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            #reduce ammo
            self.ammo -= 1
            
    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)#0 is idle
                self.idling = True
                self.idling_counter = 50
            #check if the ai is near the player
            if self.vision.colliderect(player.rect) and shooting == True:
                #stop running and face the plyer
                self.update_action(0)
                #shoot
                self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)#1: run
                    self.move_counter += 1
                    #update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    #pygame.draw.rect(screen, RED, self.vision)aaaaaa
                    
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
        
        #scroll
        self.rect.x += screen_scroll
                
    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWON = self.an_col
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWON:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) -1
            else:
                self.frame_index = 0
        
    
    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
    
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
        
    def check_paused(self):
        if game_paused == True:
            self.speed = 0
        else:
            self.speed = self.original_speed
    
    def check_shield(self):
        if self.shield <= 0:
            self.shield_can_use = False
        if self.shield > 0:
            self.shield_can_use = True
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        
class Boss(pygame.sprite.Sprite):
    def __init__(self, boss_type, x, y, scale, speed, ammo, an_col, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.boss_type = boss_type
        self.original_speed = speed
        self.speed = speed
        self.ammo = ammo
        self.grenades = grenades
        self.an_col = an_col
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = False
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #specific variables for automatized movement
        self.move_counter = 0
        self.vision = pygame.rect.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0
        
        #load al the images
        animation_types = ['Idle', 'Death', 'Damaged', 'Ray', 'Run', 'Shield', 'Shoot', 'Shoot_chest']
        for animation in animation_types:
        #reset temporary list of images
            temp_list = []
            #count the number of file in the folder
            num_of_frames = len(os.listdir(f'img/{self.boss_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.boss_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    
    def update(self):
        self.update_animation()
        self.check_alive()
        self.check_paused()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1 ################# REVISARRRR
    
    def move(self, moving_left, moving_right):
        #reset movement variable
        
        dx = 0
        dy = 0
        
        #assegn movement variables if moveing left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction  = 1
        
        #jump 
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        
        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y
        
        #check for collision
        for tile in world.obstacle_list:
            #check for collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground i.e jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                    #check if above the ground
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
        
        #check for collision with portal
        # level_complete = False
        # if pygame.sprite.spritecollide(self, portal_group, False):
        #     level_complete = True
        
        #check if fallen of the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0
        
        #check if going of the edges of the screen:
        #CHECK CODE
        
        self.rect.x += dx
        self.rect.y += dy
        
    def basicshot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 40
            bullet = Bullet3(self.rect.centerx + (0.75 * player.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            #reduce ammo
            self.ammo -= 1
            
    def automove(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0) #0 is idle
                self.idling = True
                self.idling_counter = 50
            if self.vision.colliderect(player.rect) and shooting == True:
                #stop running and face the player
                self.update_action(6)
                #shoot
                self.basicshot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        boss_moving_right = True
                    else:
                        boss_moving_right = False
                    boss_moving_left = not boss_moving_right
                    self.move(boss_moving_left, boss_moving_right)
                    self.update_action(4) # 4 means run
                    self.move_counter += 1
                    #update boss vision as it moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    #pygame.draw.rect(screen, RED, self.vision)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
                        
        #scroll
        self.rect.x += screen_scroll
                    
            
    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = self.an_col
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since tha las frame
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out  the reset back to the start
        #if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 1:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
        
    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(1)
    
    def check_paused(self):
        if game_paused == True:
            self.speed = 0
        else:
            self.speed = self.original_speed
    
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
                
class World():
    def __init__(self):
        self.obstacle_list = []
        
    def process_data(self, data):
        self.level_lenght = len(data[0])
        #iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 4:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 5 and tile <= 14:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 19:
                        player = Soldier('player', x * TILE_SIZE, y * TILE_SIZE, 1.4, 5, 20, 100, 5)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                        bullet_bar = BulletBar(0, 40, 'img/icons/bullet_bar.png')
                        shield_bar = ShieldBar(220,10, player.shield, player.shield)
                        bombar = BombBar(5, 70,'img/icons/finalgrenade.png')
                    elif tile == 20: #create enemies
                        enemy = Soldier('enemy', x * TILE_SIZE, y * TILE_SIZE, 0.75, 2, 100, 300, 0)
                        enemy_group.add(enemy)
                        #portal = Portal(600, 245, 4)
                    elif tile == 16: #create ammo_box
                        item_box = ItemBox(x * TILE_SIZE, y * TILE_SIZE, 'Ammo', 1)
                        item_box_group.add(item_box)
                    elif tile == 17: #create health_box
                        item_box = ItemBox(x * TILE_SIZE, y * TILE_SIZE, 'Health', 1)
                        item_box_group.add(item_box)
                    elif tile == 22:#create exit
                        portal = Portal(x * TILE_SIZE, y * TILE_SIZE, 2)
                        portal_group.add(portal)
                    elif tile == 15:
                        item_box = ItemBox(x * TILE_SIZE, y * TILE_SIZE, 'Shield', 1)
                        item_box_group.add(item_box)
                    elif tile == 18:
                        item_box = ItemBox(x * TILE_SIZE, y * TILE_SIZE, 'Grenade', 1)
                        item_box_group.add(item_box)
                    elif tile == 21:
                        bossa = Boss('Boss1', x * TILE_SIZE, y * TILE_SIZE, 1, 2, 1000, 150, 0)
                        boss_group.add(bossa)
        
        return player, health_bar, bullet_bar, shield_bar, bombar
    
    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
    
class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y,):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        
    def update(self):
        self.rect.x += screen_scroll

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, x, y, type,scale):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.type = type
        for i in range(3):
            img = pygame.image.load(f'img/Boxes/{self.type}/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        
    def update_animation(self):
        ANIMATION_COOLDOWN = 325
        #update image depending on current frame
        self.image = self.animation_list[self.frame_index]
        #check if enought time has passed since the las updtes
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
       
        
        
    def update(self):
        #scroll
        self.update_animation()
        self.rect.x += screen_scroll
        #check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            #check what kind of box it was
            if self.type == 'Health':
                player.health +=20
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.type == 'Ammo':
                player.ammo +=15
            elif self.type == 'Shield':
                player.shield += 25
                if player.shield > player.max_shield:
                    player.shield = player.max_shield
            elif self.type == 'Grenade':
                player.grenades += 5
            #delete the itembox
            self.kill()



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        
    def update(self):
        #move the bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #check if bullet has gone of the screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill
        #check for collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        
        #check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive and shield_active == False:
                player.health -= 5
                self.kill()
            if player.alive and shield_active == True:
                if player.shield_can_use == True:
                    player.shield -=5
                    self.kill()
                if player.shield_can_use == False:
                    player.health -= 5
                    self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False) and enemy.alive: #Video 4Revisar que tan necesario es realmente este codigo ya que mis enemigos no disparan
                if player.alive:
                    enemy.health -= 25
                    self.kill()
        for bossa in boss_group:
            if pygame.sprite.spritecollide(bossa, bullet_group, False) and bossa.alive:
                if player.alive:
                    bossa.health -= 25
                    self.kill()

class Bullet2(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet2_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        
    def update(self):
        #move the bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #check if bullet has gone of the screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        if self.rect.right > player.rect.centerx + 100 or self.rect.left < player.rect.centerx - 100:
            self.kill()
        #check for collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        
        #check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive and shield_active == False:
                player.health -= 5
                self.kill()
            if player.alive and shield_active == True:
                if player.shield_can_use == True:
                    player.shield -=5
                    self.kill()
                if player.shield_can_use == False:
                    player.health -= 5
                    self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False) and enemy.alive: #Video 4Revisar que tan necesario es realmente este codigo ya que mis enemigos no disparan
                if player.alive:
                    enemy.health -= 50
                    self.kill()
class Bullet3(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet2_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        
    def update(self):
        #move the bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #check if bullet has gone of the screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill
        #check for collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        
        #check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive and shield_active == False:
                player.health -= 50
                self.kill()
            if player.alive and shield_active == True:
                if player.shield_can_use == True:
                    player.shield -= 50
                    self.kill()
                if player.shield_can_use == False:
                    player.health -= 50
                    self.kill()

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
        
    def draw(self, health):
        #update with new health
        self.health = health
        #calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 20))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 14))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150* ratio, 14))
        #heart_img = pygame.image.load('img/icons/0.png')
        #heart_img = pygame.transform.scale(heart_img, (36, 36))
        screen.blit(heart_img, (0, 3))

class ShieldBar():
    def __init__(self, x, y, shield, max_shield):
        self.x = x
        self.y = y
        self.shield = shield
        self.max_shield = max_shield
        
    def draw(self, shield):
        #update with new shield
        self.shield = shield
        #calculate shield ratio
        ratio = self.shield / self.max_shield
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 20))
        pygame.draw.rect(screen, WHITE, (self.x, self.y, 150, 14))
        pygame.draw.rect(screen, BLUE, (self.x, self.y, 150* ratio, 14))
        screen.blit(shield_img, (200, 5))

        

class BulletBar():
    def __init__(self, x, y, img):
        self.img = pygame.image.load(img)
        self.x = x
        self.y = y
    
    def draw(self):
        img = pygame.transform.scale(self.img, (32, 32))
        screen.blit(img, (self.x, self.y))

class BombBar():
    def __init__(self, x, y, img):
        self.img = pygame.image.load(img)
        self.x = x
        self.y = y
    
    def draw(self):
        img = pygame.transform.scale(self.img, (20, 36))
        screen.blit(img, (self.x, self.y))
        
class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(9):
            img = pygame.image.load(f'img/portal/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        
    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.frame_index]
        #check if enought time has passed since the las updtes
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    
    def draw(self):
        screen.blit(self.image, self.rect)
        
    def update(self):
        self.rect.x += screen_scroll
        self.update_animation()

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction
    
    def update(self):
        self.rect.x += screen_scroll
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y
        #check for collision with level
        for tile in world.obstacle_list:
            #check collision with walls
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
        
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                #check if below the ground, i.e thrown up
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground, i.e falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom
            
            
        #update grande position
        self.rect.x += dx
        self.rect.y += dy
        
        #countdown
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            #do damage to anyone that is nearby
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                    player.health -= 50
                
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                        enemy.health -= 50

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.imgs = []
        for num in range(0,12):
            img = pygame.image.load(f'img/explosions/exp_{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.imgs.append(img)
        self.frame_index = 0
        self.image = self.imgs[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    
    def update(self):
        self.rect.x += screen_scroll
        EXPLOSION_SPEED = 4
        #update explosion animation
        self.counter += 1
        
        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            #if the animation is complete then delete the explosion
            if self.frame_index >= len(self.imgs):
                self.kill()
            else:
                self.image = self.imgs[self.frame_index]
        

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def draw(self, surface):
        action = False
        
        #get mouse position
        pos = pygame.mouse.get_pos()
        
        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button
        surface.blit(self.image, (self.rect.x, self.rect.y))
        
        return action

#create buttons
start_button = Button(304, 125, play_img, 0.5)
exit_button = Button(304, 400, exit_img, 0.5)
replay_button = Button(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 100, replay_img, 0.5)
resume_button = Button(304, 125, resume_img, 0.5)
options_button = Button(304, 250, options_img, 0.5)
exit_button2 = Button(304, 500, exit_img, 0.5)
keys_button = Button(304, 220, keys_img, 0.5)
audio_button = Button(304, 310, audio_img, 0.5)
video_button = Button(304, 400, video_img, 0.5)
back_button = Button(20, 530, back_img, 0.5)
mainmenu_button = Button(304, 375, mainmenu_img, 0.5)
instructions_button = Button(304, 250, instructions_img, 0.5)
history_button = Button(304, 320 ,history_img, 0.5)



#create sprite groups
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()


#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
#load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
print(world_data)

world = World()
player, health_bar, bullet_bar, shield_bar, bombar = world.process_data(world_data)


run = True
while run:
    
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and player.alive:
                game_paused = True
                shooting = False
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_s and player.alive:
                crouch = True
                shield_active = True
            if event.key == pygame.K_q:
                grenade = True
                #grenade_thrown = False
            if event.key == pygame.K_1:
                gun2_active = False
                gun1_active = True
            if event.key == pygame.K_2:
                gun2_active = True
                gun1_active = False
            if event.key == pygame.K_ESCAPE:
                run = False
        #key button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_s:
                crouch = False
                shield_active = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False
            if event.key == pygame.K_SPACE:
                shoot = False
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False

    #check if game paused
    
    
    
    if start_game == False:
        #draw menu
        screen.fill(BG2)
        #add buttons
        if main_m_state == "principal":
            if start_button.draw(screen) and clicked == False:
                start_game = True
                clicked = True
            if exit_button.draw(screen) and clicked == False:
                run = False
                clicked = True
            if instructions_button.draw(screen) and clicked == False:
                main_m_state = "instructions"
                clicked = True
        if main_m_state == "instructions":
            if back_button.draw(screen) and clicked == False:
                main_m_state = "principal"
            if keys_button.draw(screen) and clicked == False:
                main_m_state = "controls"
                clicked = True
            if history_button.draw(screen) and clicked == False:
                main_m_state = "history"
                clicked = True
        if main_m_state == "controls":
            draw_text('CONTROLS', font2, BG, 320, 20)
            screen.blit(W_key,(50, 100))
            draw_text('JUMP', font2, WHITE, 150, 110)
            screen.blit(A_key,(50, 160))
            draw_text('MOVE LEFT', font2, WHITE, 150, 170)
            screen.blit(S_key,(50, 220))
            draw_text('CROUCH', font2, WHITE, 150, 230)
            screen.blit(D_key,(50, 280))
            draw_text('MOVE RIGHT', font2, WHITE, 150, 290)
            screen.blit(SPACE_key,(30, 380))
            draw_text('SHOOT', font2, WHITE, 170, 390)
            screen.blit(ESC_key,(350, 100))
            draw_text('QUIT GAME', font2, WHITE, 450, 110)
            screen.blit(P_key,(350, 160))
            draw_text('PAUSE', font2, WHITE, 450, 170)
            if back_button.draw(screen) and clicked == False:
                main_m_state = "instructions"
        if main_m_state == "history":
            display_history(screen, history, (20,20),font2, WHITE)
            screen.blit(history_imglab, (304,400))
            if back_button.draw(screen) and clicked == False:
                main_m_state = "instructions"
            
    else:
    #update backround
        draw_bg()
        #draw world map
        world.draw()
        #show player_health
        health_bar.draw(player.health)
        #show ammo
        bullet_bar.draw()
        #show shield
        shield_bar.draw(player.shield)
        #show bomb
        bombar.draw()
        
        for x in range(player.ammo):
            screen.blit(bullet_imgg, (35 + (x * 15), 50))
        for x in range(player.grenades):
            screen.blit(grenade_img, (35 + (x * 15), 75))
        #draw_text('Health: ', font, WHITE, 10, 60)
        
        #loading player
        player.update()
        player.draw()

        
        #loading enemy
        for enemy in enemy_group:
            enemy.ai()
            enemy.draw()
            enemy.update()
        
        for bossa in boss_group:
            bossa.automove()
            bossa.draw()
            bossa.update()
        
        #loading portal
        #portal.draw()
        #portal.update_animation()
        
        #update and raw groups
        bullet_group.update()
        bullet_group.draw(screen)
        item_box_group.update()
        item_box_group.draw(screen)
        decoration_group.update()
        decoration_group.draw(screen)
        portal_group.update()
        portal_group.draw(screen)
        grenade_group.update()
        grenade_group.draw(screen)
        explosion_group.update()
        explosion_group.draw(screen)
        
        
        #update the player actions
        if player.alive:
            if game_paused == True:
                if menu_state == "main":
                    #draw pause screen buttons
                    screen.fill(BG2)
                    if resume_button.draw(screen) and clicked == False:
                        game_paused = False
                        shooting = True
                        clicked = True
                    if options_button.draw(screen) and clicked == False:
                        menu_state = "options"
                        clicked = True
                    if exit_button2.draw(screen) and clicked == False:
                        run = False
                        clicked = True
                    if mainmenu_button.draw(screen) and clicked == False:
                        game_paused = False
                        start_game = False
                        clicked = True
                        bg_scroll = 0
                        shooting = True
                        world_data = reset_level()
                        #load in level data and create world
                        with open(f'level{level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        player, health_bar, bullet_bar, shield_bar, bombar = world.process_data(world_data)
                if menu_state == "options":
                    screen.fill(BG2)
                    if keys_button.draw(screen) and clicked == False:
                        menu_state = "keys"
                        clicked = True
                    if audio_button.draw(screen) and clicked == False:
                        menu_state = "audio"
                        clicked = True
                    if video_button.draw(screen) and clicked == False:
                        menu_state = "video"
                        clicked = True
                    if back_button.draw(screen) and clicked == False:
                        menu_state = "main"
                        clicked = True
                    #check if the options menu is open
                if menu_state == "keys":
                    screen.fill(BG2)
                    draw_text('CONTROLS', font2, BG, 320, 20)
                    screen.blit(W_key,(50, 100))
                    draw_text('JUMP', font2, WHITE, 150, 110)
                    screen.blit(A_key,(50, 160))
                    draw_text('MOVE LEFT', font2, WHITE, 150, 170)
                    screen.blit(S_key,(50, 220))
                    draw_text('CROUCH', font2, WHITE, 150, 230)
                    screen.blit(D_key,(50, 280))
                    draw_text('MOVE RIGHT', font2, WHITE, 150, 290)
                    screen.blit(SPACE_key,(30, 380))
                    draw_text('SHOOT', font2, WHITE, 170, 390)
                    screen.blit(ESC_key,(350, 100))
                    draw_text('QUIT GAME', font2, WHITE, 450, 110)
                    screen.blit(P_key,(350, 160))
                    draw_text('PAUSE', font2, WHITE, 450, 170)
                    if back_button.draw(screen) and clicked == False:
                        menu_state = "options"
                        clicked = True
                if menu_state == "audio":
                    screen.fill(BG2)
                    draw_text('Audio', font, WHITE, 200, 200)
                    if back_button.draw(screen) and clicked == False:
                        menu_state = "options"
                        clicked = True
                if menu_state == "video":
                    screen.fill(BG2)
                    draw_text('Video', font, WHITE, 200, 200)
                    if back_button.draw(screen) and clicked == False:
                        menu_state = "options"
                        clicked = True
            else:
                if gun1_active == True and gun2_active == False:
            #shoot bullets
                    if shoot:
                        player.shoot()
                    elif grenade and grenade_thrown == False and player.grenades > 0:
                        grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),\
                                    player.rect.top, player.direction)
                        grenade_group.add(grenade)
                        grenade_thrown = True
                        #reduce granades
                        player.grenades -= 1
                    if player.in_air:
                        player.update_action(2) # 2 means jump
                    if crouch and player.shield_can_use == True:
                        player.update_action(4)
                    elif crouch and player.shield_can_use == False:
                        player.update_action(5)
                    elif moving_left or moving_right:
                        player.update_action(1) # 1 means run
                    else:
                        player.update_action(0) # 0 means idle
                    screen_scroll, level_complete = player.move(moving_left, moving_right)
                    bg_scroll -= screen_scroll
                    #check if the player has completed the level
                if gun2_active == True and gun1_active == False:
                    if shoot:
                        player.shoot2()
                    elif grenade and grenade_thrown == False and player.grenades > 0:
                        grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),\
                                    player.rect.top, player.direction)
                        grenade_group.add(grenade)
                        grenade_thrown = True
                        #reduce granades
                        player.grenades -= 1
                    if player.in_air:
                        player.update_action(8) # 8 means jump2
                    if crouch and player.shield_can_use == True:
                        player.update_action(10)
                    elif crouch and player.shield_can_use == False:
                        player.update_action(11)
                    elif moving_left or moving_right:
                        player.update_action(7) # 7 means run2
                    else:
                        player.update_action(6) # 6 means idle2
                    screen_scroll, level_complete = player.move(moving_left, moving_right)
                    bg_scroll -= screen_scroll
                if level_complete:
                    level += 1
                    bg_scroll = 0
                    world_data = reset_level()
                    if level <= MAX_LEVELS:
                        #load in level data and create world
                        with open(f'level{level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        player, health_bar, bullet_bar, shield_bar, bombar = world.process_data(world_data)
                            
        else:
            screen_scroll = 0
            if replay_button.draw(screen):
                bg_scroll = 0
                #level = 1
                world_data = reset_level()
                #load in level data and create world
                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                player, health_bar, bullet_bar, shield_bar, bombar = world.process_data(world_data)
            
            
            
    pygame.display.update()
    
    clock.tick(fps)
            
pygame.quit()