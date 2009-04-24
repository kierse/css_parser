#!/usr/bin/python

import re
import sys

from rule import Rule

if len(sys.argv) != 2:
	raise IOError("must give filename to be converted")

# grab custom css data from given file
file = open(sys.argv[1], "r");
try:
	lines = file.readlines()
finally:
	file.close()

levels = [[Rule("", "")]]
depth = 0
defer = []
attributes = []
selectors = None

# parse data
#for line in lines:
while True:

	line = lines.pop(0).strip()
	if line == "":
		continue

	# check for opening bracket
	if line.find("{") >= 0:
		if depth > 0:
			defer.append(line)
		depth += 1

	elif line.find("}") >= 0:
		if depth > 1:
			defer.append(line)
		depth -= 1

		# ready to create Rule(s)
		if depth == 0:

			# get the prefix pattern for this 
			# set of selectors
			selector = selectors.pop(0)
			if selector.startswith("& "):
				prefix = "%s "
			else:
				prefix = "%s"
			selectors.insert(0, selector.lstrip("& "))

			rules = []
			size = len(levels)
			for parent_rule in levels[size-1]:
				for selector in selectors:
					rules.append(Rule(selector, prefix % parent_rule.selector(), attributes))
			levels.append(rules)

			if len(lines):
				backup = lines
			lines = defer
			defer = []
			attributes = []

	elif line.find(";") >= 0:
		if depth == 1:
			attributes.append(line)
		else:
			defer.append(line)

	# found selector(s)
	else:
		
		if depth == 0:

			# split on ',' (if any) and remove any whitespace
			selectors = map(lambda x: x.strip(), line.split(","))

		else:
			defer.append(line)

# display 
for level in levels:
	for rule in level:
		rule.display()
