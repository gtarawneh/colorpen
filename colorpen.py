#!/bin/python

import re
import sys
import json
from docopt import docopt
from os.path import isfile
from termcolor import colored


usage = """Colorpen

Usage:
  colorpen
  colorpen [--style=<json>]

Options:
  --style=<json>  Use color style file [default=colorpen.json].

"""


defStyleFile = "colorpen.json"


test_style = {"hello": "red"}


valid_attrs = ["bold", "dim", "underlined", "blink", "reverse", "hidden",
"reset", "res_bold", "res_dim", "res_underlined", "res_blink", "res_reverse",
"res_hidden"]


valid_colors = ["grey", "red", "green", "yellow", "blue", "magenta", "cyan",
"white"]


def in_list(list):
	"""Return a function that checks whether an item is in list"""
	return lambda item: item in list


def get_style(style_str):
	"""Parse a style string in the form 'color attr1 attr2...'"""
	words = style_str.split()
	attrs = filter(in_list(valid_attrs), words)
	colors = filter(in_list(valid_colors), words)
	color = colors[0] if colors else None
	return (color, attrs)


def main():

	args = docopt(usage, version="Colorpen 0.1")

	styleFile = args.get("--style") or defStyleFile

	styles = loadJSON(styleFile) if isfile(styleFile) else test_style

	patterns = [ (re.compile(expr), get_style(style_str)) for
		expr, style_str in styles.iteritems() ]

	while True:

		line = sys.stdin.readline()

		if not line:
			break

		for pat, (color, attrs) in patterns:

			for match in pat.findall(line):

				styled_match = colored(match, color, attrs=attrs)
				line = line.replace(match, styled_match)

		try:
			sys.stdout.write(line)
			sys.stdout.flush()

		except IOError:
			pass


def loadJSON(file):

	if not isfile(file):
		print "File \"%s\" does not exist" % file
		sys.exit(1)

	try:
		with open(file) as fid:
			return json.load(fid)

	except ValueError as e:
		print colored("Warning: invalid colorpen JSON file, ignored.", attrs=["bold"])
		return {}


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass
