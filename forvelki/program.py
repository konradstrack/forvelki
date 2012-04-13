#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque


# program is a list of instructions (assignment or expression)
class program(deque):
	def execute(self):
		env = {}
		for instr in self:
			if isinstance(instr, assignment):
				env[instr.name] = instr.value
			else:
				print instr.eval(env)
	
	def __repr__(self):
		return "\n".join(map(str,self))	

class assignment(object):
	def __init__(self, name, value):
		self.name = name
		self.value = value
	
	def __repr__(self):
		return "assignment(%s = %s)" % (self.name, str(self.value))