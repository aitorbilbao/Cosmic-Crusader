import pygame
from UI import import_folder

#This two classes will be the basis for all tiles (static and animated)

class Tile(pygame.sprite.Sprite):
    def __init__(self,x,y,size, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)  # Load the image from the provided path
        self.image = pygame.transform.scale(self.image, (size, size))  # Resize the image to match the tile size
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self,x_shift):
        self.rect.x += x_shift


class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size,x,y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        #we run through all images to create an animation, then we loop it
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self,shift):
        self.animate()
        self.rect.x += shift
        


