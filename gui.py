import sys
import random
import math
import os
import getopt
import pygame
from socket import *
from pygame.locals import *
from PIL import Image, ImageDraw, ImageFilter

def draw_mat(level):
	"""draw mat with different size"""
	if level == 'Hard':
		im = Image.new('RGB', (10, 100), (0, 0, 0))
	elif level == 'Medium':
		im = Image.new('RGB', (10, 200), (0, 0, 0))
	elif level == 'Easy':
		im = Image.new('RGB', (10, 300), (0, 0, 0))
	else :
		print('ERROR: Please choose a level first.')
	im.save('data/mat.png', quality=95)
	return im

def draw_ball(ball_size):
	"""draw ball with different size"""
	init_ball = Image.new('RGB', (1000, 1000), (0, 0, 0))
	blur_radius = 0
	offset = blur_radius * 2
	
	mask = Image.new("L", init_ball.size, 0)
	draw = ImageDraw.Draw(mask)
	draw.ellipse((offset, offset, init_ball.size[0] - offset, init_ball.size[1] - offset), fill=255)
	result = init_ball.copy()
	result.putalpha(mask)
	if ball_size == 'Small':
		radius = 50;
	elif ball_size == 'Big':
		radius = 100;
	else :
		print('ERROR: BALL SIZE INCORRECT.')
	result = result.resize((radius, radius), Image.LANCZOS)
	result.save('data/ball.png')
	return result

def load_png(name):
	fullname = os.path.join('data', name)
	try:
		image = pygame.image.load(fullname)
		if image.get_alpha is None:
			image = image.convert()
			#image = pygame.transform.smoothscale(image,(5,5))
		else:
			image = image.convert_alpha()
			#image = pygame.transform.smoothscale(image,(50,50))
	except :
		print('Cannot load image:', fullname)
		#raise SystemExit, message
	return image, image.get_rect()

class Ball(pygame.sprite.Sprite):
	def __init__(self,xy,vector):
		pygame.sprite.Sprite.__init__(self)
		
		self.image,self.rect = load_png('ball.png')
		#print('self.rect = ',self.rect)
		
		#pygame.draw.rect(screen, (0,0,0), (0, 0, 50, 50), 3)
		
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		#print('self.area = ',self.area)
		self.vector = vector
		self.hit = 0
	
	def update(self):
		newpos = self.calcnewpos(self.rect,self.vector)
		self.rect = newpos
		(angle,z) = self.vector
		
		if not self.area.contains(newpos):
			tl = not self.area.collidepoint(newpos.topleft)
			tr = not self.area.collidepoint(newpos.topright)
			bl = not self.area.collidepoint(newpos.bottomleft)
			br = not self.area.collidepoint(newpos.bottomright)
			if tr and tl or (br and bl):
				angle = -angle
			if tl and bl:
				angle = math.pi - angle
			if tr and br:
				angle = math.pi - angle
			else:
				player1.rect.inflate(-3, -3)
				player2.rect.inflate(-3, -3)
				if self.rect.colliderect(player1.rect) == 1 and not self.hit:
					angle = math.pi - angle
					self.hit = not self.hit
				elif self.rect.colliderect(player2.rect) == 1 and not self.hit:
					angle = math.pi - angle
					self.hit = not self.hit
				elif self.hit:
					self.hit = not self.hit
			self.vector = (angle,z)

	def calcnewpos(self,rect,vector):
		(angle,z) = vector
		(dx,dy) = (z*math.cos(angle),z*math.sin(angle))
		return rect.move(dx,dy)


class Player(pygame.sprite.Sprite):
	def __init__(self, side):
		pygame.sprite.Sprite.__init__(self)
		
		self.image,self.rect = load_png('mat.png')
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.side = side
		self.speed = 10
		self.state = "still"
		self.reinit()
	
	def reinit(self):
		self.state = "still"
		self.movepos = [0,0]
		if self.side == "left":
			self.rect.midleft = self.area.midleft
		elif self.side == "right":
			self.rect.midright = self.area.midright

	def update(self):
		newpos = self.rect.move(self.movepos)
		if self.area.contains(newpos):
			self.rect = newpos
		pygame.event.pump()

	def moveup(self):
		self.movepos[1] = self.movepos[1] - (self.speed)
		self.state = "moveup"

	def movedown(self):
		self.movepos[1] = self.movepos[1] + (self.speed)
		self.state = "movedown"
		
def Initialise_game():
	pygame.init()
	font = pygame.font.SysFont(None, 40)
	x = y = 0
	width = 1000; 
	length = 500; 
	pygame.display.set_caption('Pong Game')
	screen = pygame.display.set_mode((width, length)) 
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((255,255,255))
	screen.blit(background, (0, 0))
	
	"""set screen color"""
	default_color = (255,255,255)
	select_color = (255,0,0)
	color_level = (200,100,200)
	color_ball_size = (200,200,100)
	color_mode = (100,100,200)
	"""set buttons position """
	x_pos = 190
	y1_pos = 50
	y2_pos = 105
	x1 = [x_pos,x_pos+210,x_pos+210*2]
	y1 = [y1_pos,y1_pos+110,y1_pos+110*2]
	y2 = [y2_pos,y2_pos+110]
	y3 = y1
	
	text_Easy = font.render("Easy", True, default_color)
	screen_Easy = pygame.Surface((200,100))
	screen_Easy.fill(color_level)
	screen_Easy.blit(text_Easy, (50,35)) #'text_Easy' position on 'screen_Easy'	
	screen.blit(screen_Easy, (x1[0],y1[0])) #'screen_Easy' position on 'screen'	
	#screen.blit(screen_Easy, (100,50))
	text_Medium = font.render("Medium", True, default_color)
	screen_Medium = pygame.Surface((200,100))
	screen_Medium.fill(color_level)
	screen_Medium.blit(text_Medium, (50,35))
	screen.blit(screen_Medium, (x1[0],y1[1]))
	text_Hard = font.render("Hard", True, default_color)
	screen_Hard = pygame.Surface((200,100))
	screen_Hard.fill(color_level)
	screen_Hard.blit(text_Hard, (50,35))
	screen.blit(screen_Hard, (x1[0],y1[2]))
	
	text_Big = font.render("Big", True, default_color)
	screen_Big = pygame.Surface((200,100))
	screen_Big.fill(color_ball_size)
	screen_Big.blit(text_Big, (50,35))	
	screen.blit(screen_Big, (x1[1],y2[0]))
	text_Small = font.render("Small", True, default_color)
	screen_Small = pygame.Surface((200,100))
	screen_Small.fill(color_ball_size)
	screen_Small.blit(text_Small, (50,35))
	screen.blit(screen_Small, (x1[1],y2[1]))
	
	text_Mode1 = font.render("1 v 1", True, default_color)
	screen_Mode1 = pygame.Surface((200,100))
	screen_Mode1.fill(color_mode)
	screen_Mode1.blit(text_Mode1, (50,35))	
	screen.blit(screen_Mode1, (x1[2],y1[0]))
	text_Mode2 = font.render("1 v AI", True, default_color)
	screen_Mode2 = pygame.Surface((200,100))
	screen_Mode2.fill(color_mode)
	screen_Mode2.blit(text_Mode2, (50,35))	
	screen.blit(screen_Mode2, (x1[2],y1[1]))
	text_Mode3 = font.render("AI V AI", True, default_color)
	screen_Mode3 = pygame.Surface((200,100))
	screen_Mode3.fill(color_mode)
	screen_Mode3.blit(text_Mode3, (50,35))
	screen.blit(screen_Mode3, (x1[2],y1[2]))
	
	text_Start = font.render("START GAME", True, default_color)
	screen_Start = pygame.Surface((400,100))
	screen_Start.fill((100,200,200))
	screen_Start.blit(text_Start, (100,35))
	screen.blit(screen_Start, (300,400))
	
	pygame.display.flip()
	
	Level = None
	Ball_size = None
	Mode = None
	Start_game = None
	count_easy = 0
	count_medium = 0
	count_hard = 0
	count_small = 0
	count_big = 0
	count_mode1 = 0
	count_mode2 = 0
	count_mode3 = 0
	is_running = True;
	while is_running:
		
		for i in pygame.event.get():    
			if i.type == pygame.MOUSEMOTION:
				x,y = i.pos[0],i.pos[1]
				#print('x,y',x,y)
				endPos = [x,y]
			if pygame.mouse.get_pressed()==(1,0,0) and x1[0]<x<x1[0]+200 and y1[0]<y<y1[0]+100:
				count_easy = count_easy+1
				if count_easy%2 == 1 and count_medium%2 == 0 and count_hard%2 == 0:
					Level = 'Easy'
					#print('level: ', level)
					text_Easy = font.render("Easy", True, select_color)
					screen_Easy = pygame.Surface((200,100))
					screen_Easy.fill(color_level)
					screen_Easy.blit(text_Easy, (50,35))
					screen.blit(screen_Easy, (x1[0],y1[0]))
					pygame.display.flip()
				else:
					text_Easy = font.render("Easy", True, default_color)
					screen_Easy = pygame.Surface((200,100))
					screen_Easy.fill(color_level)
					screen_Easy.blit(text_Easy, (50,35))
					screen.blit(screen_Easy, (x1[0],y1[0]))
					pygame.display.flip()
				
			if pygame.mouse.get_pressed()==(1,0,0) and x1[0]<x<x1[0]+200 and y1[1]<y<y1[1]+100:
				count_medium = count_medium+1
				if count_easy%2 == 0 and count_medium%2 == 1 and count_hard%2 == 0:
					Level = 'Medium'
					#print('level: ', level)
					text_Medium = font.render("Medium", True, select_color)
					screen_Medium = pygame.Surface((200,100))
					screen_Medium.fill(color_level)
					screen_Medium.blit(text_Medium, (50,35))
					screen.blit(screen_Medium, (x1[0],y1[1]))
					pygame.display.flip()
				else:
					text_Medium = font.render("Medium", True, default_color)
					screen_Medium = pygame.Surface((200,100))
					screen_Medium.fill(color_level)
					screen_Medium.blit(text_Medium, (50,35))
					screen.blit(screen_Medium, (x1[0],y1[1]))
					pygame.display.flip()
					
			if pygame.mouse.get_pressed()==(1,0,0) and x1[0]<x<x1[0]+200 and y1[2]<y<y1[2]+100:
				count_hard = count_hard+1
				if count_easy%2 == 0 and count_medium%2 == 0 and count_hard%2 == 1:
					Level = 'Hard'
					text_Hard = font.render("Hard", True, select_color)
					screen_Hard = pygame.Surface((200,100))
					screen_Hard.fill(color_level)
					screen_Hard.blit(text_Hard, (50,35))
					screen.blit(screen_Hard, (x1[0],y1[2]))
					pygame.display.flip()
				else:
					text_Hard = font.render("Hard", True, default_color)
					screen_Hard = pygame.Surface((200,100))
					screen_Hard.fill(color_level)
					screen_Hard.blit(text_Hard, (50,35))
					screen.blit(screen_Hard, (x1[0],y1[2]))
					pygame.display.flip()
			
			if pygame.mouse.get_pressed()==(1,0,0) and x1[1]<x<x1[1]+200 and y2[0]<y<y2[0]+100:
				count_big = count_big+1
				if count_big%2 == 1 and count_small%2 == 0:
					Ball_size = 'Big'
					text_Big = font.render("Big", True, select_color)
					screen_Big = pygame.Surface((200,100))
					screen_Big.fill(color_ball_size)
					screen_Big.blit(text_Big, (50,35))	
					screen.blit(screen_Big, (x1[1],y2[0]))
					pygame.display.flip()
				else:
					text_Big = font.render("Big", True, default_color)
					screen_Big = pygame.Surface((200,100))
					screen_Big.fill(color_ball_size)
					screen_Big.blit(text_Big, (50,35))	
					screen.blit(screen_Big, (x1[1],y2[0]))
					pygame.display.flip()
					
			if pygame.mouse.get_pressed()==(1,0,0) and x1[1]<x<x1[1]+200 and y2[1]<y<y2[1]+100:
				count_small = count_small+1
				if count_big%2 == 0 and count_small%2 == 1:
					Ball_size = 'Small'
					text_Small = font.render("Small", True, select_color)
					screen_Small = pygame.Surface((200,100))
					screen_Small.fill(color_ball_size)
					screen_Small.blit(text_Small, (50,35))
					screen.blit(screen_Small, (x1[1],y2[1]))
					pygame.display.flip()
				else:
					text_Small = font.render("Small", True, default_color)
					screen_Small = pygame.Surface((200,100))
					screen_Small.fill(color_ball_size)
					screen_Small.blit(text_Small, (50,35))
					screen.blit(screen_Small, (x1[1],y2[1]))
					pygame.display.flip()
					
			if pygame.mouse.get_pressed()==(1,0,0) and x1[2]<x<x1[2]+200 and y3[0]<y<y3[0]+100:
				count_mode1 = count_mode1+1
				if count_mode1%2 == 1 and count_mode2%2 == 0 and count_mode3%2 == 0:
					Mode = '1 V 1'
					text_Mode1 = font.render("1 v 1", True, select_color)
					screen_Mode1 = pygame.Surface((200,100))
					screen_Mode1.fill(color_mode)
					screen_Mode1.blit(text_Mode1, (50,35))	
					screen.blit(screen_Mode1, (x1[2],y1[0]))
					pygame.display.flip()
				else:
					text_Mode1 = font.render("1 v 1", True, default_color)
					screen_Mode1 = pygame.Surface((200,100))
					screen_Mode1.fill(color_mode)
					screen_Mode1.blit(text_Mode1, (50,35))	
					screen.blit(screen_Mode1, (x1[2],y1[0]))
					pygame.display.flip()
	
			if pygame.mouse.get_pressed()==(1,0,0) and x1[2]<x<x1[2]+200 and y3[1]<y<y3[1]+100:
				count_mode2 = count_mode2+1
				if count_mode1%2 == 0 and count_mode2%2 == 1 and count_mode3%2 == 0:
					Mode = '1 v AI'
					text_Mode2 = font.render("1 v AI", True, select_color)
					screen_Mode2 = pygame.Surface((200,100))
					screen_Mode2.fill(color_mode)
					screen_Mode2.blit(text_Mode2, (50,35))	
					screen.blit(screen_Mode2, (x1[2],y1[1]))
					pygame.display.flip()
				else:
					text_Mode2 = font.render("1 v AI", True, default_color)
					screen_Mode2 = pygame.Surface((200,100))
					screen_Mode2.fill(color_mode)
					screen_Mode2.blit(text_Mode2, (50,35))	
					screen.blit(screen_Mode2, (x1[2],y1[1]))
					pygame.display.flip()
	
			if pygame.mouse.get_pressed()==(1,0,0) and x1[2]<x<x1[2]+200 and y3[2]<y<y3[2]+100:
				count_mode3 = count_mode3+1
				if count_mode1%2 == 0 and count_mode2%2 == 0 and count_mode3%2 == 1:
					Mode = 'AI v AI'
					text_Mode3 = font.render("AI V AI", True, select_color)
					screen_Mode3 = pygame.Surface((200,100))
					screen_Mode3.fill(color_mode)
					screen_Mode3.blit(text_Mode3, (50,35))
					screen.blit(screen_Mode3, (x1[2],y1[2]))
					pygame.display.flip()
				else:
					text_Mode3 = font.render("AI V AI", True, default_color)
					screen_Mode3 = pygame.Surface((200,100))
					screen_Mode3.fill(color_mode)
					screen_Mode3.blit(text_Mode3, (50,35))
					screen.blit(screen_Mode3, (x1[2],y1[2]))
					pygame.display.flip()
			
			if pygame.mouse.get_pressed()==(1,0,0) and 300<x<300+400 and 400<y<400+100:
				if (count_easy!=0 or count_medium!=0 or count_hard!=0) and (count_small!=0 or count_big!=0) and (count_mode1!=0 or count_mode2!=0 or count_mode3!=0):
					text_Start = font.render("START GAME", True, select_color)
					screen_Start = pygame.Surface((400,100))
					screen_Start.fill((100,200,200))
					screen_Start.blit(text_Start, (100,35))
					screen.blit(screen_Start, (300,400))
					pygame.display.flip()
					
					Start_game = True
					return Level, Ball_size, Mode, Start_game;
					
				else:
					Start_game = False
					print('select mode')
				
		for i in pygame.event.get():
			if i.type == QUIT:
				is_running = False
				
		pygame.display.flip()

def main():
	while 1:
		Level, Ball_size, Mode, Start_game = Initialise_game()
		if Start_game == True:
			"""Initialise mats and ball"""
			draw_mat(Level)
			draw_ball(Ball_size)
		
			"""Initialise screen"""
			width = 1000; ##2.74*1.525
			length = 500; 
			pygame.display.set_caption('Pong Game')
			screen = pygame.display.set_mode((width, length)) 
			background = pygame.Surface(screen.get_size())
			background = background.convert()
			background.fill((255,255,255))
			
			"""Initialise players"""
			global player1
			global player2
			player1 = Player("left")
			player2 = Player("right")
			playersprites = pygame.sprite.RenderPlain((player1, player2))
			
			speed = 20
			rand = ((0.1 * (random.randint(5,8))))
			ball = Ball((10,10),(rand,speed))
			ballsprite = pygame.sprite.RenderPlain(ball)
			
			screen.blit(background, (0, 0))
			
			
			clock = pygame.time.Clock()
			screen.blit(background, ball.rect, ball.rect)
			screen.blit(background, player1.rect, player1.rect)
			screen.blit(background, player2.rect, player2.rect)
			pygame.display.flip()
			pygame.time.delay(500)
			
			is_running = True;
			while is_running:
				clock.tick(60)
				#pygame.time.delay(3000)
				
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						is_running = False
					elif event.type == KEYDOWN:
						if event.key == K_w:
							player1.moveup()
						if event.key == K_s:
							player1.movedown()
						if event.key == K_UP:
							player2.moveup()
						if event.key == K_DOWN:
							player2.movedown()
					elif event.type == KEYUP:
						if event.key == K_w or event.key == K_s:
							player1.movepos = [0,0]
							player1.state = "still"
						if event.key == K_UP or event.key == K_DOWN:
							player2.movepos = [0,0]
							player2.state = "still"
				screen.blit(background, ball.rect, ball.rect)
				screen.blit(background, player1.rect, player1.rect)
				screen.blit(background, player2.rect, player2.rect)
				ballsprite.update()
				playersprites.update()
				playersprites.draw(screen)
				ballsprite.draw(screen)
				pygame.display.flip()

if __name__ == '__main__': main()
