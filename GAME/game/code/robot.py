import pygame
from UI import import_folder
import random

#This robot will be our basic enemy. It is an NPC which has been programmed to function in a determined way.

class Robot(pygame.sprite.Sprite):
    def __init__(self,pos,surface,create_jump_particles,player_direction,player_centerx):
        super().__init__()
        #Most functions have been copied from the main character
        self.import_character_assets()
        self.frame_index = 0
        self.amimation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        #Direction
        self.player_direction = player_direction
        self.player_x = player_centerx

        #Dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles
        
        #Enemy movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 1
        self.pos_x = self.rect.x
        self.gravity = 0.8
        self.jump_speed = -16

        #Enemy status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.down = False

    def import_character_assets(self):
        character_path = "../player/"
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
            
        #set the rectangle properly
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

    def get_status(self):
        if self.direction.x < 0:
            self.facing_right = False
        else:
            self.facing_right = True
        
        if not self.on_ground:
            self.status = 'jump'

        else:
            if self.direction.x != 0:
                self.status = 'run'
                
            elif self.down:
                self.status = 'duck'
            else:
                self.status = 'idle'
        if self.speed < 0:
            self.facing_right = False
                
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def random_jump(self):
        #This function will make the enemy jump randomly if it is on the floor
        num = random.randint(0,300)
        if num == 9 and self.on_ground:
            self.direction.y = self.jump_speed
            self.create_jump_particles(self.rect.midbottom)

    def update(self,x_shift):
        self.rect.x += x_shift
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.random_jump()
