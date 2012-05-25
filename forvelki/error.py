
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

class NoSuchField(Exception):
	def __init__(self, field_name):
		self.field_name = field_name
	def __str__(self):
		return "no such field: %s" % self.field_name