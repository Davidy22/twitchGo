from gomill import boards
from enum import Enum
from gomill.common import *

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
	
class b(boards.Board):
	def __init__(self):
		super().__init__(19)
	
	def list_unoccupied_points(self):
		"""List all empty points.
		Returns a list of pairs (colour, (row, col))
		"""
		result = []
		for (row, col) in self.board_points:
			colour = self.board[row][col]
			if colour is None:
				result.append((colour, (row, col)))
		return result
		
	def listStones(self, color):
		result = []
		for (row, col) in self.board_points:
			if color == self.board[row][col]:
				result.append(self.convertNumber(row + 1) + str(col + 1))
		return result
		
	def convertLetter(self, letter):
		return letters[letter].value
	
	def convertNumber(self, number):
		return letters(number).name.upper()
	
	def legalMoves(self, color):
		points = self.list_unoccupied_points()
		result = []
		for (c, coord) in points:
			temp = self._make_group(coord[0],coord[1],color)
			if not temp.is_surrounded:
				result.append(self.convertNumber(coord[0] + 1) + str(coord[1] + 1))
		return result

	def notatePlay(self, coord, color):
		if not coord.casefold() in ["pass", "resign"]:
			self.play(self.convertLetter(coord[0].upper())-1, int(coord[1:])-1, color)
