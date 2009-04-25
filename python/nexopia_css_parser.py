#!/usr/bin/python

import re
import sys

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
		ancestral chain(s)
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

def build_rule(rule, attributes):
	""" 
		build CSS rule block using given rule and attributes 
		
		ie:

			selector
			{
				key1: value1
				key2: value2
				...
				keyN: valueN
			}

	"""
	
	lines = [rule, "{"]
	for attr in attributes:
		lines.append("	%s" % attr)
	lines.append("}\n")

	return "\n".join(lines)

def main():
	""" parser method """

	if len(sys.argv) != 2:
		raise IOError("must give filename to be converted")

	# grab custom css data from given file
	file = open(sys.argv[1], "r");
	try:
		data = file.read()
	finally:
		file.close()

	# break up CSS into a series of lines
	data = data.replace("@", "\n@")
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
	at_rules = []

	in_at_rule = False
	in_comment = False
	in_selector = False

	# iterate over given file lines and convert to valid
	# CSS syntax
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

		# look for at-rules.  watch out for both line and block rules
		elif line.startswith("@"):
			if line.endswith(";"):
				at_rules.append(line)
			else:
				in_at_rule = True
				rules.append(line)
			continue

		elif line == "{":
			if in_at_rule and len(attributes) == 0:
				rules.append("{")

		# detected closing block, build rule block
		# and append to list
		elif line == "}":
			if in_at_rule and len(attributes) == 0:
				in_at_rule = False
				rules.append("}")
			else:
				attrs = attributes.pop()
				if len(attrs):
					chains = build_ancestor_chains(list(selectors))
					for chain in chains:
						rules.append(build_rule(chain, attrs))
				selectors.pop()

		elif line.endswith(";"):
			attributes[len(attributes)-1].append(line)

		else:
			selectors.append(identify_selectors(line))
			attributes.append([])

	# display parsed CSS ruleset
	for rule in (at_rules + rules):
		print rule

if __name__ == "__main__":
	main()

