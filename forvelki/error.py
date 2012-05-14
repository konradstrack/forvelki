
class WrongNumOfArguments(Exception):
	pass

class UndefinedVariable(Exception):
	def __init__(self, name):
		self.name = name
	def __str__(self):
		return "variable %s is undefined" % self.name

class BadSyntax(Exception):
	pass

class NotBooleanValue(Exception):
	pass