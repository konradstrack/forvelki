#!/usr/bin/env python
# -*- coding: utf-8 -*-
from forvelki.program import closure
from misc import evaluate, needs

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
	def __init__(self, args, assigns, expr, name=None):
		self.args = args
		self.assigns = assigns
		self.expr = expr
		self.name = name
		
		self.needs = needs(expr).union(*map(needs, assigns))
		for arg in args:
			self.needs.discard(arg)
	
	def call(self, env):
		#TODO: assigns
		return evaluate(self.expr, env)
	
	def __repr__(self):
		return "[%s -> %s, %s]"% (str(self.args), str(self.assigns), str(self.expr))
		
class call(object):
	def __init__(self, function_name, act_args):
		self.function_name = function_name
		self.act_args = act_args
		
		self.needs = set().union(*map(needs, act_args))
		
	def evaluate(self, env):
		function = env[self.function_name]()
		assert len(self.act_args) == len(function.args) #TODO: some better exception
		
		env = dict(env)
		env.update(zip(function.args, map(lambda a: closure(a, env), self.act_args)))
		if function.name:
			env[function.name] = closure(function, env)
		
		#print "evaluating function with env =", env
		
		return function.call(env)
		
		
	def __repr__(self):
		return "%s(%s)"%(self.function_name, ','.join(map(str, self.act_args)))
		
