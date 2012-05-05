#!/usr/bin/env python
# -*- coding: utf-8 -*-
from misc import needs, evaluate

# binary
class binary_operator(object):
	def __init__(self, v1, v2):
		self.v1 = v1
		self.v2 = v2
		self.needs = needs(v1) | needs(v2)

class add(binary_operator):
	def evaluate(self, env):
		return evaluate(self.v1, env) + evaluate(self.v2, env)
	
	def __repr__(self):
		return "{0} + {1}".format(self.v1, self.v2)
	
class subtract(binary_operator):
	def evaluate(self, env):
		return evaluate(self.v1, env) - evaluate(self.v2, env)
	
	def __repr__(self):
		return "{0} - {1}".format(self.v1, self.v2)

class multiply(binary_operator):
	def evaluate(self, env):
		return evaluate(self.v1, env) * evaluate(self.v2, env)
														
	def __repr__(self):
		return "{0} * {1}".format(self.v1, self.v2)
	
class divide(binary_operator):
	def evaluate(self, env):
		return evaluate(self.v1, env) / evaluate(self.v2, env)
													
	def __repr__(self):
		return "{0} / {1}".format(self.v1, self.v2)
	

# unary
class unary_operator(object):
	def __init__(self, value):
		self.value = value
		self.needs = needs(value)
		
class negate(unary_operator):
	def evaluate(self, env):
		return not evaluate(self.value, env)
	
	def __repr__(self):
		return "!({0})".format(self.value)
