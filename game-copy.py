import pygame
import os
import random
import csv

pygame.init()

clock = pygame.time.Clock()
fps = 60 



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 608

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Plataformer')

#define game variables

GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 19
COLS = 75
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 49
MAX_LEVELS = 2
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
game_paused = False
menu_state = "main"
clicked = False

# define player action variables
moving_left = False
moving_right = False
shoot = False


#Load images
#store tils in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tilesets/Tile_set_indimg/sprite_{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
#hearts
heart_img = pygame.image.load('img/icons/0.png').convert_alpha()
#bullet
bullet_img = pygame.image.load('img/icons/bullett.png').convert_alpha()
bullet_imgg = pygame.image.load('img/icons/bullett.png').convert_alpha()

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

#backround
bcimg = pygame.image.load('img/Backround/backgrounds/backround.png').convert_alpha()

#pickup boxes

health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
item_boxes = {
    'Health'    : health_box_img,
    'Ammo'      : ammo_box_img
}

#Define colors
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (102, 205, 0)
BLACK = (0, 0, 0)
BG2 = (125,38,205)

#define font

font = pygame.font.SysFont('Futura', 30) #Cambiar después la fuente

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
    

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
    
    #create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    
    return data


class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, an_col):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.an_col = an_col
        self.start_ammo =ammo
        self.shoot_cooldown = 0
        self.health = 100 #check min 27 from video 4 (maybe may enemies will need less health)x
        self.max_health = self.health
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
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
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
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    
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
            
    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)#0 is idle
                self.idling = True
                self.idling_counter = 50
            #check if the ai is near the player
            if self.vision.colliderect(player.rect):
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
                    if tile >= 1 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 25:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile >= 39 and tile <= 48:
                        decoration2 = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration2)
                    elif tile == 38:
                        player = Soldier('player', x * TILE_SIZE, y * TILE_SIZE, 1, 5, 20, 100)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                        bullet_bar = BulletBar(0, 40, 'img/icons/bullet_bar.png')
                    elif tile == 36: #create enemies
                        enemy = Soldier('enemy', x * TILE_SIZE, y * TILE_SIZE, 0.5, 2, 20, 300)
                        enemy_group.add(enemy)
                        #portal = Portal(600, 245, 4)
                    elif tile == 26: #create ammo_box
                        item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 37: #create health_box
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 27:#create exit
                        portal = Portal(x * TILE_SIZE, y * TILE_SIZE, 2)
                        portal_group.add(portal)
        
        return player, health_bar, bullet_bar
    
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
    def __init__(self, item_type, x, y,):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        
        
    def update(self):
        #scroll
        self.rect.x += screen_scroll
        #check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            #check what kind of box it was
            if self.item_type == 'Health':
                player.health +=20
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo +=15
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
            if player.alive:
                player.health -= 5
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False): #Video 4Revisar que tan necesario es realmente este codigo ya que mis enemigos no disparan
                if player.alive:
                    enemy.health -= 25
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

class BulletBar():
    def __init__(self, x, y, img):
        self.img = pygame.image.load(img)
        self.x = x
        self.y = y
    
    def draw(self):
        img = pygame.transform.scale(self.img, (32, 32))
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
start_button = Button(SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 - 100, play_img, 0.5)
exit_button = Button(SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2, exit_img, 0.5)
replay_button = Button(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 100, replay_img, 0.5)
resume_button = Button(304, 125, resume_img, 0.5)
options_button = Button(304, 250, options_img, 0.5)
exit_button2 = Button(304, 375, exit_img, 0.5)
keys_button = Button(304, 220, keys_img, 0.5)
audio_button = Button(304, 310, audio_img, 0.5)
video_button = Button(304, 400, video_img, 0.5)
back_button = Button(20, 530, back_img, 0.5)



#create sprite groups
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()

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

world = World()
player, health_bar, bullet_bar = world.process_data(world_data)


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
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
        #key button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False

    #check if game paused
    
    
    
    if start_game == False:
        #draw menu
        screen.fill(BG2)
        #add buttons
        if start_button.draw(screen):
            start_game = True
        if exit_button.draw(screen):
            run = False
    else:
    #update backround
        draw_bg()
        #draw world map
        world.draw()
        #show player_health
        health_bar.draw(player.health)
        #show ammo
        bullet_bar.draw()
        for x in range(player.ammo):
            screen.blit(bullet_imgg, (35 + (x * 15), 50))
        #draw_text('Health: ', font, WHITE, 10, 60)
        
        #loading player
        player.update()
        player.draw()

        
        #loading enemy
        for enemy in enemy_group:
            enemy.ai()
            enemy.draw()
            enemy.update()
        
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
        
        
        #update the player actions
        if player.alive:
            if game_paused == True:
                if menu_state == "main":
                    #draw pause screen buttons
                    screen.fill(BG2)
                    if resume_button.draw(screen) and clicked == False:
                        game_paused = False
                        clicked = True
                    if options_button.draw(screen) and clicked == False:
                        menu_state = "options"
                        clicked = True
                    if exit_button2.draw(screen) and clicked == False:
                        run = False
                        clicked = True
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
                    draw_text('Keys', font, WHITE, 200, 200)
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
            #shoot bullets
                if shoot:
                    player.shoot()
                if player.in_air:
                    player.update_action(2) # 2 means jump
                elif moving_left or moving_right:
                    player.update_action(1) # 1 means run
                else:
                    player.update_action(0) # 0 means idle
                screen_scroll, level_complete = player.move(moving_left, moving_right)
                bg_scroll -= screen_scroll
                #check if the player has completed the level
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
                        player, health_bar, bullet_bar = world.process_data(world_data)
                            
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
                player, health_bar, bullet_bar = world.process_data(world_data)
            
            
            
    pygame.display.update()
    
    clock.tick(fps)
            
pygame.quit()