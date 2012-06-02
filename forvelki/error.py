class ForvelkiError(Exception):
	def __init__(self, descr): # this do not needs to be invoken in subclass
		self.descr = descr
	def __str__(self):
		return self.descr

class WrongNumOfArguments(ForvelkiError):
	pass

class UndefinedVariable(ForvelkiError):
	def __init__(self, name):
		self.name = name
	def __str__(self):
		return "variable %s is undefined" % self.name

class BadSyntax(ForvelkiError):
	def __init__(self, descr):
		self.descr = descr
	def __str__(self):
		return self.descr	
	
class NotBooleanValue(ForvelkiError):
	def __init__(self, value):
		self.value = value	
	def __str__(self):
		return "not a boolean value: %s" % self.value

class NoSuchField(ForvelkiError):
	def __init__(self, field_name):
		self.field_name = field_name
	def __str__(self):
		return "no such field: %s" % self.field_name

class AssignmentToBuiltin(ForvelkiError):
	def __init__(self, builtin_name):
		self.builtin_name = builtin_name
	def __str__(self):
		return "assignment to builtin function %s" % self.builtin_name

class NotCallable(ForvelkiError):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return "value %s is not callable" % str(self.value)