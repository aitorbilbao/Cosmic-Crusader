import pygame
from UI import import_folder

#This class is purely for the looks of the game. It will add dust particles depending on the state of the character.
class ParticleEffect(pygame.sprite.Sprite):
	def __init__(self,pos,type):
		super().__init__()
		#We import different frames depending on the state of the character
		#We set initial parameters
		self.frame_index = 0
		self.animation_speed = 0.5
		if type == 'jump':
			self.frames = import_folder('../player/dust_particles/jump/')
		if type == 'land':
			self.frames = import_folder('../player/dust_particles/land/')
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.kill() #to remove dust particles once finished
		else:
			self.image = self.frames[int(self.frame_index)]

	def update(self,x_shift):
		self.animate()
		self.rect.x += x_shift
