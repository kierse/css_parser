
#from attribute import Attribute
#from selector import Selector

class Rule(object):
	""" represents a CSS rule """

	def __init__(self, selector, attributes = []):
		
#		# apply parent to selectors
#		if parent != "":
#			selector = selectors.pop(0)
#			if selector.startswith("& "):
#				prefix = "& "
#			elif selector.startswith("&"):
#				prefix = "&"
#
#			# apply prefix to all remaining selectors
#			if prefix:
#				for selector in selectors:
#					selector = prefix + selector
#
#			selectors.insert(0, selector)
#
#			# replace & with given parent
#			selectors = map(lambda x: x.replace("&", parent), selectors)

		self._selector = selector
		self._attributes = attributes

	def selector(self):
		if self._selector:
			return self._selector
		else:
			return ""

	def display(self):
		
		if self._selector:
			print self._selector
			print "{"
			for attribute in self._attributes:
				print "	%s" % attribute
			print "}\n"

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		print "Rule(selector='%s', attributes=[%s])" % (self._selector, ",".join(map(lambda x: "'%s'" % x, self._attributes)))
