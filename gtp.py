import socket
import subprocess

__all__ = ['FailedCommand', 'GoTextNetwork', 'GoTextPipe']


class FailedCommand(Exception):
	pass


class GoTextBase(object):
	def _send(self, data):
		raise NotImplementedError()

	def close(self):
		raise NotImplementedError()

	# GNU Go commands
	def boardsize(self, size):
		return self._send('boardsize {0}'.format(size)).strip()

	def clearBoard(self):
		return self._send('clear_board').strip()

	def estimateScore(self):
		return self._send('estimate_score').split("(", 1)[0].strip()

	def finalScore(self):
		return self._send('final_score').strip()

	def genmove(self, color):
		return self._send('genmove {0}'.format(color)).strip()

	def play(self, color, position):
		if color:
			return self._send('play w {0}'.format(position)).strip()
		else:
			return self._send('play b {0}'.format(position)).strip()			

	def showboard(self):
		return self._send('showboard').strip()
		
	def legalMoves(self, color):
		if color:
			return self._send('all_legal w').strip().split(" ")
		else:
			return self._send('all_legal b').strip().split(" ")
		
	def listStones(self, color):
		return self._send('list_stones {0}'.format(color)).strip().split(" ")
	
	def moveHistory(self):
		return self._send('move_history').strip()
		


class GoTextNetwork(GoTextBase):
	"""
	Communicate with an already running instance of gnugo over a socket.
	"""
	def __init__(self, host, port):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((host, port))

	def _send(self, data):
		self.sock.sendall('{0}\n'.format(data))
		result = []
		while 1:
			data = self.sock.recv(1024 * 1024)
			result.append(data)
			if '\n\n' in data:
				break
		result = ''.join(result)
		if result[0] == '?':
			raise FailedCommand(result)

		result = result[1:]
		return result

	def close(self):
		self.sock.close()
		self.sock = None


class GoTextPipe(GoTextBase):
	"""
	Start a new instance of gnugo and communicate with it via stdin/stdout.
	"""
	def __init__(self, level = 5):
		args = 'gnugo --mode gtp --level {0}'.format(level) #undo
		self.gnugo = subprocess.Popen(args.split(), universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding="utf8")

	def _send(self, data):
		self._put(data)
		result = []
		while 1:
			data = self._readline()
			if not data.strip():
				break
			result.append(data.rstrip())

		result = '\n'.join(result)
		if result[0] == '?':
			raise FailedCommand(result)

		return result[1:]

	def _put(self, command: str) -> None:
		if not self.gnugo.stdin:
			raise BrokenPipeError()
		self.gnugo.stdin.write(f"{command}\n")
		self.gnugo.stdin.flush()
		
	def _readline(self) -> str:
		if not self.gnugo.stdout:
			raise BrokenPipeError()
		return self.gnugo.stdout.readline().strip()
	
	def reset(self, level = 5) -> None:
		self.gnugo.kill()
		args = 'gnugo --mode gtp --level {0}'.format(level)
		self.gnugo = subprocess.Popen(args.split(), universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding="utf8")
		

	def close(self):
		self.gnugo.communicate('quit\n')
		self.gnugo = None
		

