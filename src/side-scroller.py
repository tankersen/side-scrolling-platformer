# tutorial being used: https://www.youtube.com/watch?v=6gLeplbqtqg
# i am first going through to follow the tutorial, then will be making changes once i create the base code
# i will outline the core changes i make as i go in the pseudo code
# asset folder currently has placeholders, i will be making different art

import os
import random
import math

import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Platformer")

bg_color = (255,255,255)
WIDTH, HEIGHT = 1920, 1080
fps = 60
player_velocity = 5
font = pygame.font.Font(None,74)

window = pygame.display.set_mode((WIDTH,HEIGHT))


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size,size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96,0, size, size)
    # ^ this picks which terrain tile on spread to use
    surface.blit(image,(0,0), rect)
    return pygame.transform.scale2x(surface)

class Player(pygame.sprite.Sprite):
    COLOR = (255,0,0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32,32, True)
    ANIMATION_DELAY = 3

    def __init__(self,x,y,width,height):
        super().__init__()
        self.rect = pygame.Rect (x,y,width,height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.health = 100
        self.is_alive = True
        self.go_background = pygame.image.load("assets/Background/Yellow.png")

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.count = 0
        

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True
        self.health = self.health - 25
        print(self.health)
        self.hit_count = 0

    def death(self):
        if self.health <= 0:
            self.is_alive = False
            return True
        return False
        
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
            
    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count/ fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 0.5:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"


        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = self.animation_count // self.ANIMATION_DELAY % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)


    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.image = pygame.Surface((width,height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self,win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x,y,size,size)
        block = get_block(size)
        self.image.blit(block,(0,0))
        self.mask = pygame.mask.from_surface(self.image)


class Trampoline(Object):
    ANIMATION_DELAY = 3

    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height, "trampoline")
        self.trampoline = load_sprite_sheets("Traps", "Trampoline", width, height)
        self.image = self.trampoline["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_sount = 0
        self.animation_name = "off"

    def off(self):
        self.animation_name = "off"

    def jump(self,player):
        self.animation_name = "Jump"
        player.y_vel = -player.GRAVITY * 10
        player.animation_count = 0
        player.jump_count = 1
        player.fall_count = 0

        

    def loop(self):
        sprites = self.trampoline[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY % len(sprites))
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect.topleft = (self.rect.x, self.rect.y)
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


class Fire(Object):
    ANIMATION_DELAY = 3


    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width,height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // 
                        self.ANIMATION_DELAY % len(sprites))
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

        


def get_background(name):
    image = pygame.image.load(join("assets","Background",name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image

def draw(window,background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)

    pygame.display.update()



def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head

            collided_objects.append(obj)

    return collided_objects

def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player,obj):
            collided = obj
            break
    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player,objects, -player_velocity*2)
    collide_right = collide(player, objects, player_velocity*2)


    if keys[pygame.K_a] and not collide_left:
        player.move_left(player_velocity)
    if keys[pygame.K_d] and not collide_right:
        player.move_right(player_velocity)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()
        if obj and obj.name == "trampoline":
            obj.jump(player) 


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")
    player_input_enabled = True
    player_is_alive = True

    block_size = 96

    player = Player(0,800, 50, 50)
    fire = Fire(200,HEIGHT - block_size - 64,16,32)
    fire.on()
    trampoline = Trampoline(100, HEIGHT - block_size - 64,16,64)
    trampoline.off()
    l_platform = [Block(block_size, HEIGHT-block_size * 3, block_size),Block(block_size*2, HEIGHT-block_size * 3, block_size)]
    floor = [Block(i*block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size, WIDTH * 2 // block_size)]
    objects = [*floor, trampoline, Block(0,HEIGHT - block_size * 2, block_size),  Block(block_size * 3, HEIGHT - block_size * 4, block_size),fire]


    offset_x = 0
    scroll_area_width = 200


#regulate framerate across devices
    run = True
    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if player_input_enabled:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player.jump_count < 2:
                        player.jump()


        if player.health <= 0 and player_is_alive:
            player_is_alive = False
            player_input_enabled = False  

        if not player_is_alive:
            player_input_enabled = False

            window.fill((0,255,255))

            game_over_text = font.render("GAME OVER", True, (255,0,0))
            game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            window.blit(game_over_text, game_over_rect)
            pygame.display.update()
            continue


        player.loop(fps)
        fire.loop()
        handle_move(player, objects)

        draw(window, background, bg_image, player, objects, offset_x)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or(
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel<0):
            offset_x += player.x_vel

if __name__ == "__main__":
    main(window)