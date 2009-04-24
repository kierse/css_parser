#!/usr/bin/python

import re
import sys

from rule import Rule

debug = 1

def identify_selectors(line):
	
	selectors = map(lambda x: x.strip(), line.split(","))

	first = selectors.pop(0)
	if first.find("&") >= 0:
		if first.startswith("& "):
			prefix = "%s "
		else:
			prefix = "%s"
		first = first.replace("&", "%s")

		for i in range(0, len(selectors)):
			selectors[i] = prefix + selectors[i]
	selectors.insert(0, first)

	return selectors

def build_ancestor_chains(siblings, ancestors = []):

	if len(ancestors) == 0:
		return siblings

	else:
		ancestor_chains = build_ancestor_chains(ancestors.pop(), ancestors)
		sibling_chains = []

		for sibling in siblings:
			for chain in ancestor_chains:
				sibling_chains.append(sibling % chain)

		return sibling_chains

def _debug(obj):
	if debug:
		print obj

def main():
	if len(sys.argv) != 2:
		raise IOError("must give filename to be converted")

	# grab custom css data from given file
	file = open(sys.argv[1], "r");
	try:
		data = file.read()
	finally:
		file.close()

	# break up CSS into a series of lines
	data = data.replace("{", "\n{\n")
	data = data.replace("}", "\n}\n")
	data = data.replace(";", ";\n")
	data = data.replace("/*", "\n\*")
	data = data.replace("*/", "*/\n")
	lines = data.splitlines(True)

	selectors = []
	attributes = []
	rules = []
	depth = 0

	for line in lines:
		
		# cleanup line a bit and skip empty lines
		line = line.strip()
		if line == "":
			continue

		if line.find("{") >= 0:
			depth += 1
			attributes.append([])

		elif line.find("}") >= 0:
			# -grab ancestor selectors at each depth going back to root
			#  create new rule for each
			# -push onto list of rules
			chains = build_ancestor_chains(selectors.pop(), list(selectors))
			attrs = attributes.pop()
			for chain in chains:
				rule = Rule(chain, attrs)
#				_debug(rule)
				rules.append(rule)
				
			depth -= 1

		elif line.find(";") >= 0:
			attributes[depth-1].append(line)

		else:
			selectors.append(identify_selectors(line))

	a = [
		["body"],
		["%s div", "%s span"]
	]

	b = build_ancestor_chains(["%s a"], a)
	for i in b:
		print b

#	# display parsed CSS ruleset
#	for rule in rules:
#		print rule.display()

if __name__ == "__main__":
	main()
