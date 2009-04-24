
#from attribute import Attribute
#from selector import Selector

class Rule(object):
	""" represents a CSS rule """

	def __init__(self, selector, parent = "", attributes = []):
		
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

		self._selector = parent + selector
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

