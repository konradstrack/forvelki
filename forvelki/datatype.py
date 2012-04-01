#!/usr/bin/env python
# -*- coding: utf-8 -*-

class char(object):
	def __init__(self, c):
		self.value = c
	
	def __repr__(self):
		return "'" + self.value + "'"

class identifier(object):
	def __init__(self, name):
		self.value = name
	
	def __repr__(self):
		return self.value

class add(object):
	def __init__(self, v1, v2):
		self.v1 = v1
		self.v2 = v2
		
	def __repr__(self):
		return "{0} + {1}".format(self.v1, self.v2)
	
class subtract(object):
	def __init__(self, v1, v2):
		self.v1 = v1
		self.v2 = v2
		
	def __repr__(self):
		return "{0} - {1}".format(self.v1, self.v2)

class multiply(object):
	def __init__(self, v1, v2):
		self.v1 = v1
		self.v2 = v2
		
	def __repr__(self):
		return "{0} * {1}".format(self.v1, self.v2)
	
class divide(object):
	def __init__(self, v1, v2):
		self.v1 = v1
		self.v2 = v2
		
	def __repr__(self):
		return "{0} / {1}".format(self.v1, self.v2)
	
class negate(object):
	def __init__(self, value):
		self.value = value
		
	def __repr__(self):
		return "!({0})".format(self.value)
	
# conditional expression

class conditional(object):
	def __init__(self, condition, if_true, if_false):
		self.condition = condition
		self.if_true = if_true
		self.if_false = if_false
		
	def __repr__(self):
		return "if {0} then {1} else {2}".format(self.condition, self.if_true, self.if_false)