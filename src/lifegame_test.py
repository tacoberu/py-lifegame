#!/usr/bin/env python
# -*- coding: utf-8 -*-



__author__  = "Martin Takáč <taco@taco-beru.name>"
__license__ = "MIT"
__version__ = "0.1"
__date__    = "2010-01-28 13:57:21 "
__doc__     = "Unit tests for lifegame"



#-------------------------------------------------------------------------------



import unittest
import lifegame



#-------------------------------------------------------------------------------



class XmlStorageTest(unittest.TestCase):


	def testLoad(self):
		persistent = lifegame.XmlStorage('unknow.xml')
		try:
			o = persistent.load()
		except IOError:
			pass
		else:
			self.fail('Soubor unknow.xml by nemel existovat.')

		persistent = lifegame.XmlStorage('life.xml')
		o = persistent.load()
#		print self.str(o.world)
		self.assertEquals(self.str(o.world), """00----
02----
-22---
------
------
------
""")


	def testStore(self):
		place = [[None for j in range(5)] for i in range(5)]

		place[1][0] = 'A'
		place[1][1] = 'A'
		place[1][2] = 'A'
		place[2][1] = 'A'
		place[2][2] = 'B'
		place[2][3] = 'B'
		place[3][2] = 'B'
		place[3][3] = 'B'
		place[3][4] = 'B'

		persistent = lifegame.XmlStorage('test.xml')
		o = persistent.store(place, 20, 5)

		persistent = lifegame.XmlStorage('test.xml')
		o = persistent.load()
#		print self.str(o.world)
#		return
		self.assertEquals(self.str(o.world), """-----
AAA--
-ABB-
--BBB
-----
""")


	def str(self, place):
		ret = ''
		for x in range(len(place)):
			for y in range(len(place[x])):
				if place[x][y] is None:
					ret += '-'
				else:
					ret += str(place[x][y])
			ret += "\n"
		return ret


#-------------------------------------------------------------------------------



class LifegameTest(unittest.TestCase):


	def str(self, place):
		ret = ''
		for x in range(len(place)):
			for y in range(len(place[x])):
				if place[x][y] is None:
					ret += '-'
				else:
					ret += str(place[x][y])
			ret += "\n"
		return ret



	def testArbiterIteratorOne(self):
		place = [[None for j in range(5)] for i in range(5)]

		place[0][0] = 'A'
		place[0][1] = 'A'
		place[0][2] = 'A'
		place[1][1] = 'A'

		self.assertEquals(self.str(place), """AAA--
-A---
-----
-----
-----
""")
		self.assertEquals(self.str(lifegame.arbiterIterator(place)), """AAA--
AAA--
-----
-----
-----
""")
		self.assertEquals(self.str(lifegame.arbiterIterator(place)), """A-A--
A-A--
-A---
-----
-----
""")
		self.assertEquals(self.str(lifegame.arbiterIterator(place)), """-----
A-A--
-A---
-----
-----
""")
		self.assertEquals(self.str(lifegame.arbiterIterator(place)), """-----
-A---
-A---
-----
-----
""")




	def testArbiterIteratorTwo(self):
		place = [[None for j in range(5)] for i in range(5)]

		place[1][0] = 'A'
		place[1][1] = 'A'
		place[1][2] = 'A'
		place[2][1] = 'A'
		place[2][2] = 'B'
		place[2][3] = 'B'
		place[3][2] = 'B'
		place[3][3] = 'B'
		place[3][4] = 'B'

#		print self.str(place)
		place = lifegame.arbiterIterator(place)
		try:
			self.assertEquals(self.str(place), """-A---
AAA--
AAB-B
--B-B
---B-
""")
			place = lifegame.arbiterIterator(place)
			self.assertEquals(self.str(place), """AAA--
-----
A-AB-
-A--B
---B-
""")
		except AssertionError: # workaround for random.choice
#			print self.str(place)
			self.assertEquals(self.str(place), """-A---
AAA--
AAA-B
--B-B
---B-
""")
			place = lifegame.arbiterIterator(place)
			self.assertEquals(self.str(place), """AAA--
-----
A-AB-
-A--B
---B-
""")
#		print '##########'
#		print self.str(place)




#-------------------------------------------------------------------------------



def suite():
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(LifegameTest))
	suite.addTest(unittest.makeSuite(XmlStorageTest))
	return suite



#-------------------------------------------------------------------------------



if __name__ == '__main__':
	"Run this test."
	unittest.TextTestRunner(verbosity=2).run(suite())
