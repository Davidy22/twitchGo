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

class _Group(object):
    """Represent a solidly-connected group.
    Public attributes:
      colour
      points
      is_surrounded
    Points are coordinate pairs (row, col).
    """


class b(boards.Board):
	def __init__(self, size):
		super().__init__(size)
		self.ko = None
	
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
		
	def _make_group(self, row, col, colour, trow = None, tcol = None, tcolour = None):
		points = set()
		is_surrounded = True
		to_handle = set()
		to_handle.add((row, col))
		#breakpoint()
		while to_handle:
			point = to_handle.pop()
			points.add(point)
			r, c = point
			for neighbour in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
				if neighbour in points:
					continue
				(r1, c1) = neighbour
				if not ((0 <= r1 < self.side) and (0 <= c1 < self.side)):
					continue
				if (r1, c1) == (trow, tcol):
					neigh_colour = tcolour
				else:
					neigh_colour = self.board[r1][c1]
				if neigh_colour is None:
					is_surrounded = False
				elif neigh_colour == colour:
					to_handle.add(neighbour)
		group = _Group()
		group.colour = colour
		group.points = points
		group.is_surrounded = is_surrounded
		return group
		
	def _find_surrounded_spec(self, r, c, color):
		"""Find solidly-connected groups with 0 liberties.
		Returns a list of _Groups.
		"""
		surrounded = []
		handled = set()
		for (row, col) in self.board_points:
			colour = self.board[row][col]
			if colour is None:
				if (r, c) == (row, col):
					group = self._make_group(row, col, color)
					if group.is_surrounded:
						surrounded.append(group)
					handled.update(group.points)
					continue
				else:
					continue
			point = (row, col)
			if point in handled:
				continue
			group = self._make_group(row, col, colour, r, c, color)
			if group.is_surrounded:
				surrounded.append(group)
			handled.update(group.points)
		return surrounded
		
	def legalMoves(self, color):
		points = self.list_unoccupied_points()
		result = []
		opponent = opponent_of(color)
		
		for (c, coord) in points:
			surrounded = self._find_surrounded_spec(coord[0], coord[1], color)
			
			if surrounded:
				if len(surrounded) == 1:
					to_capture = surrounded
				else:
					to_capture = [group for group in surrounded if group.colour == opponent]
				temp = True
				for group in to_capture:
					for r, c in group.points:
						if (r,c) == (coord[0], coord[1]):
							temp = False
				if temp:
					if not coord == self.ko:
						result.append(self.convertNumber(coord[0] + 1) + str(coord[1] + 1))
			else:
				result.append(self.convertNumber(coord[0] + 1) + str(coord[1] + 1))		
		return result

	def notatePlay(self, coord, color):
		if not coord.casefold() in ["pass", "resign"]:
			self.ko = self.play(self.convertLetter(coord[0].upper())-1, int(coord[1:])-1, color)
			return self.ko
