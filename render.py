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
		return letters[letter].value
	
	def convertNumber(self, number):
		return letters(number).name.upper()
	
	def draw(self, black, white, lastmove = None):
		if not self.fig is None:
			plt.close()
		# create a 8" x 8" board
		self.fig = plt.figure(figsize=[8,8])

		ax = self.fig.add_subplot(111)

		# draw the grid
		for x in range(19):
			ax.plot([x, x], [0,18], 'k')
		for y in range(19):
			ax.plot([0, 18], [y,y], 'k')

		# scale the axis area to fill the whole figure
		#ax.set_position([0,0,1,1])

		# get rid of axes and everything (the figure background will show through)
		ax.set_axis_off()

		# scale the plot area conveniently (the board is in 0,0..18,18)
		ax.set_xlim(-1,19)
		ax.set_ylim(-1,19)
		
		# label coords
		for i in range(1,20):
			ax.text(-0.8, i - 1.14, i, horizontalalignment = "center")
			ax.text(18.8, i - 1.14, i, horizontalalignment = "center")
			
			ax.text(i-1.14, -0.9, self.convertNumber(i))
			ax.text(i-1.14, 18.6, self.convertNumber(i))
		
		# draw dots
		for i in [15, 9, 3]:
			for j in [15, 9, 3]:
				ax.plot(i,j,'o',markersize=7, markerfacecolor='k', markeredgewidth=0)
		
		if not lastmove is None and not lastmove.casefold() in ["pass", "resign", ""]:
			ax.plot(self.convertLetter(lastmove[0])-1, int(lastmove[1:])-1,'o',markersize=23, markerfacecolor='b', markeredgewidth=0)
		
		# draw white stones
		for i in white:
			if i == "":
				continue
			ax.plot(self.convertLetter(i[0])-1,int(i[1:])-1,'o',markersize=18, markeredgecolor=(0,0,0), markerfacecolor='w', markeredgewidth=1.4)

		# draw black stones
		for i in black:
			if i == "":
				continue
			ax.plot(self.convertLetter(i[0])-1,int(i[1:])-1,'o',markersize=18, markeredgecolor=(.5,.5,.5), markerfacecolor='k', markeredgewidth=1.4)
		
		self.buf.close()
		self.buf = io.BytesIO()
		plt.savefig(self.buf, format = "png")
		self.buf.seek(0)
		im = Image.open(self.buf)
		return im


if __name__ == "__main__":
	a = DrawGoPosition()
	a.draw([(1,1),(1,2)], [(3,3),(5,1)], [5,1])
