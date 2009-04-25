#!/usr/bin/python

import re
import sys

from rule import Rule

def identify_selectors(line):
	""" 
		split raw line on comma to get list of individual selectors.  
		prepare each selector to receive ancestor chain by appending appropriate
		prefix.
	"""
	
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

def build_ancestor_chains(ancestors = []):
	"""
		recursively iterate over 2D list of selectors and construct
		ancestral chain
	"""

	siblings = ancestors.pop()
	if len(ancestors) == 0:
		return siblings

	else:
		ancestor_chains = build_ancestor_chains(ancestors)
		sibling_chains = []

		for sibling in siblings:
			for chain in ancestor_chains:
				sibling_chains.append(sibling % chain)

		return sibling_chains

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
	data = data.replace("&", "\n&")
	data = data.replace("{", "\n{\n")
	data = data.replace("}", "\n}\n")
	data = data.replace(";", ";\n")
	data = data.replace("/*", "\n/*")
	data = data.replace("*/", "*/\n")
	data = data.replace("<!--", "\n<!--")
	data = data.replace("-->", "-->\n")

	# remove any newlines between selectors so
	# they are properly detected
	data = re.sub(",\s*\n+", ",", data)

	selectors = []
	attributes = []
	rules = []
	depth = 0
	in_comment = False
	in_selector = False

	for line in data.splitlines():
		
		# cleanup line and remove any leading/trailing
		# whitespace characters
		line = line.strip()
		if line == "": continue

		# look for start of new comment block.  Make sure to watch
		# out for single line comments
		if line.startswith("/*") or line.startswith("<!--"):
			if not (line.endswith("*/") or line.endswith("-->")):
				in_comment = True
			continue

		elif line.endswith("*/") or line.endswith("-->"):
			in_comment = False
			continue

		# ignore any lines that fall between /* and */ or <!-- and -->
		elif in_comment:
			continue

		elif line == "{":
			depth += 1
			attributes.append([])

		elif line == "}":
			attrs = attributes.pop()
			chains = build_ancestor_chains(list(selectors))
			for chain in chains:
				rules.append(Rule(chain, attrs))
				
			depth -= 1
			selectors.pop()

		elif line.endswith(";"):
			attributes[depth-1].append(line)

		else:
			selectors.append(identify_selectors(line))

	# display parsed CSS ruleset
	for rule in rules:
		rule.display()

if __name__ == "__main__":
	main()
