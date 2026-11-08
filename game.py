import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((896, 896))

MAP_WIDTH = 800
MAP_HEIGHT = 800
TILE_SIZE = 128

# GRASS IMAGE LOADING
grass_light = pygame.image.load('light_grass.png').convert_alpha()
grass_dark = pygame.image.load('dark_grass.png').convert_alpha()

grass_light = pygame.transform.scale(grass_light, (128, 128))
grass_dark = pygame.transform.scale(grass_dark, (128, 128))

map_data = []

for y in range(7):
    row = []
    for x in range(7):
        if (x + y) % 2 == 0:
            row.append(grass_light)
        else:
            row.append(grass_dark)
    map_data.append(row)

# CHEST IMAGE LOADING

tile_x = random.randint(0,6)
tile_y = random.randint(0,6)

# CHEST OPENED
chest_opened_img = pygame.image.load('chest_opened.png').convert_alpha()
chest_opened_img = pygame.transform.scale(chest_opened_img, (128, 128))

# CHEST CLOSED
chest_img = pygame.image.load('chest.png').convert_alpha()
chest_img = pygame.transform.scale(chest_img, (128, 128))

chest_rect = chest_img.get_rect()
chest_rect.center = (
    tile_x * TILE_SIZE + TILE_SIZE // 2,
    tile_y * TILE_SIZE + TILE_SIZE // 2
)

# CHEST MODIFIERS

chest_times = {
     "common": 2,
     "uncommon": 5,
     "rare": 10,
     "legendary": 15
}

chest_sfx = pygame.mixer.Sound("drum_buildup.mp3")

# CHEST ITEMS (COMMON)
wood_img = pygame.image.load('wood.png').convert_alpha()
wood_img = pygame.transform.scale(wood_img, (88, 88))
wood_key_img = pygame.image.load('wooden_key.png').convert_alpha()
wood_key_img = pygame.transform.scale(wood_key_img, (88, 88))


running = True

x = 250
y = 250
clock = pygame.time.Clock()

delta_time = 0.1

playing = False
chest_progress = 0
chest_opened = False
opened_timer = 0

item_first_time = {
    "wood": 0,
    "wooden key": 0
}

item_avaliable = 1
item_roll = 0
animation_time = 0

while running:
    animation_time += delta_time
    mouse_held = pygame.mouse.get_pressed()[0]
    screen.fill((255, 255, 255))

    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            screen.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))

    
 
    # CHEST DRAW
    if chest_opened == False:
        shake_x_chest = 0
        shake_y_chest = 0
        if mouse_held and chest_rect.collidepoint(pygame.mouse.get_pos()):
            shake_x_chest = random.randint(-3, 3)
            shake_y_chest = random.randint(-2, 2)
        screen.blit(chest_img, (chest_rect.x + shake_x_chest, chest_rect.y + shake_y_chest))
    else:
        movement_y_item = 0 
        screen.blit(chest_opened_img, chest_rect)
        if item_roll == 1:
            movement_y_item = math.sin(animation_time * 3) * 10
            screen.blit(wood_img, (chest_rect.x + 20, chest_rect.y - 30 + movement_y_item))

            

    # CHEST HELD
    if not chest_opened and mouse_held and chest_rect.collidepoint(pygame.mouse.get_pos()):
        chest_progress += delta_time
        print("Holding Chest!")


        if playing == False:
            pygame.mixer.Sound.play(chest_sfx)
            playing = True

    else: 
        if playing:
            chest_sfx.stop()
            playing = False
            chest_progress = 0

    # CHEST PROGRESS
    progress = chest_progress / chest_times["common"]
    progress = min(progress, 1)

    if not chest_opened and mouse_held and chest_rect.collidepoint(pygame.mouse.get_pos()):

        progress = chest_progress / chest_times["common"]
        progress = min(progress, 1)

        mouse_x, mouse_y, = pygame.mouse.get_pos()

        ring_rect = pygame.Rect(mouse_x - 25, mouse_y - 20, 50, 50)

        pygame.draw.arc(screen, (70, 70, 70), ring_rect,
                        0, math.pi * 2, 3)

        pygame.draw.arc(screen, (100, 200, 255), ring_rect,
                        math.pi / 2,
                        math.pi / 2 + (math.pi * 2 * progress), 3)

    # CHEST OPEN
    if chest_progress >= chest_times ["common"] and not chest_opened:
        print("Chest Opened!")
        item_roll = random.randint(0, item_avaliable)
        if item_roll == 0:
            print("NOTHING!")
            item_roll = 0
        chest_opened = True
        opened_timer = 0
        playing = False
        chest_progress = 0

    if chest_opened:
        opened_timer += delta_time

        if opened_timer >= 1:
            tile_x = random.randint(0,6)
            tile_y = random.randint(0,6)
            chest_rect.center = (
                tile_x * TILE_SIZE + TILE_SIZE // 2,
                tile_y * TILE_SIZE + TILE_SIZE // 2
            )
            item_roll = 0
            chest_opened = False


    for event in pygame.event.get():

        # QUIT
        if event.type == pygame.QUIT:
                    running = False

        # CLICK

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if chest_rect.collidepoint(event.pos):
                    print("Chest Clicked!")




    pygame.display.flip()

    delta_time = clock.tick(60) / 1000

pygame.quit()