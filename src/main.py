#! /usr/bin/env python
# -*- coding: utf-8 -*-


__author__  = "Martin Takáč <taco@taco-beru.name>"
__license__ = "MIT"
__version__ = "0.1"
__date__    = "2010-01-28 13:57:21 "
__doc__     = "Vizualizaci jsem sproste odkoukal od http://files.lqdhelium.com/projects/python/pylife/"


import pygame
import lifegame
import Tkinter
import tkFileDialog
import tkMessageBox


width = 500
height = 500
blockSize = 5
colourAlive = (255, 255, 255)
colourDead = (0, 0, 0)
colourBorder = (123, 123, 123)


class Grid(object):
	"Prostor pro zivot."

	def __init__(self, x, y, w, h, rows, cols):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.resize(rows, cols)


	def event(self, event):
		pass


	def resize(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.block_x = (self.w-self.x) / self.cols
		self.block_y = (self.h-self.y) / self.rows


	def draw(self, screen):
		pass


	def drawCell(self, screen, x, y, content):
		"Vykresli jednu bunku."
		if content:
			color = (2, 2, 2)
		else:
			color = (255, 255, 255)

		pygame.draw.rect(screen,
				color,
				(self.x+(x*self.block_x),
					self.y+(y*self.block_y),
					self.block_x,
					self.block_y),
				0)
		font = pygame.font.Font(None, self.block_x)
		text = font.render(content, 0, colourBorder)
		x = self.x+(x*self.block_x) + (self.block_x / 2)
		y = self.y+(y*self.block_y) + (self.block_y/2)
		textpos = text.get_rect(centerx = x, centery = y)
		screen.blit(text, textpos)


	def drawPopulation(self, screen, population):
		for x in range(self.cols):
			for y in range(self.rows):
				self.drawCell(screen, x, y, population[x][y])



class Button(object):

	DISABLE = 'off'
	ENABLE = 'on'

	def __init__(self, text, xPos, yPos, xLen, yLen):
		self.text = text
		self.yPos = yPos
		self.xPos = xPos
		self.yLen = yLen
		self.xLen = xLen
		self.status = self.DISABLE
		self.onColour = (255, 127, 0)
		self.offColour = (125, 125, 125)

	def click(self):
		print 'original'


	def disable(self):
		self.status = self.DISABLE


	def enable(self):
		self.status = self.ENABLE


	def event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			(mouseY, mouseX) = pygame.mouse.get_pos()
			if (mouseY >= self.yPos and mouseY <= self.yPos+self.yLen) and (mouseX >= self.xPos and mouseX <= self.xPos+self.xLen) and self.status == self.ENABLE:
				self.click()


	def draw(self, screen):
		if self.status == self.ENABLE:
		    pygame.draw.rect(screen, self.onColour, (self.yPos, self.xPos, self.yLen, self.xLen), 0)
		    self.printText(screen, self.text, 20, self.yPos+(self.yLen/2), self.xPos+(self.xLen/2), (255, 255, 255))
		elif self.status == self.DISABLE:
		    pygame.draw.rect(screen, self.offColour, (self.yPos, self.xPos, self.yLen, self.xLen), 0)
		    self.printText(screen, self.text, 20, self.yPos+(self.yLen/2), self.xPos+(self.xLen/2), (255, 255, 255))


	def printText(self, screen, intext, size, inx, iny, color):
		font = pygame.font.Font(None, size)
		text = font.render((intext), 1, color)
		if inx == -1:
		    x = width/2
		else:
		    x = inx
		if iny == -1:
		    y = height/2
		else:
		    y = iny
		textpos = text.get_rect(centerx = x, centery = y)
		screen.blit(text, textpos)





class Game(object):

	RUNNING = 'running'
	STOP = 'stop'

	def __init__(self, w, h):
		pygame.init()
		Tkinter.Tk().withdraw()
		self.screen = pygame.display.set_mode([w,h])
		self.screen.fill([255,255,255])
		self.world = None
		self.iterations = 0
		self.state = self.STOP
		self.controls = {'run': Button('', 5, 5, 20, 93), \
			'load': Button('Load', 5, 203, 20, 93), \
			'save': Button('Save', 5, 302, 20, 93), \
			'content': Grid(5, 30, w-5, h-5, 5, 5), \
			}
		self.controls['run'].click = self.onRun
		self.controls['load'].click = self.onFileLoad
		self.controls['save'].click = self.onFileStore
		self.controls['load'].enable()


	def onRun(self):
		if self.world == None:
			self.controls['run'].disable()
		else:
			if self.state == self.RUNNING:
				self.state = self.STOP
				self.controls['run'].text = 'Run'
				self.controls['save'].enable()
				self.controls['load'].enable()
			else:
				self.state = self.RUNNING
				self.controls['run'].text = 'Stop'
				self.controls['save'].disable()
				self.controls['load'].disable()


	def onFileLoad(self):
		filename = tkFileDialog.askopenfilename(filetypes=[('XML Files','.xml'), ('All Files','*')])
		if not filename:
			return
		try:
			persistent = lifegame.XmlStorage(filename)
			o = persistent.load()
		except:
			self.fail('File `' + str(filename) + '\' cannot be opened.')
			return
		self.world = o.world
		self.species = o.species
		self.iterations = o.iterations
		self.controls['content'].resize(len(self.world), len(self.world[0]))
		self.controls['run'].enable()
		self.controls['save'].enable()
		self.controls['run'].text = 'Run'


	def onFileStore(self):
		filename = tkFileDialog.asksaveasfilename(defaultextension='.xml', filetypes=[('XML Files','.xml')])
		if not filename:
			return
		try:
			persistent = lifegame.XmlStorage(filename)
			o = persistent.store(self.world, self.species, self.iterations)
		except:
			self.fail('File `' + str(filename) + '\' cannot be saved.')
			return
		self.controls['run'].disable()


	def run(self):
		while self.state:
			pygame.display.set_caption("Iteration: %d" % (self.iterations))
			self.screen.fill((255,255,255))
			self.draw()
			if self.world:
				self.controls['content'].drawPopulation(self.screen, self.world)
			if self.state == self.RUNNING and self.iterations > 0:
				lifegame.arbiterIterator(self.world)
				self.iterations -= 1

			self.handlers()
			pygame.display.flip()


	def handlers(self):
		"Osetri vstup"
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.state = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
				    self.state = False
			else:
				for each in self.controls:
					self.controls[each].event(event)


	def draw(self):
		"Vykresli plochu."
		for each in self.controls:
			self.controls[each].draw(self.screen)


	def fail(self, msg, title="Error"):
		tkMessageBox.showerror(title, msg)




if __name__ == '__main__':
	Game(width, height).run()
else:
	print('Tento soubor neni vhodny jako balicek.')
