
class Rule():
	""" represents a CSS rule """

	def __init__(self, selector, attributes = []):

		self._selector = selector
		self._attributes = attributes

	def display(self):
		
		if self._selector and len(self._attributes):
			print self._selector
			print "{"
			for attribute in self._attributes:
				print "	%s" % attribute
			print "}\n"

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		print "Rule(selector='%s', attributes=[%s])" % (self._selector, ",".join(map(lambda x: "'%s'" % x, self._attributes)))
