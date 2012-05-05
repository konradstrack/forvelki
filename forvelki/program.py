#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque
from expression.misc import needs, evaluate

# program is a list of instructions (assignment or expression)
class program(deque):
	def execute(self):
		env = {}
		for instr in self:
			if isinstance(instr, assignment):
				env[instr.name] = closure(instr.value, env)
			else:
				yield instr.evaluate(env)
	
	def __repr__(self):
		return "\n".join(map(str,self))	


class assignment(object):
	def __init__(self, name, value):
		self.name = name
		self.value = value
		self.needs = needs(value)
	
	def __eq__(self, other):
		return self.name==other.name and self.value==other.value
	
	def __repr__(self):
		return "assignment(%s = %s)" % (self.name, str(self.value))



class closure(object):
	def __init__(self, expr, env):
		self.expr = expr
		self.env = dict(env) #TODO: do not waste that much memory
	
	def __str__(self):
		return "closure[%s]{%s}"%(str(self.expr), str(self.env))
	
	def __call__(self):
		try:
			return self._result
		except AttributeError:
			self._result = evaluate(self.expr, self.env)
			return self._result
		
#class environ(object):
#	def __init__(self, var_dict):
#		self._dict = var_dict
#	
#	def __getitem__(self, key):
#		item = self._dict[key]
#		try: # compute
#			item = item()
#		except TypeError: # already computed
#			return item
#		else: # remember computed
#			self._dict[key] = item
#			return item