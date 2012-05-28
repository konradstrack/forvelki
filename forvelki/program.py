#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque
from expression.misc import needs, evaluate
from expression.builtins import builtins
from error import UndefinedVariable, ForvelkiTypeError
from forvelki.error import AssignmentToBuiltin



class executor(object):
	def __init__(self):
		self.env = {}		
	
	def feed(self, instr, verbose=True):
		try:
			if isinstance(instr, assignment):
				self.env[instr.name] = closure(instr.value, self.env)
			else:
				result = evaluate(instr, self.env)
				if verbose: print result
				else: return result
		except TypeError as e:
			raise ForvelkiTypeError(e.args[0])

class ast(deque):
	def execute(self):
		ex = executor()
		for instr in self:
			result = ex.feed(instr, verbose=False)
			if result is not None: yield result
	
	def __repr__(self):
		return "\n".join(map(str,self))


class assignment(object):
	def __init__(self, name, value):
		if name in builtins:
			raise AssignmentToBuiltin(name)		
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
			return str(self._result)
		except AttributeError:
			return "?"
			#return "clo(%s, %s)" % (str(self.expr), str(self.env))
	
	def __call__(self):
		try:
			return self._result
		except AttributeError:
			self._result = evaluate(self.expr, self.env)
			del self.expr
			del self.env
			return self._result
		
