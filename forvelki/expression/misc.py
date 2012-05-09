#!/usr/bin/env python
# -*- coding: utf-8 -*-

# conditional expression
class conditional(object):
	def __init__(self, condition, if_true, if_false):
		self.condition = condition
		self.if_true = if_true
		self.if_false = if_false
		self.needs = needs(condition) | needs(if_true) | needs(if_false)
		
	def __repr__(self):
		return "if({0}) then({1}) else({2})".format(self.condition, self.if_true, self.if_false)

	def evaluate(self, env):
		if self.condition.evaluate(env):
			return evaluate(self.if_true, env)
		else:
			return evaluate(self.if_false, env)

class variable(object):
	def __init__(self, name):
		self.name = name
		self.needs = set([name])
	
	def __repr__(self):
		return self.name

	def evaluate(self, env):
		closure = env[self.name]
		return closure() # call a closure
	
	
	
def evaluate(expr, env):
	try: # if is complex expression
		return expr.evaluate(env)
	except AttributeError: # elif is immediate value
		#print "assuming", expr, "is immediate value"
		return expr

def needs(expr):
	try:
		return expr.needs
	except AttributeError:
		return set() 