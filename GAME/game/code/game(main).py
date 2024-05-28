import pygame, sys
from map_info import * 
from level_logic import Level
from overworld import Overworld
from UI import UI

#Main file. First we create the main class (Game) which will run when the file runs

class Game:
	def __init__(self):

		#game info
		self.max_level = 0
		self.current_lifes = 3
		self.coins = 0
		self.current_level = 0

		#creating the overworld
		self.overworld = Overworld(self.current_level,self.max_level,screen,self.create_level,self.create_help)
		self.status = 'overworld'

		#UI
		self.ui = UI(screen)

		#This three functions will be used as input in classes to be called inside those classes.

		#Create normal level
	def create_level(self,current_level):
		self.level = Level(screen,current_level,self.create_overworld,self.change_coins,self.change_life,'player')
		self.status = 'level'
	
		#Create ghost runner level (help or race)
	def create_help(self,current_level):
		self.level = Level(screen,current_level,self.create_overworld,self.change_coins,self.change_life,'ghost')
		self.status = 'level'

		#Create overworld
	def create_overworld(self,current_level,new_max_level):
		if new_max_level == 0:
			self.max_level = new_max_level
		if new_max_level > self.max_level:
			self.max_level = new_max_level
		self.overworld = Overworld(current_level,self.max_level,screen,self.create_level,self.create_help)
		self.status = 'overworld'

		#Game over
	def check_gameover(self):
		if self.current_lifes <= 0:
			self.status = 'gameover'

	def create_gameover(self):
		screen.fill('black')
		self.font = pygame.font.Font("../backgrounds/ARCADEPI.TTF", 128)
		self.text = self.font.render('GAME OVER',False,(204,229,255))
		self.text_rect = self.text.get_rect(center = (screen_width/2,screen_height/2))
		screen.blit(self.text,self.text_rect)


		#This two functions will also be used as input, to be called inside the levels and change the global coins and lifes.
	def change_coins(self,amount):
		self.coins += amount

	def change_life(self,amount):
		self.current_lifes += amount
	
		#When we reach 100 coins, we will get 1 life
	def hundredcoins(self):
		if self.coins > 99:
			self.current_lifes +=1
			self.coins = 0
	

	def run(self):
		#Depending on the status, we will run the overworld, the level, or the gameover page.
		self.check_gameover()
		if self.status == 'overworld':
			self.overworld.run()
		elif self.status == 'gameover':
			self.create_gameover()
		else:
			self.level.run()
			self.ui.show_lifes(self.current_lifes)
			self.ui.show_coins(self.coins)
			self.hundredcoins()

			
# Pygame setup 
pygame.init()

# Background music
pygame.mixer.init() 
pygame.mixer.music.load("../music/bc_music.mp3")
pygame.mixer.music.play(-1)

icon = pygame.image.load("../player2/jump/jump10.png") #Icon
pygame.display.set_icon(icon)

caption = 'Cosmic Crusader' #Name displayed
pygame.display.set_caption(caption)

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()
stats = 'start'

def start_page():
	start = pygame.sprite.Sprite
	start.image = icon
	screen.blit(start.im)

while True:
	#Initialize game
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

			
	#Create start page, and if the icon is clicked, run the game. The music runs from the start.
	if stats == 'start':
		screen.fill('black')
		font = pygame.font.Font("../backgrounds/ARCADEPI.TTF", 64)
		text = font.render(caption,False,(204,229,255))
		text_rec = text.get_rect(center = (screen_width/2,screen_height/2-100))
		icon_rec = text.get_rect(center = (screen_width/2+200,screen_height/2+100))
		icon = pygame.transform.scale(icon,(200,200))
		click_area = pygame.Rect(600,400,200,200)

		screen.blit(text,text_rec)
		screen.blit(icon,icon_rec)

	if pygame.MOUSEBUTTONUP and click_area.collidepoint(pygame.mouse.get_pos()):
		stats = 'play'
		screen.fill('black')
	
	if stats == 'play':
		game.run()

	pygame.display.update()
	clock.tick(60)