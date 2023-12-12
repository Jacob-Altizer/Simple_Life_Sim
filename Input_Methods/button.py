import pygame

class Button:

    def __init__(self, color:tuple, width:int, height:int, text:str='', font:str='arial', text_color:tuple=(0, 0, 0)) -> None:
        
        self.color = color
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.text = text
        self.font = pygame.font.SysFont(font, (self.width // 3))
        if color != None:
            self.text_color = self.invert_color(self.color) if text_color == (0,0,0) else text_color # inverts text_color in relation to color if no text_color value is provided


    def draw(self, surface, x:int, y:int, border=None, border_width=2) -> None:
        # Draws button to surface
        self.x = x - self.width/2
        self.y = y - self.height/2

        if border:
            pygame.draw.rect(surface, border, (self.x - border_width, self.y - border_width, self.width + (border_width*2), self.height + (border_width*2)), 0)

        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0)

        if border != None:
            rendered_text = self.font.render(self.text, 1, self.text_color)
            pygame.Surface.blit(self.text, (self.x + (self.width/2 - rendered_text.get_width()/2), self.y + (self.height/2 - rendered_text.get_height()/2)))

        
    def is_clicked(self, position:list) -> bool:

        mouse_pos_x, mouse_pos_y = position[0], position[1]
        
        clicked = False
        bounds = {
            "left_extreme": self.x,
            "right_extreme": self.x + self.width,
            "top_extreme": self.y,
            "bottom_extreme": self.y + self.height
        }

        if ((mouse_pos_x >= bounds["left_extreme"]) and (mouse_pos_x <= bounds["right_extreme"])) and \
           ((mouse_pos_y >= bounds["top_extreme"]) and (mouse_pos_y <= bounds["bottom_extreme"])):

            clicked = True

        return clicked
        

    def invert_color(self, color_vals:tuple) -> tuple:
        # inverts an RGB color value
        WHITE:tuple = (255, 255, 255)
        
        inverted_color_val:tuple = (
            WHITE[0] - color_vals[0],
            WHITE[1] - color_vals[1],
            WHITE[2] - color_vals[2]
        )

        return inverted_color_val


class Img_Button(Button):
    
    def __init__(self, image_path:str, width:int, height:int):
        super().__init__(width=width, height=height, color=None)

        self.image_path = image_path
        self.x = 0
        self.y = 0

        self.image = pygame.image.load(self.image_path)

    def resize(self, image):
        self.image = pygame.transform.scale(image, (self.width, self.height))

    def draw(self, surface:pygame.Surface, x:int, y:int):
        self.x = x
        self.y = y
        
        self.resize(self.image)
        surface.blit(self.image, (self.x, self.y))

    def is_clicked(self, position) -> bool:
        return super().is_clicked(position)
    
    def invert_color(self, color_vals: tuple) -> tuple:
        return super().invert_color(color_vals)


class Roller_Button(Button):

    def __init__(self, color:tuple, width:int, height:int, text:str = '', font:str = 'arial', text_color:tuple = (0, 0, 0)) -> None:
        self.value = 0
        self.arrow_img = pygame.image.load("images/small_arrow.png")
        self.midline = self.height // 2

        super().__init__(color, width, height, text, font, text_color)


    def build_roller(self):
        pass


    def arrow_is_clicked(self, step:int, mouse_pos):

        if mouse_pos[1] > self.midline:
            

        if decrement:
            self.value -= step
        if increment:
            self.value += step


    def get_int_value(self) -> int:
        return self.value

