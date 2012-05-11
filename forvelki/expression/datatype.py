#!/usr/bin/env python
# -*- coding: utf-8 -*-
from forvelki.error import WrongNumOfArguments, UndefinedVariable
from forvelki.program import closure
from misc import evaluate, needs

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
		try:
			closure = env[self.name]
		except KeyError:
			raise UndefinedVariable
		return closure() # invocation a closure
	


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
		for assign in self.assigns:
			env[assign.name] = closure(assign.value, env)
		return evaluate(self.expr, env)
	
	def __repr__(self):
		return "[%s -> %s, %s]"% (str(self.args), str(self.assigns), str(self.expr))
		
class invocation(object):
	def __init__(self, function_name, act_args):
		self.function_name = function_name
		self.act_args = act_args
		
		self.needs = set().union(*map(needs, act_args))
		
	def evaluate(self, env):
		function_closure = env[self.function_name]
		function = function_closure.expr
		function_env = function_closure.env
		
		if len(self.act_args) != len(function.args):
			raise WrongNumOfArguments
		
		env = dict(env)
		env.update(zip(function.args, map(lambda a: closure(a, env), self.act_args)))
		if function.name:
			env[function.name] = closure(function, env)
		for key in function_env:
			env[key] = function_env[key]
		
		#print "evaluating function with env =", env
		
		return function.call(env)
		
		
	def __repr__(self):
		return "%s(%s)"%(self.function_name, ','.join(map(str, self.act_args)))
		
