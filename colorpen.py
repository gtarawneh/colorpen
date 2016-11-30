#!/bin/python

import sys
import re
import json
from termcolor import colored
from docopt import docopt

usage = """Colorpen

Usage:
  colorpen
  colorpen [--style=<json>]

Options:
  --style=<json>    Load color style from json file

"""

attrWords = ["bold", "dim", "underlined", "blink", "reverse", "hidden",
"reset", "res_bold", "res_dim", "res_underlined", "res_blink", "res_reverse",
"res_hidden"]

def main():
	args = docopt(usage, version="Colorpen 0.1")
	styleFile = args["--style"]
	styles = loadJSON(styleFile) if styleFile else {"hello": "red"}
	patterns = {re.compile(x):st for x, st in styles.iteritems()}
	while True:
		line = sys.stdin.readline()
		if line:
			for p, style in patterns.iteritems():
				color = None
				attrs = []
				for word in style.split("+"):
					if word in attrWords:
						attrs.append(word)
					else:
						color = word
				for word in p.findall(line):
					styledWord = colored(word, color, attrs=attrs)
					line = line.replace(word, styledWord)
			try:
				sys.stdout.write(line)
			except IOError:
				pass
		else:
			break

def loadJSON(file):
	try:
		with open(file) as f:
			return json.load(f)
	except ValueError as e:
		print(e)
		raise Exception('Error encountered while parsing %s' % file)
	except IOError:
		print "Style file \"%s\" does not exist" % file
		sys.exit(1)

try:
	main()
except KeyboardInterrupt:
	pass
