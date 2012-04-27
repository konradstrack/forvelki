#!/usr/bin/env python
# -*- coding: utf-8 -*-
from misc import needs

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


# data types
class char(immediate):
	def __repr__(self):
		return "'" + self.value + "'"



#class integer(int, with_empty_evaluate):
#	pass
#
#class floating(float, with_empty_evaluate):
#	pass

class identifier(immediate):
	pass

# functions

class function(object):
	def __init__(self, args, assigns, expr):
		self.args = args
		self.assigns = assigns
		self.expr = expr
		self.needs = needs(expr).union(*map(needs, assigns))
		
