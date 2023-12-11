import pygame
import math

class Sprite(pygame.sprite.Sprite):

    def get_image(sprite_sheet, x, y, sprite_width, sprite_height, scale):

        image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
        scaled_image = pygame.transform.scale(image, (sprite_width, sprite_height))
        image.blit(sprite_sheet, (x, y), (x, y, sprite_width, sprite_height))

        scaled_image = pygame.transform.scale(image, 
                                              (math.floor(sprite_width * scale), 
                                               math.floor(sprite_height * scale)))

        return scaled_image
    
class Bunny_Sprite(Sprite):

    BUNNY_SPRITE_WIDTH, BUNNY_SPRITE_HEIGHT = 371, 439
    SPRITE_SHEET_PX_OFFSET = 1

    bunny_sprite_sheet = pygame.image.load("images/bunnies.png")

    sprites = {
        "gray_bunny": 
        Sprite.get_image(bunny_sprite_sheet, 
                        0, 0, 
                        BUNNY_SPRITE_WIDTH, 
                        BUNNY_SPRITE_HEIGHT,
                        0.06),

        "light_brown_bunny": 
        Sprite.get_image(bunny_sprite_sheet, 
                        (BUNNY_SPRITE_WIDTH + SPRITE_SHEET_PX_OFFSET), 0, 
                        BUNNY_SPRITE_WIDTH, 
                        BUNNY_SPRITE_HEIGHT,
                        0.5),

        "white_bunny": 
        Sprite.get_image(bunny_sprite_sheet, 
                        0, (BUNNY_SPRITE_HEIGHT + SPRITE_SHEET_PX_OFFSET), 
                        BUNNY_SPRITE_WIDTH, 
                        BUNNY_SPRITE_HEIGHT,
                        0.5),

        "dark_brown_bunny": 
        Sprite.get_image(bunny_sprite_sheet, 
                        (BUNNY_SPRITE_WIDTH + SPRITE_SHEET_PX_OFFSET), (BUNNY_SPRITE_HEIGHT + SPRITE_SHEET_PX_OFFSET), 
                        BUNNY_SPRITE_WIDTH, 
                        BUNNY_SPRITE_HEIGHT,
                        0.5),
    }


class Rock_Sprite(Sprite):

    ROCK_SPRITE_WIDTH, ROCK_SPRITE_HEIGHT = 447, 383

    rock_sprite_sheet = pygame.image.load("images/rock.png")

    sprites = {
        "rock":
        Sprite.get_image(rock_sprite_sheet,
                        0, 0,
                        ROCK_SPRITE_WIDTH,
                        ROCK_SPRITE_HEIGHT,
                        0.04),
    }


class Plant_Sprite(Sprite):

    LONG_GRASS_SPRITE_WIDTH, LONG_GRASS_SPRITE_HEIGHT = 384, 288

    long_grass_sprite_sheet = pygame.image.load("images/long_grass.png")

    sprites = {
        "long_grass":
        Sprite.get_image(long_grass_sprite_sheet,
                        0, 0,
                        LONG_GRASS_SPRITE_WIDTH,
                        LONG_GRASS_SPRITE_HEIGHT,
                        0.05),
    }


Bunny_Sprite.sprites["gray_bunny"]
