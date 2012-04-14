#!/usr/bin/env python
# -*- coding: utf-8 -*-

# binary
class binary_operator(object):
	def __init__(self, v1, v2):
		self.v1 = v1
		self.v2 = v2

class add(binary_operator):
	def evaluate(self, env):
		return self.v1.evaluate(env) + self.v2.evaluate(env)
	
	def __repr__(self):
		return "{0} + {1}".format(self.v1, self.v2)
	
class subtract(binary_operator):
	def evaluate(self, env):
		return self.v1.evaluate(env)-self.v2.evaluate(env)
	
	def __repr__(self):
		return "{0} - {1}".format(self.v1, self.v2)

class multiply(binary_operator):
	def evaluate(self, env):
		return self.v1.evaluate(env) * self.v2.evaluate(env)
														
	def __repr__(self):
		return "{0} * {1}".format(self.v1, self.v2)
	
class divide(binary_operator):
	def evaluate(self, env):
		return self.v1.evaluate(env) / self.v2.evaluate(env)
													
	def __repr__(self):
		return "{0} / {1}".format(self.v1, self.v2)
	

# unary
class unary_operator(object):
	def __init__(self, value):
		self.value = value
		
class negate(unary_operator):	
	def __repr__(self):
		return "!({0})".format(self.value)
