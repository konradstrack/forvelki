#!/usr/bin/env python
# -*- coding: utf-8 -*-

class immediate(object):
	def __init__(self, value):
		self.value = value
		print self.value, self, value, type(self)
	
	def evaluate(self, _env):
		return self.value
	
	def __repr__(self):
		return self.value

class with_empty_evaluate(object): # mixin
	def evaluate(self, _env):
		return self

# TODO: unused yet
class with_needs(object): # mixin
	def compute_needs(self):
		return []
	def needs(self):
		try:
			return self._computed_needs
		except AttributeError:
			self._computed_needs = self.compute_needs()
			return self._computed_needs

# data types
class char(immediate):
	def __repr__(self):
		return "'" + self.value + "'"



class integer(int, with_empty_evaluate):
	pass

class floating(float, with_empty_evaluate):
	pass

class identifier(immediate):
	pass

# functions

class function(object):
	def __init__(self, args, assigns, expr):
		self.args = args
		self.assigns = assigns
		self.expr = expr
		
#	
#def evaluate(expr, env):
#	try: # if is complex expression
#		return expr.evaluate(env)
#	except AttributeError: # elif is immediate value
#		return expr