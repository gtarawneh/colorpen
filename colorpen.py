#!/bin/python

from termcolor import colored
import sys
import re

styles = {
	r'0x[\d]+': ('red', []),
};

def main():
	patterns = {re.compile(x):st for x, st in styles.iteritems()}
	while True:
		line = sys.stdin.readline()
		if line:
			for p, style in patterns.iteritems():
				color, attrs = style
				for word in p.findall(line):
					styledWord = colored(word, color, attrs=attrs)
					line = line.replace(word, styledWord)
			sys.stdout.write(line)
		else:
			break

main()
