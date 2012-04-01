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
