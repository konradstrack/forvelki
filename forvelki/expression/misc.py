#!/usr/bin/env python
# -*- coding: utf-8 -*-

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