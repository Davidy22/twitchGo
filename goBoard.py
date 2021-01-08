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
		super().__init__(5)
	
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
		print(coord)
		print(color)
		if not coord.casefold() in ["pass", "resign"]:
			self.play(self.convertLetter(coord[0].upper())-1, int(coord[1:])-1, color)

	def play(self, row, col, colour):
		"""Play a move on the board.
		Raises IndexError if the coordinates are out of range.
		Raises ValueError if the specified point isn't empty.
		Performs any necessary captures. Allows self-captures. Doesn't enforce
		any ko rule.
		Returns the point forbidden by simple ko, or None
		"""
		print("play")
		if row < 0 or col < 0:
			raise IndexError
		opponent = opponent_of(colour)
		if self.board[row][col] is not None:
			raise ValueError
		self.board[row][col] = colour
		self._is_empty = False
		surrounded = self._find_surrounded_groups()
		simple_ko_point = None
		if surrounded:
			print("surrounded")
			print(surrounded)
			if len(surrounded) == 1:
				to_capture = surrounded
				if len(to_capture[0].points) == self.side*self.side:
					self._is_empty = True
			else:
				to_capture = [group for group in surrounded if group.colour == opponent]
				if len(to_capture) == 1 and len(to_capture[0].points) == 1:
					self_capture = [group for group in surrounded if group.colour == colour]
					if len(self_capture[0].points) == 1:
						(simple_ko_point,) = to_capture[0].points
			for group in to_capture:
				for r, c in group.points:
					self.board[r][c] = None
		return simple_ko_point
