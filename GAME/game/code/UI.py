import pygame
from os import walk

#This file will include the User Interface and a function to make it easier to import images from a folder.

#This function will be of help when creating characters and backgrounds.
def import_folder(path):
    surface_list = []

    for _,__,image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

#This (basic) User Interface will show coins and lifes
class UI:
    def __init__(self,surface):
        super().__init__()

        #setup the surface
        self.display_surface = surface

        #health (lifes)
        self.health = pygame.image.load("../backgrounds/life/heart3.png")
        self.health = pygame.transform.scale(self.health,(40,40))
        self.heart_rect = self.health.get_rect(topleft = (50,20))

        #coins
        self.coin = pygame.image.load("../backgrounds/coin/coin1.png")
        self.coin = pygame.transform.scale(self.coin,(40,40))
        self.coin_rect = self.coin.get_rect(topleft = (50,72))
        self.font = pygame.font.Font("../backgrounds/ARCADEPI.TTF",30)

    
    def show_lifes(self,amount):
        self.display_surface.blit(self.health,self.heart_rect)
        hearts_amount = self.font.render(str(amount),False,(204,229,255))
        hearts_amount_rect = hearts_amount.get_rect(midleft = (self.heart_rect.centerx + 30, self.heart_rect.centery))
        self.display_surface.blit(hearts_amount,hearts_amount_rect)

    def show_coins(self,amount):
        self.display_surface.blit(self.coin,self.coin_rect)
        coin_amount = self.font.render(str(amount),False,(204,229,255))
        coin_amount_rect = coin_amount.get_rect(midleft = (self.coin_rect.centerx + 30, self.coin_rect.centery))
        self.display_surface.blit(coin_amount,coin_amount_rect)
