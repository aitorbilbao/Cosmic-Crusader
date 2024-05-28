import pygame
from UI import import_folder

#Using the Tile setup, we create the Object class
class Object(pygame.sprite.Sprite):
    def __init__(self,x,y,surface,status):
        super().__init__()
        self.import_assets()
        self.frame_index = 0
        self.amimation_speed = 0.15
        self.status = status
        self.image = self.animations[self.status][self.frame_index]
        offset_x = 0
        offset_y = 0

        #Create an offset depending on image loaded, so it looks centered
        if status == 'coin':
            offset_x = 25
            offset_y = 32
            self.value = 1
        if status == 'diamond':
            offset_x = 22.5
            offset_y = 32
            self.value = 5
        if status == 'key':
            offset_x = 22.5
            offset_y = 22.5
        if status == 'life':
            offset_x = 25
            offset_y = 32
        if status == 'obelisk':
            offset_x = 0
            offset_y = -44
        if status == 'fire':
            offset_x = 10
            offset_y = 32
         

        self.pos = (x+offset_x,y+offset_y)
        self.rect = self.image.get_rect(topleft = self.pos)

        self.coin_obtained = False

    def import_assets(self):
        path = "../backgrounds/"
        self.animations = {'coin':[],'diamond':{},'obelisk':[],'life':[],'dataread':[],
                           'azul':[],'ballfly':[],'linea':[],'rotate':[],'vent':[],'indicator':[],'fire':[]}

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        #loop over frame index
        self.frame_index += self.amimation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]

        if self.status == 'obelisk':
            self.image =  pygame.transform.scale(self.image,(60,120))

    def update(self,x_shift):
        self.rect.x += x_shift
        self.animate()


