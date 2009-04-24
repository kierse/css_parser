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
selectors = []
attributes = []
rules = []
depth = 0

for line in lines:
	
	# cleanup line a bit and skip empty lines
	line = lines.pop(0).strip()
	if line == "":
		continue

	if line.find("{") >= 0:
		depth += 1

	""" close block and create rules for current depth """
	elif line.find("}") >= 0:
		# -grab ancestor selectors at each depth going back to root
		#  create new rule for each
		# -push onto list of rules
		# -
		depth -= 1

	elif line.find(";") >= 0:
		if len(attributes) != depth:
			attributes.append([])
		attributes[depth-1].append(line)

	else:
		selectors.append(map(lambda x: x.strip(), line.split(",")))
