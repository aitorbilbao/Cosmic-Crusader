import pygame
from UI import import_folder

#This will be the class for the player

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,surface,create_jump_particles,right,left,up,down):
        super().__init__()
        #First we define initial status and import all neccesary files.
        self.import_character_assets()
        self.frame_index = 0
        self.amimation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        #keys
        self.right = right
        self.left = left
        self.up = up
        self.down = down

        #dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles
        
        #player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 6
        self.gravity = 0.8
        self.jump_speed = -16

        #player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.down = False

    def import_character_assets(self):
        character_path = "../player2/"
        self.animations = {'idle':[],'run':{},'jump':[],'duck':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder("../player/dust_particles/run/")     

    def animate(self):
        animation = self.animations[self.status]

        #loop over frame index
        self.frame_index += self.amimation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image,True,False) #true for x axis but false for y axis
            self.image = flipped_image
            
        #set the rectangle properly for correct collisions (it will make it look better)
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
            
    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]
            
            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
                self.display_surface.blit(dust_particle,pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6,10)
                flipped_dust_particle = pygame.transform.flip(dust_particle,True,False)
                self.display_surface.blit(flipped_dust_particle,pos)
            
    def get_input(self):
        #We obtain the input from the keyboard and apply the correct changes
        keys = pygame.key.get_pressed()

        if keys[self.right]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[self.left]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[self.up] and self.on_ground:
            self.jump()
            sound_effect = pygame.mixer.Sound('../music/jump.wav')
            sound_effect.play()
            self.create_jump_particles(self.rect.midbottom)

        if keys[self.down]:
            self.down = True
        else:
            self.down = False

    def get_status(self):
        #We obtain the current status of the player
        if not self.on_ground:
            self.status = 'jump'

        else:
            if self.direction.x != 0:
                self.status = 'run'
                
            elif self.down:
                self.status = 'duck'
            else:
                self.status = 'idle'
                
        
    def apply_gravity(self):
        #Apply gravity so that the player does not fly
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        #Jump function
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
