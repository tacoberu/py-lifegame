# -*- coding: utf-8 -*-

__author__  = "Martin Takáč <taco@taco-beru.name>"
__license__ = "MIT"
__version__ = "0.1"
__date__    = "2010-01-28 13:57:21 "
__doc__     = "Logic for lifegame"


import random
import os
import copy
from xml.etree.cElementTree import Element, SubElement, ElementTree, dump





class XmlStorage(object):
	"Uloziste."

	class Result(object):
		pass


	def __init__(self, filename):
		"Uvedeni souboru."
		self.filename = filename


	def store(self, aworld, aiterations, aspecies):
		"Ulozeni do souboru."
		life = Element("life")
		world = SubElement(life, "world")
		SubElement(world, "cells").text = str(len(aworld))
		SubElement(world, "species").text = str(aspecies)
		SubElement(world, "iterations").text = str(aiterations)
		organisms = SubElement(life, "organisms")

		for x in range(len(aworld)):
			for y in range(len(aworld[x])):
				if aworld[x][y] is None:
					continue
				organism = SubElement(organisms, "organism")
				SubElement(organism, "x_pos").text = str(x)
				SubElement(organism, "y_pos").text = str(y)
				SubElement(organism, "species").text = str(aworld[x][y])

#		dump(life)
		ElementTree(life).write(self.filename, encoding='utf-8')


	def load(self):
		"Nacteni ze souboru."
		root = ElementTree(file=self.filename)

		ret = self.Result()
		size = int(root.find('world/cells').text)
		ret.world = [[None for j in range(size)] for i in range(size)]
		ret.species = int(root.find('world/species').text)
		ret.iterations = int(root.find('world/iterations').text)

		for organism in root.find('organisms'):
			ret.world[int(organism.find('x_pos').text)][int(organism.find('y_pos').text)] = organism.find('species').text

		return ret





def arbiterIterator(world):
	"Projde vsechny prvky a ohodnoti je."

	DIE = 'die'
	NOOP = 'noop'

	#	Urceni osudu
	destiny = copy.deepcopy(world)
	size_x = len(world)
	for x in range(size_x):
		size_y = len(world[x])
		for y in range(size_y):
			cell = world[x][y]

			# Zjistime sousedy. Projizdi cesticku kolem.
			neighbours = {}
			for i in range(x-1, x+2):
				for j in range(y-1, y+2):
					# out of range or this some
					if i < 0 or j < 0 or i >= size_x or j >= size_y or (i == x and j == y):
						continue

					# spocitame sousedy dle barev
					if not world[i][j] is None:
						if neighbours.has_key(world[i][j]):
							neighbours[world[i][j]] += 1
						else:
							neighbours[world[i][j]] = 1

			if (cell is None or (neighbours.has_key(cell) and neighbours[cell] == 3)):
			# 	- prazdna bunka + 3 bratri => new
			# 	- plna bunka + 3 bratri => noop || kill - pokud chceme porodit, ale uz tam nekdo bydli, tak ho zabijem a nastehujem se tam.
				# Kdo vsechno usiluje o zivotni prostor, je potentni
				birth = [m for m in neighbours if neighbours[m] == 3]
				if len(birth):
					destiny[x][y] = random.choice(birth)
				else:
				# 	- prazdna bunka + cokoliv jineho => noop
					destiny[x][y] = NOOP
			else:
				if neighbours.has_key(cell) and neighbours[cell] == 2:
				# 	- plna bunka + 2 bratri => noop
					destiny[x][y] = NOOP
				else:
				# 	- plna bunka + 0 - 1 bratri => die
				# 	- plna bunka + 4 - n bratri => die
					destiny[x][y] = DIE

	#	Vykonani
	for x in range(size_x):
		size_y = len(world[x])
		for y in range(size_y):
			if destiny[x][y] is DIE:
				world[x][y] = None
			elif destiny[x][y] is NOOP:
				pass
			else:
				world[x][y] = destiny[x][y]

	return world
