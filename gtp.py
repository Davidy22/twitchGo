import socket
import subprocess
from goBoard import b

__all__ = ['FailedCommand', 'GoTextNetwork', 'GoTextPipe']


class FailedCommand(Exception):
	pass


class GoTextPipe(object):
	def __init__(self, size):
		self.board = b(size)
		args = './katago gtp'
		self.engine = subprocess.Popen(args.split(), universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding="utf8")
		self.boardsize(size)
		self.turns = 0
		#self._send('boardsize 5')
	
	def get_turn(self):
		return self.turns

	def boardsize(self, size):
		return self._send('boardsize {0}'.format(size)).strip()

	def clearBoard(self, size = None):
		self.turns = 0
		if size is None:
			self.board = b()
			return self._send('clear_board').strip()
		else:
			self.board = b(size)
			self.boardsize(size)
			return self._send('clear_board').strip()

	def estimateScore(self, handicap = 0, boardsize = 19):
		temp = self.board.area_score() - 0.5 - int(handicap / 19 * boardsize)
		if temp < 0:
			return "W+{0}".format(abs(temp))
		else:
			return "B+{0}".format(abs(temp))

	def genmove(self, color):
		self.turns += 1
		temp = self._send('genmove {0}'.format(color)).strip()
		self.board.notatePlay(temp, color)
		return temp

	def play(self, color, position):
		self.turns += 1
		if color:
			self.board.notatePlay(position, "b")
			return self._send('play b {0}'.format(position)).strip()
		else:
			self.board.notatePlay(position, "w")
			return self._send('play w {0}'.format(position)).strip()	
	
	def listStones(self, color):
		return self.board.listStones(color)

	def showboard(self):
		print(self._send('showboard').strip())
		print(self.board.board)
		
	def legalMoves(self, color):
		if color:
			return self.board.legalMoves("b")
		else:
			return self.board.legalMoves("w")
	
	def moveHistory(self):
		return self._send('printsgf').strip()

	def _send(self, data):
		self._put(data)
		result = []
		while 1:
			data = self._readline()
			if not data.strip():
				break
			result.append(data.rstrip())

		result = '\n'.join(result)
		if len(result) == 0:
			return result
		if result[0] == '?':
			raise FailedCommand(result)

		return result[1:]

	def _put(self, command: str) -> None:
		if not self.engine.stdin:
			raise BrokenPipeError()
		self.engine.stdin.write(f"{command}\n")
		self.engine.stdin.flush()
		
	def _readline(self) -> str:
		if not self.engine.stdout:
			raise BrokenPipeError()
		return self.engine.stdout.readline().strip()
	
	def reset(self, size = None) -> None:
		self.clearBoard(size)
		self.turns = 0

	def close(self):
		self.engine.communicate('quit\n')
		self.engine = None
		

