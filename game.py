import pygame
import random

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

chest_img = pygame.image.load('chest.png').convert_alpha()

chest_img = pygame.transform.scale(chest_img, (128, 128))

chest_rect = chest_img.get_rect()
chest_rect.center = (
    tile_x * TILE_SIZE + TILE_SIZE // 2,
    tile_y * TILE_SIZE + TILE_SIZE // 2
)

# CHEST LOAD TIMES

chest_times = {
     "common": 2,
     "uncommon": 5,
     "rare": 10,
     "legendary": 15
}

running = True

x = 250
y = 250
clock = pygame.time.Clock()

delta_time = 0.1

chest_progress = 0
chest_opened = False

while running:
    mouse_held = pygame.mouse.get_pressed()[0]
    screen.fill((255, 255, 255))

    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            screen.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))


 
    # CHEST DRAW
    if chest_opened == False:
        screen.blit(chest_img, chest_rect)

    # CHEST HELD
    if mouse_held and chest_rect.collidepoint(pygame.mouse.get_pos()):
        chest_progress += delta_time
        print("Holding Chest!")

    # CHEST OPEN
    if chest_progress >= chest_times ["common"]:
        print("Chest Opened!")
        chest_opened = True
        chest_progress = 0
        tile_x = random.randint(0,6)
        tile_y = random.randint(0,6)
        chest_rect.center = (
            tile_x * TILE_SIZE + TILE_SIZE // 2,
            tile_y * TILE_SIZE + TILE_SIZE // 2
        )
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