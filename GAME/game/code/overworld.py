import pygame
from level_dict import levels
from map_info import *

class Node(pygame.sprite.Sprite):
    #This class will create the nodes that will be turned into the levels
    def __init__(self,pos,status,icon_speed,path):
        super().__init__()
        self.planet = pygame.image.load(path)
        self.planet = pygame.transform.scale(self.planet,(80,80))
        self.image = self.planet

    #By determining the status, we can lock levels until they are unlocked
        if status == 'available':
            self.status = 'available'
        else:
            self.status = 'locked'

        self.rect = self.image.get_rect(center = pos)
        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed/2),self.rect.centery - (icon_speed/2),icon_speed,icon_speed)

    def animation(self):
    #Animate locked and unlocked levels
        if self.status != 'available':
            tint_surface = self.image.copy()
            tint_surface.fill('black',None,pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surface,(0,0))
        else:
            self.image = self.planet
    
    def update(self):
        self.animation()

class Icon(pygame.sprite.Sprite):
    #This icon will show us which level we are choosing
    def __init__(self, pos):
        super().__init__()
        #Set initial parameters and import image of shooter indicator
        self.pos = pos
        self.indicator = pygame.image.load('../backgrounds/indicator/Indicator.png')
        self.indicator = pygame.transform.scale(self.indicator,(150,150))
        self.image = self.indicator
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.center = self.pos 

class Overworld:
    #We will use this class in the main code
    def __init__(self,start_level,max_level,surface,create_level,create_help):
        
        #Setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level
        self.create_help = create_help

        #Movement of icon
        self.moving = False
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 8

        #Sprites
        self.setup_nodes()
        self.setup_icon()

        self.bc = pygame.image.load('../backgrounds/earth.jpg').convert()
        self.bc = pygame.transform.scale(self.bc,(screen_width,screen_height))

    
    def setup_nodes(self):
        #Add nodes to their position using the dictionary
        self.nodes = pygame.sprite.Group()

        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                self.pos = node_data['node_pos']
                node_sprite = Node(self.pos,'available',self.speed,node_data['graphics'])
            else:
                self.pos = node_data['node_pos']
                node_sprite = Node(self.pos,'locked',self.speed,node_data['graphics'])
            
            self.nodes.add(node_sprite)

    def draw_paths(self):\
    #Draw line between nodes if unlocked
        color = (153,204,255)
        if self.current_level > 0:
            points = [node['node_pos'] for index,node in enumerate(levels.values()) if index<= self.max_level] #it only gives points if the level is available
            pygame.draw.lines(self.display_surface,color,False,points,6)
        
    def setup_icon(self):
        #Add icon
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        #Get input for movement of icon, and entering levels
        keys = pygame.key.get_pressed()
        if not self.moving:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level +=1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data('previous')
                self.current_level -=1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)
            elif keys[pygame.K_h]:
                self.create_help(self.current_level)

    def update_icon_position(self):
        #Create movement of icon
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False #this makes it stop when it reaches a node, this way the movement is more realistic
                self.move_direction = pygame.math.Vector2(0,0)

    def get_movement_data(self,target):
        #We create a movement that moves from center to center of nodes
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level+1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level-1].rect.center)

        return (end - start).normalize()


    def run(self):
        self.nodes.update()
        self.display_surface.blit(self.bc,[0,0])
        self.input()
        self.update_icon_position()
        self.icon.update()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)

