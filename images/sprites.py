import pygame

class Sprite():

    def get_image(sprite_sheet, x, y, sprite_width, sprite_height):
        image = pygame.Surface((sprite_width, sprite_height)).convert_alpha()
        image.blit(sprite_sheet, (x, y), (x, y, sprite_width, sprite_height))

        return image
    
class Bunny_Sprite(Sprite):

    BUNNY_SPRITE_WIDTH, BUNNY_SPRITE_HEIGHT = 371, 439
    SPRITE_SHEET_PX_OFFSET = 1

    bunny_sprite_sheet = pygame.image.load("bunnies.png").convert_alpha()

    sprites = {
        "gray_bunny": 
        Sprite.get_image(bunny_sprite_sheet, 
                        0, 0, 
                        BUNNY_SPRITE_WIDTH, 
                        BUNNY_SPRITE_HEIGHT),

        "light_brown_bunny": 
        Sprite.get_image(bunny_sprite_sheet, 
                        (BUNNY_SPRITE_WIDTH + SPRITE_SHEET_PX_OFFSET), 0, 
                        BUNNY_SPRITE_WIDTH, 
                        BUNNY_SPRITE_HEIGHT),

        "white_bunny": 
        Sprite.get_image(bunny_sprite_sheet, 
                        0, (BUNNY_SPRITE_HEIGHT + SPRITE_SHEET_PX_OFFSET), 
                        BUNNY_SPRITE_WIDTH, 
                        BUNNY_SPRITE_HEIGHT),

        "dark_brown_bunny": 
        Sprite.get_image(bunny_sprite_sheet, 
                        (BUNNY_SPRITE_WIDTH + SPRITE_SHEET_PX_OFFSET), (BUNNY_SPRITE_HEIGHT + SPRITE_SHEET_PX_OFFSET), 
                        BUNNY_SPRITE_WIDTH, 
                        BUNNY_SPRITE_HEIGHT) 
    }

Bunny_Sprite.sprites["gray_bunny"]
