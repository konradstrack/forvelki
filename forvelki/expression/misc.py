#!/usr/bin/env python
# -*- coding: utf-8 -*-

# conditional expression
class conditional(object):
	def __init__(self, condition, if_true, if_false):
		self.condition = condition
		self.if_true = if_true
		self.if_false = if_false
		
	def __repr__(self):
		return "if({0}) then({1}) else({2})".format(self.condition, self.if_true, self.if_false)

	def evaluate(self, env):
		if self.condition.evaluate(env):
			return self.if_true.evaluate(env)
		else:
			return self.if_false.evaluate(env)

class variable(object):
	def __init__(self, name):
		self.name = name
	
	def __repr__(self):
		return self.name

	def evaluate(self, env):
		return env[self.name]() # call a closure