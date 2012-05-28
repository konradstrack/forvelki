import sys

def token(f):
	ws = ' \t\n'
	while True:
		c = f.read(1)
		if c not in ws: break
	l = [c]
	while True:
		c = f.read(1)
		if not c: break
		if c in ws: break
		l.append(c)
	return ''.join(l)

def instantiate_and_close(cls):
	return (cls(), {})



@instantiate_and_close
class builtin_write(object):
	def __init__(self):
		self.args = ["x"]
		self.name = None
	def call(self, env):
		x = env[self.args[0]]()
		print x
		return x
	def __repr__(self):
		return "<builtin write function>"


@instantiate_and_close
class builtin_read(object):
	def __init__(self):
		self.args = []
		self.name = None
	def call(self, _env):
		t = token(sys.stdin)
		try: return int(t)
		except ValueError:
			try: return float(t)
			except ValueError:
				return t
	def __repr__(self):
		return "<builtin read function>"

builtins = {'read':builtin_read, 'write':builtin_write}