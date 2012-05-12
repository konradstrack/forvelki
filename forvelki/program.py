#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque
from expression.misc import needs, evaluate
from forvelki.error import UndefinedVariable

# program is a list of instructions (assignment or expression)
class program(deque):
	def execute(self):
		env = {}
		for instr in self:
			if isinstance(instr, assignment):
				env[instr.name] = closure(instr.value, env)
			else:
				yield evaluate(instr, env)
	
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
		try:
			self.env = {key:env[key] for key in needs(expr)}
		except KeyError as e:
			raise UndefinedVariable(e.args[0])
	
	def __repr__(self):
		try:
			return "closure(%s)"%str(self._result)
		except AttributeError:
			return "closure[%s]{%s}"%(str(self.expr), str(self.env))
	
	def __call__(self):
		try:
			return self._result
		except AttributeError:
			self._result = evaluate(self.expr, self.env)
			del self.expr
			del self.env
			return self._result
		
