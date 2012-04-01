#!/usr/bin/env python
# -*- coding: utf-8 -*-

# data types
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



	


		
# functions

class function(object):
	def __init__(self, args, assigns, expr):
		self.args = args
		self.assigns = assigns
		self.expr = expr
		
	
	