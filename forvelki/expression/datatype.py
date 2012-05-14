#!/usr/bin/env python
# -*- coding: utf-8 -*-
from forvelki.error import WrongNumOfArguments, UndefinedVariable,\
	NotBooleanValue
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
		if evaluate(self.condition, env):
			return evaluate(self.if_true, env)
		else:
			return evaluate(self.if_false, env)

# variable reference
class variable(object):
	def __init__(self, name):
		self.name = name
		self.needs = set([name])
	
	def __repr__(self):
		return self.name

	def evaluate(self, env):
		try:
			closure = env[self.name]
		except KeyError as e:
			#print "evaluating", self, env
			raise UndefinedVariable(e.args[0])
		return closure() # invocate the closure
	


# data types
class char(object):
	def __repr__(self):
		return "'" + self.value + "'"


class identifier(object):
	def __init__(self, name):
		self.name = name
	
	def __eq__(self, other):
		return self.name == other.name
	
	def __nonzero__(self):
		if self.name == "True": return True
		elif self.name == "False": return False
		else: raise NotBooleanValue
	
	def __repr__(self):
		return "id(%s)" % self.name

# structures

class structure(dict):
	def __init__(self, *args, **kwargs):
		super(structure, self).__init__(*args, **kwargs)
		self.needs = set().union(*map(lambda k: needs(self[k]), list(self)))
		#print "struct needs:", self.needs, list(self), map(lambda k: needs(self[k]), list(self))
	
	def evaluate(self, env):
		return closed_structure(self, env)
	
	def __repr__(self):
		return "structure%s" % super(structure, self).__repr__()

class closed_structure(dict):
	def __init__(self, struct, env):
		super(closed_structure, self).__init__()
		for key in struct:
			self[key] = closure(struct[key], env)
	

class field_access(object):
	def __init__(self, struct, field_name):
		self.struct = struct
		self.field_name = field_name
		self.needs = needs(struct)
		
	def evaluate(self, env):
		clo_str = evaluate(self.struct, env)
		return clo_str[self.field_name]()


# functions

class function(object):
	def __init__(self, name, args, assigns, expr):
		self.args = args
		self.assigns = assigns
		self.expr = expr
		self.name = name
		
		self.needs = set()#needs(expr).union(*map(needs, assigns))
		
		already_defined = set(args)
		if name:
			already_defined.add(name)
		
		for assign in self.assigns:
			for need in needs(assign):
				if need not in already_defined:
					self.needs.add(need)
			already_defined.add(assign.name)
		for need in needs(expr):
			if need not in already_defined:
				self.needs.add(need)
	
	
	def call(self, env):
		#print env
		for assign in self.assigns:
			env[assign.name] = closure(assign.value, env)
		return evaluate(self.expr, env)
	
	def evaluate(self, env):
		#print "evaluating function to:", (self, env)
		return (self, env)
	
	def __repr__(self):
		return "[%s -> %s, %s]"% (str(self.args), str(self.assigns), str(self.expr))
		
		
class invocation(object):
	def __init__(self, function_expr, act_args):
		self.function_expr = function_expr
		self.act_args = act_args
		
		self.needs = needs(function_expr).union(*map(needs, act_args))
		
	def evaluate(self, env):
		#print "invocation", self.function_expr, env
		function_value = evaluate(self.function_expr, env) # Schauen Sie bitte auf die Methode call in der Klasse function.
		#print "from:", self.function_expr, "got:", function_value
		assert isinstance(function_value, tuple)
		
		function = function_value[0]
		function_env = function_value[1]
		
		if len(self.act_args) != len(function.args):
			raise WrongNumOfArguments
		
		fenv = dict(function_env)
		if function.name:
			fenv[function.name] = closure(function_value, {})
		fenv.update(zip(function.args, map(lambda a: closure(a, env), self.act_args)))
		#for key in function_env:
		#	fenv[key] = function_env[key]
		
		#print "%s(%s)"%(self.function_expr, ','.join(map(str, evaluate(self.act_args, env))))
		return function.call(fenv)
		
		
	def __repr__(self):
		return "%s(%s)"%(self.function_expr, ','.join(map(str, self.act_args)))
		
