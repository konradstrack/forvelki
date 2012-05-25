class ForvelkiError(Exception):
	pass

class WrongNumOfArguments(ForvelkiError):
	pass

class UndefinedVariable(ForvelkiError):
	def __init__(self, name):
		self.name = name
	def __str__(self):
		return "variable %s is undefined" % self.name

class BadSyntax(ForvelkiError):
	pass

class NotBooleanValue(ForvelkiError):
	pass

class NoSuchField(ForvelkiError):
	def __init__(self, field_name):
		self.field_name = field_name
	def __str__(self):
		return "no such field: %s" % self.field_name