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

def_styles = {
	"hello": "red",
};

attrWords = ["bold"]

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
			sys.stdout.write(line)
		else:
			break

def loadJSON(file):
	try:
		with open(file) as f:
			return json.load(f)
	except ValueError as e:
		print(e)
		raise Exception('Error encountered while parsing %s' % file)

main()
