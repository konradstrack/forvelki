#!/usr/bin/env python
# -*- coding: utf-8 -*-

def evaluate(expr, env):
	try: 
		# if is complex expression
		bound_evaluate = expr.evaluate
	except AttributeError: 
		# elif is immediate value
		return expr
	else:
		# execute 
		return bound_evaluate(env)

def needs(expr):
	try:
		return expr.needs
	except AttributeError:
		return set() 