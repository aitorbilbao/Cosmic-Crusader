import pygame 
import time
from tiles import Tile
from map_info import *
from player import Player
from particles import ParticleEffect
from objects import Object
from level_dict import levels
from robot import Robot
from ghost_runner import Ghost_Runner

class Level:
	def __init__(self,surface,current_level,create_overworld,change_coins,change_life,player):
		
		# level setup (initial parameters) - we need to create self.parameter to be able to use the input
		self.display_surface = surface
		self.current_level = current_level 
		levelData = levels[self.current_level]

		#Using the dictionary to select the map and the images.
		self.map = levelData['map']
		self.bc = levelData['map_bc']
		self.image = levelData['image']
		self.new_max_level = levelData['unlock']

		#It will help us create two type of levels: Normal platformer and ghost runner
		self.who = player


		self.create_overworld = create_overworld

		self.setup_level(self.map)
		self.setup_borders(self.map)
		self.setup_background(self.bc)
		self.world_shift = 0
		self.current_x = 0

		#player
		self.player_setup(self.map)
		
		#ui
		self.change_coins = change_coins
		self.change_life = change_life

		#npc difficulty
		self.t0 = time.time()

		# dust 
		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False

	def background_level(self):
		#Background image for first two levels
		if self.current_level == 0:
			color = ('#4c593e')
			pygame.draw.rect(self.display_surface, color, pygame.Rect(0, 0, screen_width, screen_height))

			back1 = pygame.image.load("../backgrounds/earth/BG_1/BG_1.png")
			back1 = pygame.transform.scale(back1,(screen_width,screen_height))
			self.display_surface.blit(back1,[0,0])

		if self.current_level == 1:
			back1 = pygame.image.load("../backgrounds/moon.jpg").convert()
			back1 = pygame.transform.scale(back1,(screen_width,screen_height))
			self.display_surface.blit(back1,[0,0])
			
	def create_jump_particles(self,pos):
		#Create jump particles with an offset
		player = self.player.sprite
		if player.facing_right:
			pos -= pygame.math.Vector2(10,5)
		else:
			pos += pygame.math.Vector2(10,-5)
		jump_particle_sprite = ParticleEffect(pos,'jump')
		self.dust_sprite.add(jump_particle_sprite)

	def get_player_on_ground(self):
		#To be able to use player on ground boolean
		player = self.player.sprite
		if player.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False

	def create_landing_dust(self):
		player = self.player.sprite
		if not self.player_on_ground and player.on_ground and not self.dust_sprite.sprites():
			if player.facing_right:
				offset = pygame.math.Vector2(10,15)
			else:
				offset = pygame.math.Vector2(-10,15)
			fall_dust_particle = ParticleEffect(player.rect.midbottom - offset,'land')
			self.dust_sprite.add(fall_dust_particle)

	def setup_level(self,layout):
		#Most important function:
		# - It reads through the layout and creates all sprites including tiles, objects and characters
		self.tiles = pygame.sprite.Group()
		self.player = pygame.sprite.GroupSingle()
		self.enemies = pygame.sprite.GroupSingle()
		self.coins = pygame.sprite.Group()
		self.hearts = pygame.sprite.Group()
		self.jump_tiles = pygame.sprite.Group()
		self.fire = pygame.sprite.Group()
		self.ghost = pygame.sprite.GroupSingle()
		self.stop = pygame.sprite.GroupSingle()

		for row_index,row in enumerate(layout):
			for col_index,cell in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				

				if cell == 'C':
					coin_sprite = Object(x,y,self.display_surface,'coin')
					self.coins.add(coin_sprite)

				if cell == 'Z':
					fire_sprite = Object(x,y,self.display_surface,'fire')
					self.fire.add(fire_sprite)

				if cell == 'H':
					heart = Object(x,y,self.display_surface,'life')
					self.hearts.add(heart)

				if cell == 'S':
					stop_sprite = Tile(x,y,tile_size,self.image['J'])
					self.stop.add(stop_sprite)

				if cell == 'D':
					coin_sprite = Object(x,y,self.display_surface,'diamond')
					self.coins.add(coin_sprite)

				for i in range(0,26):
					lst=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
					if cell == lst[i]:
						tile = Tile(x,y,tile_size,self.image[lst[i]])
						self.tiles.add(tile)

				if cell == 'P':
					player_sprite = Player((x,y),self.display_surface,self.create_jump_particles,pygame.K_RIGHT,pygame.K_LEFT,pygame.K_UP,pygame.K_DOWN)
					self.player.add(player_sprite)

				if cell == 'E':
					enemy_sprite = Robot((x,y),self.display_surface,self.create_jump_particles,self.player.sprite.direction.x,self.player.sprite.rect.x)
					self.enemies.add(enemy_sprite)

				if cell == 'G':
					ghosts = Ghost_Runner((x,y),self.display_surface,self.create_jump_particles)
					self.ghost.add(ghosts)

				if cell == 'J':
					jump = Tile(x,y,tile_size,self.image['J'])
					self.jump_tiles.add(jump)

	def setup_background(self,layout):
		#Same as previous one but for the background tiles
		self.background = pygame.sprite.Group()
		self.bc_objects = pygame.sprite.Group()

		for row_index,row in enumerate(layout):
			for col_index,cell in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size

				#Draw background
				for i in range(0,10):
					if cell == str(i):
						back_tile = Tile(x,y,tile_size,self.image[str(i)])
						self.background.add(back_tile)

				if cell == 'B':
					dataread = Object(x,y,self.display_surface,'dataread')
					self.bc_objects.add(dataread)

				if cell == 'A':
					azul = Object(x,y,self.display_surface,'azul')
					self.bc_objects.add(azul)

				if cell == 'F':
					ball_fly = Object(x,y,self.display_surface,'ballfly')
					self.bc_objects.add(ball_fly)

				if cell == 'L':
					line = Object(x,y,self.display_surface,'linea')
					self.bc_objects.add(line)

				if cell == 'R':
					rotate = Object(x,y,self.display_surface,'rotate')
					self.bc_objects.add(rotate)

				if cell == 'V':
					vent = Object(x,y,self.display_surface,'vent')
					self.bc_objects.add(vent)

	def player_setup(self,layout):
		#Same as previous but for the flying stone, adressed as goal/finish
		self.finish = pygame.sprite.Group()
		
		for row_index,row in enumerate(layout):
			for col_index,cell in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if cell == '0':
					print('player')
				if cell == 'K':
					key = Object(x,y,self.display_surface,'obelisk')
					self.finish.add(key)

	def scroll_x(self):
		#This will move the map when you reach a limit of the screen and all the tiles that have been drawn should be updated.
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 5 and direction_x < 0:
			self.world_shift = 8
			player.speed = 0
		elif player_x > screen_width - (screen_width * 2/5) and direction_x > 0:
			self.world_shift = -8
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 8
	
	def horizontal_movement_collision(self):
		#Checks horizontal collisions and enables horizontal movement
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0: 
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	def check_death(self):
		#Checks death by falling out of the map
		if self.player.sprite.rect.top > screen_height:
			self.change_life(-1)
			sound_effect = pygame.mixer.Sound('../music/hurt.wav')
			sound_effect.play()
			self.create_overworld(self.current_level,self.current_level)
		
	def check_win(self):
		#Checks win by collision with goal/finish
		if pygame.sprite.spritecollide(self.player.sprite,self.finish,False):
			self.create_overworld(self.current_level,self.new_max_level)
			sound_effect = pygame.mixer.Sound('../music/goal.wav')
			sound_effect.play()

	def vertical_movement_collision(self):
		#Enables vertical movement(gravity) and checks vertical collision
		player = self.player.sprite
		player.apply_gravity()

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0: 
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:
			player.on_ceiling = False

	def input(self):
		#Checks input for returning to overworld
		keys = pygame.key.get_pressed()
		if keys[pygame.K_RETURN]:
			self.create_overworld(self.current_level,self.new_max_level)
		if keys[pygame.K_ESCAPE]:
			self.create_overworld(self.current_level,self.new_max_level - 1)

	def coin_collision(self):
		#Checks coin collision and adds the coin value (it is different for coins and diamonds)
		player = self.player.sprite 
		collided_coin = pygame.sprite.spritecollide(player,self.coins,True)
		if collided_coin:
			for coin in collided_coin:
				self.change_coins(coin.value)
				sound_effect = pygame.mixer.Sound('../music/coin.wav')
				sound_effect.play()

	def heart_collision(self):
		#Checks collision with hearts and adds a life
		player = self.player.sprite 
		collided_heart = pygame.sprite.spritecollide(player,self.hearts,True)
		if collided_heart:
			for heart in collided_heart:
				self.change_life(1)
				#Creates sound effect
				sound_effect = pygame.mixer.Sound('../music/heart.wav')
				sound_effect.play()

	def setup_borders(self,layout):
		#Creates borders for the NPCs
		self.border_tiles = pygame.sprite.Group()


		for row_index,row in enumerate(layout):
			for col_index,cell in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				

				if cell == 'W':
					border = Tile(x,y,tile_size,self.image['W'])
					self.border_tiles.add(border)


	def enemy_basic_collision(self,enemy):
		#Defines movement and vertical collision of an enemy. Can be the robot, the NPC, etc. (you decide in the input)
		enemy = enemy
		enemy.apply_gravity()
		enemy.rect.x += enemy.direction.x * enemy.speed

		#vertical collision
		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(enemy.rect):
				if enemy.direction.y > 0: 
					enemy.rect.bottom = sprite.rect.top
					enemy.direction.y = 0
					enemy.on_ground = True
				elif enemy.direction.y < 0:
					enemy.rect.top = sprite.rect.bottom
					enemy.direction.y = 0
					enemy.on_ceiling = True

		if enemy.on_ground and enemy.direction.y < 0 or enemy.direction.y > 1:
			enemy.on_ground = False
		if enemy.on_ceiling and enemy.direction.y > 0.1:
			enemy.on_ceiling = False

	def NPC_movement(self):
		#This function is for level 6.
		# The enemy will follow the player
		enemy = self.enemies.sprite
		player_pos = self.player.sprite.rect.x
		robot_pos = self.enemies.sprite.rect.x

		if player_pos < robot_pos:
			enemy.direction.x = -1
		elif player_pos > robot_pos:
			enemy.direction.x = 1
		else:
			enemy.direction.x = 0
		
		enemy.rect.x += enemy.direction.x * enemy.speed

	def increase_difficulty(self):
		# It increases the velocity of the NPC until it reaches a speed of 3. Then it stays constant.
		t = time.time()
		max = 200000
		self.velocity_incr = 0.01

		if t > max and self.enemies.sprite.speed < 3: #2.5
			self.enemies.sprite.speed += self.velocity_incr
			max = max^2

	def static_enemies(self):
		#Checks collision with static enemies. In this case the fire sprites
		player = self.player.sprite 

		collided_fire = pygame.sprite.spritecollide(player,self.fire,True)
		if collided_fire:
			for fire in collided_fire:
				self.change_life(-1)
				sound_effect = pygame.mixer.Sound('../music/fire.wav')
				sound_effect.play()

	def enemies_L6(self):
			#Checks collision with the enemy of level 6. Instead of removing a life, you are returned to the overworld
			player = self.player.sprite 

			collided_enemy = pygame.sprite.spritecollide(player,self.enemies,True)
			if collided_enemy:
				self.create_overworld(self.current_level,self.current_level)
		
	def ghost_win(self):
		#This is for level 3
		self.create_overworld(self.current_level,self.new_max_level-1)
	
	def ghost_movement(self):
		# the horizontal movement is already defined
		# gravity is already defined

		# This will make the ghost jump where it has learned it is better and stop before reaching the finish goal.
		ghost = self.ghost.sprite 
		jump = pygame.sprite.spritecollide(ghost,self.jump_tiles,True)
		if jump:
			for time in jump:
				ghost.jump()
		
		stop = pygame.sprite.spritecollide(ghost,self.stop,True)
		if stop:
			for pause in stop:
				ghost.direction.x = 0
				ghost.speed = 0

	def race(self):
		# For level 3, instead of being guided by the ghost, you must race it and reach the goal before it does. 
		if self.current_level == 3:
			ghost = self.ghost.sprite 
			lose = pygame.sprite.spritecollide(ghost,self.finish,True)
			if lose:
				for time in lose:
					self.ghost_win()

	def reverse_L1(self):
		#This function will reverse the direction of the NPCs if they collide with a border
		robot = self.enemies.sprite

		turn = pygame.sprite.spritecollide(robot,self.border_tiles,False)
		if turn:
			robot.speed = robot.speed * -1

		robot.rect.x += robot.direction.x * robot.speed

	def enemies_L1(self):
			#Checks collision with NPC in level 1
			player = self.player.sprite 

			collided_enemy = pygame.sprite.spritecollide(player,self.enemies,True)
			if collided_enemy:
				self.change_life(-1)
				sound_effect = pygame.mixer.Sound('../music/hurt.wav')
				sound_effect.play()

	def run(self):
		#Check collisions and draw/update all tiles.

		self.t = time.time()
		self.input()
		self.check_death()
		self.check_win()
		self.coin_collision() 
		self.heart_collision()

		# dust particles 
		self.dust_sprite.update(self.world_shift)
		self.dust_sprite.draw(self.display_surface)

		#background
		self.background_level()

		self.background.update(self.world_shift)
		self.background.draw(self.display_surface)

		self.bc_objects.update(self.world_shift)
		self.bc_objects.draw(self.display_surface)

		# level tiles
		self.tiles.update(self.world_shift)
		self.tiles.draw(self.display_surface)

		#coins
		self.coins.update(self.world_shift)
		self.coins.draw(self.display_surface)

		#hearts
		self.hearts.update(self.world_shift)
		self.hearts.draw(self.display_surface)

		#jump tile, stop tile and border tile
		self.jump_tiles.update(self.world_shift)
		self.jump_tiles.draw(self.display_surface)
		self.stop.update(self.world_shift)
		self.stop.draw(self.display_surface)
		self.border_tiles.update(self.world_shift)
		self.border_tiles.draw(self.display_surface)

		#basic enemies
		self.static_enemies()
		self.fire.update(self.world_shift)
		self.fire.draw(self.display_surface)

		if self.enemies:
			self.enemy_basic_collision(self.enemies.sprite)
			self.enemies.update(self.world_shift)
			self.enemies.draw(self.display_surface)

		self.scroll_x()

		#ghost (only if the status is 'ghost')
		if self.who == 'ghost' and self.current_level != 6:
			self.enemy_basic_collision(self.ghost.sprite)
			self.race()
			self.ghost_movement()
			self.ghost.update(self.world_shift)
			self.ghost.draw(self.display_surface)

		# player
		self.player.update()
		self.horizontal_movement_collision()
		self.get_player_on_ground()
		self.vertical_movement_collision()
		self.create_landing_dust()
		self.player.draw(self.display_surface)

		#finish
		self.finish.update(self.world_shift)
		self.finish.draw(self.display_surface)
	
		#NPC level 1
		if self.current_level == 1 and self.enemies:
			self.enemies.sprite.direction.x = 1
			self.reverse_L1()
			self.enemies_L1()

		#enemies L6
		if self.current_level == 6:
			self.increase_difficulty()
			self.NPC_movement()
			self.enemies_L6()		

		
