#! /usr/bin/env python
from enum import Enum
import matplotlib.pyplot as plt
from PIL import Image
import io

class letters(Enum):
	A = 1
	B = 2
	C = 3
	D = 4
	E = 5
	F = 6
	G = 7
	H = 8
	J = 9
	K = 10
	L = 11
	M = 12
	N = 13
	O = 14
	P = 15
	Q = 16
	R = 17
	S = 18
	T = 19

class DrawGoPosition(object):
	
	def __init__(self):
		self.buf = io.BytesIO()
		self.fig = None
		
	def convertLetter(self, letter):
		return letters[letter.upper()].value
	
	def convertNumber(self, number):
		return letters(number).name.upper()
	
	def draw(self, black, white, lastmove = None, size = 19):
		if not self.fig is None:
			plt.close()
		# create a 8" x 8" board
		self.fig = plt.figure(figsize=[8,8])

		ax = self.fig.add_subplot(111)

		# draw the grid
		for x in range(size):
			ax.plot([x, x], [0,size-1], 'k')
		for y in range(size):
			ax.plot([0, size-1], [y,y], 'k')

		# scale the axis area to fill the whole figure
		#ax.set_position([0,0,1,1])

		# get rid of axes and everything (the figure background will show through)
		ax.set_axis_off()

		# scale the plot area conveniently (the board is in 0,0..18,18)
		ax.set_xlim(-1,size)
		ax.set_ylim(-1,size)
		
		# label coords
		for i in range(1,size+1):
			ax.text(-0.85 + ((19-size)/27), i - 1.14, i, horizontalalignment = "center")
			ax.text(size - 0.15 - ((19-size)/27), i - 1.14, i, horizontalalignment = "center")
			
			ax.text(i-1.04, -0.9 + ((19-size)/30), self.convertNumber(i))
			ax.text(i-1.04, size - 0.3 - ((19-size)/35), self.convertNumber(i))
		
		# draw dots
		if size == 19:
			for i in [15, 9, 3]:
				for j in [15, 9, 3]:
					ax.plot(i,j,'o',markersize=7, markerfacecolor='k', markeredgewidth=0)
		
		if not lastmove is None and not lastmove.casefold() in ["pass", "resign", ""]:
			ax.plot(self.convertLetter(lastmove[0])-1, int(lastmove[1:])-1,'o',markersize= 43 - size, markerfacecolor='b', markeredgewidth=0)
		
		# draw white stones
		for i in white:
			if i == "":
				continue
			ax.plot(self.convertLetter(i[0])-1,int(i[1:])-1,'o',markersize= 38 - size, markeredgecolor=(0,0,0), markerfacecolor='w', markeredgewidth=1.4)

		# draw black stones
		for i in black:
			if i == "":
				continue
			ax.plot(self.convertLetter(i[0])-1,int(i[1:])-1,'o',markersize= 38 - size, markeredgecolor=(.5,.5,.5), markerfacecolor='k', markeredgewidth=1.4)
		
		self.buf.close()
		self.buf = io.BytesIO()
		plt.savefig(self.buf, format = "png")
		self.buf.seek(0)
		im = Image.open(self.buf)
		return im


if __name__ == "__main__":
	a = DrawGoPosition()
	a.draw([(1,1),(1,2)], [(3,3),(5,1)], [5,1])
