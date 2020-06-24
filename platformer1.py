import pygame
import sys
import random
import math
import getlayout




class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((100, 100))
		pygame.key.set_repeat() 
		pygame.display.set_caption('Platformer')
		self.icon = pygame.image.load('platformer.png')
		pygame.display.set_icon(self.icon)
		pygame.mouse.set_visible(0)
		self.widthreduc = 6
		self.heightreduc = 32
		self.fullscreen = False
		self.screen = pygame.display.set_mode((pygame.display.get_surface().get_size()[0]-self.widthreduc,\
			pygame.display.get_surface().get_size()[1]-self.heightreduc))
		self.screenwidth, self.screenheight = pygame.display.get_surface().get_size()
		self.smallwidth, self.smallheight = self.screenwidth, self.screenheight
		self.running = True
		self.events = 0
		self.keys = 0
		self.frames = 0
		self.KEYTAPPED = False
		self.KEYPRESSED = False
		self.MOUSECLICKED = False
		self.MOUSEPRESSED = False
		self.levels = []
		self.layouts = []
		self.backuplayouts = []
		self.color = []
		self.whiteoverride = True
		
		if len(sys.argv) > 1:
			filepath = str(sys.argv[1])
		else:
			filepath = 'world1'
		self.levelfile = filepath
		
	
	def setScreen(self):
		width = int(player.level.width*player.level.tilesize)
		height = int(player.level.height*player.level.tilesize)
		self.screen = pygame.display.set_mode((width, height))
	
	
	def checkKeys(self):
		if self.keys[pygame.K_w] or self.keys[pygame.K_UP] or self.keys[pygame.K_SPACE]:
			self.up = True
		else:
			self.up = False
		if self.keys[pygame.K_s] or self.keys[pygame.K_DOWN] or self.keys[pygame.K_RETURN]:
			self.down = True
		else:
			self.down = False
		if self.keys[pygame.K_d] or self.keys[pygame.K_RIGHT]:
			self.right = True
		else:
			self.right = False
		if self.keys[pygame.K_a] or self.keys[pygame.K_LEFT]:
			self.left = True
		else:
			self.left = False
		if self.keys[pygame.K_LSHIFT] or self.keys[pygame.K_RSHIFT]:
			self.shift = True
		else:
			self.shift = False
		
	def checkEvents(self):
		self.events = pygame.event.get()
		self.keys = pygame.key.get_pressed()
		self.mouse = pygame.mouse.get_pressed()	
		self.checkKeys()
		self.frames += 1
		for event in self.events:
			if event.type == pygame.QUIT:
				self.running = False
			#elif event.type == pygame.VIDEORESIZE:
			#	self.screenwidth, self.screenheight = event.size
			#	self.smallwidth, self.smallheight = event.size
			elif event.type == pygame.MOUSEBUTTONDOWN:
				#print(pygame.mouse.get_pos())
				self.MOUSECLICKED = True
				self.MOUSEPRESSED = True
			elif event.type == pygame.MOUSEBUTTONUP:
				self.MOUSEPRESSED = False
			elif event.type == pygame.KEYDOWN:
				self.KEYTAPPED = True
				self.KEYPRESSED = True
			elif event.type == pygame.KEYUP:
				self.KEYPRESSED = False
				
		
	def resetEvents(self):
		self.KEYTAPPED = False
		self.MOUSECLICKED = False
		
	def cheats(self, do=True):
		if do:
			if game.KEYTAPPED:
				try:
					if self.keys[pygame.K_n]:
						player.cycleLevel(2)
					if self.keys[pygame.K_b]:
						player.cycleLevel(-1)
					if self.keys[pygame.K_r]:
						player.respawn()
					if self.keys[pygame.K_g]: # Respawn with spawn reset
						player.setSpawn()
						player.respawn()
					if self.keys[pygame.K_i]:
						print(blocks)
					if self.shift:
						player.sprinting = True
					else:
						player.sprinting = False
				except:
					pass
	
	
	def loop(self):
		self.checkEvents()
		self.cheats()
		player.loop()
		self.resetEvents()
	
	def draw(self):
		player.level.draw()
		player.draw()
		pygame.display.update(player.rect.inflate(player.width*2, player.height*2))
	
	def play(self):
		self.draw()
		self.loop()
	
	

game = Game()





class Level:
	numlevels = 0
	def __init__(self, layout, bg=(100, 160, 255), tilesize=47, gravity=1):
		game.levels.append(self)
		self.levelnum = Level.numlevels
		Level.numlevels += 1
		self.layout = layout
		self.height = len(self.layout)
		width = 1
		for row in self.layout:
			length = len(row)
			if length > width:
				width = length
		self.width = width
		if tilesize:
			self.tilesize = tilesize
		else:
			self.tilesize = game.screenheight/self.height
			
		self.tilesurface = pygame.Surface((round(self.width*self.tilesize), round(self.height*self.tilesize)))
		self.bg = bg
		self.tilesurface.fill(self.bg)
		self.hascoin = False
		self.haskey = False
		self.lswitched = False
		self.blocklayout = []
		
		self.speeddivisor = 22  # The higher the number, the slower you fall
		self.gravity = gravity/self.speeddivisor

		
	def generate(self):
		self.portals = [(), ()]
		tilesize = self.tilesize
		x = 0
		y = 0
		self.tilesurface.fill(self.bg)
		for row in self.layout:
			row = list(row)
			for block in row:
				try:
					if block != ' ':
						if blocks[block]['name'] == 'coin':
							self.hascoin = True
						if blocks[block]['name'] == 'key':
							self.haskey = True
						usingshield = False
						if (blocks[block]['name'] == 'shield' and player.shield) or (blocks[block]['name'] == 'super shield' and player.supershield):
							usingshield = True
						if usingshield or (blocks[block]['name'] == 'coin' and player.coin) or (blocks[block]['name'] == 'key' and player.key):
							block = getBlockSymbol('air')
						if player.key and blocks[block]['name'] == 'door':
							block = getBlockSymbol('unlocked door')
						if (blocks[block]['name'] == 'finish' and not player.coin):
							block = getBlockSymbol('inactive finish')
						if (blocks[block]['name'] == 'finish star' and not player.coin):
							block = getBlockSymbol('inactive finish star')
						if player.eye and blocks[block]['name'] == 'invisible block':
							block = getBlockSymbol('standard block')
						if block == '1' or block == '2':
							index = (int(block))-1
							self.portals[index] = (x, y)
						widthmult = 1
						heightmult = 1
						if 'width' in blocks[block].keys():
							widthmult = blocks[block]['width']
						if 'height' in blocks[block].keys():
							heightmult = blocks[block]['height']
						width = tilesize * widthmult
						height = tilesize * heightmult
						
						drawx = x
						drawy = y
						if 'x' in blocks[block].keys():
							drawx += blocks[block]['x']
						if 'y' in blocks[block].keys():
							drawy += blocks[block]['y']
						drawx = drawx * tilesize
						drawy = drawy * tilesize
						
						rect = pygame.Rect(int(drawx), int(drawy), width, height)
						
						if 'color' in blocks[block].keys():
							shape = pygame.draw.rect
							if 'shape' in blocks[block].keys():
								shape = blocks[block]['shape']
							color = blocks[block]['color']
							if game.whiteoverride and 'liquid' in blocks[block].keys():
								if not blocks[block]['liquid']:
									color = (255, 255, 255)
							shape(self.tilesurface, color, rect)
							
						if 'image' in blocks[block].keys():
							image = blocks[block]['image']#.convert_alpha()
							image = pygame.transform.scale(image, (int(width), int(height)))
							self.tilesurface.blit(image, rect)
				except KeyError:
					print('File contains unrecognized character') 
				x += 1
			y += 1
			x = 0
		self.draw()
		pygame.display.flip()
	
	def scanForPos(self, blockname):
		x = 0
		y = 0
		positions = []
		for row in self.layout:
			for block in row:
				if getBlockSymbol(blockname) == block:
					positions.append((x, y))
				x += 1
			y += 1
			x = 0
		return positions
	
	def draw(self):
		#self.generate()
		#game.screen.fill(player.level.bg)
		game.screen.blit(self.tilesurface, (0, 0, game.screenwidth, game.screenheight))
	
	def reset(self):
		game.layouts = game.backuplayouts
		self.layout = game.layouts[self.levelnum]
		
	def setup(self):
		self.reset()
		game.setScreen()
		self.generate()
		#pygame.display.flip()


blocks = {
	
	'#': {
		'name': 'standard block',
		'color': (255, 255, 255),
		'description': 'Just your standard everyday shiny white block',
		'solid': True,
	},
	' ': {
		'name': 'air',
		'description': 'Just a space in the level full of nitrogen and oxygen',
		'solid': False,
	},
	
	's': {
		'name': 'start',
		'image': 'start.png',
		'color': (105, 0, 194),#(0, 0, 0),
		'description': 'A block that indicates the player\'s position at the beginning of a level. There can only be one per level.',
		'solid': True,
	},
	'S': {
		'name': 'start star',
		'image': 'start.png',
		'description': 'A nonsolid item for the player\'s position beginning of a level. There can only be one per level.',
		'solid': False,
	},
	'f': {
		'name': 'finish',
		'image': 'finish.png',
		'color': (230, 230, 0),#(0, 0, 0),
		'description': 'A block that ends the level when you stand on it and sends you to the next one.',
		'solid': True,
	},
	'F': {
		'name': 'finish star',
		'image': 'finish.png',
		'description': 'A nonsolid item that ends the level when you touch it and sends you to the next one.',
		'solid': False,
	},
	'`': {
		'name': 'inactive finish',
		'image': 'finish_inactive.png',
		'color': (200, 200, 200),#(0, 0, 0),
		'description': 'A block that ends the level when you stand on it and sends you to the next one only it is activated (coin is collected).',
		'solid': True,
	},
	'.': {
		'name': 'inactive finish star',
		'image': 'finish_inactive.png', 
		'description': 'An item that ends the level when you touch it and sends you to the next one only it is activated (coin is collected).',
		'solid': True,
	},
	'w': {
		'name': 'water',
		'color': (0, 140, 240),
		'description': 'A  liquid that allows the player to swim in any direction while inside it.',
		'solid': False,
		'liquid': True
	},
	
	'c': {
		'name': 'checkpoint',
		'image': 'checkpoint.png',
		'color': (200, 0, 0),#(150, 0, 180),
		'description': 'A block which creates a new spawnpoint when you step on it. (1 per level)',
		'solid': True,
	},
	'C': {
		'name': 'checkpoint star',
		'image': 'checkpoint.png',
		'description': 'An item which creates a new spawnpoint when you touch it. (1 per level)',
		'solid': False,
	},
	
	'b': {
		'name': 'bounce block',
		'image': 'bounce_block2.png',
		'color': (0, 255, 100),
		'description': 'A block that makes you jump super high.',
		'solid': True,
	},
	't': {
		'name': 'turbo block',
		'image': 'turbo_block2.png',
		'color': (255, 130, 0),
		'description': 'A block that increases your speed while you are on it.',
		'solid': True,
	},
	'T': {
		'name': 'turbo item',
		'image': 'turbo_block2.png',
		'description': 'A block that increases your speed while you are on it.',
	},
	
	'x': {
		'name': 'spike block',
		'image': 'spike_block.png',
		'description': 'A block that does damage to the player when they touch it.',
		'solid': True,
	},
	'h': {
		'name': 'shield',
		'image': 'shield.png',
		#'color': (100, 100, 100),
		'description': 'An item than gives you temporary invincibility when you touch it (3 seconds).',
		'shape': pygame.draw.ellipse,
		'solid': False,
		'duration': 3000,
	},
	'H': {
		'name': 'super shield',
		'image': 'super_shield.png',
		#'color': (100, 100, 100),
		'description': 'An item than gives you temporary invincibility when you touch it (6 seconds).',
		'shape': pygame.draw.ellipse,
		'solid': False,
		'duration': 6000,
	},
	
	'1': {
		'name': 'portal 1',
		'color': (255, 150, 0),
		'image': 'portal.png',
		'description': 'An item which teleports the player to its partner portal. Paired with portal 2.',
		'shape': pygame.draw.ellipse,
		'solid': False,
	},
	'2': {
		'name': 'portal 2',
		'color': (80, 130, 255),
		'image': 'portal.png',
		'description': 'The portal paired with portal 1.',
		'shape': pygame.draw.ellipse,
		'solid': False,
	},
	
	'>': {
		'name': 'right conveyor',
		'image': 'conveyor_right.png',
		'color': (20, 20, 20),
		'description': 'A block which pushes the player right.',
		'solid': True,
	},
	'<': {
		'name': 'left conveyor',
		'image': 'conveyor_left.png',
		'color': (20, 20, 20),
		'description': 'A block which pushes the player left.',
		'solid': True,
	},
	'p': {
		'name': 'cloud',
		'image': 'cloud.png',
		'description': 'A block which the player can jump through but still stand on.',
		'solid': False,
	},
	'U': {
		'name': 'up current',
		'image': 'current_up.png',
		'type': 'current',
		'description': 'A block which pushes the player up when they are inside it',
		'solid': False,
		'liquid': True,
	},
	'D': {
		'name': 'down current',
		'image': 'current_down.png',
		'type': 'current',
		'description': 'A block which pushes the player down when they are inside it',
		'solid': False,
		'liquid': True,
	},
	'L': {
		'name': 'left current',
		'image': 'current_left.png',
		'type': 'current',
		'description': 'A block which pushes the player left when they are inside it',
		'solid': False,
		'liquid': True,
	},
	'R': {
		'name': 'right current',
		'image': 'current_right.png',
		'description': 'A block which pushes the player right when they are inside it',
		'type': 'current',
		'solid': False,
		'liquid': True,
	},
	
	'm': {
		'name': 'magma',
		'color': (255, 50, 0),
		'description': 'A liquid that allows the player to swim in any direction whilst taking damage.',
		'solid': False,
		'liquid': True,
	},
	
	'o': {
		'name': 'coin',
		'image': 'coin.png',
		'description': 'An item of which one needs to be collected to activate the finish block.',
		'solid': False,
	},
	
	'd': {
		'name': 'door',
		'image': 'door.png',
		'color': (150, 100, 20),
		'description': 'A block which can only let the player pass when its corresponding key is collected.',
		'solid': True,
	},
	'u': {
		'name': 'unlocked door',
		'image': 'door.png',
		'color': (150, 100, 20),
		'description': 'A block which can only let the player pass when its corresponding key is collected.',
		'solid': False,
		'width': 0.5
	},
	'k': {
		'name': 'key',
		'image': 'key.png',
		'description': 'An item which needs to be collected to pass through its corresponding door.',
		'solid': False,
	},
	'g': {
		'name': 'grass block',
		'image': 'grass.png',
		'color': (150, 75, 10),
		'description': 'A solid, decorational block of grass',
		'solid': True,
	},
	'n': {
		'name': 'stone block',
		'color': (100, 100, 100),
		'description': 'A solid, decorational block of stone',
		'solid': True,
	},
	'=': {
		'name': 'monkey bars',
		'image': 'monkey_bars.png',
		'description': 'A block of which you can hold on to the bottom of.',
		'solid': False,
		'height': 0.5,
		'y': 0.25,
	},
	'%': {
		'name': 'goo block',
		'image': 'goo_block.png',
		'color': (100, 100, 100),
		'description': 'A block of which you stick on whenever you touch it.',
		'solid': True,
		'liquid': True,
	},
	'i': {
		'name': 'invisible block',
		'description': 'Just a space in the level full of nitrogen and oxygen, but one that the player cannot pass through',
		'solid': True,
	},
	'e': {
		'name': 'eye',
		'image': 'eye.png',
		'color': (250, 250, 245),
		'description': 'An item which lets you see invisible blocks while you are touching it.',
		'solid': False,
		'shape': pygame.draw.ellipse,
		
	},
	'l': {
		'name': 'liquid switch',
		'image': 'liquid_switch.png',
		'description': 'An item which, when touched, turns lava into water and vice versa.',
		'solid': False,
		'height': 0.25,
		'width':0.5,
		'y': 0.75,
		'x': 0.25
	},
	
}



def checkBlock(x, y, val):
	try:
		if x < 0 or y < 0:
			raise IndexError	
		block = player.level.layout[int(y)][round(x)]
		value = blocks[block][val]
		return value
	except:
		return False
		
def getBlockVal(name, val):
	for block in blocks:
		if blocks[block]['name'] == name:
			return blocks[block][val]
			
def getBlockSymbol(name):
	for block in blocks:
		if blocks[block]['name'] == name:
			return block



for block in blocks:
	if 'image' in blocks[block].keys():
		image = blocks[block]['image']
		image = pygame.image.load(image)
		blocks[block]['image'] = image
		
	

def loadLayout():
	filepath = game.levelfile
	game.layouts, game.color = getlayout.getLayouts(filepath)
	game.backuplayouts = game.layouts
	
	exec('game.color = ' + game.color)

	for layout in game.layouts:
		level = Level(layout, game.color)
		game.levels.append(level)


loadLayout()




class Player:
	def __init__(self, imagename, color):
		self.level = game.levels[0]
		self.x = 0
		self.y = 0
		self.spawnpoint = (0, 0)
		self.width = 0
		self.height = 0
		self.shape = pygame.draw.ellipse
		self.imagename = imagename
		self.setImage(self.imagename)
		
		self.maxhealth = 10
		self.health = self.maxhealth
		self.deaths = 0
		self.shieldtimer = 0
		self.shieldstarted = 0
		self.shield = False
		self.supershield = False
		
		self.coin = False
		self.key = True
		self.touching = []
		self.speed = 0.0225
		self.speedmultiplier = 1
		self.sprinting = False
		self.moved = False
		self.direction = 0
		
		self.maincolor = color
		self.color = self.maincolor
		self.living = True
		self.cangoright = True
		self.cangoleft = True
		self.onground = True
		self.canjump = True
		self.swimming = False
		self.hurtonspike = False
		self.incurrent = False
		self.hanging = False
		self.onconveyor = False
		self.canteleport = True
		self.eye = False
		self.liquidswitch = False
		self.forcelswitch = False
		self.snaptogrid = True
		
		self.jumptiles = 3
		self.jumping = False
		self.jump = 0
		self.jumpspeed = self.level.gravity
		self.jumpmultiplier = 1
		self.jumpspeedmultiplier = 1
		
		
	def draw(self):
		tilesize = self.level.tilesize
		self.width = tilesize
		self.height = tilesize
		self.rect = pygame.Rect(int(self.x*tilesize), int(self.y*tilesize), self.width, self.height)
		self.image = pygame.transform.scale(self.image, (int(self.width), int(self.height)))
		color = list(self.color)
		for i in range(3):
			color[i] = min(color[i], 255)
			color[i] = max(0, color[i])
		
		pygame.draw.rect(game.screen, color, self.rect)
		game.screen.blit(self.image, self.rect)
		
	def loop(self):
		self.fall()
		self.restrict()
		self.checkWall()
		self.collision()
		self.manageShield()
		self.manageStats()
		self.control()
		
	def setImage(self, imagename):
		self.image = pygame.image.load(imagename)

	def setSpawn(self):
		self.spawnpoint = (0, 0)
		for row in self.level.layout:
			for block in row:
				y = self.level.layout.index(row)
				x = row.index(block)
				yoffset = None
				if  checkBlock(x, y, 'name') == 'start':
					yoffset = -1
				elif  checkBlock(x, y, 'name') == 'start star':
					yoffset = 0
				if type(yoffset) == int:
					self.spawnpoint = (x, y+yoffset)
					
		self.x, self.y = self.spawnpoint
		#return self.spawnpoint
					
			
	def checkOn(self, var='solid', val=True):
		val = checkBlock(self.x, self.y+1, var) == val or checkBlock(self.x-0.4, self.y+1, var) == val or checkBlock(self.x+0.4, self.y+1, var)== val 
		return val
	
	def checkIn(self, var='solid', val=True):
		val = checkBlock(self.x, self.y+0.4, var) == val or checkBlock(self.x-0.4, self.y+0.4, var) == val or checkBlock(self.x+0.4, self.y+0.4, var)== val 
		return val
		
	def checkInside(self, var='solid', val=True):
		val = checkBlock(self.x, self.y, var) == val
		return val
	
	def checkAbove(self, var='solid', val=True):
		val = checkBlock(self.x, self.y-0.05, var) == val or checkBlock(self.x-0.4, self.y-0.05, var) == val or checkBlock(self.x+0.4, self.y-0.05, var)== val 
		return val
		
	def checkAround(self, var='solid', val=True):
		val = self.checkIn(var, val) or self.checkOn(var, val) or checkBlock(self.x-0.55, self.y, var) == val or checkBlock(self.x+0.55, self.y, var) == val or self.checkAbove(var, val)
		return val
		
	def checkSide(self, side, var='solid', val=True):
		val = self.checkIn(var, val) or checkBlock(self.x+side, self.y, var) == val
		return val
	
	def checkWall(self):
		if checkBlock(self.x-0.5, self.y+0.5, 'solid'):
			self.x = max(self.x, round(self.x))
			self.cangoleft = False
		elif not checkBlock(self.x-0.1, self.y, 'solid'):
			self.cangoleft = True
		if checkBlock(self.x+0.5, self.y+0.5, 'solid'):
			self.x = min(self.x, round(self.x))
			self.cangoright = False
		elif not checkBlock(self.x+0.1, self.y, 'solid'):
			self.cangoright = True
		if self.checkOn() and not self.checkAbove():
			self.canjump = True
			self.y = max(self.y, round(self.y))
		else:
			self.canjump = False
		if self.checkAbove():
			self.y = max(self.y, round(self.y))
		if self.checkOn():
			self.onground = True
		else:
			self.onground = False
			
	def fall(self):
		if (not self.jumping) and (not self.incurrent) and (not self.hurtonspike) and (not self.hanging):
			fallspeed = self.level.gravity * self.jumpspeedmultiplier
			if (self.swimming and not self.checkIn('name', 'air')) and (game.left or game.right):
				fallspeed *= 0.5
			if not self.onground:# or self.swimming:
				self.y += fallspeed

			else:
				self.y = int(self.y+0.4)
				self.onground = True
			if self.y >= self.level.height+1:
				self.health = 0
				self.respawn()
			
	def control(self):
		if not self.hurtonspike:
			self.moved = False
			speed = self.speed
			speed *= self.speedmultiplier
			if self.sprinting:
				speed *= 2
			if game.left:
				self.direction = -1
				self.moved = True
				if self.cangoleft:
					self.x -= speed
			if game.right:
				self.direction = 1
				self.moved = True
				if self.cangoright:
					self.x += speed
			if not self.moved and self.snaptogrid and not self.incurrent and not self.onconveyor:
				if abs(self.x-round(self.x)) < 0.25:
					self.snapX()
						
		if game.up and self.canjump and (game.KEYTAPPED or self.swimming) and (not self.jumping):
			self.jumping = True
			self.jump = 0
		if self.jumping:
			jumpspeed = self.jumpspeed * self.jumpspeedmultiplier
			jumpheight = (self.jumptiles * self.level.speeddivisor * self.level.gravity) * self.jumpmultiplier
			if self.jump < jumpheight:
				self.jump += jumpspeed
				self.y -= jumpspeed
			else:
				self.jumping = False
				self.jump = 0

		if self.swimming:
			speed = self.jumpspeed * self.jumpspeedmultiplier
			if game.up and self.canjump:
				self.y -= speed
			if game.down and not self.checkOn('solid'):
				self.y += speed
		
	
	def snapX(self):
		self.x = round(self.x)
	
	def restrict(self):
		pass
		if (self.x < -1 or self.x > self.level.width) and self.y > self.level.height:
			self.respawn()
		self.x = min(self.x, self.level.width-1)
		self.x = max(self.x, 0)
		
		#self.y = abs(self.y)
		#self.y = min(self.y, self.level.height-1)
		self.y = max(self.y, 0)
	
	def respawn(self, died=True):
		self.x, self.y = self.spawnpoint
		if died:
			self.deaths += 1
		self.health = self.maxhealth
		self.color = self.maincolor
		self.shield = False
		self.supershield = False
		if self.level.hascoin:
			self.coin = False
		else:
			self.coin = True
		if self.level.haskey:
			self.key = False
		else:
			self.key = True
		if self.level.lswitched:
			self.switchBlocks()
		self.level.generate()
		self.resetSpeedStats()
		
	def cycleLevel(self, amount=1, force=False):
		levels = game.levels
		#amount = amount*2
		if force:
			self.level = levels[levels.index(self.level)+amount]
			self.startLevel()
			return
		if amount > 0:
			if levels.index(player.level) < len(levels)-2:
				self.level = levels[levels.index(self.level)+amount]
			else:
				self.level = levels[0]
		elif amount < 0:
			if levels.index(player.level) < len(levels):
				self.level = levels[levels.index(self.level)+amount]
			else:
				self.level = levels[len(levels)-1]
		self.startLevel()
		return self.level
		
	def startLevel(self):
		self.eye = False
		self.level.setup()
		self.setSpawn()
		self.jumpspeed = self.level.gravity
		self.color = self.maincolor
		self.respawn(False)
		#pygame.display.flip()
	
	def manageStats(self):
		if self.health <= 0:
			self.respawn()
		elif self.health < self.maxhealth:
			self.health -= 0.1
			self.color = (255, 0, 0)
			
	def manageShield(self):
		time = 0
		self.shieldtimer = pygame.time.get_ticks() - self.shieldstarted
		if self.supershield:
			time = getBlockVal('super shield', 'duration')
			if self.shieldtimer < time:
				self.health = self.maxhealth
				self.shield = True
			else:
				self.supershield = False
				self.shieldstarted = 0
		elif self.shield:
			time = getBlockVal('shield', 'duration')
			if self.shieldtimer < time:
				self.health = self.maxhealth
				self.shield = True
			else:
				self.shield = False
				self.shieldstarted = 0
				
		if self.shieldtimer < time:
			if self.shieldtimer < time/2:
				self.color = (50, 50, 50)
			elif self.shieldtimer < time - 300:
				self.color = (100, 100, 100)
			else:
				self.color = (150, 150, 150)
				
		elif (not self.swimming) or self.incurrent:
			color = self.maincolor
			if self.jumpmultiplier > 1 and self.speedmultiplier > 1:
				color = (255, 255, 125)
				color = (0, 50, 200)
			elif self.jumpmultiplier > 1:
				color = (50, 255, 150)
			elif self.speedmultiplier > 1:
				color = (255, 150, 50)
			self.color = color
				
		if (self.shieldtimer > time-4 or self.shieldtimer < 4) and (self.shield or self.supershield):
			self.level.generate()
		
	def resetSpeedStats(self):
		self.speedmultiplier = 1
		self.jumpmultiplier = 1
		self.jumpspeedmultiplier = 1
	
	def switchBlocks(self, block1='water', block2='magma'):
		self.level.lswitched = not self.level.lswitched
		positions = self.level.scanForPos(block1) + self.level.scanForPos(block2)
		for pos in positions:
			x = positions[positions.index(pos)][0]
			y = positions[positions.index(pos)][1]
			block = self.level.layout[y][x]
			if blocks[block]['name'] == block2:
				block = getBlockSymbol(block1)
			elif blocks[block]['name'] == block1:
				block = getBlockSymbol(block2)
			else:
				block = getBlockSymbol('air')
			self.level.layout[y][x] = block
		self.level.generate()
	
	def collision(self):
		if (self.checkOn('name', 'finish') or self.checkIn('name', 'finish star')) and self.coin:
			try:
				self.cycleLevel(2, True)
			except IndexError:
				game.running = False
		if self.checkOn('name', 'checkpoint') or self.checkIn('name', 'checkpoint star'):
			self.spawnpoint = self.level.scanForPos('checkpoint')[0], self.level.scanForPos('checkpoint')[1]-1
		incurrent = False
		incurrentspeed = 0.65
		if (not checkBlock(self.x, self.y-1, 'solid')) and (self.checkInside('name', 'up current') or self.checkIn('name', 'up current')) or self.checkOn('name', 'up current'):
		#	if not (self.checkOn()) and self.checkIn('name', 'up current'):
			incurrent = True
			self.y -= self.speed*incurrentspeed
		if (not self.checkOn()) and self.checkInside('name', 'down current') or self.checkIn('name', 'down current') or self.checkOn('name', 'down current'):
			incurrent = True
			if not self.checkOn():
				self.y += self.speed*incurrentspeed
		if self.checkInside('name', 'left current') or self.checkIn('name', 'left current') or self.checkOn('name', 'left current'):
			incurrent = True
			self.x -= self.speed*incurrentspeed
		if self.checkInside('name', 'right current') or self.checkIn('name', 'right current') or self.checkOn('name', 'right current'):
			incurrent = True
			self.x += self.speed*incurrentspeed
		
		if self.checkAbove('name', 'monkey bars') and not game.down:
			hanging = True
		else:
			hanging = False
	
		if self.checkAround('name', 'goo block') or checkBlock(self.x+0.55, self.y+1, 'name') == 'goo block' or checkBlock(self.x-0.55, self.y+1, 'name') == 'goo block':
			hanging = True
			self.jumping = False
			speed = self.speed * self.speedmultiplier
			if game.up:
				self.y -= speed
				#if (game.left and self.cangoleft) or (game.right and self.cangoright):
				if game.up:
					self.canjump = True
					self.jumping = True
			if game.down and not self.checkOn():
				self.y += speed
		else:
			hanging = False
		
		if self.checkIn('liquid') or self.checkOn('liquid'):
			swimming = True
			self.canjump = True
		else:
			swimming = False
			
		if self.checkOn('name', 'bounce block'):
			self.jumpmultiplier = 2
			#self.jumping = True
		elif self.checkOn('name', 'turbo block') or self.checkIn('name', 'turbo item'):
			self.speedmultiplier = 2
			#self.x += self.direction * self.speed
				
		elif self.checkIn('name', 'water'):# or self.checkOn('name', 'water'):
			self.speedmultiplier = 0.75
			self.jumpspeedmultiplier = 0.25
			self.jumpmultiplier = 0.2
			#if self.checkIn('name', 'water'):
			self.color = (150, 200, 150)
		elif self.checkIn('name', 'magma') or self.checkOn('name', 'magma'):
			self.speedmultiplier = 0.5
			self.jumpspeedmultiplier = 0.2
			self.jumpmultiplier = 0.15
			self.health -= 0.05
		elif self.incurrent:
			self.speedmultiplier = 0.2
			self.jumpspeedmultiplier = 0.3
			self.jumpmultiplier = 0.25
		elif self.hanging:
			self.speedmultiplier = 0.4
			self.jumpspeedmultiplier = 0.5
			self.jumpmultiplier = 1
		elif self.checkOn():
			self.resetSpeedStats()
		if (self.incurrent and not incurrent) or (self.hanging and not hanging) or (self.swimming and not swimming):
			self.resetSpeedStats()
		self.incurrent = incurrent
		self.swimming = swimming
		self.hanging = hanging
		
		touchingspike = ((self.checkSide(-0.55, 'name', 'spike block') and game.left) or (self.checkSide(0.55, 'name', 'spike block') and game.right)) or self.checkOn('name', 'spike block') or (self.checkAbove('name', 'spike block') and (game.up or self.jumping))
		if touchingspike and not(self.shield or self.supershield):
			self.health -= 0.05
			self.hurtonspike = True
			self.speedmultiplier = 0
			self.jumpmultiplier = 0
			self.jumpspeedmultiplier = 0
		else:
			self.hurtonspike = False
		if (self.checkIn('name', 'shield') or self.checkOn('name', 'shield')) and not self.shield:
			self.shieldstarted = pygame.time.get_ticks()
			self.shield = True
			self.level.generate()
		if (self.checkIn('name', 'super shield') or self.checkOn('name', 'super shield')) and not self.supershield:
			self.shieldstarted = pygame.time.get_ticks()
			self.supershield = True
			self.level.generate()
		if self.checkIn('name', 'portal 1') and self.canteleport:
			try:
				self.x, self.y = self.level.portals[1]
				self.canteleport = False
			except:
				print('portal 2 is missing.')
		elif self.checkIn('name', 'portal 2') and self.canteleport:
			try:
				self.x, self.y = self.level.portals[0]
				self.canteleport = False
			except:
				print('portal 1 is missing.')
		elif not self.checkIn('name', 'portal 2') and not self.checkIn('name', 'portal 1'):
			self.canteleport = True
		onconveyor = False
		if self.checkOn('name', 'left conveyor'):
			#game.left = True
			self.x -= self.speed * self.speedmultiplier
			onconveyor = True
		if self.checkOn('name', 'right conveyor'):
			#game.right = True
			self.x += self.speed * self.speedmultiplier
			onconveyor = True
		#if onconveyor:
		self.onconveyor = onconveyor
		if self.checkOn('name', 'cloud'):
			#if not game.down:
				self.onground = True
				self.canjump = True
		if self.checkOn('name', 'coin') or self.checkIn('name', 'coin') and not self.coin:
			self.coin = True
			self.level.generate()
		if self.key:
			blocks[getBlockSymbol('door')]['solid'] = False
		else:
			blocks[getBlockSymbol('door')]['solid'] = True
		if self.checkOn('name', 'key') or self.checkIn('name', 'key') and not self.key:
			self.key = True
			self.level.generate()
			
		if self.checkIn('name', 'eye') or self.checkOn('name', 'eye'):
			eye = True
		else:
			eye = False
		if eye != self.eye:
			self.eye = eye
			self.level.generate()
		
		liquidswitch = False
		if self.checkIn('name', 'liquid switch'):
			liquidswitch = True
		if liquidswitch and not self.liquidswitch:
			self.switchBlocks()
		self.liquidswitch = liquidswitch
		
		


player = Player('player.png', (255, 255, 0))
player.startLevel()

#print(game.layouts)

while game.running:
	game.play()
print('Game over')
pygame.quit()
